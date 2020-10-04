Author: Kelsey Schreiber, University of Illinois at Urbana-Champaign
Last Updated: 12.4.19

*****************
This package contains a novel Perspectives in International Project Evaluation (PIPE) Database collected for research relating to stakeholder evaluation in international water development projects. It also contains methods of adding to the database via web and PDF scraping, analysis of text within the database, and preliminary results.

Contents include:

PIPEdatabase_10292019.csv: meta-data and ID mapping to document text

key_PIPE.xlsx: ID mapping, document done hierarchy, and location hierarchy information

tools/main.py: main script that houses all other functions, including web and PDF scraping, a GUI to search the PIPE database and find representative phrases, two methods of analysis of results, and a helper function to search for certain phrases within documents

tools/text inputs: folder containing .txt files called in subroutines, including country_codes and country_list, and example input files. These can be updated as necessary by user.

tools/dictionary: folder containing saved dictionary of freq_data (input in CaseOLAP) for the entire PIPE database.

data/: folder containing income classification (from WB) and location hierarchy information (from UNSD). These can be updated as necessary. The inputs used in past iterations of web scraping are also archived here.

data/pdf_files: folder to store any pdf files to be scraped and added to PIPE database

all_text_files/: folder containing .txt of documents in PIPE database

output/pdf_converted: folder containing output of converted pdf files to .txt

output/pdf_to_db_output.csv: meta-data output from converted pdfs consistent with format of PIPE database so user can easily add to PIPEdatabase_10292019.csv

output/web_converted: folder containing output of converted web pages to .txt

output/web_to_db_output.csv: meta-data output from converted web pages consistent with format of PIPE database so user can easily add to PIPEdatabase_10292019.csv

output/PIPE_doc_output: folder containing .txt of documents returned from GUI search

output/PIPEQueryOutput.csv: meta-data of documents returned from GUI search

output/repPhrase_output.txt: ranked representative phrases returned from GUI search or manual rep_phrase_mining

past_results/repPhrase: folder containing representative phrases for the entire PIPE database (as of 10.29.19) and each stakeholder (engineer, funder, government, NGO)

past/results/QCA: folder containing results of qualitative comparative analysis on top representative phrases (as of 10.29.19)


**
AutoPhrase-master: representative phrase mining requires the AutoPhrase package (Shang, 2019). This must be downloaded separately and the folder should be placed in the 'tools' folder. See https://github.com/shangjingbo1226/AutoPhrase to download.
**

*****************

Main Functions (housed in main.py)
1. pdf_to_db
	* loc_dict_creator
	* loc_hier
	* urban_rural
	* topic_id
	** convert
	** pdf_converter
	^ doc_tone_dict
	^ doc_type_dict
	^ stakeholder_dict
	^ source_code
	^ time_codes

2. web_to_db
	* loc_dict_creator
	* loc_hier
	* web_scrape
	* text_to_string
	* topic_id	* urban_rural
	^ doc_tone_dict
	^ doc_type_dict
	^ stakeholder_dict
	^ source_code
	^ time_codes

3. GUI
	* export_data
	* lister
	* query_export
	* rep_phrase_search
	* text_to_string
	  rep_phrase_mining

4. rep_phrase_mining
	* combine_text
	* context_finder
	* freq_data_finder
	* global_score_finder
	* text_to_string
	** CaseSlim
	** AutoPhrase

5. wt_cos_sim
	* cos_sim
	* phrase_vec
	* text_to_list

6. qca_outcome_counter
	* QCA_paths
	* truth_table_builder
   	* text_to_string


7. Helper functions
   - result_splitter
   - search_in_text



* Sub-functions
- combine_text
- context_finder
- cos_sim
- export_data
- freq_data_finder
- global_score_finder
- lister- loc_dict_creator
- loc_hier
- phrase_vec
- QCA_paths
- rep_phrase_mining
- rep_phrase_search
- text_to_list
- text_to_string
- topic_id
- truth_table_builder
- urban_rural
- web_scrape
- query_export

** Imported sub-routines- AutoPhrase
- CaseSlim
- convert
- pdf_converter


^ Dictionaries- doc_tone_dict- doc_type_dict- stakeholder_dict- source_codes- time_codes

