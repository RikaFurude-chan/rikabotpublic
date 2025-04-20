import discord
from data import botinfo
import asyncio
from stringParsing import isSpaces

def getNextLine(serverid):
    mode = ''
    if (botinfo[serverid]['higstart'] + 12 >= len(botinfo[serverid]['higstuff'])):
        return ['yeastyyarlo', mode]
    while (botinfo[serverid]['higstuff'][botinfo[serverid]['higstart']:botinfo[serverid]['higstart'] + 10] != 'outputline' and botinfo[serverid]['higstuff'][botinfo[serverid]['higstart']:botinfo[serverid]['higstart'] + 12] != 'drawbustshot' and botinfo[serverid]['higstuff'][botinfo[serverid]['higstart']:botinfo[serverid]['higstart'] + 9] != 'drawscene'):
        botinfo[serverid]['higstart'] = botinfo[serverid]['higstart'] + 1
        if (botinfo[serverid]['higstart'] + 12 >= len(botinfo[serverid]['higstuff'])):
            return ['yeastyyarlo', mode]
    if (botinfo[serverid]['higstuff'][botinfo[serverid]['higstart']:botinfo[serverid]['higstart'] + 10] == 'outputline'):
        mode = 'outputline'
    elif (botinfo[serverid]['higstuff'][botinfo[serverid]['higstart']:botinfo[serverid]['higstart'] + 12] == 'drawbustshot'):
        mode = 'drawbustshot'
    else:
        mode = 'drawscene'
    while (botinfo[serverid]['higstuff'][botinfo[serverid]['higstart']] != '('):
        botinfo[serverid]['higstart'] = botinfo[serverid]['higstart'] + 1
    botinfo[serverid]['higstart'] = botinfo[serverid]['higstart'] + 1
    c1 = botinfo[serverid]['higstuff'][botinfo[serverid]['higstart']]
    c2 = botinfo[serverid]['higstuff'][botinfo[serverid]['higstart'] + 1]
    s2 = ''
    inQuote = False
    while (not (c1 == ')' and (not inQuote))):
        if (c1 != '\\' and c2 == '\"'):
            if (inQuote):
                inQuote = False
            else:
                inQuote = True
        s2 = s2 + c1
        botinfo[serverid]['higstart'] = botinfo[serverid]['higstart'] + 1
        c1 = botinfo[serverid]['higstuff'][botinfo[serverid]['higstart']]
        c2 = botinfo[serverid]['higstuff'][botinfo[serverid]['higstart'] + 1]
    return [s2, mode]


def howManyPart(s : str):
    count = 1
    inQuote = False
    j = 0
    while (j < len(s)):
        if ((not inQuote) and s[j] == ','):
            count = count + 1
        elif (inQuote and s[j-1] != '\\' and s[j] == '\"'):
            inQuote = False
        elif ((not inQuote) and s[j-1] != '\\' and s[j] == '\"'):
            inQuote = True
        j = j + 1
    return count

def readPart(s : str, i : int):
    inQuote = False
    j = 0
    count = 0
    while (count < i):
        if ((not inQuote) and s[j] == ','):
            count = count + 1
        elif (inQuote and s[j-1] != '\\' and s[j] == '\"'):
            inQuote = False
        elif ((not inQuote) and s[j-1] != '\\' and s[j] == '\"'):
            inQuote = True
        j = j + 1
    s2 = ''
    while (not (s[j] == ',' and (not inQuote))):
        if (inQuote and s[j - 1] != '\\' and s[j] == '\"'):
            inQuote = False
        elif ((not inQuote) and s[j - 1] != '\\' and s[j] == '\"'):
            inQuote = True
        s2 = s2 + s[j]
        j = j + 1
    return s2 if i == 0  else s2[1:]

def whatCom(s : str):
    if (len(s) == 0):
        return ''
    i = 0
    print(i)
    while (s[i] != '('):
        i = i + 1
    return s[:i]

async def setPos(i : int, channel, serverid):
    if (botinfo[serverid]['readid'] == -1):
        await channel.send('rika is not reading higurashi right now!')
        return
    if (botinfo[serverid]['autoread']):
        await channel.send('turn off higurashi autoread first!')
        return
    if (i < 0 or i + 12 > len(botinfo[serverid]['higstuff'])):
        await channel.send('invalid position!')
        return
    botinfo[serverid]['higstart'] = i
    await channel.send('position set!')
    return

async def getPos(channel, serverid):
    if (botinfo[serverid]['readid'] == -1):
        await channel.send('rika is not reading higurashi right now1')
        return
    await channel.send('current position is ' + str(botinfo[serverid]['higstart']) + '!')

async def higurashiChapters(channel, serverid):
    await channel.send('Higurashi contains 8 chapters, each with various parts, beginning with part 1.\n\n' +
                       'Onikakushi 18 parts\n' +
                       'Watanagashi 21 parts\n' +
                       'Tatarigoroshi 22 parts\n' +
                       'Himatsubushi 10 parts\n' +
                       'Meakashi 33 parts\n' +
                       'Tsumihoroboshi 35 parts\n' +
                       'Minagoroshi 38 parts\n' +
                       'Matsuribayashi 79 parts\n')

