import json

normal = {}
users = {}
replies = {}
replies2 = {}
images = {}
channels = {}
books = {}

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

data = {'normal' : normal, 'users' : users, 'replies' : replies, 'replies2' : replies2, 'images' : images, 'channels' : channels, 'books' : books}

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

