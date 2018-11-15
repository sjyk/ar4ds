#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
from copy import deepcopy


# In[2]:


aka_name = ["id", "person_id", "name", 
            "imdb_index", "name_pcode_cf", "name_pcode_nf", 
            "surname_code", "md5sum"]
aka_title = ["id", "movie_id", "title", 
             "imdb_index", "kind_id", "production_year", 
             "phonetic_code", "episode_of", "season_nr", 
             "episode_nr", "note", "md5sum"]
cast_info = ["id", "person_id", "movie_id",
            "person_role_id", "note", "nr_order",
            "role_id"]
char_name = ["id", "name", "imdb_index",
            "imdb_id", "name_pcode_nf", "surname_pcode",
            "md5sum"]
comp_cast_type = ["id", "kind"]
company_name = ["id", "name", "country_code",
               "imdb_id", "name_pcode_nf", "name_pcode_sf",
               "md5sum"]
company_type = ["id", "kind"]
complete_cast = ["id", "movie_id", "subject_id",
                "status_id"]
info_type = ["id", "info"]
keyword = ["id", "keyword", "phonetic_code"]
kind_type = ["id", "kind"]
link_type = ["id", "link"]
movie_companies = ["id", "movie_id", "company_id",
                  "company_type_id", "note"]
movie_info = ["id", "movie_id", "info_type_id",
             "info", "note"]
movie_info_idx = ["id", "movie_id", "info_type_id",
                 "info", "note"]
movie_keyword = ["id", "movie_id", "keyword_id"]
movie_link = ["id", "movie_id", "linked_movie_id",
             "link_type_id"]
name = ["id", "name", "imdb_index",
       "imdb_id", "gender", "name_pcode_cf",
       "name_pcode_nf", "surname_pcode", "md5sum"]
role_type = ["id", "role"]
title = ["id", "title", "imdb_index",
        "kind_id", "production_year", "imdb_id",
        "phonetic_code", "episode_of_id", "season_nr",
        "series_years", "md5sum"]
person_info = ["id", "person_id", "info_type_id",
              "info", "note"]


# In[3]:


csv_names = {"aka_name": aka_name, "aka_title": aka_title, "cast_info": cast_info, "char_name": char_name,
            "comp_cast_type": comp_cast_type, "company_name": company_name, "company_type": company_type, 
             "complete_cast": complete_cast, "info_type": info_type, "keyword": keyword, 
             "kind_type": kind_type, "link_type": link_type, "movie_companies": movie_companies, 
             "movie_info": movie_info, "movie_info_idx": movie_info_idx, "movie_keyword": movie_keyword, "movie_link": movie_link,
            "name": name, "role_type": role_type, "title": title, "person_info": person_info}


# In[4]:


csv_tables = {}

for csv_title in csv_names.keys():
    with open('./imdb/' + csv_title + '.csv', newline = '') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        table = []
        headers = csv_names[csv_title]
        counter = 0
        for row in spamreader:
            if counter >= 1000:
                break
            else:
                counter += 1
                table.append({headers[i]: row[i] for i in range(len(headers))})
    csv_tables[csv_title] = table


# In[5]:


with open('edited-queries.txt', 'r') as f:
    content = f.readlines()
    
table_info = []
join_attr_info = []

line_ctr=0
for line in content:
    if line != "\n":
        line = line.strip().strip(';')
        if line_ctr % 2 == 0:
            new_tables = line.split(", ")
            table_info.extend([table for table in new_tables if table not in table_info])
        else:
            new_attrs = line.split(" AND ")
            join_attr_info.extend([attr for attr in new_attrs if attr not in join_attr_info])
        line_ctr+=1
        
tables = {}
for table in table_info:
    info = table.split(" AS ")
    tables[info[1]] = [deepcopy(entry) for entry in csv_tables[info[0]]]


# In[6]:


# def join_tables_on_key(t1, t2, t1_key, t2_key):
#     table = []
#     for entry1 in t1:
#         for entry2 in t2:
#             if entry1[t1_key] == entry2[t2_key]:
#                 entry = entry1
#                 if t1_key==t2_key:
#                     for k,v in entry2.items():
#                         if k != t2_key:
#                             entry[k] = v
#                 else:
#                     entry.update(entry2)
#                 table.append(entry)
#     return table


# In[7]:


# def create_joined_tables():
#     joined_tables = []
#     for join_attr in join_attr_info:
#         attrs = join_attr.split(" = ")
#         join_1 = attrs[0].split(".")
#         join_2 = attrs[1].split(".")
#         table = join_tables_on_key(tables[join_1[0]].copy(), tables[join_2[0]].copy(), join_1[1], join_2[1])
#         if table != []:
#             joined_tables.append(table)
#     return joined_tables


# In[8]:


#final_tables = create_joined_tables()


# In[9]:


def insert_key(table, original_key):
    for entry in table:
        entry["id"] = entry[original_key]
    return table


# In[10]:


def remove_key(table, keys):
    for entry in table:
        for key in keys:
            del entry[key]
    return table


# In[11]:


def create_tables_to_join():
    table_pairs = []
    for join_attr in join_attr_info:
        attrs = join_attr.split(" = ")
        join_1 = attrs[0].split(".")
        join_2 = attrs[1].split(".")
        table_1 = deepcopy(tables[join_1[0]])
        table_2 = deepcopy(tables[join_2[0]])
        common_attrs = [attr for attr in table_1[0].keys() if attr in table_2[0].keys()]
        common_attrs = [attr for attr in common_attrs if attr != join_1[1] and attr != join_2[1]]
        if join_1[1] != 'id':
            table_1 = insert_key(table_1, join_1[1])
        if join_2[1] != 'id':
            table_2 = insert_key(table_2, join_2[1])
        table_1 = remove_key(table_1, common_attrs)
        table_2 = remove_key(table_2, common_attrs)
        table_pairs.append([table_1, table_2])
    return table_pairs


# In[12]:


table_pairs = create_tables_to_join()


# In[13]:


# def attempts_at_joining(pairs):
#     joined_table_indices = []
#     for i in range(len(pairs)):
#         table_1 = pairs[i][0]
#         table_2 = pairs[i][1]
#         if len(natjoin.natural_join([deepcopy(table_1), deepcopy(table_2)])) != 0:
#             joined_table_indices.append(i)
#     return joined_table_indices


# In[14]:


# joined_table_indices = attempts_at_joining(table_pairs)


# In[ ]:





# In[ ]:




