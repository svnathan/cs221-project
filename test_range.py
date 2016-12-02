import sys
import xml.etree.ElementTree as et
import random
import pickle

usersid_list = []					# 100 users who answered the questions
questionsid_list = []				# 100 questions(posts) that you must guess
questionscontent_list = []				# 100 questions(posts) that you must guess
randomusersid_list_list = []		# 2d 100*100 list, where each inner list consists of 99 random users and 1 user who answered the question
									# all 3 lists have corresponding index numbers and all items are strings

current_dir = '.'#sys.argv.pop(0)

def test_process():
	user_postsansweredcount_dict = {}
	tree = et.parse("dataset\Users.xml")
	doc = tree.getroot()

	for row in doc.findall('row'):
		user_postsansweredcount_dict[row.get('Id')] = 0

	tree = et.parse("dataset\Posts.xml")
	doc = tree.getroot()

	for row in doc.findall('row'):
		if row.get('CreationDate').split('-')[0] < '2016' and row.get('PostTypeId') == '2' and row.get('OwnerUserId') is not None:
			user_postsansweredcount_dict[row.get('OwnerUserId')] += 1

	tree = et.parse("dataset\Posts.xml")
	doc = tree.getroot()

	userid_questionsid_dict = {}	# dictionary of users who answered the question to questions
	userid_questionscontent_dict = {}

	for row in doc.findall('row'):
		if row.get('CreationDate').split('-')[0] >= '2016' and row.get('PostTypeId') == '2' and row.get('OwnerUserId') is not None and user_postsansweredcount_dict[row.get('OwnerUserId')] > 0:
			userid_questionsid_dict[row.get('OwnerUserId')] = row.get('ParentId')

	for userid, postid in userid_questionsid_dict.iteritems():
		for row in doc.findall('row'):
			if row.get('Id') == postid:
				userid_questionscontent_dict[userid] = row.get('Body')
				break

	idx = 0
	i = 0
	while idx != 100:
		userid = random.choice(userid_questionsid_dict.keys())
		if userid not in usersid_list:
			usersid_list.append(userid)
			questionsid_list.append(userid_questionsid_dict[userid])
			questionscontent_list.append(userid_questionscontent_dict[userid])
			lst = []
			lst.append(userid)
			randomusersid_list_list.append(lst)
			idx += 1

	tree = et.parse("dataset\Users.xml")
	doc = tree.getroot()

	users_list = []					# list of all users
	for row in doc.findall('row'):
		users_list.append(row.get('Id'))

	for list_idx in range(100):
		idx = 0
		while idx != 99:
			userid = random.choice(users_list)
			if userid not in randomusersid_list_list[list_idx]:
				randomusersid_list_list[list_idx].append(userid)
				idx += 1
		random.shuffle(randomusersid_list_list[list_idx])

	with open('dataset\usersid_list.pkl','w') as f:
		pickle.dump(usersid_list,f)

	with open('dataset\questionsid_list.pkl','w') as f:
		pickle.dump(questionsid_list,f)

	with open('dataset\questionscontent_list.pkl','w') as f:
		pickle.dump(questionscontent_list,f)

	with open('dataset\\randomusersid_list_list.pkl','w') as f:
		pickle.dump(randomusersid_list_list,f)

def get_usersid_list():					# returns list of users who answered the question (should not call this in your module)
	with open('dataset\usersid_list.pkl','r') as f:
		usersid_list = pickle.load(f)
	return usersid_list

def get_questionsid_list():				# returns list of questions id
	with open('dataset\questionsid_list.pkl','r') as f:
		questionsid_list = pickle.load(f)
	return questionsid_list

def get_questionscontent_list():		# returns list of questions content (not id!)
	with open('dataset\questionscontent_list.pkl','r') as f:
		questionscontent_list = pickle.load(f)
	return questionscontent_list

def get_randomusersid_list_list():		# returns 2d 100*100 list of list of users
	with open('dataset\\randomusersid_list_list.pkl','r') as f:
		randomusersid_list_list = pickle.load(f)
	return randomusersid_list_list

def check_answer(user_probability_list_dict):	# argument is list of dictionaries, where the mapping of dictionaries is from users to probability that they answered the question
	correct_count = [0,0, 0, 0, 0]
	q = get_questionsid_list()

	questionid_userids_dict = {}

	tree = et.parse("dataset\Posts.xml")
	doc = tree.getroot()

	for row in doc.findall('row'):
		if row.get('CreationDate').split('-')[0] >= '2016' and row.get('PostTypeId') == '2' and row.get('OwnerUserId') is not None:
			if row.get('ParentId') not in questionid_userids_dict: questionid_userids_dict[row.get('ParentId')] = []
			questionid_userids_dict[row.get('ParentId')].append(row.get('OwnerUserId'))

	for user_probability_dict in user_probability_list_dict:
		list_idx = user_probability_list_dict.index(user_probability_dict)

		sorted_user_probability_list = sorted(user_probability_dict.items(), key=lambda (k,v): v, reverse=True)
		usersid_list = get_usersid_list()
		for i in range(len(correct_count)):
			unique_prob = 0
			last_prob = 1.5
			recommended_users = []
			for j in range(len(sorted_user_probability_list)):
				if sorted_user_probability_list[j][1] < last_prob:
					last_prob = sorted_user_probability_list[j][1]
					unique_prob += 1
				if unique_prob > i+1 : break
				recommended_users.append(sorted_user_probability_list[j][0])
				
			if len(set(questionid_userids_dict[q[list_idx]]) & set(recommended_users)) > 0:
				correct_count[i] += 1
			'''
			#this prints results if didn't recommend top most user for error checking purposes
			elif i == 0:
				print q[list_idx]
				print "WRONG - guess =", recommended_users, "actual =", questionid_userids_dict[q[list_idx]]
				print sorted(user_probability_dict.items(), key=lambda (k,v): v, reverse=True) 
			'''
	print 'Number of correct guesses:\t', correct_count		# prints the number of correct guesses, where a correct guess is obtained by looking at the highest probability

if __name__ == '__main__':
	#random.seed(412)
	test_process()