************************************************************************
	MAIN FUNCTIONS
************************************
************************************


pdf_to_db	Scrape content and meta-data from folder of user-labeled PDF documents, generate unique naming ID for each document, save contents to text file under ID, and export CSV of meta-dataDESCRIPTIONThis algorithm scrapes a folder of PDF files and generates meta-data in the format consistent for additions to the Perspectives in International Project Evaluation Database. The algorithm performs the following tasks: (1) converts PDFs to text files, (2) reads through folder of text files (should be saved as: source_doctype_countryORregionORcontinent_year), (3) finds continent, region, country, country_code, income, urban-rural, and topic from content of text, (4) stores source, doc type, and year from file naming conventions, (5) derives stakeholder, and doc tone from source and doc type, respectively, (6) renames file: sourceIDval-yearIDval-countrycode-counter, and (7) exports data to CSV with columns 'ID', 'stakeholder', 'source', 'continent', 'region', 'country', 'country_code', 'income', 'urban rural', 'year', 'topic', ‘original_filename’.USAGEpdf_to_db(folder, name_list, UN_data, WB_data, doc_type_dict, doc_tone_dict, stakeholder_dict, source_codes, time_codes, e0 = 0, f0 = 0, g0 = 0, n0 = 0,  csv_name = ‘pdf_to_db_output.csv’)ARGUMENTSfolder		  extension and folder where PDF files residename_list	  text file listing just file names (can be copy and pasted from folder 		  into text file, each on new line)
UN_data		  country data from UN statistics division
WB_data		  income classification data from World Bankdoc_type_dict	  dictionary that maps the raw document type (from save file) to the 12 		  document type categoriesdoc_tone_dict	  dictionary that maps document type to whether it's informal or formalstakeholder_dict  dictionary that maps sources to stakeholderssource_codes	  dictionary that maps sources to values used in ID naming and file savingtime_codes	  dictionary that maps years to values used in ID naming and file savinge0, f0, g0, n0	  ID counters for engineer (e), funder (f), government (g), and ingo (n) stakeholderscsv_name	  name of file to be exported

******************

