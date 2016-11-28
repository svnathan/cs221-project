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

NUM_WORDS_IN_TUPLE = 2
PAIR_COUNT_THRESHOLD = 0

user_tagsList_dict = {}
user_tagPairList_dict = {}
tagPair_count_dict = collections.Counter()
final_tagPair_count_dict = {}

def parseDatasetForTags():
    tree = et.parse("dataset/Posts.xml")
    doc = tree.getroot()
    iter = 0
    for row in doc.findall('row'):
        iter += 1
        print'{0} out of {1} entries parsed.\r'.format(iter,len(doc.findall('row'))),
        year = row.get('CreationDate').split('-')[0]
        if int(year) < 2016:
            if row.get('PostTypeId') != '2':
                continue
            else:
                user = row.get('OwnerUserId')
                questionID = row.get('ParentId')
                tags = getTagsForQuestionID(questionID,doc)
#                 print user,questionID,tags
                if user is not None:
                    if user not in user_tagsList_dict:
                        user_tagsList_dict[user] = []
                    for t in tags:
                        user_tagsList_dict[user].append(t)
                    
def getTagsForQuestionID(questionID,doc):
    for row in doc.findall('row'):
        if row.get('Id') == questionID:
            tagList = row.get('Tags').split('><')
            tagList[0] = tagList[0].split('<')[1]
            tagList[-1] = tagList[-1].split('>')[0]
            return tagList
        else:
            continue
    return []

def create_features(user_tagsList_dict):
    for user in user_tagsList_dict:
        user_tagPairList_dict[user] = word_pairs.createWordTuples(user_tagsList_dict[user],NUM_WORDS_IN_TUPLE)
        
        for item in user_tagPairList_dict[user]:
            tagPair_count_dict[item] += 1
            
            if tagPair_count_dict[item] > PAIR_COUNT_THRESHOLD:
                final_tagPair_count_dict[item] = tagPair_count_dict[item]

parseDatasetForTags()
# print user_tagsList_dict