
# coding: utf-8

## Read through folder of text files, open and read through each
import pandas as pd
from pathlib import Path
import os

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import urllib

def text_to_string(text_file):
    '''Defn: read through text file and convert each line to a string separated by a comma
    Input: text_file: contents of text file (file should be in read mode)
    Output: flattened list of urls (as strings) separated by commas'''
    file = open(text_file, 'r')
    string = [line.split(',') for line in file.readlines()] 
    flatten = [item.rstrip() for sublist in string for item in sublist]
    return(flatten)

def web_scrape(url, t1 = None, t2 = None, t3 = None, c1 = None, c2 = None, c3 = None, y1 = None, y2 = None, y3 = None):
    '''Defn: accesses url and extracts user specified title, content, and year info
    Inputs: url: url of content
    t1, t2, t3: html identifiers for the title
    c1, c2, c3: html identifiers for the content
    y1, y2, y3: html identifiers for the date or year
    Output: title, content, and year of website article, blog, story, etc.
    '''
    # Scrape info and text from site
    page = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    response = urllib.request.urlopen(page)
    html = response.read()
    response.close()

    soup = BeautifulSoup(html, 'html.parser')

    # Get name of article/story/blog
    if t1 == None or t2 == None or t3 == None:
        title = None
    else:
        title_box = soup.find(t1, attrs={t2: t3})
        title = title_box.text.strip() # strip() is used to remove starting and trailing i.e. get text

    # Get content of article/story/blog 
    if c1 == None or c2 == None or c3 == None:
        content = None
    else:
        content_box = soup.find(c1, attrs={c2: c3})
        content = content_box.text.strip() 

    # Get date of article/story/blog
    if y1 == None or y2 == None or y3 == None:
        year = None
    else:
        year_box = soup.find(y1, attrs={y2:y3})
        year = year_box.text.strip() 
    
    return(title, content, year)


def web_to_db(url_file, doc_type_dict, doc_raw, doc_tone_dict, stakeholder_dict, source_name, source_codes, time_codes, UN_data, WB_data, e0 = 0, f0 = 0, g0 = 0, n0 = 0, t1 = None, t2 = None, t3 = None, c1 = None, c2 = None, c3 = None, y1 = None, y2 = None, y3 = None, csv_name = '../output/web_to_db_output.csv'):
    ''' Defn: 1. convert list of URLs to text files
              2. access url content (html of title, content, date is required as input)
              3. find continent, region, country, country_code, income, urban-rural, topic from content of text
              4. store source, doc type, and year from file naming
              5. derive stakeholder, doc tone, year range from source, doc type, and year (respectively)
              6. write file source ID val-year ID val-country code-counter
              7. export data to csv with columns 'ID', 'stakeholder', 'source', 'continent', 'region', 'country', 'country_code', 'income', 'urban rural', 'year', 'topic' 
    Inputs: url_file: text file of target urls to be scraped. should be from same source or should be scraped using same html identifiers
            doc_type_dict: dictionary that maps the raw document type (from doc_raw) to the 12 document type categories
            doc_raw: type of document being scraped (using raw document acronyms)
            doc_tone_dict: dictionary that maps document type to whether it's informal or formal
            stakeholder_dict: dictionary that maps sources to stakeholders
            source_name: source of documents being scraped (using source acronyms)
            source_codes: dictionary that maps sources to values used in ID naming and file saving
            time_codes: dictionary that maps years to values used in ID naming and file saving
            UN_data: country data from UN statistics division
            WB_data: income classification data from World Bank
            e0, f0, g0, n0: ID counters for engineer (e), funder (f), government (g), and ingo (n) stakeholders
            t1, t2,...y2, y3: html identifiers for title (t1, t2, t3), content (c1, c2, c3), and date or year (y1, y2, y3)
            csv_name: name of file to be exported
    Output: df: a dataframe (exported as csv) with columns (as listed above) generated from reading through data and file naming
            function also renames files in folder with ID generated
    '''
    # Read url_file into list of separated string
    url_list = text_to_string(url_file)
    
    # Initialize dataframe
    df = pd.DataFrame(columns = ['ID', 'stakeholder', 'source_ID', 'doc_tone', 'doc_type', 'doc_raw', 'continent', 'region', 'country', 'country_code', 'income_level', 'urban_rural', 'month', 'year', 'topic_ID', 'title', 'report_ID', 'URL', 'og_filename'])

    # initialize stakeholder counters
    eng_counter = e0
    fund_counter = f0
    gov_counter = g0
    ngo_counter = n0

    full_continent_list, full_region_dict, full_country_dict, full_income_dict = loc_dict_creator(UN_data, WB_data)

    # Loop through URLs
    for url in url_list:
        # scrape title, content, and year (when applicable)
        title, content, year = web_scrape(url, t1, t2, t3, c1, c2, c3, y1, y2, y3)

        # From content of files
        country_dict, income_level, country_code = loc_hier(content, UN_data, full_continent_list, full_region_dict, full_country_dict, full_income_dict)
        u_r = urban_rural(content)
        topic = topic_id(content)

        # Derived from file naming
        doc_type = doc_type_dict[doc_raw]
        doc_tone = doc_tone_dict[doc_type]
        stakeholder = stakeholder_dict[source_name]

        # ID
        if year == 'nd':
            time = None
        else:
            time = year

        if stakeholder == 'Gov':       
            code = str(source_codes[source_name]) + '-' + str(time_codes[time]) + '-' + str(country_code) + '-' + str(gov_counter)
            gov_counter += 1
        elif stakeholder == 'INGO':
            code = str(source_codes[source_name]) + '-' + str(time_codes[time]) + '-' + str(country_code) + '-' + str(ngo_counter)
            ngo_counter += 1
        elif stakeholder == 'Funder':
            code = str(source_codes[source_name]) + '-' + str(time_codes[time]) + '-' + str(country_code) + '-' + str(fund_counter)
            fund_counter += 1
        elif stakeholder == 'Eng':
            code = str(source_codes[source_name]) + '-' + str(time_codes[time]) + '-' + str(country_code) + '-' + str(eng_counter)
            eng_counter +=1

        df = df.append({'ID': code, 'stakeholder': stakeholder, 'source_ID': source_name, 'doc_tone': doc_tone, 'doc_type': doc_type, 'doc_raw': doc_raw, 'continent': country_dict['continent'], 'region': country_dict['region'], 'country': country_dict['country'], 'country_code': country_code, 'income_level': income_level, 'urban_rural': u_r, 'year': year, 'topic_ID': topic, 'title': title, 'URL': url}, ignore_index = True)

        #content = [text.encode("utf-8") for text in content]
        new_file = open('../output/web_converted/' + code + '.txt', 'w')
        new_file.write(str(content.encode("utf-8")))
        new_file.close()

    df.to_csv(csv_name)
    
    return(df)


