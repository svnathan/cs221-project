import nltk
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
		tag_list.append({row.get('TagName'): parse_tag(row.get('TagName'))})

	return tag_list

def parse_tag(tag):
	tokens = tag.split('-')
	stemmer = nltk.stem.porter.PorterStemmer()
	stems = [stemmer.stem(word) for word in tokens]
	return set(stems)

def feature_vector(tags):
	vec = []
	for i in range(len(tags)):
		added = False
		for j in range(len(vec)):
			if len(tags[i].values()[0] & vec[j].values()[0]) > 0:
				vec_key = list(vec[j].keys())[0]
				#print list(vec_key), set(tags[i].keys())
				real_t = set(list(vec_key)) | set(tags[i].keys())
				stem_t = vec[j].values()[0] | tags[i].values()[0]
				vec[j] = {tuple(real_t): stem_t}
				#print vec[j]
				added = True
		if not added: vec.append({tuple(tags[i].keys()): tags[i].values()[0]})
	return [vec[i].keys() for i in range(len(vec))]

def get_features():
	tags = get_tags()
	features = feature_vector(tags)
	result = []
	for f in features:
		result.append(list(f[0]))
	return result

get_features()





