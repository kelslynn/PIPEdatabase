from pathlib import Path
import pandas as pd
import tkinter as tk
import os
import shutil
from phrase_mining import *

# Database file
df = pd.read_csv('../PIPEdatabase_10292019.csv')

UN_data = pd.read_csv('../data/UNSD_methodology.csv')

# Search options:
# ^^ Stakeholder(stake)
# Stakeholder source (source)
# ^^ Document tone (tone) (formal, informal)
# Document type (doc) (blog, report, plan, etc.)
# ^^ Project continent (continent)
# ^^ Project region (region)
# Project country (code)
# ^^ Country income level (income)
# Urban or rural (u_r)
# Project document year (y)
# Project topic (topic) (ag, water, both)

def query_export(UN_data, stake = None, source= None, tone = None, doc= None, continent= None, region= None, code = None, income = None, u_r= None, y = None, topic= None):
    '''Defn: take user selections, search for matching items in PIPE database, and export dataframe of meta-data, folder of documents, and list of file names for matching documents
    input: UN_data: country data from UN statistics division
    stake: stakeholder selection(s)
    source: source selection(s)
    tone: document tone selection(s)
    doc: document type selection(s)
    continent: continent selection(s)
    region: region selection(s)
    code: country code selection(s)
    income: income classification selection(s)
    u_r: urban or rural selection
    y: year selection(s)
    topic: topic selection(s)
    output: dataframe of meta-data, folder of documents, and list of file names for matching documents'''
    df = pd.read_csv('../PIPEdatabase_10292019.csv')

    folder = '../all_text_files/'

    n = len(df)
    
    cont_list = []
    reg_list = []
    
    sub_alpha_codes = {'Australia and New Zealand': 'ANZ', 'Central Asia': 'CAS', 'Eastern Asia': 'EAS', 'Eastern Europe': 'EEU',
                       'Latin America and the Caribbean': 'LAC', 'Melanesia': 'MEL', 'Micronesia': 'MIC', 'Northern Africa': 'NAF',
                       'Northern America': 'NOA', 'Northern Europe': 'NEU', 'Polynesia': 'POY', 'South-eastern Asia': 'SEA',
                       'Southern Asia': 'SAS', 'Southern Europe': 'SEU', 'Sub-Saharan Africa': 'SSA', 'Western Asia': 'WAS', 'Western Europe': 'WEU'}
    sub_to_cont_codes = {'ANZ': 'OCE', 'CAS': 'AME', 'EAS': 'ASI', 'EEU': 'EUR', 'LAC': 'AME', 'MEL': 'OCE', 'MIC': 'OCE',
                         'NAF': 'AFR', 'NOA': 'AME', 'NEU': 'EUR', 'POY': 'OCE', 'SEA': 'ASI', 'SAS': 'ASI', 'SEU': 'EUR',
                         'SSA': 'AFR', 'WAS': 'ASI', 'WEU': 'EUR'}
    contin_alpha_codes = {'Americas': 'AME', 'Africa': 'AFR', 'Asia': 'ASI', 'Oceania': 'OCE', 'Europe': 'EUR'}
    
    for i in range(n):

        if df['country_code'][i] == '999':
            cont_list.append('all')
            reg_list.append('all')
        elif df['country_code'][i] in sub_alpha_codes.values():
            reg_list.append(list(sub_alpha_codes.keys())[list(sub_alpha_codes.values()).index(df['country_code'][i])])
            cont_list.append(sub_to_cont_codes[df['country_code'][i]])
        elif df['country_code'][i] in contin_alpha_codes.values():
            cont_list.append(list(contin_alpha_codes.keys())[list(contin_alpha_codes.values()).index(df['country_code'][i])])
            reg_list.append('none')
        else:
            cont_list.append(UN_data.loc[UN_data['ISO-alpha3 Code'] == df['country_code'][i]]['Region Name'].values[0])
            reg_list.append(UN_data.loc[UN_data['ISO-alpha3 Code'] == df['country_code'][i]]['Sub-region Name'].values[0])

    df['continent_main'] = cont_list
    df['region_main'] = reg_list

    if stake != None:
        stake_reg = '|'.join(stake)
        df = df.loc[df['stakeholder'].str.contains(stake_reg)]
        
    if source != None:
        source_reg = '|'.join(source)
        df = df[df['source_ID'].str.contains(source_reg)]
    
    if tone != None:
        tone_reg = '|'.join(tone)
        df = df.loc[df['doc_tone'].str.contains(tone_reg)] 
    
    if doc != None:
        doc_reg = '|'.join(doc)
        df = df.loc[df['doc_type'].str.contains(doc_reg)]
        
    if continent != None:
        cont_reg = '|'.join(continent)
        df = df[df['continent_main'].str.contains(cont_reg)]

    if region != None:
        region_reg = '|'.join(region)
        df = df[df['region_main'].str.contains(region_reg)]
        
    if code != None:
        code_reg = '|'.join(code)
        df = df.loc[df['country_code'].str.contains(code_reg, na=False)]
        
    if income != None:
        income_reg = '|'.join(income)
        df = df[df['income_level'].str.contains(income_reg)]
        
    if u_r != None:
        u_r_reg = '|'.join(u_r)
        df = df[df['urban_rural'].str.contains(u_r_reg)]
        
    if y != None:
        df = df.loc[df['year'].isin(y)]
        
    if topic != None:
        topic_reg = '|'.join(topic)
        df = df[df['topic_ID'].str.contains(topic_reg)]
    
    df.to_csv('../output/PIPEQueryOutput.csv')

    # create folder to save output
    #path = "../output/PIPE_doc_output"
    #os.mkdir(path)

    path = "../output/PIPE_doc_output"
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    # locate and save text files to folder
    index = df.index
    file_list = []
    
    for i in index:
        file = df['ID'][i]
        file_list.append(file)
        f = open(folder + file + '.txt', 'r+', encoding = 'utf-8')
        content = f.read()
        f_new = open(path + '/' + file + '.txt', 'w', encoding = 'utf-8')
        f_new.write(content)
        f_new.close()
        f.close()

    with open('./text inputs/file_list.txt', 'w') as outfile:
        for fname in file_list:
            outfile.write(str(fname) + '\n')

    return df


