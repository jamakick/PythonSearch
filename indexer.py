import bs4, nltk, nltk.stem.porter as p, os, json

def indexer(dirName, indexFile):

    with open("stopwords.txt", "r", encoding="utf8") as stopwordFile:
        stopwords = stopwordFile.read()

    with open(indexFile, "r", encoding="utf8") as indexFile:
        indexContent = indexFile.readlines()

    indexContent = [item.split(" ") for item in indexContent]

    pages = os.listdir(dirName)

    invIndex = {}

    docDict = {}

    for page in pages:
        
        print(page)

        with open(dirName + "/" + page, "r", encoding="utf8") as file:
            pageContents = file.read()

        contentLen = len(pageContents)

        content = bs4.BeautifulSoup(pageContents, "lxml")
            
        header = content.find('head')
    
        if header:
            title = str(header.find('title'))[7:-8]
    
            pageUrl = ""
    
            for fileName in indexContent:
                if fileName[0] == page:
                    pageUrl = fileName[1].strip()
    
            docDict[page] = [contentLen, title, pageUrl]
    
            text = content.find_all(text = True)
    
            text = [piece.strip().lower() for piece in text]
    
            text = " ".join(text)
    
            tokens = nltk.word_tokenize(text)
    
            tokens = [word for word in tokens if word not in stopwords]
    
            stemmer = p.PorterStemmer()
    
            stemList = [stemmer.stem(word) for word in tokens]
    
            stemList = [word for word in stemList if not [letter for letter in word if letter in "][%;/({:})`.',?!\""]]
    
    
            for term in stemList:
                if term not in invIndex:
                    invIndex[term] = []
    
            for term in set(stemList):
    
                termList = [page, stemList.count(term)]
    
                if termList not in invIndex[term]:
                    invIndex[term].append(termList)

    return invIndex, docDict


invIndex, docDict = indexer("finalRun/parsedPages", "finalRun/index.dat")

with open('invIndex.json', 'w', encoding="utf8") as invFile:
    json.dump(invIndex, invFile)

with open('docDict.json', 'w', encoding="utf8") as docFile:
    json.dump(docDict, docFile)