# Sort results into list based of top 3 and 4 word phrases
import pandas as pd


def three_four_splitter(self, df, file):
    '''input: dataframe of score, phrase
       output: list of ranked 3- and 4-grams with corresponding phrase score
    '''

    new_df = pd.DataFrame(columns = ['score', 'phrase'])
    
    n = len(df)

    for i in range(n):
        num_words = len(df['phrase'][i].split()) # split string by words, len = number of words
        if num_words == 3 or num_words ==4:
            temp_df = pd.DataFrame([[df['score'][i], df['phrase'][i]]], columns=['score', 'phrase'])
            new_df = new_df.append(temp_df)

    new_df.to_csv(file, sep='\t', index=False, header=False)

    return(new_df)

# Helper - Find number of matching top phrases (doesn't show which phrases match)
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
# Helper - Sort results into lists based on number of words
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

# Helper - Sort results into list based of top 3 and 4 word phrases
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
