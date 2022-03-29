"""Read, split and save the kaggle dataset for our model"""

import csv
import os
import sys
import numpy as np

csv.field_size_limit(sys.maxsize)

def load_dataset(path_csv, dataset = [], dataset_type='train'):
    """Loads dataset into memory from csv file"""
    # Open the csv file, need to specify the encoding for python3
    print(path_csv, dataset_type)
    use_python3 = sys.version_info[0] >= 3
    with (open(path_csv, encoding="utf8") if use_python3 else open(path_csv)) as f:
        csv_file = csv.reader(f, delimiter=',')

        # Each line of the csv corresponds to one word
        for idx, row in enumerate(csv_file):
            if idx == 0: continue
            id,content = row
            label = 0
            if dataset_type == 'train':
                if path_csv  == "data/kaggle/classifyleft.csv" or path_csv  == "data/kaggle/classifyright.csv":
                    label = 1
                elif path_csv == "data/kaggle/classifycenter.csv":
                    label = 0
                else:
                    continue
            elif dataset_type == 'test':
                if path_csv  == 'data/kaggle/lefttest.csv' or path_csv  == 'data/kaggle/righttest.csv':
                    label = 0
                else:
                    continue

            dataset.append((content.replace("\n",""), label))

    return dataset


def save_dataset(dataset, save_dir):
    """Writes sentences.txt and lsabels.txt files in save_dir from dataset

    Args:
        dataset: ([(["a", "cat"], ["O", "O"]), ...])
        save_dir: (string)
    """
    # Create directory if it doesn't exist
    print("Saving in {}...".format(save_dir))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Export the dataset
    with open(os.path.join(save_dir, 'articles.txt'), 'w') as file_articles:
        with open(os.path.join(save_dir, 'tags.txt'), 'w') as file_tags:
            for articles, tags in dataset:
                file_articles.write("{}\n".format("".join(articles)))
                file_tags.write("{}\n".format(tags))
    print("- done.")


if __name__ == "__main__":
    # Check that the dataset exists (you need to make sure you haven't downloaded the `ner.csv`)
    path_dataset1 = 'data/kaggle/classifycenter.csv'#original sentences
    path_dataset2 = 'data/kaggle/classifyleft.csv' #original sentences
    path_dataset3 = 'data/kaggle/classifyright.csv' #original sentences
  
    msg1 = "{} file not found. Make sure you have downloaded the right dataset".format(path_dataset1)
    msg2 = "{} file not found. Make sure you have downloaded the right dataset".format(path_dataset2)
    msg3 = "{} file not found. Make sure you have downloaded the right dataset".format(path_dataset3)
 
    assert os.path.isfile(path_dataset1), msg1
    assert os.path.isfile(path_dataset2), msg2
    assert os.path.isfile(path_dataset3), msg3

    # Load the dataset into memory
    print("Loading All The News dataset into memory...")
    dataset = load_dataset(path_dataset1)
    dataset = load_dataset(path_dataset2, dataset)
    dataset = load_dataset(path_dataset3, dataset)
    print("- done.")

    np.random.shuffle(dataset)

    # Split the dataset into train, dev and split (dummy split with no shuffle)
    train_dataset = dataset[:int(0.9*len(dataset))]
    dev_dataset = dataset[int(0.9*len(dataset)):]

    #CREATE TEST SETS


    path_dataset4 = 'data/kaggle/lefttest.csv' #modified sentences
    path_dataset5 = 'data/kaggle/righttest.csv' #modified sentences

    msg4 = "{} file not found. Make sure you have downloaded the right dataset".format(path_dataset4)
    msg5 = "{} file not found. Make sure you have downloaded the right dataset".format(path_dataset5)

    assert os.path.isfile(path_dataset4), msg4
    assert os.path.isfile(path_dataset5), msg5

    print("Loading All The News dataset into memory...")
    dataset_test_left = load_dataset(path_dataset4, [], dataset_type='test')
    dataset_test_right = load_dataset(path_dataset5, [],  dataset_type='test')
    print("- done.")

    #test_dataset = dataset[:int(0.1*len(dataset))]
    print("Length of train: ", len(train_dataset))
    print("Length of dev: ", len(dev_dataset))
    print("Length of test left: ", len(dataset_test_left))
    print("Length of test right: ", len(dataset_test_right))

    # Save the datasets to files
    save_dataset(train_dataset, 'data/kaggle/train')
    save_dataset(dev_dataset, 'data/kaggle/dev')
    save_dataset(dataset_test_left, 'data/kaggle/testleft')
    save_dataset(dataset_test_right, 'data/kaggle/testright')
