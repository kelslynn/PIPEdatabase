# PIPEdatabase
Author: Kelsey Schreiber, University of Illinois at Urbana-Champaign

# Description
This package contains a novel Perspectives in International Project Evaluation (PIPE) Database collected for research relating to stakeholder evaluation in international water development projects. It also contains methods of adding to the database via web and PDF scraping, analysis of text within the database, and preliminary results.

# Contents
- *PIPEdatabase_10292019.csv*: meta-data and ID mapping to document text
- *key_PIPE.xlsx*: ID mapping, document done hierarchy, and location hierarchy information
- *tools/main.py*: main script that houses all other functions, including web and PDF scraping, a GUI to search the PIPE database and find representative phrases, two methods of analysis of results, and a helper function to search for certain phrases within documents
- *tools/text inputs*: folder containing .txt files called in subroutines, including country_codes and country_list, and example input files. These can be updated as necessary by user.
- *tools/dictionary*: folder containing saved dictionary of freq_data (input in CaseOLAP) for the entire PIPE database.
- *data/*: folder containing income classification (from WB) and location hierarchy information (from UNSD). These can be updated as necessary. The inputs used in past iterations of web scraping are also archived here.
- *data/pdf_files*: folder to store any pdf files to be scraped and added to PIPE database
- *all_text_files/*: folder containing .txt of documents in PIPE database
- *output/pdf_converted*: folder containing output of converted pdf files to .txt
- *output/pdf_to_db_output.csv*: meta-data output from converted pdfs consistent with format of PIPE database so user can easily add to *PIPEdatabase_10292019.csv*
- *output/web_converted*: folder containing output of converted web pages to .txt
- *output/web_to_db_output.csv*: meta-data output from converted web pages consistent with format of PIPE database so user can easily add to *PIPEdatabase_10292019.csv*
- *output/PIPE_doc_output*: folder containing .txt of documents returned from GUI search
- *output/PIPEQueryOutput.csv*: meta-data of documents returned from GUI search
- *output/repPhrase_output.txt*: ranked representative phrases returned from GUI search or manual rep_phrase_mining
- *past_results/repPhrase*: folder containing representative phrases for the entire PIPE database (as of 10.29.19) and each stakeholder (engineer, funder, government, NGO)
- *past/results/QCA*: folder containing results of qualitative comparative analysis on top representative phrases (as of 10.29.19)
- **AutoPhrase-master**: representative phrase mining requires the AutoPhrase package (Shang, 2019). This must be downloaded separately and the folder should be placed in the 'tools' folder. See https://github.com/shangjingbo1226/AutoPhrase to download.

# Main Functions
1. pdf_to_db
2. web_to_db
3. rep_phrase_mining
4. wt_cos_sim

Note: See README.txt for the full list of functions, sub-functions, sub-routines, and dictionaries used in the analysis. Each is accompanied by a description, proper usage, and explanation of arguments.

## pdf_to_db
Scrape content and meta-data from folder of user-labeled PDF documents, generate unique naming ID for each document, save contents to text file under ID, and export CSV of meta-data

### DESCRIPTION
This algorithm scrapes a folder of PDF files and generates meta-data in the format consistent for additions to the Perspectives in International Project Evaluation Database. The algorithm performs the following tasks: (1) converts PDFs to text files, (2) reads through folder of text files (should be saved as: source_doctype_countryORregionORcontinent_year), (3) finds continent, region, country, country_code, income, urban-rural, and topic from content of text, (4) stores source, doc type, and year from file naming conventions, (5) derives stakeholder, and doc tone from source and doc type, respectively, (6) renames file: sourceIDval-yearIDval-countrycode-counter, and (7) exports data to CSV with columns 'ID', 'stakeholder', 'source', 'continent', 'region', 'country', 'country_code', 'income', 'urban rural', 'year', 'topic', 'original_filename'.

## web_to_db
Scrape content and meta-data from list of URLs, generate unique naming ID for each document, save contents to text file under ID, and export CSV of meta-data

### DESCRIPTION
This algorithm scrapes a list of web-based documents and generates meta-data in the format consistent for additions to the Perspectives in International Project Evaluation Database. The algorithm performs the following tasks: (1) converts list of URLs to text files, (2) accesses url content (html of title, content, date is required as input), (3) finds continent, region, country, country_code, income, urban-rural, topic from content of text, (4) stores source and doc type from user input, (5) derives stakeholder and doc tone from source and doc type (respectively), (6) write file and name: sourceIDval-yearIDval-countrycode-counter, and (7) exports data to CSV with columns 'ID', 'stakeholder', 'source', 'continent', 'region', 'country', 'country_code', 'income', 'urban rural', 'year', 'topic', Ôoriginal_filenameÕ.

## rep_phrase_mining
Runs representative phrase mining algorithm (CaseOLAP) on selected documents		

### DESCRIPTION

Function containing all sub-processes to find representative phrases from a set of selected docs compared to the entire corpus of PIPE database documents (default) or a user-defined comparison group.

## wt_cos_sim
Find the weighted cosine similarity between two lists of represented phrases

### DESCRIPTION
Main workflow to calculate the weighted cosine similarity from the output of CaseOLAP (representative phrases and phrase scores) and a list of the number of top phrases to be used in the calculation. Results are exported to a csv file located in the 'output' folder.
