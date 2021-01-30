import requests

total = []
dictionary = {}
stonkNames = []
URL = ''

threshold = 10000


async def ping():
    f = open('keys.txt', 'w')
    for item in f:
        print(item)
        await query.channel.send('Yo check this shit out!' + item + 'is makin\' money moves')
    f.close()


def addToFile():
    f = open('keys.txt', 'a')
    for a in dictionary.keys():
        if dictionary.get(a) > threshold:
            f.write(a)
            print(a)
            dictionary.update({a: 0})
    f.close()


def checkPing(totals):
    for thing in totals:
        for other in totals:
            if thing == other:
                if dictionary.get(thing) is None:
                    dictionary.update({thing: 2})
                else:
                    dictionary.update({thing: dictionary.get(thing) + 1})


def updateBannedList():
    global stonkNames
    f = open('stonkNames.txt', 'r')
    stonkNames = []
    temp = ''
    for word in f:
        temp = temp + word
    stonkNames = temp.splitlines()
    f.close()


def banned(w):
    for item in stonkNames:
        if w == item:
            return True
    return False


def removeSpecials(w):
    new_word = ''
    for char in w:
        if char.isalpha():
            new_word = new_word + char
    return new_word


def formatURL(strg):
    global URL
    if strg[1] == 's':
        toggle = 'submission'
    elif strg[1] == 'c':
        toggle = 'comment'
    else:
        raise Exception('Search destination not specified please use s or c.')

    subreddit = strg[2]
    searchterm = strg[3]

    URL = 'https://api.pushshift.io/reddit/search/' + toggle + '/?q=' + searchterm + '/?subreddit=' + subreddit

    try:
        request = requests.get(URL)
    except:
        print(URL)
        return
    if request.status_code == 200:
        findStonks(0)
    else:
        a = 1


def parseMessage(m):
    global query
    query = m
    s = query.content.split()
    if s[1] == 'update':
        findStonks(1)
    else:
        formatURL(s)


def findStonks(input):
    while True:
        # Uses the api's website to search reddit for posts
        if input == 0:
            global URL
        else:
            URL = 'https://api.pushshift.io/reddit/search/submission/?subreddit=wallstreetbets'

        page = requests.get(URL)

        string = ''
        for word in page.text:
            string = string + word

        words = string.split()
        counter1 = 0
        counter2 = 0
        stonks = []

        updateBannedList()

        for word in words:
            if word == '\"title\":':
                counter1 = counter1 + 1
                continue
            if word == '\"total_awards_received\":':
                counter2 = counter2 + 1
                continue
            if not counter1 == 0 and counter2 == 0:
                word = removeSpecials(word)
                if word.isupper() and banned(word):
                    stonks.append(word)
                continue
            if not counter2 == 0:
                counter1 = 0
                counter2 = 0

        for item in stonks:
            total.append(item)

        checkPing(total)
