import sys
import xml.etree.ElementTree as et
import snap
import re

current_dir = sys.argv.pop(0)

def main():
	tag_posts_dict = {}
	graph = snap.PUNGraph.New()
	
	tree = et.parse(current_dir + '/dataset/Posts.xml')
	doc = tree.getroot()
	
	for row in doc.findall('row'):
		if row.get('PostTypeId') == '1' and row.get('OwnerUserId') is not None:
			graph.AddNode(int(row.get('Id')))
			tags = row.get('Tags')
			if tags is not None:
				tags_list = tags.split('><')
				for tag in tags_list:
					tag = re.sub('[<>]', '', tag)
					if tag not in tag_posts_dict:
						tag_posts_dict[tag] = [row.get('Id')]
					else:
						tag_posts_dict[tag].append(row.get('Id'))
	
	for tag, posts in tag_posts_dict.iteritems():
		for src_post in posts:
			for dest_post in posts:
				if src_post != dest_post and not graph.IsEdge(int(src_post), int(dest_post)):
					graph.AddEdge(int(src_post), int(dest_post))
	
	communities_list_list = []	# communities of questions	
	CmtyV = snap.TCnComV()
	modularity = snap.CommunityCNM(graph, CmtyV)
	for Cmty in CmtyV:
		community_list = []
		for NI in Cmty:
			community_list.append(NI)
		communities_list_list.append(community_list)

	questions_list = get_questionsid_list()

	users_questions_dict = {}

	tree = et.parse(current_dir + '/dataset/Users.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		users_questions_dict[row.get('Id')] = []

	tree = et.parse(current_dir + '/dataset/Posts.xml')
	doc = tree.getroot()

	for row in doc.findall('row'):
		if row.get('CreationDate').split('-')[0] < '2016' and row.get('PostTypeId') == '2' and row.get('OwnerUserId') is not None:
			users_questions_dict[row.get('OwnerUserId')].append(row.get('users_questions_dict'))

	randomusersid_list_list = get_randomusersid_list_list()

	for idx in range(100):
		question = questions_list[idx]
		users = randomusersid_list_list[idx]
		for user in users:
			questions = user_posts_dict[user]
	
if __name__ == '__main__':
	main()