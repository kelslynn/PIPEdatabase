from CaseOLAP import CaseSlim
import pandas as pd
from pandas import DataFrame as DF
import codecs
import csv
from pathlib import Path
import numpy.linalg as la

    
### Phrase Frequency ###
def text_to_string(text_file):
    '''Defn: read through text file and convert each line to a string separated by a comma
    Input: text_file: contents of text file (file should be in read mode)
    Output: flattened list of urls (as strings) separated by commas'''
    file = open(text_file, 'r')
    string = [line.split(',') for line in file.readlines()] 
    flatten = [item.rstrip() for sublist in string for item in sublist]
    return(flatten)


def global_score_finder(df):
    '''Defn: Build global scores based on integrity scores
    Input: df: dataframe containing phrase and integrity scores from AutoPhrase
    Output: dictionary of phrase: integrity score mapping'''
    global_scores = {}
    n = len(df)
    for i in range(n):
        global_scores.update({df['phrase'][i]:df['integrity'][i]})
    
    return(global_scores)

def freq_data_finder(selected_docs, path, df):
    '''Defn: read through selected documents and generate dictionary that maps document to phrase and the count of appearances of each phrase in the document
    * warning: this may take a long time to run!
    Input: selected_docs: list of filenames of documents to be searched
    path: path to text of documents selected
    df: dataframe containing phrases to be searched in each document
    Output: nested dictionary of {document: {phrase: count}}'''
    
    lst_phrases = df['phrase']
    
    # Loop through path objects to get list of file names
    filenames = selected_docs
    
    freq_data = {}
    #n = 0
    
    for file in filenames:
        #n += 1
        #print(n)
        doc_freq_data = {}
        for phrase in lst_phrases:
            f = open(path + file + '.txt').read()
            if (phrase in f) and (phrase not in doc_freq_data):
                doc_freq_data[phrase] = f.count(phrase)
        freq_data[file] = doc_freq_data
    
    return(freq_data)

# Use to load pickle data to new variable!
# https://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file
import pickle
def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
    
def context_finder(context_keys, context_values):
    '''Defn: construct dictionary of selected documents and comparative sibling sets to use in the distinctiveness calculation in CaseSlim
    Input: context_keys: document set names
    context_values: documents belonging to each of the designated sets
    Output: dictionary mapping set names to documents belonging to each set'''
    context = {}
    n = len(context_keys)
    
    for i in range(n):
        context.update({context_keys[i]: text_to_string(context_values[i])})
    
    return(context)

def combine_text(file_list, path_to_text, output_name):
    '''Defn: Read through list of .txt files and combine into one .txt file
    Input: file_list: list of file names to be combined
    path_to_text: path to raw text of files to be combined
    output_name: desired name of combined .txt file
    Output: combined .txt file'''
    f = text_to_string(file_list)
    path = path_to_text

    # Loop through path objects to get list of file paths
    filenames = []
    for file in f:
        filenames.append(path + file + '.txt')

    ## Combine txt files and separate by " 
    with open(output_name, 'w', encoding="utf-8") as outfile:
        for fname in filenames:
            outfile.write('"')
            with open(fname, encoding="utf-8") as infile:
                for line in infile:
                    outfile.write(line)
                outfile.write('\n')
    return()            



def rep_phrase_mining(main_list, sibling_list = './text inputs/all_docs.txt', output_filename = '../output/repPhrase_output.txt'):
    '''Defn: Runs representative phrase mining algorithm (CaseOLAP via CaseSlim) on selected documents.
    Input: main_list: list of selected filenames to run representative phrase mining on
    sibling_list: list of sibling documents to selected documents for distinctiveness calculation
    output_filename: user-defined filename, defaults to repPhrase_output.txt
    Output: '''
    
    path = '../all_text_files/' # path to files
    integrity_list = './AutoPhrase-master/models/DBLP/AutoPhrase_multi-words.txt'
    context_keys = ['main', 'sibling'] # define context docs, i.e. comparison set for distinctiveness score
    context_values = [main_list, sibling_list]
    
    # Combine docs
    print('===Combining docs===')
    combine_text(main_list, path, './AutoPhrase-master/data/input_combined.txt')

    # Build freq_data dictionary from scratch or load from file
    print('===Building freq_data===')
    if main_list == './text inputs/all_docs.txt':
        # Load frequent data dictionary
        print('===Loading dictionary data===')
        # read through selected docs file and write to list of strings
        selected_docs = text_to_string(main_list)
        
        # Load phrases and integrity scores from AutoPhrase as df
        df = pd.read_csv(integrity_list, delimiter="\t", header=None)
        df.columns = ["integrity", "phrase"]
        global_scores = global_score_finder(df)
        
        freq_data = load_obj('./dictionary/freq_data_all')
    elif main_list == './text inputs/trimmed_docs.txt':
        # Load frequent data dictionary
        print('===Loading dictionary data===')
        # read through selected docs file and write to list of strings
        selected_docs = text_to_string(main_list)
        
        # Load phrases and integrity scores from AutoPhrase as df
        df = pd.read_csv(integrity_list, delimiter="\t", header=None)
        df.columns = ["integrity", "phrase"]
        global_scores = global_score_finder(df)
        
        freq_data = load_obj('./dictionary/freq_data_trimmed')
    else:
        # Build freq_data dictionary from scratch
        # Call a bash script (AutoPhrase)
        print('===Parsing phrases using AutoPhrase===')
        import subprocess
        subprocess.call('./AutoPhrase-master/auto_phrase.sh', shell = True)
        
        # read through selected docs file and write to list of strings
        selected_docs = text_to_string(main_list)
        
        # Load phrases and integrity scores from AutoPhrase as df
        # Build global_scores (integrity scores)
        df = pd.read_csv(integrity_list, delimiter="\t", header=None)
        df.columns = ["integrity", "phrase"]
        global_scores = global_score_finder(df)
        
        freq_data = freq_data_finder(selected_docs, path, df)
        #print('frequency data:', len(freq_data))

    context_doc_groups = context_finder(context_keys, context_values)

    ## RUN CaseOLAP ##
    # Create CaseSlim Example Object
    print('===Running CaseOLAP===')
    test = CaseSlim(freq_data, selected_docs, context_doc_groups, global_scores)

    # Compute Representative Phrase Scores
    results = test.compute()

    # Save data as TXT
    print('===Writing results to file===')
    with open(output_filename, 'w', encoding="utf-8") as f:
        for i in range(len(results)):
            f.write(str(results[i][1]) + "\t" + results[i][0] + '\n')

    return('done')
