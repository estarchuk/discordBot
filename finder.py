import requests

total = []
dictionary = {}
bannedList = []

threshold = 5000


def ping():
    for a in dictionary.keys():
        if dictionary.get(a) > threshold:
            # Ping in discord here
            print('PING ' + a)
            dictionary.update({a: 0})


def checkPing(totals):
    ping()
    for thing in totals:
        for other in totals:
            if thing == other:
                if dictionary.get(thing) is None:
                    dictionary.update({thing: 2})
                else:
                    dictionary.update({thing: dictionary.get(thing) + 1})


def updateBannedList():
    global bannedList
    f = open('bannedList.txt', 'r')
    bannedList = []
    temp = ''
    for word in f:
        temp = temp + word
    bannedList = temp.split()
    f.close()


def banned(w):
    for item in bannedList:
        if w == item:
            return False
    return True


def removeSpecials(w):
    new_word = ''
    for char in w:
        if char.isalpha():
            new_word = new_word + char
    return new_word


def main():
    while True:
        # Uses the api's website to search reddit for posts
        URL = 'https://api.pushshift.io/reddit/search/submission/?subreddit=wallstreetbets'
        page = requests.get(URL)

        counter = 0
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
                if word.isupper() and len(word) <= 4 and banned(word):
                    stonks.append(word)
                continue
            if not counter2 == 0:
                counter1 = 0
                counter2 = 0

        for item in stonks:
            total.append(item)

        checkPing(total)


if __name__ == "__main__":
    main()
