from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


try:
    os.mkdir("./dataset")
except:
    pass
try:
    os.mkdir("./dataset/images")
except:
    pass

client = MongoClient('127.0.0.1', 27017)
db = client.air_project

url = "http://vision.cs.uiuc.edu/pascal-sentences/"

data = requests.get(url).content
soup = BeautifulSoup(data)
table = soup.find("table")
dfs = pd.read_html(str(table))
data = dfs[0]
data.columns = ["img_url", "text"]
images = []
categories = []
for tr in table.find_all('tr'):
    img = tr.find("img")
    if img==None:
        continue
    categories.append(img["src"].split("/")[0])
    images.append(url+img["src"])


data["img_url"] = images
data["category"] = categories
data.to_csv("./dataset/labels.csv", index=None)



for index in range(len(data)):
    print("Downloading.... ", data["img_url"][index])
    url = data["img_url"][index]
    name = url.split("/")[-1]
    # Also save in mongo
    db.images_data.insert({
        "image_path": "./dataset/images/"+name,
        "text": data["text"][index],
        "category": data["category"][index]
    })
    with open("./dataset/images/"+name, "wb") as file:
        file.write(requests.get(url).content)


print("completed..... ")