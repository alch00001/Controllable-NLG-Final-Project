import string
import os
import sys
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


#ignore, just for combining into one csv file
#because of connection interruptions while webscraping
# df1 = pd.read_csv('headlines.csv')
# df2 = pd.read_csv('headlines2.csv')
# df3 = pd.read_csv('headlines3.csv')
# df4 = pd.read_csv('headlines4.csv')
# print(df1.shape[0],df2.shape[0],df3.shape[0])
# df = pd.concat([df1,df2, df3, df4]).drop_duplicates().reset_index(drop=True)
# df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
# df["id"] = df.index + 1
# print(df.shape[0])
# df.to_csv('all.csv', index=False, header=True)

df = pd.read_csv('all.csv')

df.columns = df.columns.str.replace('allsides media bias rating: ', '')
df['center_story_leaning'] = df['center_story_leaning'].str.replace('AllSides Media Bias Rating: ', '')
df['left_story_leaning'] = df['left_story_leaning'].str.replace('AllSides Media Bias Rating: ', '')
df['right_story_leaning'] = df['right_story_leaning'].str.replace('AllSides Media Bias Rating: ', '')
df.columns = df.columns.str.strip()

# #add WNC format stuff
# #{id}  {sent} {sent}   no_deleted_chunks   no_added_chunks
df['no_deleted_chunks']='no_deleted_chunks'
df['no_added_chunks']='no_added_chunks'
print("HEADLINES BEFORE: ", len(df))

#shuffle dataframe
df=df.sample(frac=1)

# #include X_leaning headlines
central = df[['id','center_story_title', 'no_deleted_chunks', 'no_added_chunks']]
left = df[['id','left_story_title', 'no_deleted_chunks', 'no_added_chunks', 'left_story_leaning']]
right = df[['id','right_story_title', 'no_deleted_chunks', 'no_added_chunks', 'right_story_leaning']]

#show how much data we have before dropping
print("before: ", left.shape[0]) #see data amount before removing lean
print("before: ", right.shape[0]) 

#drop rows that contain the partial string "Lean" in the X_story_leaning column
discard = ["Lean"]
left = left[~left.left_story_leaning.str.contains('|'.join(discard))]
right = right[~right.right_story_leaning.str.contains('|'.join(discard))]

left.drop('left_story_leaning', axis=1, inplace=True) 
right.drop('right_story_leaning', axis=1, inplace=True) 

print("after: ", left.shape[0]) #see data amount before removing lean
print("after: ", right.shape[0]) 

#make in WNC format

central['target'] = central['center_story_title']
central = central[['id', 'center_story_title', 'target', 'no_deleted_chunks', 'no_added_chunks']]

left['target'] = left['left_story_title']
left = left[['id', 'target', 'left_story_title', 'no_deleted_chunks', 'no_added_chunks']]
left = left.head(250) #arbitrary amount, just want to have adecent amount for training classifier

right['target'] = right['right_story_title']
right = right[['id', 'target', 'right_story_title', 'no_deleted_chunks', 'no_added_chunks']]
right = right.head(250)

#drop all rows that we took data from from the csv file 
# so we can use it to train our classifier later
left_ids = left['id'].tolist()
right_ids = right['id'].tolist()
ids_to_remove = list(set(left_ids + left_ids))
new_df = df[~df.id.isin(ids_to_remove)]

# #save to tsv file in WNC format
left.to_csv('left.tsv', sep="\t", index=False, header=False)
right.to_csv('right.tsv', sep="\t", index=False, header=False)
new_df.to_csv('training.csv', index=False, header = True)