def text_to_string(text_file):
    '''Defn: read through text file and convert each line to a string separated by a comma
    Input: text_file: contents of text file (file should be in read mode)
    Output: flattened list of text separated by a comma'''
    file = open(text_file, 'r')
    string = [line.split(',') for line in file.readlines()] 
    flatten = [item.rstrip() for sublist in string for item in sublist]
    return(flatten)

def lister(entry, parent_list):
    '''Defn: take entries from user selections, returned as position within options, and map back to text of selection
    Input: entry: list of entry positions selected by user
    parent_list: list of all entry options
    Output: list of entries in their original text format'''
    n = len(entry)
    entries = []
    for i in range(n):
        entries.append(parent_list[entry[i]])
    
    return entries

def export_data(*args):
    '''Defn: generate selection options for search of PIPE database and print number of matched entries
    '''
    #global result

    # Get entry data
    stakeholder = Lb1.curselection()
    source = Lb2.curselection()
    continent = Lb3.curselection()
    region = Lb4.curselection()
    country = Lb5.curselection()
    #code = Lb12.curselection()
    income = Lb6.curselection()
    urb_rur = Lb7.curselection()
    tone = Lb8.curselection()
    doc_type = Lb9.curselection()
    year = Lb10.curselection()
    topic = Lb11.curselection()

    # Create list of items to search from entry data

    stake_list = lister(stakeholder, stake_all)
    if len(stake_list) == 0:
        stake_list = None

    source_list = lister(source, source_all)
    if len(source_list) == 0:
        source_list = None

    continent_list = lister(continent, continent_all)
    if len(continent_list) == 0:
        continent_list = None

    region_list = lister(region, region_all)
    if len(region_list) == 0:
        region_list = None

    country_list = lister(country, code_all)
    if len(country_list) == 0:
        country_list = None

    code_list = lister(code, code_all)
    if len(code_list) == 0:
        code_list = None

    income_list = lister(income, income_all)
    if len(income_list) == 0:
        income_list = None

    urb_rur_list = lister(urb_rur, urbrur_all)
    if len(urb_rur_list) == 0:
        urb_rur_list = None

    tone_list = lister(tone, tone_all)
    if len(tone_list) == 0:
        tone_list = None

    type_list = lister(doc_type, type_all)
    if len(type_list) == 0:
        type_list = None

    year_list = lister(year, year_all)
    if len(year_list) == 0:
        year_list = None

    topic_list = lister(topic, topic_all)
    if len(topic_list) == 0:
        topic_list = None

    # Run the search and export data
    df_new = query_export(UN_data, stake = stake_list, source = source_list, tone = tone_list, doc = type_list, continent = continent_list, region = region_list, code = country_list, income = income_list, u_r = urb_rur_list, y = year_list, topic = topic_list)
    n = df_new.shape

    print("New search for %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, found %i entries" % (stake_list, source_list, tone_list, type_list, continent_list, region_list, country_list, income_list, urb_rur_list, year_list, topic_list, n[0]))
    print("Export complete")
    return()




