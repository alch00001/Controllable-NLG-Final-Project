import string
import os
import sys
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

df = pd.read_csv('training.csv')

df.columns = df.columns.str.replace('allsides media bias rating: ', '')
df['center_story_leaning'] = df['center_story_leaning'].str.replace('AllSides Media Bias Rating: ', '')
df['left_story_leaning'] = df['left_story_leaning'].str.replace('AllSides Media Bias Rating: ', '')
df['right_story_leaning'] = df['right_story_leaning'].str.replace('AllSides Media Bias Rating: ', '')
df.columns = df.columns.str.strip()


# #include X_leaning headlines
central = df[['id','center_story_title']]
left = df[['id','left_story_title', 'left_story_leaning']]
right = df[['id','right_story_title', 'right_story_leaning']]

central.rename(columns={'center_story_title': 'content'}, inplace=True)
left.rename(columns={'left_story_title': 'content'}, inplace=True)
right.rename(columns={'right_story_title': 'content'}, inplace=True)

print(len(left), len(right),len(central))
#drop rows that contain the partial string "Lean" in the X_story_leaning column
discard = ["Lean"]
left = left[~left.left_story_leaning.str.contains('|'.join(discard))]
right = right[~right.right_story_leaning.str.contains('|'.join(discard))]

left.drop('left_story_leaning', axis=1, inplace=True) 
right.drop('right_story_leaning', axis=1, inplace=True)

print(len(left), len(right),len(central))
left.to_csv('classifyleft.csv', index=False, header=True)
right.to_csv('classifyright.csv', index=False, header=True)
central.to_csv('classifycenter.csv', index=False, header=True)