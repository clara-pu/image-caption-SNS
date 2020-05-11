import os
import pickle
import random
import string
from collections import Counter

import numpy as np
from scipy import spatial
from sklearn import preprocessing
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

import tensorflow_hub as hub

filename = 'tree.sav'
with open(filename, "rb") as f:
    tree = pickle.load(f)
    popular_tags = pickle.load(f)

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def euclidean_predict_one_image(filepath, tree=tree, popular_tags=popular_tags):
  resnet_model = ResNet50(weights='imagenet')
  image = load_img(filepath, target_size=(224, 224))
  image = img_to_array(image)  # (224, 224, 3)
  image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
  image = preprocess_input(image)
  feature = resnet_model.predict(image, verbose=0)
  labels = decode_predictions(feature)
  label = labels[0][0][1].replace("_", " ")
  encode_prediction = embed([label])[0]
  prob_index_2d = tree.query(encode_prediction, k = 15)
  prob_index_2d = np.array(prob_index_2d)
  prob_index_2d = prob_index_2d[1, prob_index_2d[0] < 1.1]
  euclidean_final_tag_prediction = ["#" + popular_tags[int(i)].replace(" ", "") for i in prob_index_2d]
  return list(euclidean_final_tag_prediction)[:15]