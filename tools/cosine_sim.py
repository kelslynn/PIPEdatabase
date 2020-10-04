from CaseOLAP import CaseSlim
import pandas as pd
from pandas import DataFrame as DF
import codecs
from pandas import to_datetime
import csv
from pathlib import Path
import numpy as np
import numpy.linalg as la

### Phrase Frequency ####
def phrase_vec(vec_stake1, vec_stake2, k):
    ''' Input: results from stakeholder 1 documents, results from stakeholder 2 documents, 
                k # of top phrases used
        Output: Weighted phrase frequency vectors, dependent on ranking of phrase'''
    subset_stake1 = vec_stake1[:k]
    dict_stake1 = {x[0]:x[1] for x in subset_stake1}

    subset_stake2 = vec_stake2[:k]
    dict_stake2 = {x[0]:x[1] for x in subset_stake2}

    all_terms = []
    for j in range(k):
        subset_stake1[j][0]
        all_terms.append(subset_stake1[j][0])
    for j in range(k):
        if subset_stake2[j][0] not in all_terms:
            all_terms.append(subset_stake2[j][0])

    # create phrase vectors for each stakeholder based on ranking given by relevance score
    stake1_vec = []
    stake2_vec = []

    for i in all_terms:
        if i in dict_stake1:
            wt = len(dict_stake1) - list(dict_stake1.keys()).index(i)
            stake1_vec.append(wt)
        else:
            stake1_vec.append(0)
        if i in dict_stake2:
            wt = len(dict_stake2) - list(dict_stake2.keys()).index(i)
            stake2_vec.append(wt)
        else:
            stake2_vec.append(0)
        wt -= 1
    return(stake1_vec, stake2_vec)

### Cosine Similarity ###
def cos_sim(x, y):
    ''' Input: Two term frequency vectors for comparison
        Output: Cosine similarity score [0, 1] -- closer to 1, more similar'''
    dot = np.dot(x, y)
    norm_x = la.norm(x)
    norm_y = la.norm(y)
    return(dot/(norm_x*norm_y))

def wt_cos_sim(phrase_scores1, phrase_scores2, num_top_phrase_list):
    ''' Input: two lists of phrases and rep phrase scores,
                the number of top phrases you'd like to calculate cosine sim for
    Output: cosine similarity of two vectors'''
    n = len(num_top_phrase_list)

    cos_sim_vals = np.zeros((n, 2))
    cos_sim_vals[:, 0] = np.array((num_top_phrase_list))

    for j in range(n):
        vec_1, vec_2 = phrase_vec(phrase_scores1, phrase_scores2, num_top_phrase_list[j])
        cos_sim_vals[j,1] = cos_sim(vec_1, vec_2)

    return(cos_sim_vals)


# Sort results into lists based on number of words
def result_splitter(results):
    '''input: results as list
       output: lists of phrases by word count
    '''
    
    two_words = []
    three_words = []
    four_words = []
    five_words = []
    six_plus_words = []
    
    n = len(results)
    
    for i in range(n):
        num_words = len(results[i][0].split()) # split string by words, len = number of words
        if num_words == 2:
            two_words.append(results[i])
        elif num_words == 3:
            three_words.append(results[i])
        elif num_words == 4:
            four_words.append(results[i])
        elif num_words == 5:
            five_words.append(results[i])
        else:
            six_plus_words.append(results[i])
    
    return(two_words, three_words, four_words, five_words, six_plus_words)

# Sort results into list based of top 3 and 4 word phrases
def three_four_splitter(results):
    '''input: results as list
       output: list of ranked 3- and 4-grams
    '''
    
    three_four_words = []
    
    n = len(results)
    
    for i in range(n):
        num_words = len(results[i][0].split()) # split string by words, len = number of words
        if num_words == 3 or num_words ==4:
            three_four_words.append(results[i])
    
    return(three_four_words)


def text_to_list(text_file):
    '''Defn: 
    Input: text_file: 
    Output: '''
    file = open(text_file, 'r')
    string = [line.split('\t') for line in file.readlines()]
    
    new_list = []
    for i in range(len(string)):
        temp = []
        temp.append(string[i][1])
        temp.append(string[i][0])
        new_list.append(temp)
    #flatten = [item.rstrip() for sublist in string for item in sublist
    return(new_list)


# Find number of matching top phrases (doesn't show which phrases match)
def matches(df1, df2, n):
    #df1_list = list(df1['phrase'])[0:n]
    m = len(df1[0:n])
    df1_list = []
    for i in range(m):
        df1_list.append(df1[i][0])
    
    #df2_list = list(df2['phrase'])[0:n]
    k = len(df2[0:n])
    df2_list = []
    for i in range(k):
        df2_list.append(df2[i][0])
    
    count = 0
    for i in df1_list:
        if(i in df2_list):
            count += 1
    return(count)


def cosine_compare(phrase1, phrase2, num_phrases, output = 'cosine_similarity.csv'):
    # Save cosine sim data in csv
    path = '../output/'

    x = text_to_list(phrase1)
    y = text_to_list(phrase2)
    
    result = wt_cos_sim(x, y, num_phrases)

    with open(path + output, 'w') as csv_file:
        writer = csv.writer(csv_file) # call the csv writer function
        for x, y in result:
            writer.writerow([x, y])

    return('done')
