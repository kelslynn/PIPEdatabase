################## Main Script ##################
# Author: Kelsey Schreiber
# Date created: 10-29-19
# Last updated: 12-3-19
# Comments: Descriptions of functions and variables can be found in README.txt or subfunction .py files

#### Contents ####
# Add to PIPE database
# 1. PDF Scraping -- scrape file of PDF files, create metadata file, create text file with corresponding ID
# 2. Web Scrape -- scrape file of URLs, create metadata file, create text file with corresponding ID

# Search and analyze PIPE
# 3. GUI -- search PIPE and return metadata and files with option to directly run representative phrase algorithm
# 4. Representative Phrase Mining -- find representative phrases from collection of documents compared to user-defined sibling set
# 5. Cosine Similarity -- find cosine similarity between two output files of representative phrases
# 6. Qualitative Comparative Analysis -- build QCA truth table
# 7. Helper functions -- split results into phrase lengths, search through PIPE database for certain terms

################## 1. PDF Scraping ##################
from PDFText_to_IDedText import *
import pandas as pd

# extension and folder where PDF files reside
folder = "../data/pdf_files/"

# text file listing just file names (can be copy and pasted from folder into text file, each on new line)
text_file = "./text inputs/file_names.txt"

# country and income data
WB_data = pd.read_csv('../data/income_classification.csv')
UN_data = pd.read_csv('../data/UNSD_Methodology.csv')

#uncomment next line to scrape text from pdf
#pdf_to_db(folder, text_file, UN_data, WB_data, doc_type_dict, doc_tone_dict, stakeholder_dict, source_codes, time_codes, e0 = 0, f0 = 0, g0 = 0, n0 = 0, csv_name = '../output/pdf_to_db_output.csv')

################## 2. Web Scraping ##################
from webText_to_IDedText import *
# Input variables for scrape test
title_1 = 'h1'
title_2 = 'class'
title_3 = 'entry-title'
content_1 = 'div'
content_2 = 'class'
content_3 = 'entry-content'
year_1 = None
year_2 = None
year_3 = None

# From user inputs
source_name = 'DB'
doc_raw = 'B'

# Identify text file with URLs
url_file = './text inputs/urls.txt'

# country and income data
WB_data = pd.read_csv('../data/income_classification.csv')
UN_data = pd.read_csv('../data/UNSD_Methodology.csv')

# uncomment next line to scrape text from website
#web_to_db(url_file, doc_type_dict, doc_raw, doc_tone_dict, stakeholder_dict, source_name, source_codes, time_codes, UN_data, WB_data, t1 = title_1, t2 = title_2, t3 = title_3, c1 = content_1, c2 = content_2, c3 =content_3, csv_name = '../output/web_to_db_output.csv')


################## 3. Graphical User Interface ##################
# Uncomment next line to run GUI to search through PIPE database and find representative phrases (for search results using default inputs)
from GUI import *


################## 4. Representative Phrase Mining ##################
# Use when to run representative phrase mining algorithm separate from search and with user defined sibling set
from phrase_mining import *

# Required input
# use './text inputs/all_docs.txt' to find rep phrases for all docs in PIPE database
# use './text inputs/trimmed_docs.txt' to find rep phrases of trimmed version of PIPE database (more proportional stakeholders)
# use './text inputs/file_list.txt' to find rep phrases of documents from last query (use default sibling list)
phrase_list = './text inputs/file_list.txt'

# Optional inputs, comment out for default
#sibling_list = './text inputs/ngo_test.txt'
#output_filename = '../output/repPhrase_output.txt'

# uncomment next line to phrase mine
#rep_phrase_mining(phrase_list) #, sibling_list, output_filename)

################## 5. Cosine Similarity ##################
from cosine_sim import *

file1 = '../output/repPhrase_output.txt'
file2 = '../output/repPhrase_output.txt'
phrase_range = range(1, 10, 1) # choose start, stop, and frequency

# Optional inputs, comment out for default
#output = 'cosine_similarity.csv'

# uncomment next line to find cosine similarity between file1 and file2
#wt_cos_sim(file1, file2, phrase_range)

################## 6. Qualitative Comparative Analysis ##################
from QCA import *

#import pathways and path totals from QCA_paths.py
from QCA_paths import *

df = truth_table_builder('./text inputs/qca_search_example.txt', './text inputs/file_list.txt')
qca_outcome_counter(df, eng_path, eng_tot)

################## 7. Extra Functionality ##################
from helper import *

#result_splitter('../output/repPhrase_output.txt')
#search_in_text('failure')

