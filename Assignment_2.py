# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 22:24:00 2019

@author: M.Hamza Ashraf
"""

#python "E:\FAST\7th_Semester\Information Retrieval\Assignments\Assignment_2\Assignment_2.py" --score dirichlet
#python "E:\FAST\7th_Semester\Information Retrieval\Assignments\Assignment_2\Assignment_2.py" --score okapi
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer
from bs4 import BeautifulSoup
import sys

import time
import math
start_time = time.time()

#scoring_function = sys.argv[2]
scoring_function = "dirichlet"

dirichlet = 0
okapi = 0
if(scoring_function == "dirichlet"):
    dirichlet = 1
elif(scoring_function == "okapi"):
    okapi = 1

word_count = 0
doc_count = 0
mu = 0
query = 0

doc_len_dict = {}
tokens_dict = {}
termdict = {}

q_id = {}
doc_dict = {}
occurrence_dict = {}
doc_occurrence_dict = {}
total_occurrence_dict = {}
query_word_occ_dict = {}
relevance_dict = {}

new_tokens=[]
#unique_list = []

templ = []
templ1 = []
final=""
stemmer = SnowballStemmer('english')
tk = RegexpTokenizer("[\w']+") 

#arg=r"E:\FAST\7th_Semester\Information Retrieval\Assgnments\Assgnment_2\topics.xml"
#arg=sys.argv[1]
outputf = open(r"E:\FAST\7th_Semester\Information Retrieval\Assignments\Assignment_2\output_ranking_dirichlet.txt", "w")
outputff = open(r"E:\FAST\7th_Semester\Information Retrieval\Assignments\Assignment_2\output_ranking_BM25.txt", "w")
docf = open(r"E:\FAST\7th_Semester\Information Retrieval\Assignments\Assignment_1\docids.txt","r")
termf = open(r"E:\FAST\7th_Semester\Information Retrieval\Assignments\Assignment_1\termids.txt","r")
topicf = open(r"E:\FAST\7th_Semester\Information Retrieval\Assignments\Assignment_2\topics.xml","r")
indexf = open(r"E:\FAST\7th_Semester\Information Retrieval\Assignments\Assignment_1\term_index.txt","r")
relevancef = open(r"E:\FAST\7th_Semester\Information Retrieval\Assignments\Assignment_2\relevance judgements.qrel","r")

StopList = [line.rstrip('\n') for line in open(r"E:\FAST\7th_Semester\Information Retrieval\Assignments\Assignment_1\stoplist.txt").readlines()]
s=set(StopList)

soup = BeautifulSoup(topicf.read(), "html.parser")
lines = indexf.readlines()
liness = docf.readlines()
linesss = termf.readlines()
relevance_doc = relevancef.readlines()

for ext in soup(["script", "style"]):
    ext.extract()
    
#print(soup.find('topic').attrs)

for a in soup.find_all('topic'):
    if (soup.find_all('topic')) is not None:
        rows = a.attrs['number']
    else:
        rows = ''        
    tokens_dict.update({int(rows):[]})

rows =""    

for a,b in zip(soup.find_all('query'), tokens_dict):
    if (soup.find_all('query')) is not None:
        rows = a.text
        templ = rows.split()
        
        for c in templ:
            templ1 = [tok.lower() for tok in templ if tok.isalpha()]
        tokens_dict[b] = templ1        
    else:
        rows = ''        
    #final = final + rows + ' '
temp =[]
rel_list=[]
curr = 0

for i in relevance_doc:
    prev = curr
    thisline = i.split(" ")
    curr = thisline[0]
    
    if(prev != curr):
        rel_list=[]
        relevance_dict.update({curr:[]})
        temp.append(thisline[0])
        temp.append(thisline[2])
        temp.append(thisline[3])
        rel_list.append(temp)
        temp =[]
    else:
        temp.append(thisline[0])
        temp.append(thisline[2])
        temp.append(thisline[3])
        rel_list.append(temp)
        relevance_dict[curr] = rel_list
        temp =[]
    
    

for i in linesss:
    thisline = i.split("\t")
    termdict.update({thisline[1]:thisline[0]})

for a,b in zip(tokens_dict, linesss):
    thisline = b.split("\t")
    k = 0
    
    for c in tokens_dict[a]:
        if tokens_dict[a][k] not in s:
            word = stemmer.stem(tokens_dict[a][k]) + "\n"
            termid = termdict.get(word)
            new_tokens.append(stemmer.stem(tokens_dict[a][k]) + "," + termid)
            q_id.update({termid:0})
        k = k + 1
    tokens_dict[a] = new_tokens
    new_tokens = []
        
#Till here, QUERY TOKENIZATION IS DONE

for b in liness:
    doc_count = doc_count + 1
    thisline = b.split()
    doc_dict.update({doc_count:thisline[1]})

loop = 0
for a in lines:
    thisline = a.split(" ")
    word_count = word_count + int(thisline[1])
    total_occurrence_dict.update({thisline[0] : thisline[1]})
    doc_occurrence_dict.update({int(thisline[0]):thisline[2]})
    loop = int(thisline[1])
    term_id = thisline[0]
    temp=""
    q_word_flag = 0
    x = 0
    count = 0
    occ = 0
    index = 0
    
    if(term_id in q_id.keys()):
        q_word_flag = 1
    else:
        q_word_flag = 0
    
    for x in range(loop):  
        temp = thisline[3 + x]
        temp = temp.split(",")
        curr = int(temp[0])

        index = index + curr
        
        if(q_word_flag == 1):
            if(curr!=0):
                if index not in occurrence_dict.keys():
                    occurrence_dict.update({index : {term_id:1}})
                elif term_id not in (occurrence_dict[index].keys()):
                    occurrence_dict[index].update({term_id:1})
                else:
                    occurrence_dict[index][term_id] = occurrence_dict[index][term_id] + 1
                
            else:
                occurrence_dict[index][term_id] = occurrence_dict[index][term_id] + 1
        
        if(curr!=0):
            
            if index not in doc_len_dict.keys():
                doc_len_dict.update({index : count + 1})
            else:
                doc_len_dict[index] = doc_len_dict[index] + 1
            
        else:
            doc_len_dict[index] = doc_len_dict[index] + 1
        
    #print(temp[0])
count = 0

for j in doc_len_dict:
    count = count + doc_len_dict[j]

mu = word_count / doc_count
#Till here, Average Doc length has been calculated and Doc length

for a,b in tokens_dict.items():
    for c in (range(len(b))):
        termid = (b[c].split(","))[1]
        query_word_occ_dict.update({termid:b.count(b[c])})


answers_dict = {}
temp_list = []
ans_list = []
temp = {}
occ = 0
ans =1

answers_dict_BM25 = {}
temp_list1 = []
ans_list1 = []
k1 = 1.2
k2 = 800
b_val = 0.75
D = doc_count
ans1 = 0

for b,c in tokens_dict.items():
    for a in (range(doc_count)):
        for d in (range(len(c))):

            termid = (c[d].split(","))[1]

            try:
                temp = occurrence_dict.get(a + 1)
          
                occ = temp.get(termid)
            
            except AttributeError:
                if(temp is None):
                    occ = 0
                
            if(occ is None):
                occ = 0
            
            if((a+1) in doc_len_dict.keys()):
                
                val1 = ((doc_len_dict[a + 1])/(doc_len_dict[a + 1] + mu))
                val2 = ((mu)/(doc_len_dict[a + 1] + mu))
                prob1 = (occ / doc_len_dict[a + 1])
                prob2 = (loop / word_count)
                
                val11 = (math.log(D + 0.5) / (int(doc_occurrence_dict.get(int(termid))) + 0.5))
                K  = ((b_val*((doc_len_dict[a + 1])/mu)) + (1 - b_val)) * k1
                val22 = ((1 + k1)*(occ))/ (K + occ)
                val33 = ((1 + k2) * query_word_occ_dict.get(termid)) / (k2 + query_word_occ_dict.get(termid))
                
    
                ans = ans * ((val1*prob1) + (val2*prob2))
                ans1 = ans1 + (val11 * val22 * val33)    
            
            #break
        if(ans !=1):
            temp_list.append(str(b))
            temp_list.append(doc_dict.get(a + 1))
            temp_list.append(ans)
            temp_list.append("run 1")
            ans_list.append(temp_list)
            
            
        
        if(ans1 !=0):
            temp_list1.append(str(b))
            temp_list1.append(doc_dict.get(a + 1))
            temp_list1.append(ans1)
            temp_list1.append("run 1")
            ans_list1.append(temp_list1)
            
        ans = 1
        ans1 = 0
        temp_list = []
        temp_list1 = []
        #break
    ans_list.sort(key = lambda x: (x[2]), reverse = True)    
    ans_list1.sort(key = lambda x: (x[2]), reverse = True)    
    answers_dict.update({b:ans_list})
    answers_dict_BM25.update({b:ans_list1})
    ans_list = []
    ans_list1 = []
    
    #answers.append(ans_list)
    #break
    
    
for a,b in answers_dict.items():
    rank = 1
    rank1 = 1
    for c in b:
        
        if(dirichlet == 1):
            print(str(c[0]) + "\t\t" + str(c[1]) + "\t\t" + str(rank1) + "\t\t" + str(c[2]) + "\t\t" + str(c[3]))
            rank1 = rank1 + 1
            print("\n")
        
        #rank = 1
        outputf.write(str(c[0]) + "\t\t")
        outputf.write(str(c[1]) + "\t\t")
        outputf.write(str(rank) + "\t\t")
        outputf.write(str(c[2]) + "\t\t")
        outputf.write(str(c[3]) + "\t\t")
        rank = rank + 1
        outputf.write("\n")


for a,b in answers_dict_BM25.items():
    rank = 1
    rank1 = 1
    for c in b:
        
        if(okapi == 1):
            print(str(c[0]) + "\t\t" + str(c[1]) + "\t\t" + str(rank1) + "\t\t" + str(c[2]) + "\t\t" + str(c[3]))
            rank1 = rank1 + 1
            print("\n")
        
        #rank = 1
        
        outputff.write(str(c[0]) + "\t\t")
        outputff.write(str(c[1]) + "\t\t")
        outputff.write(str(rank) + "\t\t")
        outputff.write(str(c[2]) + "\t\t")
        outputff.write(str(c[3]) + "\t\t")
        rank = rank + 1
        outputff.write("\n")


inputf = open(r"E:\FAST\7th_Semester\Information Retrieval\Assignments\Assignment_2\output_ranking_dirichlet.txt", "r")
inputff = open(r"E:\FAST\7th_Semester\Information Retrieval\Assignments\Assignment_2\output_ranking_BM25.txt", "r")


line = inputf.readlines()
line1 = inputff.readlines()
relevant_docs_retrieved = {}
temp = []

for i in line:
    thisline = i.split("\t\t")
    if thisline[0] not in relevant_docs_retrieved.keys():
        temp = []
        temp.append(thisline[1])
        relevant_docs_retrieved.update({thisline[0]:temp})
        
    else:
        temp.append(thisline[1])
        relevant_docs_retrieved[thisline[0]] = temp
        

relevant_docs_retrieved_BM25 = {}
temp = []

for i in line1:
    thisline = i.split("\t\t")
    if thisline[0] not in relevant_docs_retrieved_BM25.keys():
        temp = []
        temp.append(thisline[1])
        relevant_docs_retrieved_BM25.update({thisline[0]:temp})
        
    else:
        temp.append(thisline[1])
        relevant_docs_retrieved_BM25[thisline[0]] = temp

temp =[]
only_relevant_doc_dict = {}
for a,b in relevance_dict.items():
    for c in b:
        if(int(c[2]) > 0):
            temp.append(c)
    only_relevant_doc_dict.update({a:temp})
    temp = []
    

total_relevant_docs = 0
for a,b in only_relevant_doc_dict.items():
    total_relevant_docs = total_relevant_docs + len(b)

total_queries = len(only_relevant_doc_dict)

p5 = 0
p10 = 0
p20 = 0
p30 = 0
count = 0
p_at_dict = {}
avg_precision_query_dirichlet = {}
temp1=[]
rel_docs_retr = 0 
curr_doc = ""
sum_preciisons = 0
MAP_dirichlet = 0 
for a,b in relevant_docs_retrieved.items():
    for i in range(len(b)):
        curr_doc = b[i]
    
        temp = only_relevant_doc_dict.get(a)
        for j in range(len(temp)):
            if(curr_doc in temp[j]):
                rel_docs_retr = rel_docs_retr + 1
                sum_preciisons = sum_preciisons + (rel_docs_retr / (i + 1))
        
        if(i == 4):
            p5 = rel_docs_retr / 5
            temp1.append(p5)
        if(i == 9):
            p10 = rel_docs_retr / 10
            temp1.append(p10)
        if(i == 19):
            p20 = rel_docs_retr / 20
            temp1.append(p20)
        if(i == 29):
            p30 = rel_docs_retr / 30
            temp1.append(p30)
    
    rel_docs_retr = 0
    avg_precision_query_dirichlet.update({a:(sum_preciisons / len(temp))})
    sum_preciisons = 0
    p_at_dict.update({a:temp1})
    temp1 = []

p5 = 0
p10 = 0
p20 = 0
p30 = 0
count = 0
p_at_dict_BM25 = {}
avg_precision_query_BM25 = {}
temp1=[]
rel_docs_retr = 0 
curr_doc = ""
sum_preciisons = 0
MAP_BM25 = 0 
for a,b in relevant_docs_retrieved_BM25.items():
    for i in range(len(b)):
        curr_doc = b[i]
    
        temp = only_relevant_doc_dict.get(a)
        for j in range(len(temp)):
            if(curr_doc in temp[j]):
                rel_docs_retr = rel_docs_retr + 1
                sum_preciisons = sum_preciisons + (rel_docs_retr / (i + 1))
        
        if(i == 4):
            p5 = rel_docs_retr / 5
            temp1.append(p5)
        if(i == 9):
            p10 = rel_docs_retr / 10
            temp1.append(p10)
        if(i == 19):
            p20 = rel_docs_retr / 20
            temp1.append(p20)
        if(i == 29):
            p30 = rel_docs_retr / 30
            temp1.append(p30)
    
    rel_docs_retr = 0
    p_at_dict_BM25.update({a:temp1})
    avg_precision_query_BM25.update({a:(sum_preciisons / len(temp))})
    sum_preciisons = 0
    temp1 = []

sum = 0
for a,b in avg_precision_query_dirichlet.items():
    sum  = sum + b
MAP_dirichlet =   (sum / (total_queries))
print("MAP Dirichlet " + str(MAP_dirichlet))

sum = 0
for a,b in avg_precision_query_BM25.items():
    sum =  sum + b
   
MAP_BM25 =   (sum / (total_queries))
print("MAP Okapi BM25 " + str(MAP_BM25))

#print("--- %s seconds ---" % (time.time() - start_time))
docf.close()
termf.close()
topicf.close()
indexf.close()
outputf.close()
outputff.close()
inputf.close()
inputff.close()