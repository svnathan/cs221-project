import json
import sys

def main(argv):
    dataset_dir = argv.pop(0)
    print dataset_dir
    with open(dataset_dir+'yelp_academic_dataset_business.json') as f:
        for line in f:
            print line
            break

if __name__ == '__main__':
	main(sys.argv)
