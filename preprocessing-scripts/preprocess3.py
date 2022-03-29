import string
import os
import sys
import pandas as pd
import re
import csv

pd.options.mode.chained_assignment = None  # default='warn'
i = 0
headlines = []
with open('output.txt', 'rt') as f:
    data = f.readlines()
for line in data:
    if 'PRED SEQ:' in line:
        i+=1
        headlines.append(line.strip())


headlines = [sentence.replace('PRED SEQ:', '') for sentence in headlines]
headlines = [sentence.replace(' ##', '') for sentence in headlines]
headlines = [sentence.strip() for sentence in headlines]
headlines = [sentence.lstrip('b\'') for sentence in headlines]
headlines = [sentence.rstrip('\'') for sentence in headlines]
headlines = [sentence.replace(' \' ', '\'') for sentence in headlines]
headlines = [sentence.replace(' & ', '&') for sentence in headlines]
headlines = [re.sub(' +', ' ', x) for x in headlines]
headlines = [re.sub('\s*([.,!?])\s*', r'\1 ',  x) for x in headlines]
headlines = [sentence.replace(' ,', ',') for sentence in headlines]
headlines = [sentence.replace(' .', '.') for sentence in headlines]
headlines = [sentence.replace(' :', ':') for sentence in headlines]
headlines = [sentence.replace('"""', '"') for sentence in headlines]

fields = ['id', 'content']
final = []
i = 1
for s in headlines:
    final.append([i, s])
    i+=1

#with open('righttest.csv', 'w') as f:
with open('lefttest.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(final)