import requests
import os

def download(url):
    requests.get(url)
def getListOfDirDownloaded(direcotry):
    file=open('filesDownloaded.txt', 'w+')
    directoryList = [ name for name in os.listdir(direcotry) if os.path.isdir(os.path.join(direcotry, name)) ]
    for item in directoryList:
        file.write("%s\n" % item)
    file.close()
    return directoryList

def getListOfDirToDownload():
    dirList = []
    file=open("dir-names.txt")
    for dir in file:
        dirList.append(dir)
    file.close()
    return dirList

directoryList = ['/data/d01/kba2013/aws-publicdatasets/trec/kba/kba-streamcorpus-2013-v0_2_0-english-and-unknown-language',\
                 '/data/d02/kba2013/aws-publicdatasets/trec/kba/kba-streamcorpus-2013-v0_2_0-english-and-unknown-language',\
                 '/data/d02/kba2013/aws-publicdatasets/trec/kba/kba-streamcorpus-2013-v0_2_0-english-and-unknown-language']
listOfFilesDownloaded=[]
for directory in directoryList:
    listOfFilesDownloaded.append(getListOfDirDownloaded(directory))


toDownloadSet = set(getListOfDirToDownload()).difference(set(listOfFilesDownloaded))
print toDownloadSet
