import textmining
import numpy as np
import sklearn
from sklearn.cluster import KMeans
import sys
import xml.etree.ElementTree as et

def get_tags():
	tag_list = []
	tree = et.parse("dataset\\Tags.xml")
	#tree = et.parse(current_dir + '/dataset/Tags.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		tag_list.append({row.get('TagName'):[]})

	return tag_list

def get_question_tags(tags):
	tree = et.parse("dataset\\Posts.xml")
	#tree = et.parse(current_dir + '/dataset/Posts.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		if row.get('CreationDate').split('-')[0] < '2016' and row.get('PostTypeId') == '1':
			q_tags = []
			if row.get('Tags') is None:
				continue
			tag_line = row.get("Tags")
			tag_line = tag_line[1:-1].split("><")
			for i in range(len(tags)):
				t = tags[i]
				if t.keys()[0] in tag_line:
					t.values()[0].append(1)
				else:
					t.values()[0].append(0)
				tags[i] = t

def get_question_taglists():
	question_tags_dict = {}
	tree = et.parse("dataset\\Posts.xml")
	#tree = et.parse(current_dir + '/dataset/Posts.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		if row.get('CreationDate').split('-')[0] < '2016' and row.get('PostTypeId') == '1':
			if row.get('Tags') is None:
				question_tags_dict[row.get('Id')] = []
			else:
				tag_line = row.get("Tags")
				tag_line = tag_line[1:-1].split("><")
				question_tags_dict[row.get('Id')] = tag_line
	return question_tags_dict

def get_answer_tags():
	qtags = get_question_taglists()
	user_tag_dict = {}
	tree = et.parse("dataset\\Posts.xml")
	#tree = et.parse(current_dir + '/dataset/Posts.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		if row.get('CreationDate').split('-')[0] < '2016' and row.get('PostTypeId') == '2'and row.get('OwnerUserId') is not None:
			u = row.get('OwnerUserId')
			if u in user_tag_dict:
				user_tag_dict[u] |= set(qtags[row.get('ParentId')])
			else:
				user_tag_dict[u] = set(qtags[row.get('ParentId')])

	return [user_tag_dict[u] for u in user_tag_dict]

def get_clusters(tags):
	cluster_vecs = []
	for i in range(len(tags)):
		cluster_vecs.append(tags[i].values()[0])
	kmeans = KMeans(n_clusters=100, random_state=0).fit(cluster_vecs)
	clusters = kmeans.labels_
	result = [[] for i in range(100)]
	for i in range(len(clusters)):
		result[clusters[i]].append(tags[i].keys()[0])
	return result

def get_q_features():
	tags = get_tags()
	print "creating features"
	get_question_tags(tags)
	print "features created"
	feature_vec = get_clusters(tags)
	return feature_vec

def get_u_features():
	tags = get_tags()
	print "creating features"
	utags = get_answer_tags()
	for i in range(len(tags)):
		t = tags[i]
		for j in range(len(utags)):
			if t.keys()[0] in utags[j]:
				t.values()[0].append(1)
			else:
				t.values()[0].append(0)
		tags[i] = t
	feature_vec = get_clusters(tags)
	return feature_vec