def rep_phrase_search(*args):
    '''Defn: generate selection options for search of PIPE database, use query_export to search for selections, and run representative phrase mining on selected documents and return ranked phrases'''
    # Get entry data
    stakeholder = Lb1.curselection()
    source = Lb2.curselection()
    continent = Lb3.curselection()
    region = Lb4.curselection()
    country = Lb5.curselection()
    #code = Lb12.curselection()
    income = Lb6.curselection()
    urb_rur = Lb7.curselection()
    tone = Lb8.curselection()
    doc_type = Lb9.curselection()
    year = Lb10.curselection()
    topic = Lb11.curselection()

    # Create list of items to search from entry data

    stake_list = lister(stakeholder, stake_all)
    if len(stake_list) == 0:
        stake_list = None

    source_list = lister(source, source_all)
    if len(source_list) == 0:
        source_list = None

    continent_list = lister(continent, continent_all)
    if len(continent_list) == 0:
        continent_list = None

    region_list = lister(region, region_all)
    if len(region_list) == 0:
        region_list = None

    country_list = lister(country, code_all)
    if len(country_list) == 0:
        country_list = None

    income_list = lister(income, income_all)
    if len(income_list) == 0:
        income_list = None

    urb_rur_list = lister(urb_rur, urbrur_all)
    if len(urb_rur_list) == 0:
        urb_rur_list = None

    tone_list = lister(tone, tone_all)
    if len(tone_list) == 0:
        tone_list = None

    type_list = lister(doc_type, type_all)
    if len(type_list) == 0:
        type_list = None

    year_list = lister(year, year_all)
    if len(year_list) == 0:
        year_list = None

    topic_list = lister(topic, topic_all)
    if len(topic_list) == 0:
        topic_list = None

    # Run the search and export data
    df_new = query_export(UN_data, stake = stake_list, source = source_list, tone = tone_list, doc = type_list, continent = continent_list, region = region_list, code = country_list, income = income_list, u_r = urb_rur_list, y = year_list, topic = topic_list)
    n = df_new.shape

    print("===New search for %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, found %i entries===" % (stake_list, source_list, tone_list, type_list, continent_list, region_list, country_list, income_list, urb_rur_list, year_list, topic_list, n[0]))
    print("===Beginning Representative Phrase Mining ===")
    
    rep_phrase_mining('./text inputs/file_list.txt')

    return()

########
ht = 700
wd = 800

root = tk.Tk()

canvas = tk.Canvas(root, height = ht, width = wd, bg = 'black')
canvas.pack()

frame = tk.Frame(root)
frame.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.8)


# Parent lists
stake_all = ['Engineer', 'Funder', 'Gov', 'NGO'] #['1', '2', '3', '4'] # 1 - Engineer, 2 - Funder, 3 - Gov, 4 - INGO
source_all = list(df.source_ID.unique())

continent_all = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania'] 
region_all = ['Northern Africa', 'Sub-Saharan Africa', 'Latin America and the Carribean', 'Northern America', 'Central Asia', 'Eastern Asia', 'South-eastern Asia', 'Southern Asia', 'Western Asia', 'Eastern Europe', 'Northern Europe', 'Southern Europe', 'Western Europe', 'Australia and New Zealand', 'Melanesia', 'Micronesia', 'Polynesia']
country_all = text_to_string('./text inputs/country_list.txt')
code_all = text_to_string('./text inputs/country_codes.txt')

income_all = ['LO', 'LM', 'UM', 'H']
urbrur_all = ['rural', 'urban']

tone_all = ['I', 'F']
type_all = ['IA', 'PR', 'SR', 'IS', 'PL', 'AR', 'CS', 'FG', 'PP', 'B', 'ST', 'AT']

#year_range_all = ['0', '1', '2', '3', '4']
num = list(range(2000, 2020, 1))
year_all = [str(i) for i in num]

topic_all = ['ag', 'water']


## 1. Stakeholder
label1 = tk.Label(frame, text = "Stakeholder")
label1.place(relx = 0, rely = 0)

Lb1 = tk.Listbox(frame, selectmode = 'multiple', exportselection = 0)
Lb1.insert(1, 'Engineer')
Lb1.insert(2, 'Funder')
Lb1.insert(3, 'Government')
Lb1.insert(4, 'INGO')
Lb1.place(relx = 0, rely = 0.05, relheight = 0.15)


# 2.Source
label2 = tk.Label(frame, text = 'Source')
label2.place(relx = 0, rely = 0.2)

Lb2 = tk.Listbox(frame, selectmode = 'multiple', exportselection = 0)
for i in range(len(source_all)):
    Lb2.insert(i+1, source_all[i])
