import json
from pip._vendor import requests
import csv

# @dictFiles empty dictionary of files
# @lstTokens GitHub authentication tokens
def countfiles(authorlist, dictFiles, lsttokens, repo):
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
                    #Only include files that are written in specific back end language
                    if filename.endswith(('.java','.h','.kt','.js','.cpp')):
                        #Save the file, author and date in the authorlist
                        author = list()
                        author.append(filename)
                        author.append(shaDetails['commit']['author']['name'])
                        author.append(shaDetails['commit']['author']['date'])
                        authorlist.append(author)
                        #Use the dictfiles to store the ccount of files
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1 
            ipage += 1
    except Exception as e:
        print(e)
        exit(0)
        
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack'
# repo = 'mendhak/gpslogger'
# repo = 'k9mail/k-9'

# put your tokens here
lstTokens = ['0b0923f7c7f008611cfe72e093bef4c0d8a8c1fe']

dictfiles = dict()
authorlist = list()
countfiles(authorlist, dictfiles, lstTokens, repo)
#Sort the dictfiles in ascending order for the count value
dictfiles = dict(sorted(dictfiles.items(), key=lambda x:x[1]))

import matplotlib.pyplot as plt
from datetime import datetime
import math

listfiles = (sorted(dictfiles.items(), key=lambda x:x[1]))
top50files = dict()

count=1
#Simple function to rename the files to f01 to f50
if len(listfiles) <=50:
    for file in listfiles:
        if count<10:
            top50files[file[0]]= 'f0' + str(count)
        else:
            top50files[file[0]]='f' + str(count)
        count+=1
else:
    for file in listfiles[len(listfiles)-50]:
        if count<10:
            top50files[file[0]]='f0' + str(count)
        else:
            top50files[file[0]]='f' + str(count)
        count+=1

x = list()
y = list()
c = list()
a = dict()

c1=0

#Function to get the data ready for plotting
for author in authorlist:
    if author[0] in top50files:
        x.append(top50files[author[0]])
        y.append(author[2].split('T')[0])
        if author[1] not in a:
            a[author[1]] = c1
            c1+=25
        c.append(a[author[1]])   

#Use this to first sort the data based on the dates (y-axis)
lists = sorted(zip(y,x,c))
new_y, new_x, new_c= list(zip(*lists))

weeks= list()
week = 0
date_prev = 0

#Function to get the corresponding weeks for the y-axis
for day in new_y:
    date = datetime.strptime(day, '%Y-%m-%d')
    if date_prev == 0:
        weeks.append(week)
        date_prev = date
    else:
        diff = (date - date_prev).days
        if diff < 7:
            weeks.append(week)
        else:
            if diff%7 == 0:
                week = week + diff/7
                weeks.append(week)
            else:
                week += math.floor(diff/7)
                weeks.append(week)
        date_prev = date

plt.scatter(new_x,weeks,c=new_c,s=20)
plt.xlabel("File")
plt.ylabel("Weeks")
plt.grid(True)
plt.show()

file = repo.split('/')[1]
plt.savefig(file+'Plot.png')
