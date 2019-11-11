# Append and deduplicate partitions

import os
import json


def flatten(l):
    sl = [item for sublist in l for item in sublist]
    return sl

def read_partitions(partitions):
    pub_list = []
    for p in partitions:
        with open(p) as json_file:
            partition = json.load(json_file)
            pub_list.append(partition)
    pub_list = flatten(pub_list)
    return pub_list




import collections
from collections import defaultdict
import pandas as pd

def combine_metadata(dics):
    dd = defaultdict(list)
    for dic in dics:
        for key, val in dic.items():  
            if not pd.isnull(val):
                dd[key].append(val)
#                 dd[key].append(val.lower())
                dd[key] = list(set(dd[key]))
            else: 
                continue
    return dict(dd)

def merge_metadata(dicts):
    res = collections.defaultdict(list)
    md_list = []
    for d in dicts:
        for k, v in d.items():
            if k  == 'original':
                md_list.append(v)
            if k == 'title':
                res[k].append(v)
            if k == 'datasets':
                res[k].append(v)
    res['original']  = combine_metadata(md_list)
    res['title'] = list(set(res['title']))[0]
    res['datasets'] = list(set(flatten(res['datasets'])))
    return dict(res)


#### Account for duplicates, merging any metadata into one subdictionary ('original')


# read in partitions

def import_partitions():
    partitions = [os.path.join('/Users/sophierand/RCPublications/partitions',f) for f in os.listdir('/Users/sophierand/RCPublications/partitions') if f.endswith('.json')]
    pub_list_flat = read_partitions(partitions)
    return pub_list_flat

def merge_md(pub_list_flat):
    groups = {}
    for d in pub_list_flat:
        if d['title'] not in groups:
            groups[d['title']] = {'datasets': d['datasets'], 'original': d['original']}
        else:
            for ds in d['datasets']:
                groups[d['title']]['datasets'].append(ds)
            groups[d['title']]['datasets'] = list(set(groups[d['title']]['datasets']))
            groups[d['title']]['original'].update(d['original'])
    result = [{**{'title': k}, **v} for k, v in groups.items()]
    return result


pub_list_flat =  import_partitions()
result = merge_md(pub_list_flat)
n_titles = len(result)
n_dupes = len(pub_list_flat) - n_titles



print('Among all publication partitions, there were {} duplicate titles - they have been deduplicated, their metadata merged and exported to publications.json'.format(n_dupes))

json_pub_path = '/Users/sophierand/RCPublications/publications.json'
with open(json_pub_path, 'w') as outfile:
    json.dump(result, outfile, indent=2)
    
    
# n_unique_titles = df.title.nunique()
print('There were {} unique publications found in partitions which have been compiled and exported to publications.json'.format(n_titles))


# # create counter on title for deduplications
# from collections import Counter

# ct = Counter(i['title'] for i in pub_list_flat)

# # deduplicate by title
# new_l = []
# for i,v in ct.items():
#     if v > 1:
#         dup_pubs = [p for p in pub_list_flat if p['title'] == i]
#         dup_pubs_merged = merge_metadata(dup_pubs)
#         new_l.append(dup_pubs_merged)
#     if v == 1:
#         unique_pubs = [p for p in pub_list_flat if p['title'] == i]
#         new_l.append(unique_pubs)
# new_l = flatten(new_l)

# # create df from counter to print # of duplicates
# df = pd.DataFrame.from_dict(ct, orient='index').reset_index()
# df = df.rename(columns={'index':'title', 0:'count'})
# nduplicate_titles = df.loc[df['count'] > 1].title.nunique()
# print('Among all publication partitions, there were {} duplicate titles - they have been deduplicated, their metadata merged and exported to publications.json'.format(nduplicate_titles))

# json_pub_path = '/Users/sophierand/RCPublications/publications.json'
# with open(json_pub_path, 'w') as outfile:
#     json.dump(new_l, outfile, indent=2)
    
    
# n_unique_titles = df.title.nunique()
# print('There were {} unique publications found in partitions which have been compiled and exported to publications.json'.format(n_unique_titles))

