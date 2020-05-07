# semantic-image-search
Information retrieval project that is used to retrieve images by describing in words


## Step1:
##### Install python3
**Run following commands**
**Linux:**
```python
			sudo add-apt-repository ppa:jonathonf/python-3.6
			sudo apt-get update
			sudo apt-get install python3.6
			sudo apt install python3-pip
```
**In order to install python on Windows follow this [link](https://phoenixnap.com/kb/how-to-install-python-3-windows "link") and Mac OS follow this [link](https://docs.python-guide.org/starting/install3/osx/ "link")**

## Step2: 
###### Download Word2vec model 
You can download latest word2vec model or you can follow [link](https://drive.google.com/file/d/1_OSzEyCpyLBHWjwRn47qVIaOugyK60SM/view?usp=sharing "link") to download these pretrained embeddings. 
######Extract that model file in backend/data folder 

## Step3:
#####  Install mongoDB
######### For linux run the following commands in order 
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 68818C72E52529D4
    sudo echo "deb http://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
    sudo apt-get update
    sudo apt-get install -y mongodb-org
    sudo systemctl start mongod
    sudo systemctl enable mongod
    
	