# In[11]:


# ID codes
# Source
source_codes = {'AEC': '100', 'ARUP': '101', 'CDM': '102', 'COF': '103', 'EWB': '104', 
                'EWB-CA': '105', 'MM': '106', 'STA': '107', 'TT': '108',
                'AfDB': '201', 'AsDB': '202', 'IDB': '203', 'USAID': '204', 'WB': '205',
                'SDG': '301', 'GW': '302', 'COMGOV': '303', 'ERIGOV': '304', 'GMBGOV': '305', 
                'MWIGOV': '306', 'AMCOW': '307', 'WW': '308', 'BTNGOV': '309',
                'ACU': '401', 'IRD': '402', 'CARE': '403', 'CRS': '404', 'CW': '405',
                'CWH': '406', 'COW': '407', 'DB': '408', 'HELV': '409', 'HI': '410',
                'HFL': '411', 'II': '412', 'IE': '413', 'IPA': '414', 'IDE': '415',
                'IMC': '416', 'IWMI': '417', 'IRC': '418', 'TLW': '419', 'LI': '420',
                'LC': '421', 'OCWP': '422', 'PAWL': '423', 'PWW': '424', 'RTI': '425',
                'RWF': '426', 'WFP': '427', 'WP': '428', 'WV': '429'}

# Time
time_codes = {'2000': '00', '2001': '01', '2002': '02', '2003': '03', '2004': '04', 
              '2005': '05', '2006': '06', '2007': '07', '2008': '08', '2009': '09', 
              '2010': '10', '2011': '11', '2012': '12', '2013': '13', '2014': '14',
              '2015': '15', '2016': '16', '2017': '17', '2018': '18', '2019': '19', None: '99'}


# In[12]:


# Derived dimension dictionaries
doc_type_dict = {'IA': 'IA',
                'MidE': 'PR', 'PR': 'PR', 'ME': 'PR', 'R': 'PR', 'SR': 'PR', 'PrjE': 'PR', 'PCR': 'PR', 'ES': 'PR', 'FE': 'PR', 'ICR': 'PR', 'PE': 'PR', 'PrjR': 'PR',
                'VNR': 'SR', 'AcR': 'SR', 'C': 'SR', 'BA': 'SR', 'SE': 'SR',
                'IS': 'IS', 'PIM': 'IS',
                'PPl': 'PL', 'SP': 'PL', 'WAD': 'PL', 'S': 'PL', 'EA': 'PL', 'CP': 'PL',
                'AR': 'AR',
                'CS': 'CS',
                'FG': 'FG',
                'PP': 'PP', 'FS': 'PP',
                'B': 'B',
                'ST': 'ST',
                'AT': 'AT'}

doc_tone_dict = {'IA': 'F', 'PR': 'F', 'SR': 'F', 'IS': 'F', 'IS': 'F', 'PL': 'F', 'AR': 'F', 'CS': 'F', 'FG': 'F',
                'PP': 'I', 'B': 'I', 'ST': 'I', 'AT': 'I'}

stakeholder_dict = {'AEC': 'Engineer', 'ARUP': 'Engineer', 'CDM': 'Engineer', 'COF': 'Engineer', 'EWB': 'Engineer', 'EWB-CA': 'Engineer', 
                    'MM': 'Engineer', 'STA': 'Engineer', 'TT': 'Engineer',
                'AfDB': 'Funder', 'AsDB': 'Funder', 'IDB': 'Funder', 'USAID': 'Funder', 'WB': 'Funder',
                'SDG': 'Gov', 'GW': 'Gov', 'COMGOV': 'Gov', 'ERIGOV': 'Gov', 'GMBGOV': 'Gov', 
                'MWIGOV': 'Gov', 'AMCOW': 'Gov', 'WW': 'Gov', 'BTNGOV': 'Gov',
                'ACU': 'INGO', 'IRD': 'INGO', 'CARE': 'INGO', 'CRS': 'INGO', 'CW': 'INGO',
                'CWH': 'INGO', 'COW': 'INGO', 'DB': 'INGO', 'HELV': 'INGO', 'HI': 'INGO',
                'HFL': 'INGO', 'II': 'INGO', 'IE': 'INGO', 'IPA': 'INGO', 'IDE': 'INGO',
                'IMC': 'INGO', 'IWMI': 'INGO', 'IRC': 'INGO', 'TLW': 'INGO', 'LI': 'INGO',
                'LC': 'INGO', 'OCWP': 'INGO', 'PAWL': 'INGO', 'PWW': 'INGO', 'RTI': 'INGO',
                'RWF': 'INGO', 'WFP': 'INGO', 'WP': 'INGO', 'WV': 'INGO'}


# In[1]:


## Find geographic info, income, urban rural, and topic
# To-do: auto generate income_dict from website csv

import pandas as pd
import csv
from pathlib import Path

# built based on World Bank 2019 fiscal year income classifcations
# Source: https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups
def loc_dict_creator(loc_data, income_data):
    '''Description: Build dictionaries used in loc_hier. Faster than building for every document.
        input: loc_data: pandas df from UNSD methodology csv
                        latest source: https://unstats.un.org/unsd/methodology/m49/overview/ (download as CSV (UTF-8))
               income_data: pandas df from latest World Bank income breakdown csv
                        latest source: https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups
                        *Download and delete first three or four lines for correct column headings!
        output: continent list: list of continents for loc_hier
                region_dict: {region: continent}
                country_dict: {country: [region, continent]}
                income_dict: {country code: income level}'''

    # Build location dictionary from UN database
    m = len(loc_data)
    
    # Account for Niger/Nigeria searching issues
    x = loc_data.loc[loc_data['Country or Area'] == 'Niger'].index[0]
    loc_data.at[x, 'Country or Area'] = 'Niger '
    
    # Account for Laos searching issues
    x = loc_data.loc[loc_data['Country or Area'] == 'Lao People\'s Democratic Republic'].index[0]
    loc_data.at[x, 'Country or Area'] = 'Lao'
    
    # Account for Tanzania searching issues
    x = loc_data.loc[loc_data['Country or Area'] == 'United Republic of Tanzania'].index[0]
    loc_data.at[x, 'Country or Area'] = 'Tanzania'
        
    # Construct list of continents
    continent_list = list(loc_data['Region Name'].dropna().unique())
    
    # Initialize region and country dictionary
    region_dict = {}
    country_dict = {}
    
    # Construct region dictionary
    sub_regions = list(loc_data['Sub-region Name'].dropna().unique())

    for i in sub_regions:
        new_df = loc_data.loc[loc_data['Sub-region Name'] == i]
        region = list(new_df['Region Name'])[0]
        region_dict.update({i: region})
      
    # Construct country dictionary
    for i in range(m):
        country_dict.update({loc_data['Country or Area'][i]:[loc_data['Sub-region Name'][i], loc_data['Region Name'][i]]})
    
    # Build income dictionary from World Bank database
    p = len(income_data)

    # Initialize dictionary
    income_dict = {}
    
    # Build income dictionary
    for i in range(p):
        income_dict.update({income_data['Code'][i]: income_data['Income group'][i]})
        
    return(continent_list, region_dict, country_dict, income_dict)


