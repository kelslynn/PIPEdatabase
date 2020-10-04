import pandas as pd
import csv

def result_splitter(rep_phrase_output):
    '''Defn: Sort results into lists based on number of words in phrase
    Input: rep_phrase_output: .txt file containing output from CaseOLAP
    Output: .txt file of phrase scores and phrases ordered by word count and score
            lists of phrases by word count'''
    file = open(rep_phrase_output, 'r')
    string = [line.split('\t') for line in file.readlines()]
    results = []
    
    #for i in range(len(string)):
    #    temp = []
    #    temp.append(string[i][1].rstrip())
    #    results.append(temp)
        
    two_words = []
    three_words = []
    four_words = []
    five_words = []
    six_plus_words = []

    n = len(string)

    for i in range(n):
        #num_words = len(results[i][0].split()) # split string by words, len = number of words
        num_words = len(string[i][1].split()) # split string by words, len = number of words
        if num_words == 2:
            two_words.append(string[i][0] + '\t' + string[i][1])
        elif num_words == 3:
            three_words.append(string[i][0] + '\t' + string[i][1])
        elif num_words == 4:
            four_words.append(string[i][0] + '\t' + string[i][1])
        elif num_words == 5:
            five_words.append(string[i][0] + '\t' + string[i][1])
        else:
            six_plus_words.append(string[i][0] + '\t' + string[i][1])
    
    with open('../output/split_results.txt', 'w', encoding="utf-8") as f:
        for i in range(len(two_words)):
            f.write(two_words[i])
        for i in range(len(three_words)):
            f.write(three_words[i])
        for i in range(len(four_words)):
            f.write(four_words[i])
        for i in range(len(five_words)):
            f.write(five_words[i])
        for i in range(len(six_plus_words)):
            f.write(six_plus_words[i])

    
    return(two_words, three_words, four_words, five_words, six_plus_words)



def search_in_text(search_term):
    '''Defn: search for key word or phrase in documents in the PIPE database
        Input: search_term: a search term or phrase (as a string)
        Output: .csv that returns a column of results showing which rows match search term
                a list of doc_IDs that match search term/phrase'''
    
    folder = '../all_text_files/'
    df = pd.read_csv('../PIPEdatabase_10292019.csv')
    
    n = len(df)
    doc_match_ID = []

    with open('../output/search_results.csv', 'w') as csv_file: # open .csv and append data into file
        for i in range(n):
            temp = []
            file = df['ID'][i]
            f = open(folder + file + '.txt', 'r', encoding="utf-8")

            text = f.read()

            if (search_term in text):
                temp.append('%s' % search_term)
                doc_match_ID.append(df['ID'][i])
            else:
                temp.append('')

            writer = csv.writer(csv_file)# call the csv writer function 
            writer.writerow([temp])
            
    return(doc_match_ID)


