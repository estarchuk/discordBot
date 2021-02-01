import requests

# Define global variables as needed
total = []
dictionary = {}
stonkNames = []
URL = ''
returnToggle = 0

# Threshold for the amount of instances needed for a ping
threshold = 10000


def removeDupes(filename):
    f = open(filename, '+')
    for item in f:
        x = item.split()
        for i in x:
            for j in x:
                if i == j:
                    j = ''
    f.close()


# Method to ping in discord
def ping():
    f = open('keys.txt', 'r')
    for item in f:
        print(item)
    f.close()
    return 'keys.txt'


# Method to check for keywords as they've been found
def addToFile():
    f = open('keys.txt', 'a')
    for a in dictionary.keys():
        if dictionary.get(a) > threshold:
            global returnToggle
            returnToggle = 1
            f.write(a)
            # print(a)
            dictionary.update({a: 0})
    f.close()


# Method to transfer from dictionary that holds kv pairs to just the key
def checkPing(totals):
    for thing in totals:
        for other in totals:
            if thing == other:
                if dictionary.get(thing) is None:
                    dictionary.update({thing: 2})
                else:
                    dictionary.update({thing: dictionary.get(thing) + 1})
    addToFile()


# This method update the variable banned list with all the names of the stocks for easy comparison
def updateBannedList():
    global stonkNames
    f = open('stonkNames.txt', 'r')
    stonkNames = []
    temp = ''
    for word in f:
        temp = temp + word
    stonkNames = temp.splitlines()
    f.close()


# This method checks if the words found are stock names or not
def banned(w):
    for item in stonkNames:
        if w == item:
            return True
    return False


# this method removes the special characters from a string
def removeSpecials(w):
    new_word = ''
    for char in w:
        if char.isalpha():
            new_word = new_word + char
    return new_word


# this method formats the URL when searching for specific things
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
        print('Website not active.')
        return


# This method checks if the message is just a general check or something else
def parseMessage(m):
    open('keys.txt', 'w').close()
    global query
    query = m
    s = query.content.split()
    if s[1] == 'update':
        findStonks(1)
    else:
        formatURL(s)
    x = ping()
    return x


# This method uses the pushshift api to check for the amount of uses of a keyword in a specific time
def findStonks(inp):
    while True:
        # Uses the api's website to search reddit for posts
        if inp == 0:
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

        f1 = open('keys.txt', 'a')
        for item in stonks:
            f1.write(item + ' ')
            total.append(item)
        f1.close()

        checkPing(total)

        if returnToggle > 0:
            return
