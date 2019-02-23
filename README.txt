Jacob Kickbush
I427 Final Project

Link to search engine: 

http://cgi.soic.indiana.edu/~jamakick/i427/final/index.html


Enter your name for your search history to be tracked and be given 
recommendations based on other users' history

Improvements from Assignment 3:

recommendation engine
pagerank and tfidf determine score together
some interface enhancements
make the search quicker by separating my code into different files and
saving them as json for the informatino that doesn't change. (pageranks, index)

search.cgi does the actual search engine work

indexer.py creates my docDict and invIndex and saves them to json

scraper.py does the web scraping on my pages and save them in a folder

pagerank.py creates the pageranks and saves them to a json

userhistory.json contains the users search histories. You can see
how the recommendation works here.