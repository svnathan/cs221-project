import xml.etree.ElementTree as et
import random
import pickle
import math
import test
import operator
import collections
import string
import re
import word_pairs
import time

NUM_WORDS_IN_TUPLE = 2
PAIR_COUNT_THRESHOLD = 15

questionTagsDict = {}
user_tagsList_dict = {}
user_tagPairList_dict = {}
tagPair_count_dict = collections.Counter()
final_tagPair_count_dict = {}

percentDone = 0 # For status completion

def parseDatasetForTags():
    print "Reading Dataset..."
    tree = et.parse("dataset/Posts.xml")
    doc = tree.getroot()
    print "Done!!" 
    iter = 0
    totalRows = len(doc.findall('row'))
    createQuestionTagsDict(doc)
    global percentDone
    percentDone = 0
    print "Parsing the answers now..."
    for row in doc.findall('row'):
        iter += 1
        printCompletionStatus(iter,totalRows)
        year = row.get('CreationDate').split('-')[0]
        if int(year) < 2016:
            if row.get('PostTypeId') != '2':
                continue
            else:
                user = row.get('OwnerUserId')
                questionID = row.get('ParentId')
                tags = getTagsForQuestionID(questionID)
#                 print user,questionID,tags
                if user is not None:
                    if user not in user_tagsList_dict:
                        user_tagsList_dict[user] = []
                    for t in tags:
                        if (t not in user_tagsList_dict[user]):
                            user_tagsList_dict[user].append(t)
    print "Answers Parsed!!"
                    
def createQuestionTagsDict(doc):
    iter = 0
    maxRows = len(doc.findall('row'))
    global percentDone
    percentDone = 0
    print "Parsing the Tags in the Questions:"
    for row in doc.findall('row'):
        iter += 1
        printCompletionStatus(iter,maxRows)
        if row.get('PostTypeId') == '1':
            tagList = row.get('Tags').split('><')
            tagList[0] = tagList[0].split('<')[1]
            tagList[-1] = tagList[-1].split('>')[0]
            questionTagsDict[row.get('Id')] = tagList
    print "Tags Parsed!!"

def getTagsForQuestionID(questionID):
    if questionID in questionTagsDict:
        return questionTagsDict[questionID]
    else:
        return []

def create_features(user_tagsList_dict):
    global percentDone
    percentDone = 0
    iter = 0
    maxIter = len(user_tagsList_dict)
    for user in user_tagsList_dict:
        iter += 1
        user_tagPairList_dict[user] = word_pairs.createWordTuples(user_tagsList_dict[user],NUM_WORDS_IN_TUPLE)
        
        for item in user_tagPairList_dict[user]:
            if item not in tagPair_count_dict:
                tagPair_count_dict[item] = 1
            else:
                tagPair_count_dict[item] += 1
            
            if tagPair_count_dict[item] > PAIR_COUNT_THRESHOLD:
                final_tagPair_count_dict[item] = tagPair_count_dict[item]
        
        printCompletionStatus(iter,maxIter)
    print "Collab Filter Feature Vector created!!"
    print "Number of Thresholded unique pairs: %d" % len(final_tagPair_count_dict)
                
def printCompletionStatus(currIter,maxIter):
    global percentDone
    percentDoneNext = currIter*100/maxIter
    if percentDone != percentDoneNext:
        print'{0}% Done...\r'.format(percentDoneNext),
        percentDone = percentDoneNext
        time.sleep(0.025)

parseDatasetForTags()
create_features(user_tagsList_dict)
# print final_tagPair_count_dict