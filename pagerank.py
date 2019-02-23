import json, re


def pageRank(pageRanks, linkingIndex, p, n):
    
    #equation
    #rj = (p/n) + (1-p) x sum(ri/di)
    
    #random probability of being clicked on
    randomProb = p / n
    
    #1-p in the equation
    minusConstant = 1 - p
    
    #for every page in our pageranks dictionary
    for page in pageRanks:
        
        #grab all the pages that our page links to
        linkedPages = linkingIndex[page]        
        
        #if there are no pages it links to, then it's rank is just p/n
        #since the right side of the equation will end up 0
        if not linkedPages:
            pageRanks[page] = randomProb
        
        #if we do have pages in our linked pages
        else:
            #create a variable to store the sums of individual pages in the linkedPages
            pageRankSums = []
            
            #for every page in the linkedpages
            for item in linkedPages:
                #get its current pagerank
                pageRank = pageRanks[item]
                
                #start a count for outgoing links
                totalOutgoing = 0
                
                #for every node in the whole index, we check to see if our page is linked to
                for node in linkingIndex:
                    if item in linkingIndex[node]:
                        #if it is we add 1 to the outgoing links
                        totalOutgoing += 1
                
                #divide the current pagerank by how many outgoing links there are
                indivRank = pageRank / totalOutgoing
                
                #and append it to our sums list for that page
                pageRankSums.append(indivRank)
            
            #take all the indiv ranks, sum them and multiply them by our 1-p minusConstant
            #then you add that to the randomProb, the p/n
            newRank = randomProb + (minusConstant * (sum(pageRankSums)))
            
            #and that becomes the new pagerank for that page
            pageRanks[page] = newRank

    #once every page's rank gets updated we return the new dictionary of rankings
    return pageRanks



try:
    with open('invIndex.json', 'r', encoding="utf8") as invFile:
        invIndex = json.load(invFile)

    with open('docDict.json', 'r', encoding="utf8") as docFile:
        docDict = json.load(docFile)
except:
    invIndex = ""
    docDict = ""
    
webGraph = []
    
allKeyUrls = []
fileToUrl = []
for item in docDict.keys():
    url = docDict[item][2]
    allKeyUrls.append(url)
    fileToUrl.append([item, url])

for item in docDict.items():
    filename = item[0]
    
    with open("finalRun/parsedPages/" + filename, "r", encoding="utf8") as file:
        contents = file.read()
        
    hits = re.findall('(?<=href=").+?(?=")', contents, re.DOTALL)        

    hits = [hit for hit in hits if hit in allKeyUrls]
    
    for hit in hits:
        
        for item1 in fileToUrl:
            if hit in item1[1]:
                correctName = item1[0]
    
        webGraph.append([filename, correctName])
    

#create a set of all the pages, even if they don't link to anything
allPages = []
for pair in webGraph:
    allPages.append(pair[0])
    allPages.append(pair[1])   
allPages = set(allPages)


#Create an index for each page, where the key of the dict is the page, 
#and the value is a list of pages it links to
linkingIndex = {}
for pair in webGraph:
    if pair[0] not in linkingIndex:
        linkingIndex[pair[0]] = [pair[1]]
    else:
        if pair[1] not in linkingIndex[pair[0]]:
                linkingIndex[pair[0]].append(pair[1])
#for the pages that don't link to anything, we 
for page in allPages:
    if page not in linkingIndex:
        linkingIndex[page] = []

#print out our linking index
#print(" Linking Index: ")
#for link in linkingIndex.items():
#    print(link[0], link[1])
#print()


#create the initial page ranks for every page using 1/n
pageRanks = {}
for page in allPages:
    pageRanks[page] = 1 / len(allPages)
    
#print(" Initial 1/n PageRanks ")
#for page in pageRanks:
#    print(page, pageRanks[page])
#print()

#p constant given, and n is the number of pages
p = 0.05
n = len(linkingIndex)

#keep track of the previous sum to find when to break
previousSum = 0

#how many iterations of page rank has happened
count = 0

##while loop so that we run pagerank until the results stop changing
while True:
    #keep track of how many iterations
    count += 1
    
    print(count)
    
    #keep track of the new previous sum 
    previousSum = sum(pageRanks.values())
    print(previousSum)

    #update the pageranks with another iteration
    pageRanks = pageRank(pageRanks, linkingIndex, p, n)
    
   

    #print out the new ranks, the sum of the ranks, and how many iterations
#    print("Current page ranks",pageRanks)
#
#    print("Sum of page ranks", sum(pageRanks.values()))
#    
#    print("Num of rank cycles", count)
    
    #if our current sum and previous sum are the same
    #then we break our loop as the values have stabilized
    if previousSum == sum(pageRanks.values()):
        break

with open('pageranks.json', 'w', encoding="utf8") as rankFile:
    json.dump(pageRanks, rankFile)