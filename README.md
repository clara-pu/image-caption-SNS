# Image Captioning for Social Network Posts

Berkeley IEOR 290 Data-X Project \
Team: Joanne Jiang, Zhongyao Ma, Yangyiying Pu, Chengwu Shen, Huidi Wang


## Objective

Our project aims to provide a solution to users who want to become social media influencers or simply want to share with specific groups with an easy-to-use product that can generate a list of hashtags based on the picture in less than 1 seconds. Users will no longer need to manually type out the hashtags. Instead, all they need to do is to upload the picture they would like to post to our product and select from the generated hashtags. 


## Description

1. Data collection \
We run `apify-scrape.py` to collect posts from Instagram associated with specific hashtags. We downloaded 3822 pictures (saved in `images/`) and their hashtags (saved in `tags.pickle`), which are connected by post ID. 

2. Model construction \
We train two models, K-dimensional tree (`model_kdtree.py`) and logistic regression (`model_logreg.py`), for hashtag prediction. We use techniques for image classification and natural language processing. The output of each program is the overall prediction accuracy on the test dataset. The function defined at last is for a single prediction in user interface. 

3. User Interface \
We built a UI with Python Flask and all associated files are in the UI folder. Demo video is the `demo_video_480p.mov` file. Due to the limitation on file size (25MB) on GitHub, we also shared a clearer version (2KB) via email.


## Installation 

1. Install Python 3.7

2. Git clone or download the repository

3. Optional: create a conda environment

4. Install packages: 

```bash
tensorflow==2.0.1
tensorflow_hub==0.8.0
flask==1.1.1
wordsegment==1.3.1
scipy==1.4.1
sklearn==0.21.3
pickle==4.0
werkzeug==0.16.0
```

5. Change directory to `image-caption-SNS/` in terminal


## Run Model

1. K-dimensional tree model (runtime = 1 hour, accuracy = 0.42): 

```bash 
python model_kdtree.py
```

2. Logistic regression model (runtime = 10 hour, accuracy = 0.46):

```bash
python model_logreg.py
```


## Run User Interface

1. Change directory to `image-caption-SNS/UI/` in terminal

2. Initiate the UI website (might take up to 5 minutes):

```bash
python app.py
```

3. Copy the local IP address shown on the terminal into a web browser and access the user website.


## Deliverables

1. News story: `news_story.pdf`
2. Final report: `final_report.pdf`
3. Demo video: `demo_video_480p.mov`
4. Presentation: `final_presentation.pdf`
