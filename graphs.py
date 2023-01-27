import numpy as np
import matplotlib.pyplot as plt

colorCodes = {
	'brasil': 'limegreen',
	'religiao': 'yellow',
	'ataque': 'red',
	'shitpost': 'darkgoldenrod',
	'cm': 'black',
	'corrupcao': 'indianred',
	'defesa': 'deepskyblue',
	'cml': 'slategray',
	'anti-lgbt': 'pink',
	'pro-policia': 'darkblue'
}

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

def getNumberOfTweetsAndTotalLikesByCategory(tweets):
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

	return categoryNumbers

def turnDictionaryIntoSortedAverageLists(categoryNumbers:dict):
	list1 = sorted([(a, b) for a, b in categoryNumbers.items()], key=lambda x: x[1][0]/x[1][1], reverse=True)
	keys = [a + "\n" + str(b[1]) for a, b in list1]
	values = [b[0]/b[1] for a, b in list1]
	return keys, values
def getLikeAverageByCategory(tweets):
	sortedTweets = getNumberOfTweetsAndTotalLikesByCategory(tweets)
	return turnDictionaryIntoSortedAverageLists(sortedTweets)

def turnDictionaryIntoTotalTweetsList(categoryNumbers:dict):
	list1 = sorted([(a, b) for a, b in categoryNumbers.items()], key=lambda x: x[1][1], reverse=True)
	keys = [a + "\n" + str(b[1]) for a, b in list1]
	values = [b[0] / b[1] for a, b in list1]
	return keys, values
def getMostTweetsByCategory(tweets):
	tweets = getNumberOfTweetsAndTotalLikesByCategory(tweets)
	return turnDictionaryIntoTotalTweetsList(tweets)

def turnDictionaryIntoSortedTotalTweetsList(categoryNumbers:dict):
	list1 = sorted([(a, b) for a, b in categoryNumbers.items()], key=lambda x: x[1][1], reverse=True)
	keys = [a + "\n" + str(int(b[0] / b[1])) for a, b in list1]
	values = [b[1] for a, b in list1]
	return keys, values
def getMostTweetsSortedByCategory(tweets):
	sortedTweets = getNumberOfTweetsAndTotalLikesByCategory(tweets)
	return turnDictionaryIntoSortedTotalTweetsList(sortedTweets)

def findBrasil(keys):
	for i, name in enumerate(keys):
		if "brasil" in name:
			return i
def showGraph(keys, values, colors, title, yLim=-1, xlabel="Categoria + Nº de Tweets", yLabel="Likes"):
	f = plt.figure()
	f.set_figwidth(6)
	f.set_figheight(6)
	plt.bar(keys, values, color=colors, width=0.7)
	if yLim != -1:
		plt.ylim(0, yLim)
	plt.xlabel(xlabel)
	plt.ylabel(yLabel)
	plt.title(title)
	plt.show()

def createBarPlot(categoryAverage:tuple, categoryTotal:tuple, categoryTotalSorted:tuple):

	yLim = 1300

	keys, values = categoryAverage
	colors = [colorCodes.setdefault(a.split('\n')[0], 'maroon') for a in keys]

	showGraph(keys[:7], values[:7], colors[:7], "Média de likes de tweets do André Ventura\nOrdenado por categoria (Com Brasil)\n")

	i = findBrasil(keys)
	keys.pop(i)
	values.pop(i)
	colors.pop(i)
	showGraph(keys[:6], values[:6], colors[:6], "Média de likes de tweets do André Ventura\nOrdenado por categoria (Sem Brasil)\n1º Parte", yLim=yLim)
	showGraph(keys[6:], values[6:], colors[6:], "Média de likes de tweets do André Ventura\nOrdenado por categoria (Sem Brasil)\n2º Parte", yLim=yLim)

	keys, values = categoryTotal
	i = findBrasil(keys)
	keys.pop(i)
	values.pop(i)
	colors = [colorCodes.setdefault(a.split('\n')[0], 'maroon') for a in keys]
	showGraph(keys, values, colors, "Tweets do André Ventura\nOrdenados por nº total de tweets\n", yLim=yLim)

	keys, values = categoryTotalSorted
	i = findBrasil(keys)
	keys.pop(i)
	values.pop(i)
	colors = [colorCodes.setdefault(a.split('\n')[0], 'maroon') for a in keys]
	showGraph(keys, values, colors, "Nº de tweets do André Ventura\nOrdenados por nº total de tweets\n", yLim=100, yLabel="Nº de Tweets", xlabel="Categoria + Média de likes")


tweets = getTweetsFromCSV("tweets.txt")
categoryAverage = getLikeAverageByCategory(tweets)
categoryTotal = getMostTweetsByCategory(tweets)
categoryTotalSorted = getMostTweetsSortedByCategory(tweets)
createBarPlot(categoryAverage, categoryTotal, categoryTotalSorted)