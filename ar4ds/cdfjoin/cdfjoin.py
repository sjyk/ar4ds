
from copy import deepcopy
import csv
import minhash
from loadimdbdata import table_pairs
import random
import time
from math import factorial
from datetime import datetime
from scipy.special import comb
from scipy import linspace
from statistics import median
import numpy as np
import matplotlib.pyplot as plt

def unit_step_function(a, t):
    if t < a:
        return 0
    else:
        return 1

def cdf(n, t):
    if n <= 0:
        return 0
    else:
        my_sum = 0.0
        for i in range(n+1):
            my_sum += ((-1)**i * comb(n, i) * ((t-i)**n)/factorial(n) * unit_step_function(i, t))
        return my_sum
  
# def cdf_multiple_values(n, t):
#   cdf_values = []
#   for target_value in t:
#     cdf_values.append(cdf(n, target_value))
#   return cdf_values

# def find_value_threshold(n, cdf_value):
#   cdf_value *= 1.0
#   t_index = 0
#   while cdf(n, t_index) < cdf_value:
#     t_index+=1
#   if cdf_value -.001 <= cdf(n, t_index) <= cdf_value + .001:
#     return t_index
#   else:
#     lower_bound = t_index-1.0
#     bound_difference = 1.0
#     midpoint = lower_bound + bound_difference/2.0
#     bound_difference/=2.0
#     midpoint_cdf = cdf(n, midpoint)
#     while not cdf_value - .01 <= midpoint_cdf <= cdf_value+.01:
#       if midpoint_cdf > cdf_value:
#         midpoint -= bound_difference/2.0
#       else:
#         midpoint += bound_difference/2.0
#       midpoint_cdf = cdf(n, midpoint)
#       bound_difference /= 2.0
#     return midpoint

# # def cdf_plotter(n, multiple_n = False):,
# #     plt.style.use('seaborn'),
# #     plt.rcParams['figure.figsize'] = (12, 8),
# #     plt.ylabel('Probability'),
# #     plt.xlabel('Sum'),
# #     if multiple_n:,
# #         for number in n:,
# #             cdf_plotter(number),
# #     else:,
# #         x = linspace(0, n+2, 500),
# #         plt.plot(x, cdf_multiple_values(n,x), label='n = {i}'.format(i=n)),
# #         plt.legend(loc='best')

# # def threshold_value_plotter(n, cdf, multiple_n = False, multiple_cdf = False):,
# #     plt.style.use('seaborn'),
# #     plt.rcParams['figure.figsize'] = (12, 8),
# #     plt.ylabel('Probability'),
# #     plt.xlabel('Sum'),
# #     if multiple_n:,
# #         for n_value in n:,
# #             x = linspace(0, n_value+2, 500),
# #             plt.plot(x, cdf_multiple_values(n_value,x), label='n = {i}'.format(i=n_value)),
# #             plt.legend(loc='best'),
# #             if multiple_cdf:,
# #                 for cdf_value in cdf:,
# #                     x = find_value_threshold(n_value, cdf_value),
# #                     y = cdf_value,
# #                     plt.plot(x, y, marker='o', color='black', label='t = {i}'.format(i=x)),
# #             else:,
# #                 x = find_value_threshold(n_value, cdf),
# #                 y = cdf,
# #                 plt.plot(x, y, market='o', color='black', label='t = {i}'.format(i=x)),
# #     else:,
# #         x = linspace(0, n+2, 500),
# #         plt.plot(x, cdf_multiple_values(n,x), label='n = {i}'.format(i=n)),
# #         plt.legend(loc='best'),
# #         if multiple_cdf:,
# #             for cdf_value in cdf:,
# #                 x = find_value_threshold(n, cdf_value),
# #                 y = cdf_value,
# #                 plt.plot(x, y, marker='o', color='black', label='t = {i}'.format(i=x)),
# #         else:,
# #             x = find_value_threshold(n, cdf),
# #             y = cdf,
# #             plt.plot(x, y, marker='o', color='black', label='t = {i}'.format(i=x)),

def cartesian_product(r,s):
    output = []
    for r_entry in r:
        for s_entry in s:
            r_copy = r_entry.copy()
            r_copy.update(s_entry)
            output.append(r_copy)
    return output

