import numpy as np
import matplotlib.pyplot as plt

def getTweetContents(tweet):
	split = tweet.split(',')
	tweetID = split[0]
	likes = split[-2]
	categories = split[-1].strip()
	contents = split[1:-2]
	text = ""
	for a in contents:
		text += a
	return int(tweetID), text, int(likes), categories
def getTweetsFromCSV(file):
	file = open(file, 'r')
	tweets = []
	for line in file:
		tweets.append(getTweetContents(line))
	return tweets

def turnDictionaryIntoSortedLists(categoryNumbers:dict):
	list1 = sorted([(a, b) for a, b in categoryNumbers.items()], key=lambda x: x[1][0]/x[1][1], reverse=True)
	keys = [a + "\n" + str(b[1]) for a, b in list1]
	values = [b[0]/b[1] for a, b in list1]
	return keys, values
def getLikeAverageByCategory(tweets):
	categoryNumbers = {}
	for tweet in tweets:
		likes = tweet[2]
		categories = tweet[3].split('|')

		for category in categories:
			if category not in categoryNumbers.keys():
				categoryNumbers[category] = (likes, 1)
			else:
				previousLikes, previousNumber = categoryNumbers[category]
				categoryNumbers[category] = (previousLikes + likes, previousNumber + 1)

	return turnDictionaryIntoSortedLists(categoryNumbers)

def createBarPlot(categoryAverage:tuple):
	keys, values = categoryAverage

	# creating the bar plot
	plt.bar(keys, values, color='maroon',
			width=0.4)

	plt.xlabel("Categorias")
	plt.ylabel("Likes")
	plt.title("Média de likes de tweets do André Ventura por categoria")
	plt.show()


tweets = getTweetsFromCSV("tweets.txt")
categoryAverage = getLikeAverageByCategory(tweets)
createBarPlot(categoryAverage)