qca_outcome_counter	Searches truth table for success/failure pathways to determine weighted outcomesDESCRIPTIONThis algorithm uses a truth table, built using a list of files and QCA phrases with the truth_table_builder function, to determine the number of success and failure pathways satisfied to calculate a weighted outcome for each document in the list of files in the truth table. The success and failure pathways are determined using the fs/QCA software and supplied in the QCA_paths.py file. The function returns a .txt file showing [# success pathways satisfied, #failure pathways satisfied (as negative) \t weighted outcome \t binary outcome (where a weighted outcome <0 = failure (0), weighted outcome >0 = success (1).USAGEqca_outcome_counter(truth_table, path, path_total)ARGUMENTStruth_table	dataframe supplied as the output of truth_table_builder
path		success and failure pathways found using fs/QCA software and input as a nested list showing whether the phrase should be present (1) or absent (0) and whether it is associated with a success pathway (1) or failure pathway (0) (see QCA_paths.py for example and to change pathways)
path_total	number of success and failure pathways as a listed pair

******************rep_phrase_mining		Runs representative phrase mining algorithm (CaseOLAP) on selected documents		DESCRIPTIONFunction containing all sub-processes to find representative phrases from a set of selected docs compared to the entire corpus of PIPE database documents (default) or a user-defined comparison group.USAGErep_phrase_mining(main_list, sibling_list = './text inputs/all_docs.txt', output_filename = '../output/repPhrase_output.txt')ARGUMENTSmain_list		list of selected filenames to run representative phrase mining on
sibling_list		list of sibling documents to selected documents for distinctiveness calculation
output_filename		user-defined filename, defaults to repPhrase_output.txt
******************web_to_db	Scrape content and meta-data from list of URLs, generate unique naming ID for each document, save contents to text file under ID, and export CSV of meta-dataDESCRIPTIONThis algorithm scrapes a list of web-based documents and generates meta-data in the format consistent for additions to the Perspectives in International Project Evaluation Database. The algorithm performs the following tasks: (1) converts list of URLs to text files, (2) accesses url content (html of title, content, date is required as input), (3) finds continent, region, country, country_code, income, urban-rural, topic from content of text, (4) stores source and doc type from user input, (5) derives stakeholder and doc tone from source and doc type (respectively), (6) write file and name: sourceIDval-yearIDval-countrycode-counter, and (7) exports data to CSV with columns 'ID', 'stakeholder', 'source', 'continent', 'region', 'country', 'country_code', 'income', 'urban rural', 'year', 'topic', ‘original_filename’.USAGEweb_to_db(url_file, doc_type_dict, doc_raw, doc_tone_dict, stakeholder_dict, source_name, source_codes, time_codes, UN_data, WB_data, e0 = 0, f0 = 0, g0 = 0, n0 = 0, t1 = None, t2 = None, t3 = None, c1 = None, c2 = None, c3 = None, y1 = None, y2 = None, y3 = None, csv_name = ‘web_to_db_output.csv’)ARGUMENTSurl_file	  text file of target urls to be scraped. should be from same source or should be scraped using 			  same html identifiersdoc_type_dict	  dictionary that maps the raw document type (from save file) to the 12 document type categoriesdoc_raw		  type of document being scraped (using raw document acronyms)doc_tone_dict	  dictionary that maps document type to whether it's informal or formalstakeholder_dict  dictionary that maps sources to stakeholderssource_name	  source of documents being scraped (using source acronyms)source_codes	  dictionary that maps sources to values used in ID naming and file savingtime_codes	  dictionary that maps years to values used in ID naming and file saving
UN_data		  country data from UN statistics division
WB_data		  income classification data from World Banke0, f0, g0, n0	  ID counters for engineer (e), funder (f), government (g), and ingo (n) stakeholderst1, ..., y3	  html identifiers for title (t1, t2, t3), content (c1, c2, c3), and date 					  or year (y1, y2, y3)csv_name	  name of file to be exported*****************wt_cos_sim		find the weighted cosine similarity between two lists of represented phrases
DESCRIPTIONMain workflow to calculate the weighted cosine similarity from the output of CaseOLAP (representative phrases and phrase scores) and a list of the number of top phrases to be used in the calculation. Results are exported to a csv file located in the 'output' folder.
USAGEwt_cos_sim(phrase_score1, phrase_scores2, num_top_phrases_list, output = 'cosine_similarity.csv')ARGUMENTSphrase_scores1, phrase_scores2		lists of phrases and rep phrase scores to be compared
num_top_phrases_list			list of the number of top phrases for cosine similarity calculation, e.g. input as range(0, 10, 1)
output					file name for exported cosine similarity values
************************************
************************************
	SUB FUNCTIONS
************************************
************************************context_finder			construct dictionary of selected documents and comparative sibling sets to use in the distinctiveness calculation in CaseSlim
DESCRIPTIONBuilds a dictionary of the selected documents and one or more sibling sets of documents used in the distinctiveness score calculation in CaseSlim.USAGEcontext_finder(context_keys, context_values)ARGUMENTScontext_keys		document set names
context_values		documents belonging to each of the designated sets******************

cos_sim				calculates cosine similarity between two term frequency vectorsDESCRIPTIONCalculates the cosine similarity score [0, 1] between two term frequency vectors. The closer to 1, the more similar the two vectors are.USAGEcos_sim(x, y)ARGUMENTSx, y 		two term frequency vectors
******************export_data			generate selection options for search of PIPE database and print number of matched entriesDESCRIPTIONUsed in GUI to take user search criteria and find matching documents in PIPE database. Search uses OR logic within unit (i.e. country) and AND logic across unit. For example, a searcher may want documents from projects in 'Africa' OR 'Asia' AND related to 'water.'USAGEexport_data(*args)
******************freq_data_finder		read through selected documents and generate dictionary that maps document to phrase and the count of appearances of each phrase in the document
DESCRIPTIONSearches for each phrase in a list of quality phrases (generated from AutoPhrase) and counts the number of times it appears for each document. This information is then housed in a nested dictionary with the structure of {document name: {phrase: count}}. USAGEfreq_data_finder(selected_docs, path, df)ARGUMENTSselected_docs		list of filenames of documents to be searched
path			path to text of documents selected
df			dataframe containing phrases to be searched in each document
******************

loc_dict_creator		Build dictionaries used in loc_hier to speed up process rather than building for every document.DESCRIPTIONWhen pdf_to_db is initialized, this function is run to generate the dictionaries used to determine region and continent based off of country and continent based off of region. It also assigns an income classification to each country. The function uses location data from the UNSD and income classifications from the World Bank. These files (.csv) can be updated with the current versions to update these mappings.USAGEloc_dict_creator(loc_data, income_data)ARGUMENTSloc_data:		pandas df from UNSD methodology csv (latest source: https://unstats.un.org/unsd/methodology/m49/overview/)
income_data:		pandas df from latest World Bank income breakdown csv (latest source: https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups) *Download and delete first three or four lines for correct column headings!
******************
loc_hier			Search through content of document for continent, region, country, country code (of country mentioned most), and income levelDESCRIPTIONSearch text file to determine location(s). If country or region specified in text, function will automatically infer corresponding higher-level locations (i.e. country will populate corresponding region and continent). The algorithm also searches for the most mentioned country, region, or continent (depending on lowest level available) to populate the country code used in ID naming and file saving. Lastly, it will generate the income-level of the country based on the income_dict as defined by World Bank.USAGEloc_hier(file, UN_data, continent_list, region_dict, country_dict, income_dict)ARGUMENTSfile			contents of text file (file should be in read mode)
UN_data			country data from UN statistics division
continent_list		list of continents (generated by loc_dict_creator
region_dict		dictionary mapping region to continent (generated by loc_dict_creator)country_dict		dictionary mapping country to region and continent (generated by loc_dict_creator)income_dict		a dictionary that breaks countries into high, upper middle, lower middle, and lower economies based on World Bank data******************pdf_to_csv			Reads through list of PDF files and exports to comma-separated values      fileDESCRIPTIONReads through list of PDF files and exports to comma-separated values file, where each row contains the text contents of a specific fileUSAGEpdf_to_csv(filenames, save_file_name)ARGUMENTS	filenames		list of PDF filessave_file_name		html identifiers for the title

******************

pdf_to_text			Reads through list of PDF files and converts each to text fileDESCRIPTIONReads through list of PDF files, scraping the text and removing extra lines, apostrophes, quotations, and spaces and converts each document to a text fileUSAGEpdf_to_text(filenames)ARGUMENTSfilenames		list of PDF files

******************

phrase_vec			creates the weighted phrase frequency vectors used in cosine similarity calculations	DESCRIPTIONTakes two lists of representative phrases and generates a weighted phrase frequency vector with the option of limiting the number of top phrases used (k). USAGEphrase_vec(vec_stake1, vec_stake2, k)ARGUMENTSvec_stake1		results from stakeholder 1 documents
vec_stake2		results from stakeholder 2 documents
k			# of top phrases used

******************

QCA_paths			.py file of success and failure pathways and total success and failure pathway informationDESCRIPTIONFile containing information on pathways identified using fs/QCA software as leading to successful and failed outcomes. Data is called in the qca_outcome_counter function.CONTENTSxxx_path		nested list of pathway information. List holds the phrases in each pathway, whether each phrase should be present (1) or absent (0), and whether the pathway is a success (1) of failure (0) pathway.
xxx_tot			listed pair of the number of success pathways and the number of failure pathways

******************

query_export			take user selections, search for matching items in PIPE database, construct folder of documents and list of file names for matching documents, and export dataframe of meta-data.DESCRIPTIONUsed in GUI to take user search criteria and find matching documents in PIPE database. Search uses OR logic within unit (i.e. country) and AND logic across unit. For example, a searcher may want documents from projects in 'Africa' OR 'Asia' AND related to 'water.'USAGEquery_export(UN_data, stake = None, source = None, tone = None, doc = None, continent = None, region = None, code = None, income = None, u_r = None, y = None, topic = None)ARGUMENTSfile		contents of text file (file should be in read mode)
******************

rep_phrase_search		generate selection options for search of PIPE database, use query_export to search for selections, and run representative phrase mining on selected documents and return ranked phrasesDESCRIPTIONThis option allows users to return selected documents meta-data and folder of document text, but also analyze the selected documents using representative phrase mining.USAGErep_phrase_search(*args)******************
result_splitter			sort results into lists based on number of words in phrase
DESCRIPTIONTakes results from CaseOLAP and splits phrases based on their word count. Returns .txt file of phrases listed by word count and ordered in descending phrase score. Also returns nested list of phrases of length two, three, four, five, and greater than six.
USAGEresult_splitter(rep_phrase_output)ARGUMENTSrep_phrase_output		.txt file containing output from CaseOLAP

******************
search_in_text			search for key word or phrase in documents in the PIPE database
DESCRIPTIONUses binary matching to search through document text in the PIPE database to match a given search term or phrase. The function returns results as a .csv showing which rows match the search term or phrase and a list of doc_IDs that match search term/phrase.
USAGEsearch_in_text(search_term)ARGUMENTSsearch_term		a search term or phrase (as a string)

*****************

text_to_list			convert output of CaseOLAP to listDESCRIPTIONFunction returns a nested list of [[phrase 1, phrase score 1], [phrase 2, phrase score 2], ...].USAGEtext_to_list(text_file)ARGUMENTS	text_file		.txt file containing output from CaseOLAP (representative phrases and scores separated by tab)
******************text_to_string			read through text file and convert each line to a string separated by a commaDESCRIPTIONUsed to convert a list of URLs into a string to be read into the web_scrape algorithm, each line of URL is converted to a string and separated by a comma.USAGEtext_to_string(text_file)ARGUMENTS	text_file		contents of text file (file should be in read mode)

******************

topic_id			Search through text file to determine topic(s). Uses list of related terms to determine topicDESCRIPTIONSearch through text file to determine topic(s). Uses the following water terms: water, WASH, sanitation, hygiene. Uses the following agriculture terms: irrigation, crop, agriculture, farm, farmer, yield, and harvest.USAGEtopic_id(file)ARGUMENTSfile		contents of text file (file should be in read mode)

******************

truth_table_builder		Make truth table from rep_phrasesDESCRIPTIONSearch through documents outlined in file_list for the top phrases identified using QCA (supplied in rep_phrase_list). Output dataframe (pandas df) of documents searched and whether QCA phrase was found (1) or not (0) and .csv (truth_table.csv) of same output.USAGEtruth_table_builder(rep_phrase_list, file_list)ARGUMENTSrep_phrase_list		list (.txt file) of QCA phrases to search for to build truth table
file_list		list of doc_IDs for files to search for QCA phrases******************

urban_rural	Search through text file to determine whether project is in an urban or rural settingDESCRIPTIONSearch through text file to determine whether project is in an urban or rural setting by using a keyword search of urban and rural.USAGEurban_rural(file)ARGUMENTSfile		contents of text file (file should be in read mode)******************
web_scrape			accesses url and extracts user specified title, content, and year infoDESCRIPTIONThis algorithm searches through a list of common urls (of the same source website) and searches for the title, content, and year through user-generated html attributes (t1, t2, …, y2, y3).USAGEweb_scrape(url, t1 = None, t2 = None, t3 = None, c1 = None, c2 = None, c3 = None, y1 = None, y2 = None, y3 = None)ARGUMENTSurl			url of contentt1, t2, t3		html identifiers for the titlec1, c2, c3		html identifiers for the contenty1, y2, y3		html identifiers for the date or year******************
Lister		take entries from user selections, returned as position within options, and map back to text of selectionDESCRIPTIONEntries returned from GUI selection are returned as the position of the selection in the list of options. This function takes the position and returns the corresponding text of the selected entries.USAGElister(entry, parent_list)ARGUMENTSentry			list of entry positions selected by user
parent_list		list of all entry options
******************combine_text		read through list of .txt files and combine into one .txt fileDESCRIPTIONTakes a list of filenames to be combined, reads through text of files in designated folder, and combines the text, separated by a new line, into one .txt file.USAGEcombine_text(file_list, path_to_text, output_name)ARGUMENTS	file_list		list of file names to be combined
path_to_text		path to raw text of files to be combined
output_name		desired name of combined .txt file************************************************************************
	DICTIONARIES
************************************
************************************doc_type_dict	Dictionary that maps the type of document being scraped, from user-generated input, to a broader category of 12 different document types.doc_tone_dict	Dictionary that maps the 12 document types into formal or informal document tone.Tone	Type				Type (raw)				Type (raw, acronym)Formal	 Internal Assessment (IA)	Internal Assessment			IA	 Project report (PR)		Mid-Term Report				MidE					Performance Report			PerR
					Monitoring and Evaluation Report	ME
					Report					R					Summary Report				SR					Project Evaluation			PrjE
					Project Completion Report		PCR					Evaluation Summary			ES					Final Evaluation			FE					Implem Completion and Results Report	ICR					Performance Evaluation			PerE					Project Review				PrjR	 Special Report (SR)		Volunteer National Report		VNR					Accountability Report			AcR					Collaboration				C					Beneficiary Assessment			BA					Special Evaluation			SE	 Impact Study (IS)		Impact Study				IS					Program Impact Monitoring Report	PIM	 Plan (PL)			Performance Plan			PerP					Strategic Plan				SP					Water Action Decade			WAD					Strategy				S					Evaluation Approach			EA					Country Plan				CP					Policy					PCY	 Annual Review (AR)		Annual Review				AR	 Case Study (CS)		Case Study				CS	 Focus Group (FG)		Focus Group				FGInformal Project Profile (PP)		Project Page				PP	 				Project Fact Sheet			FS	 Blog (B)			Blog					B	 Story (ST)			Story					ST	 Article (AT)			Article					AT******************source_codes	Dictionary that assigns each source_ID to a source_ID_val to generate ID for unique identification and file naming. The first number (1, 2, 3, 4) in each ID value corresponds to one stakeholder group (engineer, funder, government, INGO).stakeholder_dict	Dictionary that maps each source to its corresponding stakeholder group.Stakeholder	Source				Source_ID	Source_ID_valEngineer	Aecom				AEC		100		ARUP				ARUP		101		CDM Smith			CDM		102		Coffey				COF		103		Eng Without Borders		EWB		104		EngWithout Borders - Canada	EWB-CA		105		Mott MacDonald			MM		106		Stantec				STA		107		Tetra Tech, Inc.		TT		108Funder		African Development Bank	AfDB		201		Asian Development Bank		AsDB		202		Inter-American Development Bank	IDB		203		USAID				USAID		204		World Bank			WB		205Government	Comoros Government		COMGOV		303		Eritrea Government		ERIGOV		304		Gambia Government		GMBGOV		305		Global Waters - USAID		GW		302		Mali Government			MLIGOV		307		Malawi Government		MWIGOV		306		SDG - Voluntary Nat'y Reviews	SDG		301		WASHwatch			WW		308INGO		Acumen				ACU		401		Blumont (Int'l Relief and Dev)	IRD		402		CARE				CARE		403		Catholic Relief Services	CRS		404		charity:water			CW		405		Clean Water for Haiti		CWH		406		Concern Worldwide		COW		407		Drop in the Bucket		DB		408		Helvetas			HELV		409		The Her Initiative		HI		410		H2O For Life			HFL		411		Improve International		II		412		Initiative: Eau			IE		413		Innovations for Poverty Action	IPA		414		Int'l Dev Enterprises (iDE)	IDE		415		International Medical Corps	IMC		416		Int'l Water Mgt Institute	IWMI		417		IRC				IRC		418		The Last Well			TLW		419		Lifewater			LI		420		Lifewater.ca			LC		421		OK Clean Water Project		OCWP		422		Pump Aid			PAWL		423		Pure Water for the World	PWW		424		RTI International		RTI 		425		Ryan's Well Foundation		RWF		426		Water for People		WFP		427		The Water Project		WP		428		World Vision			WV		429******************time_codes	Dictionary that maps the document year, from web-scraped data or user-input, to to year_ID_val to generate ID for unique identification and file naming.year	year_ID_val2000	002001	012002	022003	032004	042005	052006	062007	072008	082009	092010	102011	112012	122013	132014	142015	152016	162017	172018	182019	19None	99