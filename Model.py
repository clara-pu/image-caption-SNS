import os
import string
import random
import numpy as np
import tensorflow_hub as hub
from wordsegment import load, segment
from collections import Counter
from scipy import spatial
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.applications.vgg16 import VGG16
from tensorflow.python.keras.applications.vgg16 import preprocess_input
from tensorflow.python.keras.preprocessing.image import load_img
from tensorflow.python.keras.preprocessing.image import img_to_array
from tensorflow.python.keras.applications.vgg16 import decode_predictions
from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import preprocess_input, decode_predictions

# preprocessing tag content
# separate words of each tag, remove punctuation, etc
# make "#catoftheday" -> "cat of the day"
def collect_tags_and_decomposition(path):
  tags = pickle.load(open(path, "rb"))
  print(len(tags))
  load()
  for key, value in tags.items():  
    cur_list = []
    for v in value[0]:
      cur = v.split('#')[1].lower()
      cur = segment(cur)
      cur = ' '.join(cur)
      if cur:
        cur_list.append(cur)
    tags[key] = cur_list
  return tags
tags = collect_tags_and_decomposition("final-imgs.pickle")
print(len(tags))

# group all tags and select popular tags
# select images with at least one of the popular tags
# save {image id : list of popular tags} in dictionary
def filter_images_with_popular_tags(tags):
  popular_tags = [v for value in tags.values() for v in value]
  popular_tags = Counter(popular_tags).most_common(500)
  popular_tags = [k[0] for k in popular_tags]
  image_to_tag_mapping = dict()
  for key, value in tags.items():
    target_value = []
    for v in value:
      if v in popular_tags:
        target_value.append(v)
    if target_value:
      image_to_tag_mapping[key] = target_value
  return popular_tags, image_to_tag_mapping

popular_tags, image_to_tag_mapping = filter_images_with_popular_tags(tags)
print(len(popular_tags))
print(len(image_to_tag_mapping))

# encode each popular tag into a 512 vector using universal sentence encoding 
# store the encoding in a list with the same length as popular_tags
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
def sentence_encode_tags(popular_tags):
  return embed(popular_tags)
encode_tags = sentence_encode_tags(popular_tags)
print(len(encode_tags))
tree = spatial.KDTree(encode_tags)   # important !!

# make one predictions of each selected image (with at least one popular tag) using pre-trained VGG16 model
def make_vgg_predictions(directory, image_to_tag_mapping_keys):
	vgg_model = VGG16()
	vgg_model = Model(inputs = vgg_model.inputs, outputs = vgg_model.layers[-1].output)
	vgg_predictions = dict()
	temp = 0
	for name in os.listdir(directory):
		if temp % 100 == 0:
			print(temp)
		temp += 1 
		filename = directory + name
		name = name.split('.')[0]
		if name not in image_to_tag_mapping_keys:
			continue
		image = load_img(filename, target_size=(224, 224))
		image = img_to_array(image)  # (224, 224, 3)
		image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
		image = preprocess_input(image)
		feature = vgg_model.predict(image, verbose=0)
		label = decode_predictions(feature)[0]
		vgg_predictions[name] = label[0][1].replace("_", " ")
	return vgg_predictions
	
vgg_predictions = make_vgg_predictions('images/', image_to_tag_mapping.keys())
print(len(vgg_predictions))

# encode prediction of each image into a 512 vector using universal sentence encoding 
def sentence_encode_vgg_predictions(vgg_predictions):
  encode_predictions = dict()
  for key, value in vgg_predictions.items():
    encode_predictions[key] = embed([value])[0]
  return encode_predictions
encode_predictions = sentence_encode_vgg_predictions(vgg_predictions)
print(len(encode_predictions))
print(len(list(encode_predictions.values())[0]))

# find the top k nearest encoded popular tag for each encoded prediction
def euclidean_find_nearest_popular_tags(popular_tags, tree, encode_predictions):
  euclidean_final_tag_predictions = dict()
  for key, value in encode_predictions.items():
    euclidean_final_tag_predictions[key] = [popular_tags[i] for i in tree.query(value, k = 36)[1]]
  return euclidean_final_tag_predictions
euclidean_final_tag_predictions = euclidean_find_nearest_popular_tags(popular_tags, tree, encode_predictions)
print(len(euclidean_final_tag_predictions))

# if the top k prediction has at least one match with the true tag set, count as correct
# calculate the prediction accuracy
# used for both euclidean and logistic regression  !!!
def calculate_correctness(image_to_tag_mapping, final_tag_predictions):
  correct_num = 0
  for key, value in final_tag_predictions.items():
    if not set(value).isdisjoint(image_to_tag_mapping[key]):
      correct_num += 1
  return correct_num / len(image_to_tag_mapping)
euclidean_correctness = calculate_correctness(image_to_tag_mapping, euclidean_final_tag_predictions)
print(euclidean_correctness)

def euclidean_predict_one_image(filename, tree, popular_tags):
  vgg_model = VGG16()
  vgg_model = Model(inputs = vgg_model.inputs, outputs = vgg_model.layers[-1].output)
  image = load_img(filename, target_size=(224, 224))
  image = img_to_array(image)  # (224, 224, 3)
  image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
  image = preprocess_input(image)
  feature = vgg_model.predict(image, verbose=0)
  label = decode_predictions(feature)[0][0][1].replace("_", " ")
  print(label)
  encode_prediction = embed([label])[0]
  euclidean_final_tag_prediction = ["#" + popular_tags[i].replace(" ", "") for i in tree.query(encode_prediction, k = 12)[1]]
  return euclidean_final_tag_prediction
 
# euclidean_predict_one_image("cat.jpg", tree, popular_tags)

