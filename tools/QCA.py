#import pathways and path totals from QCA_paths.py
#from QCA_paths import *

import pandas as pd
import csv
#from string import printable
#import numpy as np

def text_to_string(text_file):
    file = open(text_file, 'r')
    string = [line.split(',') for line in file.readlines()] 
    flatten = [item.rstrip() for sublist in string for item in sublist]
    return(flatten)

def qca_outcome_counter(truth_table, path, path_total):
    '''Defn: searches truth table and success/failure pathways to determine outcomes
        Input: truth_table: truth table (output from truth_table_builder function)
                path: success and failure pathways found using fs/QCA software. 
                        Input as a nested list showing whether the phrase should be present (1) or absent (0) and whether it is associated with a success pathway (1) or failure pathway (0)
                        (see QCA_paths.py for example and to change pathways)
                path_total: number of success and failure pathways as a listed pair
        Output: .txt file showing [# success pathways satisfied, #failure pathways satisfied (as negative) \t weighted outcome \t binary outcome (weighted outcome <0 = failure (0), weighted outcome >0 = success (1)'''

    file_path = '../output/'
    file_name = 'qca_outcome.txt'

    suc_path_tot = path_total[0]
    fail_path_tot = path_total[1]

    r = len(truth_table) # number of rows
    n = len(path) # number of paths

    raw_labels = []
    for k in range(r):
        suc_label = 0
        fail_label = 0
        for i in range(n):
            temp = 0
            m = len(path[i][0]) #number of phrases in path
            for j in range(m):
                if truth_table[path[i][0][j]][k] == path[i][1][j]:
                    temp += 1
            if temp == m and path[i][2] == 1:
                suc_label += 1
            if temp == m and path[i][2] == 0:
                fail_label -= 1

        
        raw_labels.append([suc_label, fail_label])
    
    label_score = []
    binary_label = []
    for i in range(len(raw_labels)):
        if (raw_labels[i][0] == 0) and (raw_labels[i][1] == 0):
            label_score.append(0)
        else:
            a = raw_labels[i][0]/suc_path_tot + raw_labels[i][1]/fail_path_tot
            label_score.append(a)
        
        if label_score[i] > 0:
            binary_label.append(1)
        elif label_score[i] < 0:
            binary_label.append(0)
        else:
            binary_label.append(None)
            
        
    f = open(file_path + file_name, 'w')
    for i in range(len(raw_labels)):
        f.write(str(raw_labels[i]) + '\t' + str(label_score[i]) + '\t' + str(binary_label[i]) + '\n')
        
    return(raw_labels, label_score)


def truth_table_builder(rep_phrase_list, file_list):
    ''' Defn: make truth table from rep_phrases
        Input: rep_phrase_list: list (.txt file) of QCA phrases to search for to build truth table
                file_list: list of doc_IDs for files to search for QCA phrases
        Output: dataframe (pandas df) of documents searched and whether QCA phrase was found (1) or not (0)
                .csv (truth_table.csv) of same output'''

    file_path = '../all_text_files/'

    rep_phrases = text_to_string(rep_phrase_list)
    rep_phrases.insert(0, 'ID')
    
    df = pd.DataFrame(columns = rep_phrases)
    
    filenames = text_to_string(file_list)
    
    n = 0
    for file in filenames:
        df.loc[n, 'ID'] = file
        for phrase in rep_phrases[1:]:
            f = open(file_path + file + '.txt').read()
            if (phrase in f):
                df.loc[n, phrase] = 1
        n += 1

    df = df.fillna(0)

    df.to_csv('../output/truth_table.csv', index=False)
    
    return(df)