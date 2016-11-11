from scipy import spatial
import sys
import xml.etree.ElementTree as et
import random
import pickle
import math
import test
import operator

def main():
	tags = get_tags() #return list of tags
	votes = get_answer_votes() #return dict of post_id mapped to positive votes - negative votes
	answers, questions = get_questions_and_answers(tags) #return dict of users mapped to list of (postid of question, postid of answer) tuples and dict mapping question id to tag vector
	#100 simulations
	results = []

	q = test.get_questionsid_list()
	rndm_users = test.get_randomusersid_list_list()
	for i in range(100):
		results.append(recommendation(q[i], rndm_users[i], questions, answers, votes))
	test.check_answer(results)

def recommendation(q, users, questions, answers, votes):
	recs = {}
	rec_sum = 0
	for u in users:
		if u not in answers: 
			recs[u] = 0
		else:
			recs[u] = get_rank(q, u, questions, answers, votes)
	min_r = recs[min(recs, key=recs.get)]
	rec_sum = 0
	for r in recs:
		recs[r] -= min_r
		rec_sum += recs[r]
	if rec_sum == 0:
		for r in recs:
			recs[r] = .01
	else:
		for r in recs:
			recs[r] /= rec_sum
	
	recommendations = sorted(recs.items(), key=lambda (k,v): (v,k), reverse=True)
	#print q, recommendations
	return recs

def get_rank(q, u, questions, answers, votes):
	q_by_u = answers[u]
	sims = []
	for i in q_by_u:
		sims.append(compute_similarity(questions[q], questions[i[0]]))
	norm_factor = sum(sims)
	if norm_factor == 0: return 0
	result = 0
	sims_sum = 0
	for i in range(len(q_by_u)):
		v = 0
		if q_by_u[i][1] in votes:
			v = votes[q_by_u[i][1]]
			if v == 0: v = .5
		result += v*sims[i]/norm_factor
		sims_sum += sims[i]/norm_factor
	return result/sims_sum

def compute_similarity(q1, q2):
	return 1 - spatial.distance.cosine(q1, q2)

def get_tags():
	tag_list = []
	tree = et.parse("dataset\\Tags.xml")
	#tree = et.parse(current_dir + '/dataset/Tags.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		tag_list.append(row.get('TagName'))

	return tag_list


def get_answer_votes():
	answer_vote_dict = {}

	tree = et.parse("dataset\\Votes.xml")
	#tree = et.parse(current_dir + '/dataset/Votes.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		if row.get('CreationDate').split('-')[0] < '2016':
			v_type = row.get('VoteTypeId')
			v = 0
			if v_type in ['1', '2', '5', '11', '16']:
				v = 1 
			elif v_type in ['3', '4', '10', '12', '15']:
				v = -1
			post = row.get('PostId')
			if post in answer_vote_dict:
				answer_vote_dict[post] += v
			else:
				answer_vote_dict[post] = v

	return answer_vote_dict


def get_questions_and_answers(tag_list):
	question_tags_dict = {}
	user_answer_question_dict = {}
	tree = et.parse("dataset\\Posts.xml")
	#tree = et.parse(current_dir + '/dataset/Posts.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		if row.get('PostTypeId') == '1':
			q_tags = []
			if row.get('Tags') is None:
				q_tags = [0] * len(tag_list)
			else:
				tag_line = row.get("Tags")
				tag_line = tag_line[1:-1].split("><")
				tags = set(tag_line)
				for t in tag_list:
					if t in tags:
						q_tags.append(1)
					else:
						q_tags.append(0)
			question_tags_dict[row.get('Id')] = q_tags

		elif row.get('CreationDate').split('-')[0] < '2016' and row.get('PostTypeId') == '2'and row.get('OwnerUserId') is not None:
			u = row.get('OwnerUserId')
			if u in user_answer_question_dict:
				user_answer_question_dict[u].append((row.get('ParentId'), row.get('Id')))
			else:
				user_answer_question_dict[u] = [(row.get('ParentId'), row.get('Id'))]

	return user_answer_question_dict, question_tags_dict


main()







