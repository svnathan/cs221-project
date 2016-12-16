About:
The project aims to create a recommender system for the online question and answer computer science community hosted on StackExchange.com. We used NLP, Community Detection and Collaborative Filtering to recommend upto 5 users who are capable of answering the question of interest. Using our evaluation metric, we were able to get accuracies of upto 75% for the top user who is likely to answer the question of interest.

Note:
1) The dataset only contains a small sample
2) Download the entire dataset from https://archive.org/download/stackexchange/cs.stackexchange.com.7z

Files:
1) Elevator Pitch.docx				- Draft of the pitch for the poster presentation
2) cf_test.py 						- 
3) clustering.py 					- Implementation of clustering algorithm
4) collab_filter_clean.py 			- 
5) collab_filter_edit.py 			- 
6) collab_filter_features.py 		-
7) dataset 							- Folder containing the entire dataset
8) kmeans_tags.py 					- Implementation of k-means for community detection
9) linear_predictor.py 				- Script that uses linear predictor for recommending likely users
10) nlp.py 							- Implementation of NLP algorithms for text similarity
11) pickle 							- Folder containing preprocessed data that is used by various algorithms 
12) script.py 						- Main script file which runs different algorithms and tests the output
13) snap.py 						- Essential file to run community detection (Provided by Stanford SNAP group)
14) stem_tags.py 					-
15) test.py 						- Script to test the output of the different algorithms and print the accuracies
16) word_pairs.py 					-

Setup and Execution Instructions:
1) Download the entire dataset from https://archive.org/download/stackexchange/cs.stackexchange.com.7z
2) Rename the folder containing the dataset to "dataset", and place this folder within the "code" folder
3) The "code" folder from "code.zip" should contain the python script files and the "dataset" folder
4) Create a folder called "pickle" in the "code" folder
5) Go into the "code" folder and run "python script.py" from the terminal
6) The output should print the accuracy for the top 5 users for each algorithm