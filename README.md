# Controllable-NLG-Final-Project

## Quick setup to just run classifier and/or view data:
all.csv: Scraped headlines formatted into csv. \
left.tsv: Subset of 250 left-aligned headlines in WNC format for bias-removal algorithm. \
right.tsv: Subset of 250 right-aligned headlines in WNC format for bias-removal algorithm.\ 
training.csv: Scraped headlines with ids that are in right.tsv or left.tsv removed.

output.txt:  Output from bias-removal algorithm with left.tsv as input.\
outputright.txt: Output from bias-removal algorithm with right.tsv as input.

classifbycenter.csv: Only center headlines from training.csv with only id and headline columns.\
classifyleft.csv: Only left headlines from training.csv with only id and headline columns.\
classifyright.csv: Only rightheadlines from training.csv with only id and headline columns.

lefttest.csv: output.txt formatted for classifier.\
righttest.csv: outputright.txt formatted for classifier.


Unzip data.zip which contains all the files and place the data folder in Classifier (so you have directory data/kaggle) and run Classify.ipynb. You can train it or skip the cell and just load the model weights and evaluate. You can train it or skip the cell and just load the model weights and evaluate. 



## TO RUN FROM SCRATCH: 

#### To scrape headlines from AllSides:
Run 01_scrape_data.ipynb located in WebScraping/notebooks. This will create headlines.csv.
Move this file to preprocessing-scripts and run preprocess.py. This will create three files: left.tsv, right.tsv and training.csv.

The two tsv files are for the Bias Removal algorithm and should be placed in:
neutralizing-bias/harvest

#### To remove bias from our two sets of 250 headlines:
BiasRemoval.ipynb: Processes our tsv files, downloads model checkpoint and runs it through the bias removal algorithm, creating output.txt (result of our left headlines) and outputright.text (result of our right headlines) in neutralizing-bias/src/TEST. These two text files should be moved to preprocessing-scripts. 


Run preprocess2.py and preprocess3.py which create classifbycenter.csv, classifyleft.csv, classifyright.csv, lefttest.csv and righttest.csv. Place these in Classifier/data/kaggle, along with classifbycenter.csv, classifyleft.csv and classifyright.csv. 
Run Classify.ipynb. You can train it or skip the cell and just load the model weights and evaluate. You can train it or skip the cell and just load the model weights and evaluate. 
If there are directory issues make sure these directories exist and you downloaded the glove embedding to Classifier/data/GloVe and have the data in Classifier/data/kaggle.

## PREPROCESSING SCRIPT EXPLANATION:

Preprocess.py: takes webscraped headlines and puts them into the appropriate format for the bias-removal algorithm and removes the amount specified from the original data so we have some leftover for training our classifier later on.

Preprocess2.py: creates files that the classifier can use to make train and validation sets (and test set if you want).

Preprocess3.py: creates test sets for the classifier of headlines that have been run through the bias removal algorithm.