# logistic regression
# train test split of image keys
random.seed(123)
train_ratio = 0.8
all_image_keys = list(image_to_tag_mapping.keys())
random.shuffle(all_image_keys)
train_size = int(len(all_image_keys) * train_ratio)
train_image_keys = all_image_keys[:train_size]
test_image_keys = all_image_keys[train_size:]
print("train size: " + str(len(train_image_keys)))
print("test size: " + str(len(test_image_keys)))

# used to prepare both train data and test data separately
def log_reg_prepare_data_matrix(target_image_keys, encode_predictions, image_to_tag_mapping, popular_tags, encode_tags):
  # X : encode_cross_popular_tag      y : target_binary
  encode_cross_popular_tag = []  # number of image * number of popular tags
  target_binary = []             # 1 if the tag is in popular tag, 0 otherwise
  for key in target_image_keys:
    for i in range(len(encode_tags)):   
      encode_cross_popular_tag.append(encode_tags[i] * encode_predictions[key])
    cur_target = [0] * len(encode_tags)
    for j in [popular_tags.index(item) for item in image_to_tag_mapping[key]]:
      cur_target[j] = 1
    target_binary.extend(cur_target)
  return encode_cross_popular_tag, target_binary
  
# encode_predictions ----- {id: vector length 512}
# image_to_tag_mapping ----- {id: list of popular tags appeared}
# popular_tags ----- list of tags
# encode_tags ----- list of vector (length 512)
# return: X, y from train data with keys "train_image_keys"
X_train, y_train = log_reg_prepare_data_matrix(train_image_keys, encode_predictions, image_to_tag_mapping, popular_tags, encode_tags)

# logistic regression model with X_train and y_train
def log_reg_model_construction(X_train, y_train):
  # down sampling 
  index_class_0 = [i for i in range(len(y_train)) if y_train[i] == 0]   
  index_class_1 = [i for i in range(len(y_train)) if y_train[i] == 1]   
  index_class_0_down_sample = np.random.choice(index_class_0, size = len(index_class_1) * 5, replace = False)
  y_train = [y_train[i] for i in index_class_1] + [y_train[i] for i in index_class_0_down_sample]
  X_train = [X_train[i] for i in index_class_1] + [X_train[i] for i in index_class_0_down_sample]
  print(len(X_train))
  print(len(X_train[0]))
  print(len(y_train))

  scaler = preprocessing.StandardScaler().fit(X_train)
  X_train = scaler.transform(X_train)    # standardization
  log_reg_model = LogisticRegression(max_iter = 1000, n_jobs = -1, tol = 0.001, solver = 'sag', verbose = 0)
  log_reg_model.fit(X_train, y_train)
  print("logistic model fitting done")

  return log_reg_model, scaler

log_reg_model, scaler = log_reg_model_construction(X_train, y_train)

# calculate test data accuracy
def log_reg_find_nearest_popular_tags(test_image_keys, log_reg_model, scaler, X_test, y_test, popular_tags):
  X_test = scaler.transform(X_test)    # standardization
  log_reg_accuracy = log_reg_model.score(X_test, y_test)   # accuracy is not much useful in this case
  probability_table = log_reg_model.predict_proba(X_test)[:, 1]   # probability that the label is 1
  log_reg_final_tag_predictions = dict()
  j = 0  # where we are in the iteration of test_image_keys
  temp = 0
  for i in range(0, len(probability_table), len(popular_tags)):
     if temp % 10 == 0:
       print(temp)
     temp += 1
     cur_proba_list = probability_table[i: i + len(popular_tags)]
     index_list = sorted(range(len(cur_proba_list)), key = lambda k: cur_proba_list[k])[-20:] 
     log_reg_final_tag_predictions[test_image_keys[j]] = [popular_tags[i] for i in index_list]
     j += 1
  return log_reg_final_tag_predictions, log_reg_accuracy

X_test, y_test = log_reg_prepare_data_matrix(test_image_keys, encode_predictions, image_to_tag_mapping, popular_tags, encode_tags)
print("test data preparation done!")
log_reg_final_tag_predictions, log_reg_accuracy = log_reg_find_nearest_popular_tags(test_image_keys, log_reg_model, scaler, X_test, y_test, popular_tags)
print("logistic regression test data prediction done!")
print(log_reg_accuracy)
log_reg_correctness = calculate_correctness(image_to_tag_mapping, log_reg_final_tag_predictions)
print("calculate correctness done!")
print(log_reg_correctness)

# predict tags from a brand-new image
def log_reg_predict_one_image(filename, log_reg_model, scaler, encode_tags, popular_tags):
  vgg_model = VGG16()
  vgg_model = Model(inputs = vgg_model.inputs, outputs = vgg_model.layers[-1].output)
  image = load_img(filename, target_size=(224, 224))
  image = img_to_array(image)  # (224, 224, 3)
  image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
  image = preprocess_input(image)
  feature = vgg_model.predict(image, verbose=0)
  label = decode_predictions(feature)[0][0][1].replace("_", " ")
  encode_prediction = embed([label])[0]
  encode_cross_popular_tag = []
  for i in range(len(encode_tags)):
    encode_cross_popular_tag.append(encode_tags[i] * encode_prediction)
  encode_cross_popular_tag = scaler.transform(encode_cross_popular_tag)  # standardization
  probability_table = log_reg_model.predict_proba(encode_cross_popular_tag)[:, 1]  # probability that the label is 1
  index_list = sorted(range(len(probability_table)), key = lambda k: probability_table[k])[-12:]   # 12 index with the largest probability
  final_tag_prediction = ["#" + popular_tags[i].replace(" ", "") for i in index_list]
  return final_tag_prediction
 
# log_reg_predict_one_image("cat.jpg", log_reg_model, scaler, encode_tags, popular_tags)