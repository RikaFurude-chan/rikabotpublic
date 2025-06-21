#used in counting leaderboard, sorts by second index
def merge(list1, list2):
    list = []
    i1 = 0
    i2 = 0
    while (i1 != len(list1) and i2 != len(list2)):
        if (list1[i1][1] >= list2[i2][1]):
            list.append(list2[i2])
            i2 = i2 + 1
        else:
            list.append(list1[i1])
            i1 = i1 + 1
    if (i1 == len(list1)):
        while (i2 != len(list2)):
            list.append(list2[i2])
            i2 = i2 + 1
    elif (i2 == len(list2)):
        while (i1 != len(list1)):
            list.append(list1[i1])
            i1 = i1 + 1
    return list

def mergeSort(list):
    if (len(list) <= 1):
        return list
    n = len(list)
    list1 = mergeSort(list[0:(n//2)])
    list2 = mergeSort(list[(n//2):n])
    return merge(list1,list2)

def mergeLex(list1, list2):
    list = []
    i1 = 0
    i2 = 0
    while (i1 != len(list1) and i2 != len(list2)):
        if (list1[i1] >= list2[i2]):
            list.append(list2[i2])
            i2 = i2 + 1
        else:
            list.append(list1[i1])
            i1 = i1 + 1
    if (i1 == len(list1)):
        while (i2 != len(list2)):
            list.append(list2[i2])
            i2 = i2 + 1
    elif (i2 == len(list2)):
        while (i1 != len(list1)):
            list.append(list1[i1])
            i1 = i1 + 1
    return list

def mergeSortLex(list):
    if (len(list) <= 1):
        return list
    n = len(list)
    list1 = mergeSortLex(list[0:(n//2)])
    list2 = mergeSortLex(list[(n//2):n])
    return mergeLex(list1,list2)

def listEquality(list1, list2):
    if (len(list1) != len(list2)):
        return False
    for i in range(len(list1)):
        if (list1[i] != list2[i]):
            return False
    return True