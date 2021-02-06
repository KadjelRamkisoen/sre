import json
from pip._vendor import requests
import csv

# @dictFiles empty dictionary of files
# @lstTokens GitHub authentication tokens
def countfiles(authorlist, lsttokens, repo):
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
                        author = list()
                        author.append(filename)
                        author.append(shaDetails['commit']['author']['name'])
                        author.append(shaDetails['commit']['author']['date'])
                        authorlist.append(author)
                        
            ipage += 1
    except Exception as e:
        print(e)
        exit(0)

repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack'
# repo = 'mendhak/gpslogger'
# repo = 'k9mail/k-9'

# put your tokens here
lstTokens = ['']

authorlist = list()
countfiles(authorlist, lstTokens, repo)

file = repo.split('/')[1]
#change this to the path of your file
fileOutput = file+'Author.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
for x in authorlist:
    print(x)
    rows = [x[0],x[1],x[2]]
    writer.writerow(rows)
fileCSV.close()
