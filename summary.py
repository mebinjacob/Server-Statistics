#!/usr/bin/python
# dependency airspeed
# install airspeed, by typing
# sudo ./summary.py install, inside airspeed directory
import requests
import airspeed
import ConfigParser
import os
from subprocess import check_output

# configuration reading utility
configParser = ConfigParser.RawConfigParser()
configFilePath = r'property.ini'
configParser.read(configFilePath)
path = configParser.get('Folders', 'folderList')
emailAddresses = configParser.get('Email_Address', 'emails')
serverName = configParser.get('Server_Details', 'name')
################Global variables passed to view########################
folderSummaryList = []
usageSummaryList = []
dockerImagesList = []
dockerInstanceList = []
cpuIOUsageList = []
mailString = ''
#################End of global variables passed to view################
base_folders = path.split(",")


# mailgun attributes are hardcoded, change if you want to use another account!!
def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox4ad92269e9dd4ec6af5a43db995df318.mailgun.org/messages",
        auth=("api", "key-03786fc32080a30fb6e38060f03fe25f"),
        data={"from": serverName + " Server <mailgun@sandbox4ad92269e9dd4ec6af5a43db995df318.mailgun.org>",
              "to": [emailAddresses],  # "mebinjacob@gmail.com"
              "subject": serverName + " - Usage Summary Report",
              "html": mailString,
              })


class folderSummary:
    folderPath = ''
    folderSize = ''
    noOfFiles = 0

    def __init__(self, path, size, noOfFiles):
        self.folderPath = path
        self.folderSize = size
        self.noOfFiles = noOfFiles


class UsageSummary:
    path = ''
    size = 0
    used = ''
    avail = ''
    usedPercent = ''

    def __init__(self, path, size, used, avail, usedPercent):
        self.path = path
        self.size = size
        self.used = used
        self.avail = avail
        self.usedPercent = usedPercent


templateString = ''
with open("template.html", "r") as templateFile:
    templateString = templateFile.read()
for folder in base_folders:
    if not os.path.isdir(folder):
        continue
    folders = check_output(["find", folder, "-maxdepth", "1"])
    folderList = folders.split("\n")
    folderAndnoOfFilesDict = {}
    folderAndSpaceUsedDict = {}
    for f in folderList:
        if f.strip():
            folderSize = 1  # check_output(["du", "-sh", f]).split('\t')[0]
            folderAndSpaceUsedDict[f] = folderSize
            files = check_output(["find", f, "-type", "f"]).split('\n')
            fileCount = 0
            for serverFile in files:
                if serverFile.strip():
                    fileCount += 1
            folderAndnoOfFilesDict[f] = fileCount

            fs = folderSummary(f, folderAndSpaceUsedDict[f], folderAndnoOfFilesDict[f])
            folderSummaryList.append(fs)

    # usage summary of /data/dataset and /data/tmp folders only
    usageSummaryStringList = check_output(["df", "-h", folder]).split('\n')[1].split(' ')
    usageSummarySize = usageSummaryStringList[2]
    usageSummaryUsed = usageSummaryStringList[4]
    usageSummaryAvail = usageSummaryStringList[6]
    usageSummaryUsedPercent = usageSummaryStringList[8]
    us = UsageSummary(folder, usageSummarySize, usageSummaryUsed, usageSummaryAvail, usageSummaryUsedPercent)
    usageSummaryList.append(us)


# docker images
def printDockerImages():
    class DockerImages:
        repo = ''
        tag = ''
        id = ''
        created = ''
        virtualSize = ''

        def __init__(self, repo, tag, id, created, virtualSize):
            self.repo = repo
            self.tag = tag
            self.id = id
            self.created = created
            self.virtualSize = virtualSize

    dockerImagesInfoList = check_output(["docker", "images"]).split('\n')
    firstLine = None
    for dockerImages in dockerImagesInfoList:
        if firstLine == None:
            firstLine = True
            continue
        if dockerImages == '':
            continue
        dI = DockerImages(dockerImages[0:20].strip(), dockerImages[20:40].strip(), dockerImages[40:60].strip(),
                          dockerImages[60:80].strip(), dockerImages[80:100].strip())
        dockerImagesList.append(dI)


# splits the string by two spaces and gets the strings and not the spaces
def getStringList(string, headerPos):
    stringList = []
    index = 1
    stringList.append(string[0:headerPos[0]].strip())
    for header in headerPos:
        if index < len(headerPos):
            stringList.append(string[header:headerPos[index]].strip())
            index += 1
    stringList.append(string[headerPos[index-1]:].strip())
    return stringList


def getFromList(list, index):
    if index >= len(list):
        return ''
    else:
        return list[index]

def getHeaderPos(firstLine, firstLineKeywords):
    headerPos = []
    index = 1
    for key in firstLineKeywords:
                if index < len(firstLineKeywords):
                    headerPos.append( firstLine.find(firstLineKeywords[index]))
                    index += 1
    return headerPos

def printDockerInstances():
    class DockerInstance:
        container_id = ''
        image = ''
        command = ''
        created = ''
        status = ''
        ports = ''
        names = ''

        def __init__(self, container_id, image, command, created, status, ports, names):
            self.container_id = container_id
            self.image = image
            self.command = command
            self.created = created
            self.status = status
            self.ports = ports
            self.names = names

    dockerInstanceInfoList = check_output(["docker", "ps", "-a"]).split('\n')
    firstLine = None

    firstLineKeywords=['CONTAINER ID', 'IMAGE', 'COMMAND', 'CREATED', 'STATUS', 'PORTS', 'NAMES']
    headerPos = []
    for dockerinstance in dockerInstanceInfoList:
        if firstLine == None:
            firstLine = True
            headerPos = getHeaderPos(dockerinstance, firstLineKeywords)
            continue
        if dockerinstance == '':
            continue
        stringList = getStringList(dockerinstance, headerPos)
        dI = DockerInstance(getFromList(stringList, 0), getFromList(stringList, 1), getFromList(stringList, 2),
                            getFromList(stringList, 3), getFromList(stringList, 4),
                            getFromList(stringList, 5), getFromList(stringList, 6))
        dockerInstanceList.append(dI)


def printCPUAndIOUsageSummary():
    class CPUIOSummary:
        userName = ''
        cpu = ''
        elapsedTime = ''
        totalIO = ''
        cpuAvg = ''

        def __init__(self, userName, cpu, elapsedTime, totalIO, cpuAvg):
            self.userName = userName
            self.cpu = cpu
            self.elapsedTime = elapsedTime
            self.totalIO = totalIO
            self.cpuAvg = cpuAvg

    cpuIOUsageInfoList = check_output(["sa", "-D", "--user-summary"]).split('\n')
    firstLine = None
    for cpuIOUsage in cpuIOUsageInfoList:
        if firstLine == None:
            firstLine = True
            continue
        if cpuIOUsage == '':
            continue
        cI = CPUIOSummary(cpuIOUsage[0:20].strip(), cpuIOUsage[60:70].strip(), cpuIOUsage[50:60].strip(),
                          cpuIOUsage[70:80].strip(), cpuIOUsage[80:100].strip())
        cpuIOUsageList.append(cI)


printDockerImages()
printDockerInstances()
printCPUAndIOUsageSummary()
template = airspeed.Template(templateString)
mailString = template.merge(locals())
send_simple_message()
# print mailString
