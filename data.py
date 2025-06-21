import json

normal = {}
users = {}
replies = {}
replies2 = {}
images = {}
channels = {}
books = {}
album = {}
youtube = {}

with open('json/normal.json', 'r') as fp:
    normal = json.load(fp)

with open('json/users.json', 'r') as fp:
    users = json.load(fp)

with open('json/replies.json', 'r') as fp:
    replies = json.load(fp)

with open('json/replies2.json', 'r') as fp:
    replies2 = json.load(fp)

with open('json/images.json', 'r') as fp:
    images = json.load(fp)

with open('json/channels.json', 'r') as fp:
    channels = json.load(fp)

with open('json/books.json', 'r') as fp:
    books = json.load(fp)

with open('json/trivia.json', 'r') as fp:
    trivia = json.load(fp)

with open('json/album.json', 'r') as fp:
    album = json.load(fp)

with open('json/youtube.json', 'r') as fp:
    youtube = json.load(fp)

data = {'normal' : normal, 'users' : users, 'replies' : replies, 'replies2' : replies2, 'images' : images, 'channels' : channels, 'books' : books, 'trivia' : trivia, 'album' : album, 'youtube' : youtube}

botinfo = {}
for key in users:
    botinfo[key] = {'countStop' : 0, 'saidStop' : False, 'mad' : 0, 'clock' : 0.0, 'readid' : -1, 'autoread' : False, 'readid2' : -1, 'autoread2' : False,
                    'readingbook' : '', 'start' : 0, 'stuff' : '', 'chapter' : '', 'part' : '', 'higstart' : 0, 'higstuff' : ''}

def save(s : str):
    if (s == 'normal'):
        with open('json/normal.json', 'w') as fp:
            json.dump(normal, fp)
    elif (s == 'users'):
        with open('json/users.json', 'w') as fp:
            json.dump(users, fp)
    elif (s == 'replies'):
        with open('json/replies.json', 'w') as fp:
            json.dump(replies, fp)
    elif (s == 'replies2'):
        with open('json/replies2.json', 'w') as fp:
            json.dump(replies2, fp)
    elif (s == 'images'):
        with open('json/images.json', 'w') as fp:
            json.dump(images, fp)
    elif (s == 'channels'):
        with open('json/channels.json', 'w') as fp:
            json.dump(channels, fp)
    elif (s == 'books'):
        with open('json/books.json', 'w') as fp:
            json.dump(books, fp)
    elif (s == 'trivia'):
        with open('json/trivia.json', 'w') as fp:
            json.dump(trivia, fp)
    elif (s == 'album'):
        with open('json/album.json', 'w') as fp:
            json.dump(album, fp)
    elif (s == 'youtube'):
        with open('json/youtube.json', 'w') as fp:
            json.dump(youtube, fp)


for serverid in users:
    for user in users[serverid]:
        users[serverid][user]['triviaName'] = ''
        users[serverid][user]['trivia'] = False
        users[serverid][user]['albumName'] = ''
        users[serverid][user]['album'] = False
        users[serverid][user]['albumView'] = -1
        users[serverid][user]['albumAuto'] = False
        save('users')

for serverid in trivia:
    for triviaName in trivia[serverid]:
        trivia[serverid][triviaName]['numUsing'] = 0

for serverid in album:
    for albumName in album[serverid]:
        album[serverid][albumName]['numUsing'] = 0