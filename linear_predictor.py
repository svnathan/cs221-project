import sys
import xml.etree.ElementTree as et
import random
import pickle
import math
import test
import operator
import collections

def gradient(weight,phiX,y,trainingSetSize):
	gradientVector = {}
	for word,count in weight.iteritems():
		product = count*phiX[word] if word in phiX else 0
		result = (2.0*product*phiX[word])/trainingSetSize if word in phiX else 0
		gradientVector[word] = result
	return gradientVector
	
def updateWeight(eta,weight,gradientVector):
	newWeight = {}
	for word,count in weight.iteritems():
		newWeight[word] = count - eta*gradientVector[word] if word in gradientVector else count
	return newWeight
	
def linear_predictor():
    rndm_users = test.get_randomusersid_list_list()
    posts = get_posts(rndm_users)
    print "Dataset Parsed!!"
    phi_X = {} # Matrix of feature vectors - one vector for each user. Sparse representation.
    for userID,comments in posts.iteritems(): # Loop over all the users
    	#comments = posts[userID]
    	word_counter = collections.Counter()
    	for nextComment in comments: # For each user, loop over all the comments
    		text = nextComment.split() # Split each comment into individual words using ' ' as delimiter
    		for word in text: # Update the counts corresponding to each word.
    			if word in word_counter:
    				word_counter[word] += 1
    			else:
    				word_counter[word] = 1
    	
    	phi_X[userID] = word_counter # Update the feature vector matrix
    print "phi-of-X generated!!"
    
    weight_vector = {}
    y_vector = {}
    eta = 0.1
    for userID,comments in phi_X.iteritems(): # Initialize the weight vector:
    	weights = {}
    	for word,count in comments.iteritems():
    		if word not in weights:
    			weights[word] = 0.0
    	weight_vector[userID] = weights
    print "Weight Vector initialized"
    
#     iter = 0
#     while eta > 0:
#     	iter += 1
#     	print "Regression : Iter %d" % iter
#     	for userID_1,comments_1 in phi_X.iteritems():
#     		weights = weight_vector[userID_1]
#     		for userID_2,comments_2 in phi_X.iteritems():
#     			y = 1 if userID_1 == userID_2 else 0
#     			newWeights = updateWeight(eta,weights,gradient(weights,comments_2,y,len(phi_X)))
#     		weight_vector[userID_1] = newWeights
#     	eta = eta - 0.02

def get_posts(user_list):
	tree = et.parse("dataset/Posts.xml")
	doc = tree.getroot()
	
	posts_dict = {}
	for row in doc.findall('row'):
		ownerUserID = row.get('OwnerUserID')
		if ownerUserID in user_list and ownerUserID not in posts_dict:
			posts_dict[ownerUserID] = [row.get('Body')]
		else:
			posts_dict[ownerUserID].append(row.get('Body'))
			
	tree = et.parse("dataset/Comments.xml")
	doc = tree.getroot()
	for row in doc.findall('row'):
		ownerUserID = row.get('UserId')
		if ownerUserID in user_list and ownerUserID not in posts_dict:
			posts_dict[ownerUserID] = [row.get('Text')]
		else:
			posts_dict[ownerUserID].append(row.get('Text'))
			
	return posts_dict
linear_predictor()