#!/usr/bin/env python
# coding: utf-8

# In[10]:


import requests
import json
from datetime import datetime as dt
import pickle
# Get your token from Apify website
API_TOKEN = "sCHbLRzBwT8QzGiaXQSj9Aeny"

# Constants: do not change
CREATE_TASK = "https://api.apify.com/v2/actor-tasks?token=" + API_TOKEN
RUN_ACTOR1 = "https://api.apify.com/v2/acts/jaroslavhejlek~instagram-scraper/runs?token=" + API_TOKEN
RUN_ACTOR2 = "https://api.apify.com/v2/acts/jaroslavhejlek~instagram-scraper/run-sync?token=" + API_TOKEN
GET_RUN_LIST = "https://api.apify.com/v2/acts/jaroslavhejlek~instagram-scraper/runs?token=" + API_TOKEN
GET_LAST_RUN = "https://api.apify.com/v2/acts/jaroslavhejlek~instagram-scraper/runs/last?token=" + API_TOKEN
GET_LAST_RUN_DATA = "https://api.apify.com/v2/acts/jaroslavhejlek~instagram-scraper/runs/last/dataset/items?token=" + API_TOKEN
HEADER = {'Content-Type': 'application/json'}

# Change to the your desire path
PATH = "/Users/shengli/Desktop/IEOR 290/imgs.pickle"
DEST = "/Users/shengli/Desktop/IEOR 290/images/"


# In[11]:


# Parameters:
# hashtag name
# searchLimit: How many search results (eq. pages) should be processed
# resultsType options: "posts", "comments", "details"
# resultsLimit: 
# How many posts or comments to scrape from each Instagram URL, ignored when "details" type is specified
def scrape(hashtag, searchLimit = 5, resultsType = "posts", resultsLimit = 10, tagsLimit = 10):
    # dictionary -> Javascript Object Notation
    data = json.dumps({'search': hashtag, 'searchType': 'hashtag', "searchLimit": searchLimit, "resultsType": resultsType, "resultsLimit": resultsLimit, "proxy": {"useApifyProxy": True}})
    print("Running...")
    # 运行instagram-srcaper
    run = requests.post(url = RUN_ACTOR2, data = data, headers = HEADER)

    if run.status_code == 201:
        print("Run Success!")
    else:
        print("Run Failure! " + str(run.status_code))
        print(run.json())
        return
    
    try:
        f = open(PATH, "rb")
        out_dict = pickle.load(f)
        f.close()
    except EOFError:
        out_dict = dict()
        
        
    # Get the data that just ran through
    getdata = requests.get(url = GET_LAST_RUN_DATA)
    if getdata.status_code == 200:
        l = getdata.json()
        print("Get Posts Success!" + " Number of posts in total: " + str(len(l)))
        for i in range(len(l)):
            try:
                imgurl = l[i]['imageUrl']
                firstCommentStr = l[i]['firstComment']
            except:
                continue
            else:
                hashtags = [i for i in firstCommentStr.split() if i[0] == '#']
                postid = l[i]["url"].split('/')[-1]
                out_dict[postid] = (hashtags, imgurl)
            #getimg = requests.get(imgurl)
            #if getimg.status_code == 200:
            #    print("Downloading Image No." + str(i) +"...")
            #Nameing of the pictures are set to ID for uniqueness
            #    if FOLDERPATH != "":
            #        with open(FOLDERPATH + hashtag + '-' + l[i]["url"].split('/')[-1] + ".jpg", 'wb') as f:
            #            f.write(getimg.content)
            #    else:
            #        with open(hashtag + '-' + l[i]["url"].split('/')[-1] + ".jpg", 'wb') as f:
            #            f.write(getimg.content)
            #else:
            #    print("Image No." + str(i) + " Failed!")
    print(out_dict)
    f = open(PATH, "wb")
    pickle.dump(out_dict, f)
    f.close()

def download():
    f = open(PATH, "rb")
    out_dict = pickle.load(f)
    for postid in out_dict.keys():
        imgurl = out_dict[postid][1]
        getimg = requests.get(imgurl)
        if getimg.status_code == 200:
            print("Downloading Image " + imgurl)
            with open(DEST + postid + ".jpg", 'wb') as ff:
                ff.write(getimg.content)
        else:
            print("Failed!" + imgurl)


# In[13]:


#Some of the hashtags we have collected
#tags_list = ["cat","dog","puppy","sunset","nature","flower","coffee","tea","wine","sushi","art","food","selfie","fashion","ootd","shoes","beach","hair","gym","baby","tatoo"]
#1
#tags_list = ["sunrise","flowers","sea","landscape","trees","waterfall","oilpainting","drawing "
#             ,"architecture","makeup","lipsticks","tattoo","jewelry","fish","insects","birds"]
#2
#tags_list = ["pet","horses","vegan"]
#3
#tags_list = ["pet","horses","vegan","drinks","pizza"]
#4
tags_list = ["succulent","brunch","handmade","christmas","holiday","museum","swag","techie","yoga","aroma","wedding"]

for tag in tags_list:
    scrape(tag)
    download()


# In[ ]:




