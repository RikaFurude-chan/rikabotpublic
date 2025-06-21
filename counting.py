from data import normal, users, save
import discord
from stringParsing import emoToPic
from sorting import mergeSort

async def rikaIncr(userid : str, channel, serverid):
    users[serverid][userid]['rikaCount'] = users[serverid][userid]['rikaCount'] + 1
    name = users[serverid][userid]['givenName']
    save('users')
    rikaCount = users[serverid][userid]['rikaCount']
    if (rikaCount % 10 == 0 and rikaCount >= 10):
        await channel.send(
            'nipah~! ' + name + ' has reached a rika count of ' + str(
                rikaCount) + '! rika is very proud of ' + name
            + '! fight on!')
        await channel.send(file=discord.File('images/ri_waraia1.png'))

async def howManyRika(user : str, channel, serverid):
    if (not user in normal[serverid]):
        await channel.send('rika don\'t know ' + user)
        return
    userid = normal[serverid][user]
    rikaCount = users[serverid][userid]['rikaCount']
    if (rikaCount == 0):
        await channel.send(user + ' has a rika count of ' + str(rikaCount))
        await channel.send(file=discord.File('images/ri_komarua2.png'))
    elif (rikaCount < 5):
        await channel.send(user + ' has a rika count of ' + str(rikaCount))
        await channel.send(file=discord.File('images/ri_defa1.png'))
    elif (rikaCount < 20):
        await channel.send(user + ' has a rika count of ' + str(rikaCount) + ' nipah!')
        await channel.send(file=discord.File('images/ri_nikoa1.png'))
    else:
        await channel.send(user + ' has a rika count of ' + str(rikaCount) + ' nipah!' +
                                   'more rika more rika!')
        await channel.send(file=discord.File('images/ri_waraia1.png'))
    return

async def skullIncr(userid : str, channel, mode : str, serverid):
    users[serverid][userid]['skullCount'] = users[serverid][userid]['skullCount'] + 1
    name = users[serverid][userid]['givenName']
    save('users')
    skullCount = users[serverid][userid]['skullCount']
    if (skullCount % 20 == 0 and skullCount >= 20):
        await channel.send(
            'holy shit ' + name + ' STOP SKULL EMOJI GRINDING! you already have a skull count of ' + str(
                skullCount) +
            '!!! this is extremely unhealthy! rika is getting very mad!')
        await channel.send(file=discord.File(emoToPic('enragedly', serverid, True)))
    elif (skullCount % 5 == 0 and skullCount >= 5):
        await channel.send(
            name + ' just ' + mode + ' the skull emoji again! ' + name + ' has a skull count of ' +
            str(skullCount) + '! shame on ' + name + '!')
        await channel.send(file=discord.File('images/ri_majimea1.png'))
    else:
        await channel.send(name + ' just ' + mode + ' the skull emoji :skull:')

async def howManySkull(user : str, channel, serverid):
    if (not user in normal[serverid]):
        await channel.send('rika don\'t know ' + user)
        return
    userid = normal[serverid][user]
    skullCount = users[serverid][userid]['skullCount']
    if (skullCount == 0):
        await channel.send(
            user + ' has a skull count of ' + str(skullCount) + '! rika is very proud of ' + user + '!')
        await channel.send(file=discord.File('images/ri_waraia1.png'))
    elif (skullCount < 5):
        await channel.send(user + ' has a skull count of ' + str(
            skullCount) + '. rika thinks this is an excusable amount of skull reactions,' +
                                   ' but ' + user + ' can do better!')
        await channel.send(file=discord.File('images/ri_defa1.png'))
    elif (skullCount < 20):
        await channel.send(
            user + ' has a skull count of ' + str(skullCount) + '. rika thinks this is an unhealthy number of skulls!' +
            ' rika urges ' + user + ' to control their skull reaction impulses!')
        await channel.send(file=discord.File('images/ri_majimea1.png'))
    else:
        await channel.send(user + ' has a skull count of ' + str(skullCount) + '. unbelievable. for the last time ' +
                                   user + ' STOP SKULL EMOJI GRINDING!!!')
        await channel.send(file=discord.File('images/higurashiold/ri_majimea1.png'))
    return

async def rikaLeaderboard(channel, serverid):
    keys = users[serverid].keys()
    list = []
    for key in keys:
        list.append([users[serverid][key]['givenName'], users[serverid][key]['rikaCount']])
    list = mergeSort(list)
    response = ''
    for i in range (len(list)):
        mode = ''
        if (list[len(list)-i-1][1] == 0):
            mode = ' rikas. use the rikasmile emoji!\n'
        elif (list[len(list)-i-1][1] <= 5):
            mode = ' rikas. you can do better!\n'
        elif (list[len(list)-i-1][1] <= 10):
            mode = ' rikas. mii~ very good!\n'
        elif (list[len(list)-i-1][1] <= 20):
            mode = ' rikas. nipah! fight on!\n'
        else:
            mode = ' rikas. nipah! rika is very proud of ' + list[len(list)-i-1][0] + '!\n'
        response = response + str(i+1) + '. ' + list[len(list)-i-1][0] + ': ' + str(list[len(list)-i-1][1]) + mode
    await channel.send(response)
    await channel.send(file=discord.File('images/ri_defa1.png'))

async def skullLeaderboard(channel, serverid):
    keys = users[serverid].keys()
    list = []
    for key in keys:
        list.append([users[serverid][key]['givenName'], users[serverid][key]['skullCount']])
    list = mergeSort(list)
    response = ''
    for i in range (len(list)):
        mode = ''
        if (list[len(list) - i - 1][1] == 0):
            mode = ' skulls. nipah! rika is very proud of ' + list[len(list)-i-1][0] + '!\n'
        elif (list[len(list) - i - 1][1] <= 5):
            mode = ' skulls. this is okay!\n'
        elif (list[len(list) - i - 1][1] <= 10):
            mode = ' skulls. this is getting unhealthy. be more thoughtful about the emojis you use!\n'
        elif (list[len(list) - i - 1][1] <= 20):
            mode = ' skulls. please use less skull emojis! rika is very mad! shame on you!\n'
        else:
            mode = ' skulls. what in the hell are you doing?!? STOP SKULL EMOJI GRINDING!!!\n'
        response = response + str(i+1) + '. ' + list[len(list) - i - 1][0] + ': ' + str(list[len(list) - i - 1][1]) + mode
    await channel.send(response)
    await channel.send(file=discord.File('images/ri_fumana1.png'))

async def skullApology(userid : str, channel, serverid):
    name = users[serverid][userid]['givenName']
    if (users[serverid][userid]['skullCount'] == 0):
        await channel.send('your record is already clean!')
    else:
        users[serverid][userid]['skullCount'] = users[serverid][userid]['skullCount'] - 1
        save('users')
        await channel.send('as long as you are sincere ' + name + ', rika forgives you! rika has removed one skull from your record!')
    await channel.send(file=discord.File('images/ri_defa1.png'))

async def counting(result, result2, message, lowered, serverid):
    # skull count
    if (len(result2) == 6 and result2[1] == 'what' and result2[2] == 'is' and result2[4] == 'skull' and result2[
        5] == 'count'):
        user = result[3]
        await howManySkull(user, message.channel, serverid)
        return 0

    if (lowered == 'rika show skull hall of shame please'):
        await skullLeaderboard(message.channel, serverid)
        return 0

    if (lowered == 'rika i sincerely apologize for using the skull emoji. i promise to be more thoughtful about what emojis i use in the future.'):
        userid = str(message.author.id)
        if (not userid in users[serverid]):
            await message.channel.send('mii? who are you?')
        else:
            await skullApology(userid, message.channel, serverid)
        return 0

    # rika count
    if (len(result2) == 6 and result2[1] == 'what' and result2[2] == 'is' and result2[4] == 'rika' and result2[
        5] == 'count'):
        user = result[3]
        await howManyRika(user, message.channel, serverid)
        return 0

    if (lowered == 'rika show rika leaderboard please'):
        await rikaLeaderboard(message.channel, serverid)
        return 0

    return 1