import collections
import sys
import string

def createWordTuples(inputList,nMax):
# inputList - The input list of words. We expect the words to be preprocessed with no punctuations
# n         - The number of words in a tuple.
# return    - This function returns a list of all possible n-tuples. Each n-tuple is stored
#               as a LIST.

    def addWordToList(wordList,num,wordNum):
        if num > 2:
            returnList = []
            for x in range(wordNum+1,len(inputList)):
                newList = [word for word in wordList]
                newList.append(inputList[x])
                wordPairs = addWordToList(newList,num-1,x)
                for item in wordPairs:
                    returnList.append(item)
            return returnList
        else:
            returnList = []
            for x in range(wordNum+1,len(inputList)):
                newList = [word for word in wordList]
                newList.append(inputList[x])
                returnList.append(newList)
            return returnList
    
    wordTuples = []
    for x in range(len(inputList)):
        newList = addWordToList([inputList[x]],nMax,x)
        if len(newList) > 0:
            for item in newList:
                wordTuples.append(sorted(item))
#     print len(wordTuples)
    return wordTuples

# s = 'This is also a trial String'
# print createWordTuples(s.split(),4)