Lb2.place(relx = 0, rely = 0.25, relheight = 0.25)


## Geography
# 3. Continent
label3 = tk.Label(frame, text = 'Continent')
label3.place(relx = 0.375, rely = 0)

Lb3 = tk.Listbox(frame, selectmode = 'multiple', exportselection = 0)
Lb3.insert(1, 'Africa')
Lb3.insert(2, 'Americas')
Lb3.insert(3, 'Asia')
Lb3.insert(4, 'Europe')
Lb3.insert(5, 'Oceania')
Lb3.place(relx = 0.375, rely = 0.05, relheight = 0.15)


# 4. Region
label4 = tk.Label(frame, text = 'Region')
label4.place(relx = 0.375, rely = 0.25)

Lb4 = tk.Listbox(frame, selectmode = 'multiple', exportselection = 0)
for i in range(len(region_all)):
    Lb4.insert(i+1, region_all[i])
Lb4.place(relx = 0.375, rely = 0.3, relheight = 0.2)


# 5. Country
label5 = tk.Label(frame, text = 'Country')
label5.place(relx = 0.375, rely = 0.55)

Lb5 = tk.Listbox(frame, selectmode = 'multiple', exportselection = 0)
for i in range(len(country_all)):
    Lb5.insert(i+1, country_all[i])
Lb5.place(relx = 0.375, rely = 0.6, relheight = 0.3)


# 6. Income level
label6 = tk.Label(frame, text = "Country income level")
label6.place(relx = 0.75, rely = 0)

Lb6 = tk.Listbox(frame, selectmode = 'multiple', exportselection = 0)
Lb6.insert(1, 'Low')
Lb6.insert(2, 'Lower middle')
Lb6.insert(3, 'Upper middle')
Lb6.insert(4, 'High')
Lb6.place(relx = 0.75, rely = 0.05, relheight = 0.15)


# 7. Urban/Rural
label7 = tk.Label(frame, text = 'Rural or urban project')
label7.place(relx = 0.75, rely = 0.2)

Lb7 = tk.Listbox(frame, selectmode = 'multiple', exportselection = 0)
Lb7.insert(1, 'Rural')
Lb7.insert(2, 'Urban')
Lb7.place(relx = 0.75, rely = 0.25, relheight = 0.1)

## 8. Document Tone
label8 = tk.Label(frame, text = "Document Tone")
label8.place(relx = 0.75, rely = 0.35)

Lb8 = tk.Listbox(frame, selectmode = 'multiple', exportselection = 0)
Lb8.insert(1, 'Informal')
Lb8.insert(2, 'Formal')
Lb8.place(relx = 0.75, rely = 0.4, relheight = 0.1)

# 9. Document type
label9 = tk.Label(frame, text = "Document Type")
label9.place(relx = 0.75, rely = 0.5)

Lb9 = tk.Listbox(frame, selectmode = 'multiple', exportselection = 0)
Lb9.insert(1, 'Internal assessment')
Lb9.insert(2, 'Project report')
Lb9.insert(3, 'Special report')
Lb9.insert(4, 'Impact study')
Lb9.insert(5, 'Plan')
Lb9.insert(6, 'Annual review')
Lb9.insert(7, 'Case study')
Lb9.insert(8, 'Focus group')
Lb9.insert(9, 'Project profile')
Lb9.insert(10, 'Blog')
Lb9.insert(11, 'Story')
Lb9.insert(12, 'Article')
Lb9.place(relx = 0.75, rely = 0.55, relheight = 0.25)

# 10. Year
label10 = tk.Label(frame, text = "Year(s)")
label10.place(relx = 0, rely = 0.7)

Lb10 = tk.Listbox(frame, selectmode = 'multiple', exportselection = 0)
for i in range(len(year_all)):
    Lb10.insert(i+1, year_all[i])
Lb10.place(relx = 0, rely = 0.75, relheight = 0.2)

# 11. Topic
label11 = tk.Label(frame, text = "Topic")
label11.place(relx = 0.75, rely = 0.8)

Lb11 = tk.Listbox(frame, selectmode = 'multiple', exportselection = 0)
Lb11.insert(1, 'Agriculture')
Lb11.insert(2, 'Water')
Lb11.place(relx = 0.75, rely = 0.85, relheight = 0.1)


# Generate button to export data to csv and content to folder
button1 = tk.Button(root, text ="Export csv and files", command = export_data)
button1.pack(side='left')


# Generate button to run representative phrase algorithm on data -- return list of top xx phrases
button2 = tk.Button(root, text ="Find representative phrases", command = rep_phrase_search)
button2.pack(side='right')

root.mainloop()
