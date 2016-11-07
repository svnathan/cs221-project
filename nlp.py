import sys
import xml.etree.ElementTree as et
import random
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import math

current_dir = sys.argv.pop(0)

def randomusersid_list_list_filtered_and_get_user_posts_dict():
	randomusersid_list_list = get_randomusersid_list_list()
	user_postsansweredcount_dict = {}
	user_posts_dict = {}
	
	tree = et.parse(current_dir + '/dataset/Users.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		user_postsansweredcount_dict[row.get('Id')] = 0
		user_posts_dict[row.get('Id')] = []

	tree = et.parse(current_dir + '/dataset/Posts.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		if row.get('CreationDate').split('-')[0] < '2016' and row.get('PostTypeId') == '2' and row.get('OwnerUserId') is not None:
			user_postsansweredcount_dict[row.get('OwnerUserId')] += 1
			user_posts_dict[row.get('OwnerUserId')].append(row.get('Body'))

	userid_remove_list_list = []
	for randomusersid_list in randomusersid_list_list:
		userid_remove_list = []
		for userid in randomusersid_list:
			if user_postsansweredcount_dict[userid] == 0:
				userid_remove_list.append(userid)
		userid_remove_list_list.append(userid_remove_list)

	for userid_remove_list in userid_remove_list_list:
		idx = userid_remove_list_list.index(userid_remove_list)
		for userid in userid_remove_list:
			randomusersid_list_list[idx].remove(userid)

	return randomusersid_list_list, user_posts_dict

def main():
	randomusersid_list_list, user_posts_dict = randomusersid_list_list_filtered_and_get_user_posts_dict()
	questions_list = get_questionscontent_list()

	user_probability_list_dict = []
	unfiltered_randomusersid_list_list = get_randomusersid_list_list()
	for idx in range(100):
		user_probability_list_dict.append({})
		for user in unfiltered_randomusersid_list_list[idx]:
			user_probability_list_dict[idx][user] = 0

	for idx in range(100):
		question = questions_list[idx]
		users = randomusersid_list_list[idx]
		for user in users:
			posts = user_posts_dict[user]
			posts_to_compare = [question] + posts
			vect = TfidfVectorizer(min_df=1)
			tfidf = vect.fit_transform(posts_to_compare)
			similarity_values = (tfidf * tfidf.T).A
			similarity_values[0][0] = 0
			user_probability_list_dict[idx][user] = float(sum(similarity_values[0])+max(similarity_values[0]))

	for idx in range(100):
		score_sum = 0
		for user, score in user_probability_list_dict[idx].iteritems():
			score_sum += score
		for user, score in user_probability_list_dict[idx].iteritems():
			if score_sum != 0:
				user_probability_list_dict[idx][user] = score/score_sum

	check_answer(user_probability_list_dict)
	
if __name__ == '__main__':
	main()
