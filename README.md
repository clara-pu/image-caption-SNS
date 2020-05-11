# Image Caption for Social Network Posts
Data-X Project \
Team: Yangyiying Pu, Zhongyao Ma, Joanne Jiang, Huidi Wang, Chengwu Shen.

# Installation 
1. Git clone or download the repository
2. Optional: create a conda environment
3. Install packages: tensorflow (2.1.0), tensorflow_hub, flask, wordsegment, scipy, sklearn

# Run Model
1. K-Dimensional Tree Model: 
```python Model_KDTree

1. We first used the apify-py-script.py file to collect posts from Instagram associated with specific hashtags.\
We downloaded 3000+ pictures (saved in images folder) and their hashtags (saved in final-imgs.pickle). Pictures and their hashtags can be linked through the ID of the picture. 
2. Then we trained a model with image processing and natural language processing, as the model.py contained.
3. Finally we built a UI with Python Flask and all associated files are in the UI folder. Demo video attached in the last slide of the presentation.\
The code can be executed by cd into the UI folder and run "python app.py" in terminal.