def classic_hash_join(r, s):
    if len(s) == 0 or len(r) == 0:
        return []
    
    r_attributes = r[0].keys()
    s_attributes = s[0].keys()
    common_attributes = list(filter(lambda ra: ra in s_attributes, r_attributes))
    if len(common_attributes) > 0:
        s_unique_attributes = list(filter(lambda sa: sa not in common_attributes, s_attributes))
        hashtable = {}
        hashtable_keys = []
        hashkey = ""
        
        #build hash table
        row_index = 0
        for entry in r:
            hashkey = "".join([entry[attribute] for attribute in common_attributes if attribute in entry.keys()])
            if hashkey not in hashtable_keys:
                hashtable[hashkey] = [row_index]
                hashtable_keys.append(hashkey)
            else:
                hashtable[hashkey].append(row_index)
            hashkey = ""
            row_index+=1
        
        #join
        output = []
        for entry in s:
            hashkey = "".join([entry[attribute] for attribute in common_attributes if attribute in entry.keys()])
            if hashkey in hashtable_keys:
                filtered_dict = {k:v for (k,v) in entry.items() if k in s_unique_attributes}
                for r_index in hashtable[hashkey]:
                    new_entry = (r[r_index].copy())
                    new_entry.update(filtered_dict)
                    output.append(new_entry)
            hashkey=""
            
        return output
    else:
        return cartesian_product(r,s)

def natural_join(tables):
    l1 = tables[0]
    for i in range(1, len(tables)):
        l1 = classic_hash_join(l1, tables[i])
    return l1

def normalize(value):
    return float(value) / float(minhash.NEXTPRIME-1)

def remove_hashsum_key(tables):
    for table in tables:
        for entry in table:
            if "hash sum" in entry.keys():
                del entry["hash sum"]
            
    return tables

def cdfjoin(tables, sampling_threshold, random_threshold=0.0):
    if len(tables) <= 1:
        return tables
    else:
        attrs = {}
        join_attrs = []
        
        #find join attributes
        for i in range(len(tables)):
            table = tables[i]
            for table_key in table[0].keys():
                if table_key in attrs.keys(): attrs[table_key].append(i)
                else: attrs[table_key] = [i]
        join_attrs = [k for k,v in attrs.items() if len(v) > 1]
        
        #generate hash functions for each join_attr
        hash_functions = minhash._generate_hash_fns(len(join_attrs))
        attrs_hash_dict = {join_attrs[i]: hash_functions[i] for i in range(len(hash_functions))}
        
        #copy tables
        tables_copy = []
        for table in tables:
            tables_copy.append(deepcopy(table))
        
        #calculate hash sum for each entry in each table
        for table in tables_copy:
            table_attrs = [key for key in table[0].keys() if key in join_attrs]
            norm_hashed_table = {}
            hashed_table = {}
            hashed_table = {attr: minhash._min_hash([attr], table, attrs_hash_dict[attr]) for attr in table_attrs}
            for k,v in hashed_table.items():
                norm_v = {normalize(v1): v2 for v1, v2 in v.items()}
                norm_hashed_table[k] = norm_v
            for i in range(len(table)):
                entry = table[i]
                hash_scores = []
                for k, v in norm_hashed_table.items():
                    for v1, v2 in v.items():
                        if i in v2:
                            hash_scores.append(v1)
                            break
                entry["hash sum"] = sum(hash_scores)
        
        #filter for all entries whose cdf <= sampling probability
        filtered_tables = []
        start = time.time()
        for i in range(len(tables)):
            table = tables_copy[i]
            filtered_table = []
            if "hash sum" in table[0].keys():
                n_join_attrs = len([i for i in table[0].keys() if i in join_attrs])
                for entry in table:
                    if cdf(n_join_attrs, entry["hash sum"]) <= sampling_threshold:
                        filtered_table.append(entry)
            else:
                filtered_table = table
            if len(filtered_table) > 0:
                filtered_tables.append(filtered_table)
            else:
                filtered_tables = []
                break
        filtered_time = time.time() - start
    
                
        #filter for all entries whose cdf > random probability
        random_tables = []
        start = time.time()
        for i in range(len(tables)):
            table = tables_copy[i]
            if random_threshold == 0.0:
                random_threshold = random.uniform(0,1)
            random_table = []
            if "hash sum" in table[0].keys():
                n_join_attrs = len([i for i in table[0].keys() if i in join_attrs])
                for entry in table:
                    if random_threshold < cdf(n_join_attrs, entry["hash sum"]):
                        random_table.append(entry)
            else:
                random_table = table
            if len(random_table) > 0:
                random_tables.append(random_table)
            else:
                random_tables = []
                break
        random_time = time.time() - start
        
        if filtered_tables == []:
            joined_filtered_tables = []
        else:
            filtered_tables = remove_hashsum_key(filtered_tables)
            start = time.time()
            joined_filtered_tables = natural_join(filtered_tables)
            filtered_time += time.time() - start
            
        if random_tables == []:
            joined_random_tables = []
        else:
            random_tables = remove_hashsum_key(random_tables)
            start = time.time()
            # print(len(random_tables))
            joined_random_tables = natural_join(random_tables)
            random_time += time.time() - start
            
        return [(joined_filtered_tables, filtered_time), (joined_random_tables, random_time)]