def loc_hier(file, UN_data, continent_list, region_dict, country_dict, income_dict):
    '''Defn: Search text file to determine location(s). If country or region specified in text, 
            function will automatically infer corresponding higher level locations
            (i.e. country will populate corresponding region and continent). 
            Will also generate country code (for ID purposes) based on most populous country, region, or continent
            Will also generate the income-level of country based on income_hierarchy_dict as defined by World Bank
       Input: file: contents of text file (file should be in read mode)
              UN_data: country data from UN statistics division
              continent_list: list of continents (generated by loc_dict_creator
              region_dict: dictionary mapping region to continent (generated by loc_dict_creator)
              country_dict: dictionary mapping country to region and continent (generated by loc_dict_creator)
              income_hierarchy_dict: a dictionary that breaks countries into high, upper middle, lower middle, and lower economies based on World Bank data
       Output: Dictionary with country, region, continent, income level of country/ies, country code of most frequent country/region/continent'''
    
    file_read = file
      
    # dictionary of alpha codes for sub-regions and continents (user-defined)
    sub_alpha_codes = {'Australia and New Zealand': 'ANZ', 'Central Asia': 'CAS', 'Eastern Asia': 'EAS', 'Eastern Europe': 'EEU',
                       'Latin America and the Caribbean': 'LAC', 'Melanesia': 'MEL', 'Micronesia': 'MIC', 'Northern Africa': 'NAF',
                       'Northern America': 'NOA', 'Northern Europe': 'NEU', 'Polynesia': 'POY', 'South-eastern Asia': 'SEA',
                       'Southern Asia': 'SAS', 'Southern Europe': 'SEU', 'Sub-Saharan Africa': 'SSA', 'Western Asia': 'WAS', 'Western Europe': 'WEU'}
    contin_alpha_codes = {'Americas': 'AME', 'Africa': 'AFR', 'Asia': 'ASI', 'Oceania': 'OCE', 'Europe': 'EUR'}
    
    temp = {'country': [], 'region': [], 'continent': []}
        
    country = country_dict.keys()
    region = region_dict.keys()    
    
    for i in country:
        vals = country_dict.get(i)
        if i in file_read and i not in temp['country']:
            temp['country'].append(i)
        if i in file_read and vals[0] not in temp['region']:
            temp['region'].append(vals[0])
        if i in file_read and vals[1] not in temp['continent']:
                temp['continent'].append(vals[1])

    for j in region:
        val = region_dict.get(j)
        if j in file_read and j not in temp['region']:
            temp['region'].append(j)
        if j in file_read and val not in temp['continent']:
            temp['continent'].append(val)
    
    for k in continent_list:
        if k in file_read and k not in temp['continent']:
            temp['continent'].append(k)
    
    if not temp['country'] and not temp['region'] and not temp['continent']:
        temp['country'].append('all')
        temp['region'].append('all')
        temp['continent'].append('all')
    
    if not temp['country']:
        temp['country'].append(None)
    
    if not temp['region']:
        temp['region'].append(None)
        
                 
    # Find country mentioned the most in text to use as country code
    if temp['country'] == ['all'] and temp['region'] == ['all'] and temp['continent'] == ['all']:
        code = '999'

    elif None in temp['country'] and None in temp['region']:
        country_list = temp['continent']
        count_2 = 0
            
        for i in country_list:
            count_1 = 0
            count_1 += file_read.count(i)
            if count_1 > count_2:
                count_2 = count_1
                main_continent = i
            
        code = contin_alpha_codes[main_continent]
            
    elif None in temp['country']:
        country_list = temp['region']
        count_2 = 0

        for i in country_list:
            count_1 = 0
            count_1 += file_read.count(i)
            if count_1 > count_2:
                count_2 = count_1
                main_region = i

        code = sub_alpha_codes[main_region]

    else:
        country_list = temp['country']
        count_2 = 0

        for i in country_list:
            count_1 = 0
            count_1 += file_read.count(i)
            if count_1 > count_2:
                count_2 = count_1
                main_country = i

        code = UN_data.loc[UN_data['Country or Area'] == main_country]['ISO-alpha3 Code'].values[0]
    
    # Find income levels of countries in temp
    if code in income_dict: 
        income_level_temp = income_dict[code]
        if income_level_temp == 'Low income':
            income_level = 'LO'
        elif income_level_temp == 'Lower middle income':
            income_level = 'LM'
        elif income_level_temp == 'Upper middle income':
            income_level = 'UM'
        elif income_level_temp == 'High income':
            income_level = 'H'
        else:
            income_level = 'none'
    else:
        income_level = 'none'
             
    return temp, income_level, code

