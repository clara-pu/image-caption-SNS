# Image Captioning for Social Network Posts
Data-X Project \
Team:Joanne Jiang, Zhongyao Ma, Yangyiying Pu, Chengwu Shen, Huidi Wang

## Description
1. We run `apify-scrape.py` to collect posts from Instagram associated with specific hashtags.\
We downloaded 3822 pictures (saved in `images/`) and their hashtags (saved in `tags.pickle`), which are connected by post ID. 
2. We train two models: K-dimensional tree (`model_kdtree.py`) and logistic regression (`model_logreg.py`). ..??????.... a model with image processing and natural language processing, as the model.py contained.
3. Finally we built a UI with Python Flask and all associated files are in the UI folder. Demo video is the `demo_video_480p.mov` file. Due to the limitation on file size (<25MB) on GitHub, we also shared a 2K version via email.

## Installation 
1. Git clone or download the repository
2. Optional: create a conda environment
3. Install packages: 
```bash
tensorflow (2.1.0)
tensorflow_hub
flask
wordsegment
scipy
sklearn
pickle
werkzeug.utils
```
4. Change directory to `image-caption-SNS/` in terminal

## Run Model
1. K-dimensional tree model (1h): 
```bash 
python model_kdtree.py
```
2. Logistic regression model (5h):
```bash
python model_logreg.py
```

## Run User Interface
1. Change directory to `image-caption-SNS/UI/` in terminal
2. Initiate the UI website (might take up to 5 minutes):
```bash
python app.py
```
3. Copy the address from terminal into web browser.
