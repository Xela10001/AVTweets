import os
import re

import requests
import tweepy
from dotenv import load_dotenv


def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F64F-\U0001F914"  # ...
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printCategorias(categorias):
    if categorias:
        print(f"{bcolors.OKCYAN}Categorias existentes{bcolors.ENDC}:{bcolors.WARNING}")
    for i, categoria in enumerate(categorias):
        print(categoria, end="")
        if i != len(categorias) - 1:
            if (i + 1) % 5 == 0:
                print()
            else:
                print(", ", end="")
        else:
            print(f"{bcolors.ENDC}", end=f"\n{bcolors.HEADER}====={bcolors.ENDC}")

def readCategorias():
    categoriasFile = open("categorias.txt", "r")
    categoriasString = categoriasFile.read()
    categorias = categoriasString.split(',') if categoriasString else []
    return categorias

def writeCategorias(categorias):
    categoriasFile = open("categorias.txt", "w")
    categoriasString = ""
    for i, categoria in enumerate(categorias):
        categoriasString += categoria
        if i != len(categorias) - 1:
            categoriasString += ','
    categoriasFile.write(categoriasString)

    categoriasFile.close()

def printTweet(tweet:str):
    tweet = tweet.replace(". ", ".\n").replace("! ", "!\n").replace("? ", "?\n")
    return tweet

def handle_tweets(user_me):
    tweets = user_me['data']
    next_token = user_me['meta']['next_token']

    FTfile = open("last_fetch_token.txt", "w")
    FTfile.write(next_token)
    FTfile.close()

    tweetsFile = open("tweets.txt", "a")

    categorias = readCategorias()

    for tweet in tweets:
        print(f"{bcolors.HEADER}====={bcolors.ENDC}")
        tweetText = tweet['text']
        tweetID = tweet['id']
        tweetLikes = tweet['public_metrics']['like_count']
        print(printTweet(tweetText))
        print(f"{bcolors.FAIL}Likes{bcolors.ENDC}: {tweetLikes}")
        print(f"{bcolors.HEADER}====={bcolors.ENDC}")
        printCategorias(categorias)
        categoriaInput = input(f"\n{bcolors.BOLD}Como categoriza este tweet? (s to SKIP TWEET){bcolors.ENDC}\n").lower()
        if categoriaInput == 's':
            continue
        for categoria in categoriaInput.split(','):
            if categoria not in categorias:
                categorias.append(categoria)
        cleansedText = remove_emoji(tweetText.replace("\n", ' '))
        tweetsFile.write(f"{tweetID},{cleansedText},{tweetLikes},{categoriaInput.replace(',', '|')}\n")

    writeCategorias(categorias)

    tweetsFile.close()


andreVenturaHandle = 'andrecventura'
andreVenturaID = 1097962618596327424

load_dotenv()

consumer_key = os.environ["API_KEY"]
consumer_secret = os.environ["API_KEY_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]


oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=client_id,
    redirect_uri="https://example.com/",
    scope=["tweet.read", "users.read"],
    # Client Secret is only necessary if using a confidential client
    client_secret=client_secret
)

auth_url = oauth2_user_handler.get_authorization_url()
print(auth_url)
full_url = input("Paste in the full URL after you authorized your App: ")
access_token2 = oauth2_user_handler.fetch_token(full_url)
access = access_token2['access_token']

numberOfTweets = 20


while True:
    fetchtokenfile = open("last_fetch_token.txt", "r")
    fetch_token = fetchtokenfile.read()
    fetchtokenfile.close()
    if fetch_token:
        fetch_token = "&pagination_token=" + fetch_token
    user_me = requests.request("GET", f"https://api.twitter.com/2/users/{andreVenturaID}/tweets/?tweet.fields=public_metrics&max_results={numberOfTweets}{fetch_token}",
                               headers={'Authorization': 'Bearer {}'.format(access)}).json()

    handle_tweets(user_me)

    response = input("Continuar? (y/n)\n")
    yes = ['y', 'yes', 's', 'sim']
    if response not in yes:
        break


exit(0)