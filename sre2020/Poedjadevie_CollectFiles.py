import json
from pip._vendor import requests
import csv

# @dictFiles empty dictionary of files
# @lstTokens GitHub authentication tokens
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
# loop though all the commit pages until the last returned empty page
    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            if ct == len(lstTokens):
                ct = 0
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + \
                        '&per_page=100&access_token=' + lsttokens[ct]
            
            ct += 1
            content = requests.get(commitsUrl)
            jsonCommits = json.loads(content.content)
            # break out of the while loop if there are no more commits in the pages
            
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in a page
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                if ct == len(lstTokens):
                    ct = 0
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha \
                         + '?access_token=' + lstTokens[ct]
                ct += 1
                
                content = requests.get(shaUrl)
                shaDetails = json.loads(content.content)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if filename.endswith(('.java','.h','.kt','.js','.cpp')):
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
            ipage += 1
    except Exception as e:
        print("Error receiving data")
        print(e)
        exit(0)

repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack'
# repo = 'mendhak/gpslogger'
# repo = 'k9mail/k-9'

# put your tokens here
lstTokens = ['']

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)

file = repo.split('/')[1]

#change this to the path of your file
fileOutput = file+'.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
fileCSV.close()