def get_cdfjoin_plot_data(tables, x_values, size = True, runtime = True):
    cdfjoin_data = []
    for threshold in x_values:
        cdfjoin_result = cdfjoin(tables, threshold)
        if size and runtime:
            cdfjoin_data.append([(len(cdfjoin_result[0][0]), cdfjoin_result[0][1]),
                                (len(cdfjoin_result[1][0]), cdfjoin_result[1][1])])
        elif size and not runtime:
            cdfjoin_data.append([(len(cdfjoin_result[0][0]), None), (len(cdfjoin_result[1][0]), None)])
        elif not size and runtime:
            cdfjoin_data.append([(None, cdfjoin_result[0][1]), (None, cdfjoin_result[1][1])])
            
    return cdfjoin_data


def display_cdfjoin_plots(num_trials, tables, size = True, runtime = True):
    if not size and not runtime:
        print("Error: Select at least one of the following types of data to display: size, runtime")
    
    else:
        x = linspace(0, 1, 100)
        size_hashed_data_multiple = {}
        size_random_data_multiple = {}
        runtime_hashed_data_multiple = {}
        runtime_random_data_multiple = {}
    
  #         gathering data for 1000 trials,
  #         num_trials = 1000,
        for i in range(num_trials): 
            trial_data = get_cdfjoin_plot_data(tables, x, size, runtime)
            for j in range(len(x)):
                x_value = x[j]
                trial_values = trial_data[j]
                if size:
                    if x_value in size_hashed_data_multiple.keys():
                        size_hashed_data_multiple[x_value].append(trial_values[0][0])
                        size_random_data_multiple[x_value].append(trial_values[1][0])
                    else:
                        size_hashed_data_multiple[x_value] = [trial_values[0][0]]
                        size_random_data_multiple[x_value] = [trial_values[1][0]]

                if runtime:
                    if x_value in runtime_hashed_data_multiple.keys():
                        runtime_hashed_data_multiple[x_value].append(trial_values[0][1])
                        runtime_random_data_multiple[x_value].append(trial_values[1][1])
                    else:
                        runtime_hashed_data_multiple[x_value] = [trial_values[0][1]]
                        runtime_random_data_multiple[x_value] = [trial_values[1][1]]
                
        
  #         organizing data for each trial by x-value (sampling threshold),
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(25,8))
        fig = plt.subplots_adjust(wspace=.5)
        
        if size:
            size_hashed_data = []
            size_random_data = []
            for k,v in size_hashed_data_multiple.items():
                size_hashed_data.append(median(v))
            for k,v in size_random_data_multiple.items():
                size_random_data.append(median(v))
            ax1.plot(x, size_hashed_data, label='Hashed sampling')
            ax1.plot(x, size_random_data, label='Random sampling')
            ax1.legend(loc='best')
            ax1.set_xlabel('Sampling Threshold')
            ax1.set_ylabel('Output size')
            ax1.set_title('Output size')

        if runtime:
            runtime_hashed_data = []
            runtime_random_data = []
            for k,v in runtime_hashed_data_multiple.items():
                runtime_hashed_data.append(median(v))
            for k,v in runtime_random_data_multiple.items():
                runtime_random_data.append(median(v))
            ax2.plot(x, runtime_hashed_data, label='Hashed sampling')
            ax2.plot(x, runtime_random_data, label='Random sampling')
            ax2.legend(loc='best')
            ax2.set_xlabel('Sampling Threshold')
            ax2.set_ylabel('Runtime')
            ax2.set_title('Runtime')

        plt.show()

# num_table_pairs = len(table_pairs)
# experiment_tables = []
# for i in range(10):
#     # random = random.randint(0, num_table_pairs)
#     table_index = random .randint(0, num_table_pairs)
#     print(table_index)
#     experiment_tables.append(table_index)
#     display_cdfjoin_plots(100, table_pairs[table_index], True, True)

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

csv_names = {"aka_name": aka_name, "aka_title": aka_title, "cast_info": cast_info, "char_name": char_name,
            "comp_cast_type": comp_cast_type, "company_name": company_name, "company_type": company_type, 
             "complete_cast": complete_cast, "info_type": info_type, "keyword": keyword, 
             "kind_type": kind_type, "link_type": link_type, "movie_companies": movie_companies, 
             "movie_info": movie_info, "movie_info_idx": movie_info_idx, "movie_keyword": movie_keyword, "movie_link": movie_link,
            "name": name, "role_type": role_type, "title": title, "person_info": person_info}