def chapterToParts(chapter : str):
    if (chapter == 'onikakushi'):
        return 18
    elif (chapter == 'watanagashi'):
        return 21
    elif (chapter == 'tatarigoroshi'):
        return 22
    elif (chapter == 'himatsubushi'):
        return 10
    elif (chapter == 'meakashi'):
        return 33
    elif (chapter == 'tsumihoroboshi'):
        return 35
    elif (chapter == 'minagoroshi'):
        return 38
    elif (chapter == 'matsuribayashi'):
        return 79
    else:
        return -1

async def startReading(channel, chapter2 : str, part2 : int, serverid):
    botinfo[serverid]['chapter'] = chapter2
    botinfo[serverid]['part'] = part2
    parts = chapterToParts(botinfo[serverid]['chapter'])
    if (parts == -1):
        await channel.send('rika don\'t recognize this higurashi chapter')
        return
    if (botinfo[serverid]['part'] <= 0 or botinfo[serverid]['part'] > parts):
        await channel.send(botinfo[serverid]['chapter'] + ' has ' + str(parts) + ' parts, starting from part 1')
        return
    path = 'higurashiText/' + botinfo[serverid]['chapter'] + '/' + str(botinfo[serverid]['part']) + '.txt'
    file = open(path, 'r', encoding="utf-8")
    botinfo[serverid]['higstuff'] = file.read()
    file.close()
    botinfo[serverid]['higstart'] = 0
    A = getNextLine(serverid)
    canExit = False
    while(not canExit):
        if (A[1] == ''):
            await channel.send('done!')
        if (A[1] == 'drawbustshot' and howManyPart(A[0]) >= 2):
            line = readPart(A[0], 1)
            line = line[1:len(line)-1]
            picture = 'higurashiText/' + botinfo[serverid]['chapter'] + '/CGAlt/' + line + '.png'
            try:
                await channel.send(file=discord.File(picture))
            except:
                picture = 'higurashiText/' + botinfo[serverid]['chapter'] + '/CG/' + line + '.png'
                await channel.send(file=discord.File(picture))
        elif (A[1] == 'drawscene'):
            line = readPart(A[0], 0)
            line = line[2:len(line) - 1]
            picture = 'higurashiText/' + botinfo[serverid]['chapter'] + '/CG/' + line + '.png'
            await channel.send(file=discord.File(picture))
        elif (A[1] == 'outputline' and howManyPart(A[0]) >= 4 and readPart(A[0],3) != 'NULL'):
            break
        A = getNextLine(serverid)
    line = readPart(A[0],3)
    line = line[1:len(line)-1]
    if isSpaces(line):
        line = line + '.'
    message = await channel.send(line)
    return message.id

async def nextline(channel, serverid):
    A = getNextLine(serverid)
    canExit = False
    while (not canExit):
        if (A[1] == ''):
            await channel.send(botinfo[serverid]['chapter'] + ' part ' + str(botinfo[serverid]['part']) + ' done!')
            return -1
        if (A[1] == 'drawbustshot' and howManyPart(A[0]) >= 2):
            line = readPart(A[0], 1)
            line = line[1:len(line) - 1]
            picture = 'higurashiText/' + botinfo[serverid]['chapter'] + '/CGAlt/' + line + '.png'
            try:
                await channel.send(file=discord.File(picture))
            except:
                picture = 'higurashiText/' + botinfo[serverid]['chapter'] + '/CG/' + line + '.png'
                await channel.send(file=discord.File(picture))
        elif (A[1] == 'drawscene'):
            line = readPart(A[0], 0)
            line = line[2:len(line) - 1]
            picture = 'higurashiText/' + botinfo[serverid]['chapter'] + '/CG/' + line + '.png'
            await channel.send(file=discord.File(picture))
        elif (A[1] == 'outputline' and howManyPart(A[0]) >= 4 and readPart(A[0], 3) != 'NULL'):
            break
        A = getNextLine(serverid)
    line = readPart(A[0], 3)
    line = line[1:len(line) - 1]
    if isSpaces(line):
        line = line + '.'
    message = await channel.send(line)
    return message.id

async def autoread(channel, result2, serverid):
    if (botinfo[serverid]['autoread'] or botinfo[serverid]['readid'] == -1):
        return
    botinfo[serverid]['autoread'] = True
    interval = float(result2[5])
    while (botinfo[serverid]['autoread'] and not botinfo[serverid]['readid'] == -1):
        botinfo[serverid]['readid'] = await nextline(channel, serverid)
        await asyncio.sleep(interval)
    botinfo[serverid]['autoread'] = False



async def readingHigurashi(result2, message, lowered, serverid):
    if (lowered == 'rika higurashi chapters'):
        await higurashiChapters(message.channel, serverid)
        return 0

    if (len(result2) == 7 and result2[2] == 'start' and result2[3] == 'reading' and result2[5] == 'part'):
        if (botinfo[serverid]['autoread']):
            await message.channel.send('turn off autoread first!')
            return
        botinfo[serverid]['readid'] = await startReading(message.channel, result2[4].lower(), int(result2[6]), serverid)
        return 0

    if (len(result2) == 7 and result2[2] == 'autoread' and result2[3] == 'on' and result2[4] == 'every' and result2[
        6] == 'seconds'):
        await autoread(message.channel, result2, serverid)
        return 0

    if (lowered == 'rika higurashi autoread off'):
        botinfo[serverid]['autoread'] = False
        return 0

    if (len(result2) == 5 and result2[2] == 'goto' and result2[3] == 'position'):
        await setPos(int(result2[4]), message.channel, serverid)
        return 0

    if (lowered == 'rika higurashi get current position'):
        await getPos(message.channel, serverid)
        return 0

    return 1

