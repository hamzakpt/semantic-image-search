import utils_fun
import os
import pickle
import gensim
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pymongo import MongoClient



client = MongoClient('127.0.0.1', 27017)
db = client.air_project


if os.path.isfile('/home/hmzakpt/xfactor_backend/model.pik'):
    model = pickle.load(open("/home/hmzakpt/xfactor_backend/model.pik", "rb"))
else:
    model = gensim.models.KeyedVectors.load_word2vec_format('/home/hmzakpt/xfactor_backend/conceptnet.txt',
                                                            binary=False)
    pickle.dump(model, open("/home/hmzakpt/xfactor_backend/model.pik", "wb"))



stop_words = stopwords.words('english')
wordnet_lemmatizer = WordNetLemmatizer()


def get_data_from_database():
    images = []
    texts = []
    category = []
    all_records = db.images_data.find({})
    for record in all_records:
        images.append(record["image_path"])
        category.append(record["category"])
        texts.append(record["text"])
    return images, texts, category

images, texts, category = get_data_from_database()

csv_path = "./dataset/labels.csv"

# Predefined query for ecah category
queries = {"aeroplane": "airplanes"}

IMAGE_FOLDER_PATH = "./dataset/images/"