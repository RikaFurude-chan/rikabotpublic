import discord
from stringParsing import parser1, parser2, emoToPic
from data import normal, users, replies, replies2, save

async def registrate(result, message, serverid):
    userid = str(result[2])
    user = result[4]
    if (user in [serverid]):
        await message.channel.send('rika already know ' + user + '!')
        await message.channel.send(file=discord.File('images/ri_nikoa1.png'))
        return
    if (userid in users[serverid]):
        await message.channel.send('rika already know ' + users[userid]['givenName'] + '!')
        await message.channel.send(file=discord.File('images/ri_nikoa1.png'))
        return
    normal[serverid][user] = userid
    if (not userid in users[serverid]):
        users[serverid][userid] = {'isReply': False, 'replyStrings': {}, 'changed': False, 'changeName': '', 'oldName': '',
                         'morphTime': 0.0, 'skullCount': 0, 'givenName': user, 'rikaCount': 0, 'trivia': False, 'trivNum': 0, 'triviaName': '', 'replyStrings': {}, 'albumName': '', 'album': False, 'albumNum': 0, 'albumView': -1, 'albumAuto': False, 'city': ''}
    await message.channel.send('hi ' + user)
    await message.channel.send(file=discord.File('images/ri_defa1.png'))
    save('users')
    save('normal')
    return

async def repeatAfter(user_message, result2, message, serverid):
    strings = parser2(user_message)
    replyString = strings[2]
    middleString = strings[1]
    initString = strings[0]
    middleStrings = middleString.split()
    middleString = middleStrings[1]
    user = result2[2]
    if (not user in normal[serverid]):
        await message.channel.send('rika don\'t know ' + user)
        return
    if (replyString == ''):
        await message.channel.send('say what mii?')
        return
    userid = normal[serverid][user]
    users[serverid][userid]['replyStrings'][initString] = {}
    users[serverid][userid]['replyStrings'][initString]['replyString'] = replyString
    if (middleString == 'say' or emoToPic(middleString, serverid, False) == 'none'):
        users[serverid][userid]['replyStrings'][initString]['mood'] = 'none'
    else:
        users[serverid][userid]['replyStrings'][initString]['mood'] = middleString
    await message.channel.send(file=discord.File('images/ri_niyaria1.png'))
    save('users')
    return

async def stopReplyTo(result2, message, serverid):
    initString = parser1(message.content)
    user = result2[4]
    if (not user in normal[serverid]):
        await message.channel.send('smh rika don\'t even know ' + user)
        await message.channel.send(file=discord.File('images/ri_fumana1.png'))
        return
    userid = normal[serverid][user]
    if (not initString in users[serverid][userid]['replyStrings']):
        await message.channel.send('smh rika not even reply to ' + user)
        await message.channel.send(file=discord.File('images/ri_fumana1.png'))
        return
    del users[serverid][userid]['replyStrings'][initString]
    await message.channel.send('o okie mii~ ')
    await message.channel.send(file=discord.File('images/ri_defa1.png'))
    save('users')
    return

async def sayYafterX(user_message, message, result2, serverid):
    strings = parser2(user_message)
    replyString = strings[0]
    middleString = result2[1]
    initString = strings[2]
    replies[serverid][initString] = {}
    replies[serverid][initString]['replyString'] = replyString
    if (middleString == 'say' or emoToPic(middleString, serverid, False) == 'none'):
        replies[serverid][initString]['mood'] = 'none'
    else:
        replies[serverid][initString]['mood'] = middleString
    save('replies')
    await message.channel.send(file=discord.File('images/ri_niyaria1.png'))
    return

async def stopRespondTo(user_message, message, serverid):
    initString = parser1(user_message)
    if (not initString in replies[serverid]):
        await message.channel.send('rika never respond to ' + initString + ' in first place!')
        await message.channel.send(file=discord.File('images/ri_majimea1.png'))
        return
    del replies[serverid][initString]
    save('replies')
    await message.channel.send('okay')
    await message.channel.send(file=discord.File('images/ri_defa1.png'))

async def seeSay(user_message, message, serverid):
    strings = parser2(user_message)
    replyString = strings[2]
    middleString = strings[1]
    initString = strings[0].lower()
    middleStrings = middleString.split()
    middleString = middleStrings[1]
    replies2[serverid][initString] = {}
    replies2[serverid][initString]['replyString'] = replyString
    if (middleString == 'say' or emoToPic(middleString, serverid, False) == 'none'):
        replies2[serverid][initString]['mood'] = 'none'
    else:
        replies2[serverid][initString]['mood'] = middleString
    save('replies2')
    await message.channel.send(file=discord.File('images/ri_niyaria1.png'))

async def ignorePhrase(user_message, message, serverid):
    initString = parser1(user_message).lower()
    if (not initString in replies2[serverid]):
        await message.channel.send('rika never pay attention to ' + initString + ' in first place!')
        await message.channel.send(file=discord.File('images/ri_majimea1.png'))
        return
    del replies2[serverid][initString]
    save('replies2')
    await message.channel.send('okay')
    await message.channel.send(file=discord.File('images/ri_defa1.png'))

async def sayAfter(result, result2, lowered, message, user_message, serverid):
    # registration
    if (len(result2) >= 5 and result2[1] == 'userid' and result2[3] == 'is' and len(result2) == 5):
        await registrate(result, message, serverid)
        return 0

    # repeats after someone else
    if (len(result2) >= 8 and result2[1] == 'when'):
        await repeatAfter(user_message, result, message, serverid)
        return 0

    if (len(result2) >= 9 and result2[1] == 'stop' and result2[2] == 'reply' and result2[3] == 'to' and 'when they say' in lowered):
        await stopReplyTo(result, message, serverid)
        return 0

    # says y after x
    if (len(result2) >= 5 and (result2[1] == 'say' or result2[2] == 'say') and "after" in lowered):
        await sayYafterX(user_message, message, result2, serverid)
        return 0

    if (len(result2) >= 5 and result2[1] == 'stop' and result2[2] == 'respond' and result2[3] == 'to'):
        await stopRespondTo(user_message, message, serverid)
        return 0

    if (len(result2) >= 6 and result2[1] == 'see' and 'say' in lowered):
        await seeSay(user_message, message, serverid)
        return 0

    if (len(result2) >= 4 and result2[1] == 'ignore' and result2[2] == 'phrase'):
        await ignorePhrase(user_message, message, serverid)
        return 0
    return 1
