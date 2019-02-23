#Jacob Kickbush jamakick
#Programming Assignment 1

import sys, bs4, urllib.request, os, re, time, urllib.robotparser
from urllib.parse import urlparse
from collections import deque

def validVars(): 
    
    unchecked = sys.argv
    
    try:
        
        pageReq = urllib.request.Request(unchecked[1], headers={'User-Agent': 'IUB-I427-jamakick'})
        
        page = urllib.request.urlopen(pageReq)
     
        page.close()
        
    except:
        print("The seed url was not given a proper URL/not in the proper position.")

    try:
        maxPages = int(unchecked[2])
        
        if maxPages < 1:
            print("The amount of pages to crawl needs to be at least 1.")
    except:
        print("The amount of pages given is not an integer/not in the proper position.")
        
    if unchecked[4] not in ("dfs", "bfs"):
        raise Exception("The search type given was invalid/not in the proper position. Valid values are 'dfs' and 'bfs'.")

    try:
        home = os.getcwd()
        
        newDirPath = os.path.join(home, unchecked[3])
        if not os.path.isdir(newDirPath):
            os.mkdir(newDirPath)
    except:
        print("Directory name given was not valid/not in the proper position.")
        print(home)
        print(newDirPath)
        print(unchecked[3])

def webCrawler(url, maxPages, saveLoc, searchType):
    
    try:
        seedReq = urllib.request.Request(url, headers={'User-Agent': 'IUB-I427-jamakick'})
    
        seed = urllib.request.urlopen(seedReq)
 
        seedContents = seed.read().decode(errors="replace")
 
        seed.close()
        
        fileOut = open(saveLoc + "/0.html", "w", encoding="utf-8")
        fileOut.write(seedContents)
        fileOut.close()
        
    except:
        raise Exception("Seed url could not be accessed.")
        
    seedContents = bs4.BeautifulSoup(seedContents, "lxml")
    
    links = [link.get('href') for link in seedContents.find_all('a', attrs={'href': re.compile("http")})]
    
    hits = []
    
    hits = [link for link in links if link not in hits]
    
    hits = deque(hits)
    
    indexDict = {0: url}
    
    for i in range(int(maxPages)):
        if searchType == "dfs":
            current = ""
            while True:
                current = hits.pop()
                if current not in indexDict.values():
                    break
            
            try:
                rp = urllib.robotparser.RobotFileParser()
                                
                robotLink = urlparse(current)
                
                robotLink = '{0}://{1}/robots.txt'.format(robotLink.scheme, robotLink.netloc)
                
                rp.set_url(robotLink)
                rp.read()
                
                if rp.can_fetch("IUB-I427-jamakick", current):
                    req = urllib.request.Request(current, headers={'User-Agent': 'IUB-I427-jamakick'})
    
                    page = urllib.request.urlopen(req)
 
                    contents = page.read().decode(errors="replace")
 
                    page.close()
                   
                    fileOut = open(saveLoc + "/" + str(len(indexDict)) + ".html", "w", encoding="utf-8")
                    fileOut.write(contents)
                    fileOut.close()
               
                
                    contents = bs4.BeautifulSoup(contents, "lxml")
                    
                    links = [link.get('href') for link in contents.find_all('a', attrs={'href': re.compile("http")})]
                    
                    for link in links:
                        if link not in hits:
                            hits.append(link)
                    
                    indexDict[len(indexDict)+1] = current
                    
                    time.sleep(1)
            except:
                pass
            
        elif searchType == "bfs":
            current = ""
            while True:
                current = hits.popleft()
                if current not in indexDict.values():
                    break
            
            try:
                rp = urllib.robotparser.RobotFileParser()
                                
                robotLink = urlparse(current)
                
                robotLink = '{0}://{1}/robots.txt'.format(robotLink.scheme, robotLink.netloc)
                
                rp.set_url(robotLink)
                rp.read()
                
                if rp.can_fetch("IUB-I427-jamakick", current):
                    req = urllib.request.Request(current, headers={'User-Agent': 'IUB-I427-jamakick'})
    
                    page = urllib.request.urlopen(req)
 
                    contents = page.read().decode(errors="replace")
 
                    page.close()
                   
                    fileOut = open(saveLoc + "/" + str(len(indexDict)) + ".html", "w", encoding="utf-8")
                    fileOut.write(contents)
                    fileOut.close()
               
                
                    contents = bs4.BeautifulSoup(contents, "lxml")
                    
                    links = [link.get('href') for link in contents.find_all('a', attrs={'href': re.compile("http")})]
                    
                    for link in links:
                        if link not in hits:
                            hits.append(link)
                    
                    indexDict[len(indexDict)] = current
                    
                    time.sleep(1)
            except:
                pass
        
        
    return indexDict


validVars()

checked = sys.argv

indexDict = webCrawler(checked[1], checked[2], checked[3], checked[4])


fileOut = open(checked[3] + "/index.dat", "w", encoding="utf-8")
for line in indexDict.items():
    fileOut.write(str(line[0]) + ".html " + line[1] + "\n")
fileOut.close()

print("finished writing files")
        

