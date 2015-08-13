import requests
import os

def download(url):
    requests.get(url)
def getListOfFileDownloaded(direcotry):
    file=open('filesDownloaded.txt', 'w+')
    directoryList = [ name for name in os.listdir(direcotry) if os.path.isdir(os.path.join(direcotry, name)) ]
    for item in directoryList:
        file.write("%s\n" % item)
    file.close()

directoryList = ['/data/d01/kba2013/aws-publicdatasets/trec/kba/kba-streamcorpus-2013-v0_2_0-english-and-unknown-language',\
                 '/data/d02/kba2013/aws-publicdatasets/trec/kba/kba-streamcorpus-2013-v0_2_0-english-and-unknown-language',\
                 '/data/d02/kba2013/aws-publicdatasets/trec/kba/kba-streamcorpus-2013-v0_2_0-english-and-unknown-language']
for directory in directoryList:
    getListOfFileDownloaded(directory)