def get_queries():
    with open('edited-queries.txt', 'r') as f:
        content = f.readlines()
        
    query_info = []
    
    line_ctr = 0
    query_nicknames = {}
    for line in content:
        if line != "\n":
            line = line.strip().split(";")
            if line_ctr % 2 == 0:
                table_names = line[0].split(", ")
                for name in table_names:
                    name = name.split(" AS ")
                    query_nicknames[name[1]] = name[0]
            else:
                join_clauses = line[0].split(" AND ")
                for join_clause in join_clauses:
                    join_clause = join_clause.split(" = ")
                    join_info = []
                    for clause in join_clause:
                        clause = clause.split(".")
                        join_info.append((query_nicknames[clause[0]], clause[1]))
                    if join_info not in query_info:
                        query_info.append(join_info)
                query_nicknames = {}
            line_ctr +=1
            
    return query_info


def cdfselect(query, sampling_threshold):
    # parse queries for tables and attributes
    path_prefix = './imdb/'
    table_names = [query[0][0], query[1][0]]
    query_attrs = [query[0][1], query[1][1]]
    
    table_headers = [csv_names[table_names[0]], csv_names[table_names[1]]]
    attr_indices = [table_headers[0].index(query_attrs[0]), table_headers[1].index(query_attrs[1])]
    join_attrs = [header for header in table_headers[0] if header in table_headers[1]]
    
    if query_attrs[0] != query_attrs[1]:
        functions = minhash._generate_hash_fns(len(join_attrs[0])+1)
        if len(join_attrs[0]) == 0:
            hash_functions['id'] = functions[0]
        else:
            hash_functions = {join_attrs[i]:functions[i] for i in range(len(join_attrs))}
            hash_functions['id'] = functions[len(join_attrs)+1]
    else:
        functions = minhash._generate_hash_fns(len(join_attrs))
        hash_functions = {join_attrs[i]:functions[i] for i in range(len(join_attrs))}
        
    empty_hashed = False
    empty_random = False
    
    filtered_tables = []
    runtime=0
    for (table_name, attr) in query:
        print(table_name, attr)
        table = []
        path = path_prefix + table_name + '.csv'
        with open(path, newline='') as csvfile:
            table_headers = csv_names[table_name]
            csv_data = csv.reader(csvfile, delimiter=',')
            headers = csv_names[table_name]
            start_time = time.time()
            if query_attrs[0] != query_attrs[1]:
                # move attr into 'id' column
                for line in csv_data:
                    line = {headers[i]: line[i] for i in range(len(headers))}
                    line['id'] = line[attr]
                    hash_values = [hash_functions[join_attr](line[join_attr]) for join_attr in join_attrs]
                    hash_values.append(hash_functions['id'](line['id']))
                    hash_sum = sum([normalize(hash_value) for hash_value in hash_values])
                    if cdf(len(join_attrs)+1, hash_sum) <= sampling_threshold:
                        table.append(line)
            else:
                for line in csv_data:
                    line = {headers[i]: line[i] for i in range(len(headers))}
                    hash_values = [hash_functions[join_attr](line[join_attr]) for join_attr in join_attrs]
                    hash_sum = sum([normalize(hash_value) for hash_value in hash_values])
                    if cdf(len(join_attrs), hash_sum) <= sampling_threshold:
                        table.append(line)
            runtime += time.time() - start_time
            if table == []:
                print("empty table")
                empty_hashed = True
                break
            filtered_tables.append(table)
            print(filtered_tables)
        if empty_hashed:
            break
        
    hashed_runtime = runtime
    
    if empty_hashed:
        hashed_result = []
    else:
        start = time.time()
        hashed_result = natural_join(filtered_tables)
        hashed_runtime += time.time() - start
        
    random_tables = []
    runtime=0
    for (table_name, attr) in query:
        table = []
        path = path_prefix + table_name + '.csv'
        with open(path, newline='') as csvfile:
            table_headers = csv_names[table_name]
            csv_data = csv.reader(csvfile, delimiter=',')
            headers = csv_names[table_name]
            start_time = time.time()
            random_threshold = random.uniform(0, 1)
            if query_attrs[0] != query_attrs[1]:
                # move attr into 'id' column
                for line in csv_data:
                    line = {headers[i]: line[i] for i in range(len(headers))}
                    line['id'] = line[attr]
                    hash_values = [hash_functions[join_attr](line[join_attr]) for join_attr in join_attrs]
                    hash_values.append(hash_functions['id'](line['id']))
                    hash_sum = sum([normalize(hash_value) for hash_value in hash_values])
                    if cdf(len(join_attrs)+1, hash_sum) > random_threshold:
                        table.append(line)
            else:
                for line in csv_data:
                    line = {headers[i]: line[i] for i in range(len(headers))}
                    hash_values = [hash_functions[join_attr](line[join_attr]) for join_attr in join_attrs]
                    hash_sum = sum([normalize(hash_value) for hash_value in hash_values])
                    if cdf(len(join_attrs), hash_sum) > random_threshold:
                        table.append(line)
        runtime += time.time() - start_time
        if table == []:
            empty_random = True
            break
        random_tables.append(table)
    random_runtime = runtime
    
    if empty_random:
        random_result = []
    else:
        start = time.time()
        random_result = natural_join(random_tables)
        random_runtime += time.time() - start
        
    return [(hashed_result, hashed_runtime), (random_result, random_runtime)]

