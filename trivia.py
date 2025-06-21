from stringParsing import parser1, parser2, parser3
from data import trivia, users, save

async def triviaHandler(result2, lowered, message, user_message, serverid):

    if (len(result2) >= 4 and result2[1] == 'start' and result2[2] == 'trivia'):
        triviaName = parser1(user_message)
        userid = str(message.author.id)
        if (not userid in users[serverid]):
            await message.channel.send('rika don\'t know who you are')
            return 0
        if (not triviaName in trivia[serverid]):
            await message.channel.send('rika don\'t know trivia ' + triviaName)
            return 0
        users[serverid][userid]['trivia'] = True
        users[serverid][userid]['triviaName'] = triviaName
        trivia[serverid][triviaName]['numUsing'] = trivia[serverid][triviaName]['numUsing'] + 1
        trivNum = users[serverid][userid]['trivNum']
        length = trivia[serverid][triviaName]['length']
        if (length == 0):
            await message.channel.send('trivia ' + triviaName + ' has no questions mii!')
            return 0
        reply = trivia[serverid][triviaName]['questions'][trivNum % length]['question']
        await message.channel.send(reply)
        return 0

    if (lowered == 'rika stop trivia'):
        userid = str(message.author.id)
        if (not userid in users[serverid]):
            await message.channel.send('rika don\'t know who you are')
            return 0
        if (not users[serverid][userid]['trivia']):
            await message.channel.send('trivia is already off!')
            return 0
        users[serverid][userid]['trivia'] = False
        triviaName = users[serverid][userid]['triviaName']
        users[serverid][userid]['triviaName'] = ''
        trivia[serverid][triviaName]['numUsing'] = trivia[serverid][triviaName]['numUsing'] - 1
        await message.channel.send('mii~! trivia stopped!')
        return 0

    if (len(result2) >= 11 and result2[1] == 'add' and result2[2] == 'to' and result2[3] == 'trivia' and result2[4]):
        strings = parser3(user_message)
        triviaName = strings[0]
        x = strings[1]
        y = strings[2].lower()
        if (triviaName in trivia[serverid] and trivia[serverid][triviaName]['numUsing'] > 0):
            await message.channel.send('trivia ' + triviaName + ' currently in use!')
            return 0
        if (not triviaName in trivia[serverid]):
            trivia[serverid][triviaName] = {}
            trivia[serverid][triviaName]['numUsing'] = 0
            trivia[serverid][triviaName]['length'] = 0
            trivia[serverid][triviaName]['questions'] = []
        length = trivia[serverid][triviaName]['length']
        questions = trivia[serverid][triviaName]['questions']
        n = len(questions)
        index = -1
        for i in range(n):
            if (x == questions[i]['question']):
                index = i
                break
        if (index >= 0):
            questions[index]['answers'].append(y)
        else:
            questions.append({})
            questions[length]['question'] = x
            questions[length]['answers'] = [y]
            trivia[serverid][triviaName]['length'] = length + 1
        save('trivia')
        await message.channel.send('question added mii~!')
        return 0

    if (len(result2) >= 8 and result2[1] == 'remove' and result2[2] == 'from' and result2[3] == 'trivia'):
        strings = parser2(user_message)
        triviaName = strings[0]
        question = strings[2]
        if (not triviaName in trivia[serverid]):
            await message.channel.send('rika don\'t know trivia ' + triviaName)
            return 0
        if (triviaName in trivia[serverid] and trivia[serverid][triviaName]['numUsing'] > 0):
            await message.channel.send('trivia ' + triviaName + ' currently in use!')
            return 0
        questions = trivia[serverid][triviaName]['questions']
        n = len(questions)
        index = -1
        for i in range(n):
            if (question == questions[i]['question']):
                index = i
                break
        if (index == -1):
            await message.channel.send('question does not exist in ' + triviaName + '!')
            return 0
        questions.pop(index)
        trivia[serverid][triviaName]['length'] = trivia[serverid][triviaName]['length'] - 1
        save('trivia')
        await message.channel.send('question removed mii~!')
        return 0

    return 1

