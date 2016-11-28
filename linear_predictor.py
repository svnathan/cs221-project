import sys
import xml.etree.ElementTree as et
import random
import pickle
import math
import test
import operator
import collections
import string
import re

def main():
    rndm_users = test.get_randomusersid_list_list()
    questionsList = test.get_questionscontent_list()
    resultList = []
    dataset = parseDataset()
    print "Dataset Parsed!!"
    numIterations = len(rndm_users)
    
    for iter in range(numIterations):
        posts = filterDataset(dataset, rndm_users[iter])
        weights = linear_predictor(posts)
        question = processQuestion(questionsList[iter])
        probabilityMatrix = computeLikelihood(weights,question)
        print probabilityMatrix
        resultList.append(probabilityMatrix)
    test.check_answer(resultList)

def linear_predictor(posts):
    phi_X = {} # Matrix of feature vectors - one vector for each user. Sparse representation.
    for userID,comments in posts.iteritems(): # Loop over all the users
        word_counter = collections.Counter()
        for nextComment in comments: # For each user, loop over all the comments
            text = nextComment.split() # Split each comment into individual words using ' ' as delimiter
            for word in text: # Update the counts corresponding to each word.
                if word in word_counter:
                    word_counter[word] += 1
                else:
                    word_counter[word] = 1
        
        phi_X[userID] = word_counter # Update the feature vector matrix
#     print "phi-of-X generated!!"
    
    weight_vector = {}
    weights = {}
    eta = 0.1
    thisUserID = None
    for userID,comments in phi_X.iteritems(): # Initialize the weight vector:
        for word,count in comments.iteritems():
            if word not in weights:
                weights[word] = 0.0
    for userID in phi_X:
        weight_vector[userID] = weights
    
    iter = 0
    while eta > 0:
        iter += 1
#         print "Regression : Iter %d" % iter
        for userID_1,comments_1 in phi_X.iteritems():
            weights = weight_vector[userID_1]
            for userID_2,comments_2 in phi_X.iteritems():
                y = 1.0 if userID_1 == userID_2 else -1.0
                weights = updateWeight(eta,weights,gradient(weights,comments_2,y,len(phi_X)))
            weight_vector[userID_1] = weights
        eta = eta - 0.01
    return weight_vector

def gradient(weight,phiX,y,trainingSetSize):
    gradientVector = {}
    for word,count in weight.iteritems():
        product = count*phiX[word] if word in phiX else 0
        result = (2.0*(product-y)*phiX[word])/trainingSetSize if word in phiX else 0
        gradientVector[word] = result
    return gradientVector
    
def updateWeight(eta,weight,gradientVector):
    newWeight = {}
    for word,count in weight.iteritems():
        newWeight[word] = count - eta*gradientVector[word] if word in gradientVector else count
    return newWeight
    
def computeLikelihood(weights,question):
    likelyhood = {}
    normalizingFactor = 1.0
    total = 0
    for user in weights:
        for word in question:
            if word in weights[user]:
                total += weights[user][word]*question[word]
        likelyhood[user] = total if total > 0 else 0
        normalizingFactor += likelyhood[user]
    
    for user in weights:
        likelyhood[user] = likelyhood[user]/normalizingFactor
        
    return likelyhood

def processQuestion(question):
    wordList = question.split()
    q = {}
    for word in wordList:
        q[word] = q[word] + 1.0 if word in q else 1.0
    return q

def parseDataset():
    tree = et.parse("dataset/Posts.xml")
    doc = tree.getroot()
    
    posts_dict = {}
    for row in doc.findall('row'):
        ownerUserID = row.get('OwnerUserID')
        year = row.get('CreationDate').split('-')[0]
        if int(year) < 2016:
            if ownerUserID not in posts_dict:
                posts_dict[ownerUserID] = [row.get('Body')]
            else:
                posts_dict[ownerUserID].append(row.get('Body'))
            
    tree = et.parse("dataset/Comments.xml")
    doc = tree.getroot()
    for row in doc.findall('row'):
        ownerUserID = row.get('UserId')
        year = row.get('CreationDate').split('-')[0]
        if int(year) < 2016:
            if ownerUserID not in posts_dict:
                posts_dict[ownerUserID] = [row.get('Text')]
            else:
                posts_dict[ownerUserID].append(row.get('Text'))
            
    return posts_dict

def filterDataset(dataset, userList):
    posts = {}
#     i = 0
    for user in userList:
        if user in dataset:
            posts[user] = preprocessStrings(dataset[user])
#             if i == 0:
#                 print dataset[user]
#                 print posts[user]
#             i = 1
    return posts

def preprocessStrings(stringList):
    returnList = []
    for s in stringList:
        returnList.append(\
                        removeCommonWords(\
                        strip_punctuations(\
                        dehyphenateWords(\
                        removeURLs(\
                        s.lower()\
                        )))))
    return returnList
    
def strip_punctuations(s):
    si = list(s)
    for i,j in enumerate(si):
        if j in string.punctuation:
            si[i] = ''
    return ''.join(si)
    
def removeURLs(s):
    return re.sub(r'http.*[/ a-zA-Z0-9."]','',s,re.MULTILINE)
    
def dehyphenateWords(s): # This function replaces hyphenated words with words seperated by space
    return re.sub(r'-',' ',s,re.MULTILINE)
    
def removeCommonWords(s):
    commonWords = ['all','a','after','the','will','they','there','their','then',\
                    'am','an','you','your','them','your','youre','theres','beside',\
                    'besides','in','on','he','hes','she','shes','do','to','by','if',\
                    'of','as','or','what','when','why','also','is','might','may',\
                    'be','have','having','gave','give','giving','not','no','many',\
                    'this','our','from','find','finding','me','my','that','but',\
                    'does','doesnt','like','so','it','its','can','for','and','are',\
                    'could','would','should','each','where','we','i','get','gets',\
                    'now','too','any','more','take','taken','taking','been','use',\
                    'used','still','dont','couldnt','wouldnt','shouldnt','was']
                    
    s_list = s.split()
    s_list_new = []
    for word in s_list:
        if word not in commonWords:
            s_list_new.append(word)
    return ' '.join(s_list_new)

main()