def get_cdfselect_plot_data(query, x_values, size = True, runtime = True):
    cdfselect_data = []
    for threshold in x_values:
        cdfselect_result = cdfselect(query, threshold)
        print(threshold, "result", cdfselect_result)
        if size and runtime:
            cdfselect_data.append([(len(cdfselect_result[0][0]), cdfselect_result[0][1]),
                                (len(cdfselect_result[1][0]), cdfselect_result[1][1])])
        elif size and not runtime:
            cdfselect_data.append([(len(cdfjoin_result[0][0]), None), (len(cdfselect_result[1][0]), None)])
        elif not size and runtime:
            cdfselect_data.append([(None, cdfjoin_result[0][1]), (None, cdfselect_result[1][1])])
            
    return cdfselect_data


def display_cdfselect_plots(num_trials, query, size = True, runtime = True):
    if not size and not runtime:
        print("Error: Select at least one of the following types of data to display: size, runtime")
        
    else:
        print(query)
        x = linspace(0, 1, 100)
        size_hashed_data_multiple = {}
        size_random_data_multiple = {}
        runtime_hashed_data_multiple = {}
        runtime_random_data_multiple = {}
        
        for i in range(num_trials): 
            trial_data = get_cdfselect_plot_data(query, x, size, runtime)
            for j in range(len(x)):
                x_value = x[j]
                trial_values = trial_data[j]
                if size:
                    if x_value in size_hashed_data_multiple.keys():
                        size_hashed_data_multiple[x_value].append(trial_values[0][0])
                        size_random_data_multiple[x_value].append(trial_values[1][0])
                    else:
                        size_hashed_data_multiple[x_value] = [trial_values[0][0]]
                        size_random_data_multiple[x_value] = [trial_values[1][0]]
    
                if runtime:
                    if x_value in runtime_hashed_data_multiple.keys():
                        runtime_hashed_data_multiple[x_value].append(trial_values[0][1])
                        runtime_random_data_multiple[x_value].append(trial_values[1][1])
                    else:
                        runtime_hashed_data_multiple[x_value] = [trial_values[0][1]]
                        runtime_random_data_multiple[x_value] = [trial_values[1][1]]
                    
            
    #         organizing data for each trial by x-value (sampling threshold)
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(25,8))
        fig = plt.subplots_adjust(wspace=.5)
        
        if size:
            size_hashed_data = []
            size_random_data = []
            for k,v in size_hashed_data_multiple.items():
                size_hashed_data.append(median(v))
            for k,v in size_random_data_multiple.items():
                size_random_data.append(median(v))
            ax1.plot(x, size_hashed_data, label='Hashed sampling')
            ax1.plot(x, size_random_data, label='Random sampling')
            ax1.legend(loc='best')
            ax1.set_xlabel('Sampling Threshold')
            ax1.set_ylabel('Output size')
            ax1.set_title('Output size')
                
                
        if runtime:
            runtime_hashed_data = []
            runtime_random_data = []
            for k,v in runtime_hashed_data_multiple.items():
                runtime_hashed_data.append(median(v))
            for k,v in runtime_random_data_multiple.items():
                runtime_random_data.append(median(v))
            ax2.plot(x, runtime_hashed_data, label='Hashed sampling')
            ax2.plot(x, runtime_random_data, label='Random sampling')
            ax2.legend(loc='best')
            ax2.set_xlabel('Sampling Threshold')
            ax2.set_ylabel('Runtime')
            ax2.set_title('Runtime')

        plt.show()


queries = get_queries()
display_cdfselect_plots(1, queries[0], True, True)
