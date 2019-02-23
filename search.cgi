#! /usr/bin/env python3

import cgi, cgitb, bs4, nltk, nltk.stem.porter as p, os, json, math, random

print('Content-type: text/html\n')


def retrieve(queryTerms, invIndex, pageRanks):

    with open("stopwords.txt", "r", encoding="utf8") as stopwordFile:
        stopwords = stopwordFile.read()

    text = [piece.strip().lower() for piece in queryTerms]

    text = " ".join(text)

    tokens = nltk.word_tokenize(text)

    tokens = [word for word in tokens if word not in stopwords]

    stemmer = p.PorterStemmer()

    stemList = [stemmer.stem(word) for word in tokens]

    stemList = [word for word in stemList if not [letter for letter in word if letter in "][%;/({:})`.',?!\""]]

    queryTerms = stemList

    half = int(len(queryTerms) / 2)

    matchedPages = []

    termList = []

    completeMatch = []

    try:
        for term in queryTerms:
            pageMatch = invIndex[term]
            termList.append(pageMatch)

        for page in pageMatch:
            if page[0] not in matchedPages:
                matchedPages.append(page[0])

        for page in matchedPages:
            found = 0
            for outer in termList:
                for inner in outer:
                    if page in inner:
                        found += 1

            if found >= half:
                completeMatch.append(page)

        tf_idf = []

        for page in completeMatch:
            totalScore = 0
            for term in queryTerms:
                for allCounts in invIndex[term]:
                    if page in allCounts:
                        wordCount = allCounts[1]

                pageInfo = docDict[page]

                totalCount = pageInfo[0]

                ntf = int(wordCount) / int(totalCount)

                df = len(invIndex[term])

                idf = 1 / (1 + math.log(df))

                score = ntf * idf

                score *= 100000

                totalScore += score

            rankScore = pageRanks[page]
            
            totalScore = score * rankScore

            tf_idf.append([totalScore, pageInfo[2], pageInfo[1]])

        matchedPages = tf_idf

        matchedPages = [(link, title, score) for (score, link, title) in sorted(matchedPages, reverse=True)]

        if len(matchedPages) >= 25:
            matchedPages = matchedPages[0:25]
    except:
        matchedPages = None

    return matchedPages


form = cgi.FieldStorage()

cgitb.enable()

html = """
<!doctype html>
<html>
<head><meta charset='utf-8'>
<title>Searching Proto Recipe Search</title>
<meta http-equiv='x-ua-compatible' content='ie=edge'>
<meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>

<!-- Stylesheets -->
<link rel='stylesheet' href='css/normalize.css'>
<link rel='stylesheet' href='css/styles.css'>
<link href='https://fonts.googleapis.com/css?family=KoHo|Courgette' rel='stylesheet'>
</head>
    <body>
	<div id='cgi'>

   <div class="form">
	<a href="index.html"><h2>Recipe Search</h2></a>

	<form action='search.cgi' method='get'>
	<input type="hidden" name="username" value="{3}">
	<input type='text' name='queryTerms'>

	<input type='submit' value='Search'>
	</form>

    </div>
    
   <div class="results">
	<h2 class="smaller">Results for {1}</h2>
	<ul>
	{0}
	</ul>
	</div>
	</div>
	
	
	<div class="recommend">
	<h2 class="smaller">Recommendations</h2>
	<ul>
	{2}
	</ul>
	</div>
    </body>
</html>"""

# nltk.download('punkt')

try:
    with open('invIndex.json', 'r', encoding="utf8") as invFile:
        invIndex = json.load(invFile)

    with open('docDict.json', 'r', encoding="utf8") as docFile:
        docDict = json.load(docFile)

    with open('pageranks.json', 'r', encoding="utf8") as rankFile:
        pageRanks = json.load(rankFile)
        
    with open('userhistory.json', 'r', encoding="utf8") as histFile:
        histories = json.load(histFile)
except:
    docDict = ""
    invIndex = ""
    pageRanks = ""
    

queryTerms = form.getfirst("queryTerms", "html breakfast").split()

username = form.getfirst("username", "")

results = retrieve(queryTerms, invIndex, pageRanks)

if username:
    if username not in histories.keys():
        histories[username] = []
        
        for term in queryTerms:
            if term not in histories[username]:
                histories[username].append(term)
    else:
        for term in queryTerms:
            if term not in histories[username]:
                histories[username].append(term)


with open('userhistory.json', 'w', encoding="utf8") as histFile:
    json.dump(histories, histFile)

recommendations = []

try:
    for user in histories.keys():
        if user != username:
            userhist = histories[user]
            
            for term in histories[username]:
                if term in userhist:
                    
                    for simterm in userhist:
                        if simterm != term:
                            if simterm not in histories[username]:
                                recommendations.append([user, simterm])
    
    try:
        recommend = []
        
        for i in range(4):
            rec = random.choice(recommendations)
            recommend.append(rec)
            recommendations.remove(rec)
    except:
        recommend = recommendations[0]
except:
    recommend = ["No user", "No recommendation"]

recOutput = ""

if recommendations:
    for rec in recommend:
        recOutput += "<li>"
        recOutput += 'You should try searching for <a href="http://cgi.soic.indiana.edu/~jamakick/i427/final/search.cgi?queryTerms='
        recOutput += rec[1]
        recOutput += '">' + rec[1] + '</a></li>'
        recOutput += '<li class="userrec">' + rec[0] + " likes this.</li><br>"
else:
    recOutput += "<li>You have no recommendations</li>"


output = ""
if results:

	for result in results:
		output += "<li>"
		output += "<a href='" + str(result[0]) + "'>" + str(result[1]) + "</a>"
		output += "<p>Score: " + str(result[2]) + "</p>"
		output += "</li>"
else:
	output +="<li>No Results Found</li>"

print(html.format(output.encode("utf8"), form.getfirst("queryTerms", "html breakfast"), recOutput, username))
