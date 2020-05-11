# Image Caption for Social Network Posts
Data-X Project \
Team: Yangyiying Pu, Zhongyao Ma, Joanne Jiang, Huidi Wang, Chengwu Shen.


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
```bash
python UI/app.py
```

## Description
1. We run `apify-scrape.py` to collect posts from Instagram associated with specific hashtags.\
We downloaded 3822 pictures (saved in `images/`) and their hashtags (saved in `tags.pickle`), which are connected by post ID. 
2. We train two models: K-dimensional tree (`model_kdtree.py`) and logistic regression (`model_logreg.py`). ..??????.... a model with image processing and natural language processing, as the model.py contained.
3. Finally we built a UI with Python Flask and all associated files are in the UI folder. Demo video attached in the last slide of the presentation.\
