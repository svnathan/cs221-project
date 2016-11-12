import sys
import xml.etree.ElementTree as et
import random
import pickle

usersid_list = []					# 100 users who answered the questions
questionsid_list = []				# 100 questions(posts) that you must guess
questionscontent_list = []			# 100 questions(posts) that you must guess
randomusersid_list_list = []		# 2d 100*100 list, where each inner list consists of 99 random users and 1 user who answered the question
									# all 3 lists have corresponding index numbers and all items are strings

current_dir = sys.argv.pop(0)

def test_process():
	user_postsansweredcount_dict = {}
	tree = et.parse(current_dir + '/dataset/Users.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		user_postsansweredcount_dict[row.get('Id')] = 0

	tree = et.parse(current_dir + '/dataset/Posts.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		if row.get('CreationDate').split('-')[0] < '2016' and row.get('PostTypeId') == '2' and row.get('OwnerUserId') is not None:
			user_postsansweredcount_dict[row.get('OwnerUserId')] += 1

	tree = et.parse(current_dir + '/dataset/Posts.xml')
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

	tree = et.parse(current_dir + '/dataset/Users.xml')
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

	with open(current_dir + '/pickle/usersid_list.pkl','w') as f:
		pickle.dump(usersid_list,f)

	with open(current_dir + '/pickle/questionsid_list.pkl','w') as f:
		pickle.dump(questionsid_list,f)

	with open(current_dir + '/pickle/questionscontent_list.pkl','w') as f:
		pickle.dump(questionscontent_list,f)

	with open(current_dir + '/pickle/randomusersid_list_list.pkl','w') as f:
		pickle.dump(randomusersid_list_list,f)

def get_usersid_list():					# returns list of users who answered the question (should not call this in your module)
	with open(current_dir + '/pickle/usersid_list.pkl','rb') as f:
		usersid_list = pickle.load(f)
	return usersid_list

def get_questionsid_list():				# returns list of questions id
	with open(current_dir + '/pickle/questionsid_list.pkl','rb') as f:
		questionsid_list = pickle.load(f)
	return questionsid_list

def get_questionscontent_list():		# returns list of questions content (not id!)
	with open(current_dir + '/pickle/questionscontent_list.pkl','rb') as f:
		questionscontent_list = pickle.load(f)
	return questionscontent_list

def get_randomusersid_list_list():		# returns 2d 100*100 list of list of users
	with open(current_dir + '/pickle/randomusersid_list_list.pkl','rb') as f:
		randomusersid_list_list = pickle.load(f)
	return randomusersid_list_list

def check_answer(user_probability_list_dict):	# argument is list of dictionaries, where the mapping of dictionaries is from users to probability that they answered the question
	correct_count = 0
	for user_probability_dict in user_probability_list_dict:
		list_idx = user_probability_list_dict.index(user_probability_dict)
		max_val_score = -1
		max_val_user = -1
		for user, score in user_probability_dict.iteritems():
			if score > max_val_score:
				max_val_score = score
				max_val_user = user
		usersid_list = get_usersid_list()
		if max_val_user == usersid_list[list_idx]:
			correct_count += 1
	print 'Number of correct guesses:\t', correct_count		# prints the number of correct guesses, where a correct guess is obtained by looking at the highest probability

if __name__ == '__main__':
	test_process()