def topic_id(file):
    '''Defn: Search through text file to determine topic(s). Uses list of related terms to determine topic
       Input: file: contents of text file (file should be in read mode)
       Output: List with topic(s) for file'''

    ## Working list of terms to help categorize reports.
    water_terms = ['water', 'WASH', 'sanitation', 'hygiene'] # drinking, thirsty
    ag_terms = ['irrigation', 'crop', 'agriculture', 'farm', 'farmer', 'yield', 'harvest'] # hunger, food, security
    ###
    
    file_read = file

    wat_len = len(water_terms)
    ag_len = len(ag_terms)
    temp = []

    for k in range(wat_len):
        if (water_terms[k] in file_read) & ('water' not in temp):
            temp.append('water')
    for m in range(ag_len):
        if (ag_terms[m] in file_read) & ('ag' not in temp):
            temp.append('ag')
    if not temp:
        temp.append('none')
         
    return temp

def urban_rural(file):
    '''Defn: Search through text file to determine whether project is in an urban or rural setting. 
       Input: file: contents of text file (file should be in read mode) 
       Output: List with urban/rural/na for file'''
    
    file_read = file
    temp = []
        
    if ('urban' in file_read): 
        temp.append('urban')
    if ('rural' in file_read):
        temp.append('rural')
    if not temp:
        temp.append('none')
        
    return temp


# In[78]:


## Convert folder of PDF files to text

# PDF to TXT Files 
#converts pdf, returns its text content as a string
def convert(filenames, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(filenames, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close    
        
    return(text)

def pdf_converter(filenames):
    '''Description: Reads through list of PDF files and converts each to txt file
    Input: list of PDF files
    Output: .txt file for each document'''
    n = 0    
    for file in filenames:
        print(file)
        text = []
        raw_text = convert(file)
        text_by_page = raw_text.split("\n\n\x0c") # Split text on new page delimiter
        num_pages = len(text_by_page)-1
        
        for i in range(num_pages):
            #text_by_page[i] = text_by_page[i].replace('\n', '').replace('\n', '')
            text_by_page[i] = text_by_page[i].replace('\n', '') # new line
            text_by_page[i] = text_by_page[i].replace('\t', ' ') # tab
            text_by_page[i] = text_by_page[i].replace("'", "") # delete all '
            text_by_page[i] = text_by_page[i].replace('"', '') # delete all "
            #text_by_page[i] = text_by_page[i].strip(" ") 
            text_by_page[i] = text_by_page[i].replace("  ", " ") # double space
        
        text.append(text_by_page) 
        flat_text = [item for sublist in text for item in sublist]
        
        # Write to .txt file
        f = open('3' + '%s' %n + '.txt', 'w+') # 1 - engineer, 2 - funder, 3 - gov, 4 - ngo, 5 - recipient
        f.writelines(flat_text)
        n +=1
        
    return('done')


# In[133]:


# Rename elements of files in folder
# Note: this will permanently change file names, make copy if you'd like to keep original naming
def rename(folder, file_names):
    #folder = "/Users/klschre2/Desktop/gov_test/"
    data_folder = Path(folder)
    file_path= sorted(data_folder.glob('*.txt'))

    # Get names of files from user-generated text file
    file_list = open(file_names, 'r')
    names = file_list.read().split('\n')

    # Loop through path objects to get list of file paths
    filenames = []
    for path in file_path:
        filenames.append(str(path))

    for i in range(len(filenames)):
        os.rename(filenames[i], folder + 'SDG_' + names[i])


# In[134]:
