# Image Caption for Social Network Posts
Data-X Project \
Team: Yangyiying Pu, Zhongyao Ma, Joanne Jiang, Huidi Wang, Chengwu Shen.

1. We first used the apify-py-script.py file to collect posts from Instagram associated with specific hashtags.\
We downloaded 3000+ pictures (uploaded 10 as examples in this "/images" folder due to memory limitation and the folder on Google Drive with all pictures is shared with our assigned GSI) and their hashtags (saved in the pickle file). Pictures and their hashtags can be linked through the ID of the picture.
2. Then we trained a model with image processing and natural language processing, as the model.py contained.
3. Finally we built a UI with Python Flask and all associated files are in the UI folder. Demo video attached in the last slide of the presentation.\
The code can be executed by cd into the UI folder and run "python app.py" in terminal.
