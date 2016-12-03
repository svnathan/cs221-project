from scipy import spatial
import sys
import xml.etree.ElementTree as et
#import random
import pickle
import math
import test_range
import operator

def main():
	tags = get_tags() #return list of tags
	votes = get_answer_votes() #return dict of post_id mapped to positive votes - negative votes
	reputations, dates = get_user_reputations()
	num_answered = get_answer_counts(dates)
	answers, questions, user_tags = get_questions_and_answers(tags) #return dict of users mapped to list of (postid of question, postid of answer) tuples and dict mapping question id to tag vector
	#100 simulations
	results = []

	q = test_range.get_questionsid_list()
	rndm_users = test_range.get_randomusersid_list_list()
	for i in range(100):
		normalized_reps = norm_reps(reputations, rndm_users[i])
		counts = norm_counts(num_answered, rndm_users[i])
		results.append(recommendation(q[i], rndm_users[i], questions, answers, votes, counts, normalized_reps, user_tags))
		#print rndm_users[i]
		#print q[i], sorted(results[i].items(), key=lambda (k,v): v, reverse=True), "\n\n"
	test_range.check_answer(results)

def get_user_reputations():
	rep_dict = {}
	create_date = {}
	tree = et.parse("dataset\\Users.xml")
	#tree = et.parse(current_dir + '/dataset/Tags.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		date = float(row.get('CreationDate').split('-')[0])
		if date < 2016:
			rep_dict[row.get('Id')]=float(row.get('Reputation'))/(2017-date)
			create_date[row.get('Id')]=2017-date
		else:
			rep_dict[row.get('Id')]=0
	'''
	for r in rep_dict:
		rep_dict[r] =math.sqrt(rep_dict[r])
	'''
	return rep_dict, create_date	

def norm_reps(reps, users):
	result = {}
	norm = 0
	for u in users:
		result[u] = reps[u]
		norm += reps[u]
	#print result
	#print norm
	for r in result:
		result[r] /= float(norm)
	return result

def norm_counts(counts, users):
	result = {}
	norm = 0
	for u in users:
		result[u] = counts[u] if u in counts else 0
		norm += result[u]
	#print result
	#print norm
	for r in result:
		result[r] /= float(norm)
	return result

def get_answer_counts(dates):
	counts = {}
	user_answer_question_dict = {}
	tree = et.parse("dataset\\Posts.xml")
	#tree = et.parse(current_dir + '/dataset/Posts.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		if row.get('PostTypeId') == '2' and row.get('CreationDate').split('-')[0] < '2016' and row.get("OwnerUserId"):
			user = row.get("OwnerUserId")
			if user not in counts: counts[user]=0
			counts[user] += 1
	for c in counts:
		if c == '57749': counts[c]/2.0
		else: counts[c] /= float(dates[c])#math.sqrt(counts[c])
	return counts

def recommendation(q, users, questions, answers, votes, counts, rep, user_tags):
	recs = {}
	rec_sum = 0
	for u in users:
		if u not in answers: 
			recs[u] = 0
		else:
			recs[u] = get_rank(q, u, questions, answers, votes, counts[u], rep[u])
	min_r = recs[min(recs, key=recs.get)]
	rec_sum = 0
	for r in recs:
		#d = 1
		u_c = 0
		u_r = 0
		#if r in user_tags:
			#d = 2 - spatial.distance.jaccard(questions[q], user_tags[r])
		if r in counts:
			u_c = counts[r]
		if r in rep:
			u_r = rep[r]
		#recs[r] -= min_r
		#recs[r] = .4*recs[r] + .6*u_c + 0*u_r
		#recs[r] *= d
		rec_sum += recs[r]
	
	if rec_sum == 0:
		for r in recs:
			recs[r] = .01
	else:
		for r in recs:
			recs[r] /= rec_sum
	
	recommendations = sorted(recs.items(), key=lambda (k,v): v, reverse=True)
	#print q, recommendations
	return recs

def get_rank(q, u, questions, answers, votes,c,r):
	q_by_u = answers[u]
	sims = {}
	count = 0
	for i in q_by_u:
		sims[count] = compute_similarity(questions[q], questions[i[0]])
		count += 1
	sims = sorted(sims.items(), key=lambda (k,v): v, reverse=True)[0:5]
	norm_factor = 0
	for s in sims:
		norm_factor += s[1]
	if norm_factor == 0: return 0
	result = 0
	sims_sum = 0
	for s in sims:
		v = 0
		if q_by_u[s[0]][1] in votes:
			v = votes[q_by_u[s[0]][1]]
			if v == 0: v = 1
		result += (c+r+v)*s[1]/norm_factor
		sims_sum += s[1]/norm_factor
	return result/sims_sum 

def compute_similarity(q1, q2):
	return 1 - spatial.distance.jaccard(q1, q2)

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
			if v_type =='2':#in ['1', '2', '5', '11', '16']:
				v = 1 
			elif v_type == '3': #in['3', '4', '10', '12', '15']:
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
	user_tag_dict = {}
	tree = et.parse("dataset\\Posts.xml")
	#tree = et.parse(current_dir + '/dataset/Posts.xml')
	doc = tree.getroot()

	save_for_later = {}
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
			'''
			if row.get('CreationDate').split('-')[0] < '2016' and row.get('OwnerUserId') != row.get('LastEditorUserId'):
				u = row.get('LastEditorUserId')
				if u in user_answer_question_dict:
					user_answer_question_dict[u].append((row.get('Id'), row.get('Id')))
				else:
					user_answer_question_dict[u] = [(row.get('ParentId'), row.get('Id'))]
			'''
		elif row.get('CreationDate').split('-')[0] < '2016' and row.get('PostTypeId') == '2'and row.get('OwnerUserId') is not None:
			u = row.get('OwnerUserId')
			if u in user_answer_question_dict:
				user_answer_question_dict[u].append((row.get('ParentId'), row.get('Id')))
				if row.get('ParentId') not in question_tags_dict:
					if u in save_for_later:
						save_for_later[u] |= row.get("ParentId")
					else:
						save_for_later[u] = set([row.get('ParentId')])
					continue
				new_vec = []
				for i in range(len(tag_list)):
					new_vec.append(question_tags_dict[row.get('ParentId')][i] | user_tag_dict[u][i])
				user_tag_dict[u] = new_vec
			else:
				user_answer_question_dict[u] = [(row.get('ParentId'), row.get('Id'))]
				if row.get('ParentId') not in question_tags_dict:
					if u in save_for_later:
						save_for_later[u] |= row.get("ParentId")
					else:
						save_for_later[u] = set([row.get('ParentId')])
					continue
				user_tag_dict[u] = question_tags_dict[row.get('ParentId')]
	for u in save_for_later:
		vec = [0 for i in range(len(tag_list))]
		for q in save_for_later[u]:
			for i in range(len(tag_list)):
				vec[i] = vec[i] | question_tags_dict[q][i]
		new_vec = []
		for i in range(len(tag_list)):
			new_vec.append(user_tag_dict[u][i] | vec[i])

	return user_answer_question_dict, question_tags_dict, user_tag_dict


main()







