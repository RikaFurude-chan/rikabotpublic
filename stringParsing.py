import time
from data import botinfo

def isQuote(c : str):
    return c == '\"' or c == '“' or c == '”'

def removeExtraSlash(s : str) -> str:
    newString = s
    index = 0
    while (index < len(newString)):
        if (index < len(newString) - 1 and newString[index] == '\\' and isQuote(newString[index+1])):
            newString = newString[:index] + newString[index+1:]
        else:
            index = index + 1
    return newString

def howManyQuotes(s : str):
    count = 0
    index = 0
    while (index < len(s)):
        if (index < len(s) - 1 and s[index] != '\\' and isQuote(s[index + 1])):
            count = count + 1
        index = index + 1
    return count

def parser1(s : str) -> str:
    start = -1
    end = -1
    count = 0
    for i in range(len(s)):
        if (isQuote(s[i]) and s[i-1] != '\\' and count == 0):
            start = i+1
            count = count + 1
        elif (isQuote(s[i]) and s[i-1] != '\\' and count == 1):
            end = i
            break
    return removeExtraSlash(s[start:end])

def parser2(s : str):
    start = -1
    end = -1
    count = 0
    i = 0
    for i in range(len(s)):
        if (isQuote(s[i]) and s[i - 1] != '\\' and count == 0):
            start = i + 1
            count = count + 1
        elif (isQuote(s[i]) and s[i - 1] != '\\' and count == 1):
            end = i
            break
    list = []
    list.append(removeExtraSlash(s[start:end]))
    i = i + 1
    start = i+1
    end = -1
    j = i
    for j in range(i, len(s)):
        if (isQuote(s[j])):
            end = j
            break
    list.append(removeExtraSlash(s[start:end]))
    i = j
    start = -1
    end = -1
    count = 0
    for j in range(i, len(s)):
        if (isQuote(s[j]) and s[j - 1] != '\\' and count == 0):
            start = j + 1
            count = count + 1
        elif (isQuote(s[j]) and s[j - 1] != '\\' and count == 1):
            end = j
            break
    list.append(removeExtraSlash(s[start:end]))
    return list

def isSpaces(s : str):
    for i in range(len(s)):
        if (s[i] != ' '):
            return False
    return True

def emoToPic(s : str, serverid, real):
    if (s == 'angrily'):
        if (real):
            botinfo[serverid]['mad'] = 1
            botinfo[serverid]['clock'] = time.time()
        return 'images/ri_majimea1.png'
    elif (s == 'happily'):
        if (real):
            botinfo[serverid]['mad'] = 0
        return 'images/ri_nikoa1.png'
    elif (s == 'seriously'):
        return 'images/ri_fumana1.png'
    elif (s == 'contentedly'):
        return 'images/ri_defa1.png'
    elif (s == 'nipahly'):
        if (real):
            if (botinfo[serverid]['mad'] > 0):
                return 'images/higurashiold/ri_fumana1.png'
        return 'images/ri_waraia1.png'
    elif (s == 'uncomfortably'):
        return 'images/ri_komarua2.png'
    elif (s == 'abashedly'):
        return 'images/ri_komarua1.png'
    elif (s == 'deviously'):
        return 'images/ri_niyaria1.png'
    elif (s == 'blankly'):
        return 'images/higurashiold/ri_defa1.png'
    elif (s == 'uncontentedly'):
        return 'images/higurashiold/ri_fumana1.png'
    elif (s == 'embarassedly'):
        return 'images/higurashiold/ri_komarua1.png'
    elif (s == 'dejectedly'):
        return 'images/higurashiold/ri_komarua2.png'
    elif (s == 'enragedly'):
        if (real):
            botinfo[serverid]['mad'] = 1
            botinfo[serverid]['clock'] = time.time()
        return 'images/higurashiold/ri_majimea1.png'
    elif (s == 'smilingly'):
        return 'images/higurashiold/ri_nikoa1.png'
    elif (s == 'smugly'):
        return 'images/higurashiold/smug.png'
    elif (s == 'complacently'):
        return 'images/higurashiold/ri_niyaria1.png'
    elif (s == 'joyfully'):
        if (real):
            if (botinfo[serverid]['mad'] > 0):
                return 'images/higurashiold/ri_fumana1.png'
        return 'images/higurashiold/ri_waraia1.png'
    else:
        return 'none'