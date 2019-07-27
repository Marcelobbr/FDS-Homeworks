#!/usr/bin/env python
# coding: utf-8

import sqlite3
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

class UpdateTools:
    def __init__(self):
        pass
    
    def update(self, papers_raw, initialize=True):
        if papers_raw is None: return
        
        ###################################################
        #                   PART 1
        ###################################################
        soup = BeautifulSoup(papers_raw, 'html.parser')
        soup.findAll("td", {"class": "gsc_a_t"})
    
        papers = []
        table = soup.find("table", id="gsc_a_t") 
        for tr in table.find_all('tr')[2:]:
            for td in tr.find_all("td", {"class": "gsc_a_t"}):
                paper = {}
                text = re.sub("'", "", tr.find("a", {"class": "gsc_a_at"}).get_text()).strip()
                paper['title'] = text
                authors = tr.find("div", {"class": "gs_gray"}).get_text().split(',')[:4]
                authors = [a.strip().upper() for a in authors] #remove espaçamento antes de alguns nomes e resolve case sensitiveness
                paper['authors'] = authors
                papers.append(paper)
        papers = papers[:10] #CHANGE BEFORE SUBMISSION
        print(papers)
    
        ###################################################
        #                   PART 2
        ###################################################
        # ### AUTHORS # ###
        author_paper = pd.DataFrame(papers, columns=['title', 'authors'])
    
        authors_table = author_paper.authors.apply(pd.Series).stack(dropna=True).reset_index(drop=True)
        authors_table = pd.DataFrame(authors_table)[0].apply(lambda x: x.strip()).unique()
        authors_table = pd.DataFrame(authors_table, columns=['author'])
        authors_table = authors_table.sort_values('author')
        authors_table = authors_table.reset_index().drop('index', axis=1)
    
        # ### PAPERS # ###
        #papers_table = author_paper['title'] # old style
        papers_table = author_paper['title'].apply(pd.Series).reset_index(drop=True)
        papers_table = papers_table.rename(columns={0: 'title'})
        #papers_table.head()
    
        # ### SQL # ###
        sql_db = 'hw1.sqlite'
        conn = sqlite3.connect(sql_db, isolation_level=None)
        cur = conn.cursor()
        
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables_list = cur.fetchall()  
        print("\nTABLES_LIST:", tables_list, "\n")
        
        #this function builds new tables (only used once during initialization)
        def build_sql_table(dataframe, table_name):  
            dataframe.to_sql(table_name, conn, index_label = "id", if_exists="replace")
            print('Table',table_name, 'was created on database', sql_db)
            
        #this function checks tables and inserts new data corresponding to user queries
        def insert_data(table, column, df_table): 
            cur.execute("SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(table))
            new_id = cur.fetchone()[0] + 1
        
            count = 1
            for index, row in df_table.iterrows():
                cur.execute("SELECT EXISTS(SELECT * FROM {} WHERE {} = '{}')".format(table, column, row[0]))
                is_name = cur.fetchone()[0]
                if is_name == 0: 
                    new_id += 1
                    cur.execute("INSERT INTO {} VALUES ({}, '{}')".format(table, new_id,row[0]))
                    count += 1
                    
        #cur.execute('''CREATE TABLE IF NOT EXISTS author_paper 
        #               (title_id INT, author_id INT)
        #               ;''')
        
        if initialize == True:
            cur.execute("DROP TABLE IF EXISTS author_paper")
            cur.execute('''CREATE TABLE author_paper 
                       (title_id INT, author_id INT)
                       ;''')
            build_sql_table(authors_table, 'authors')
            build_sql_table(papers_table, 'papers')

        if initialize == False:
            insert_data("authors", "author", authors_table)
            insert_data("papers", "title", papers_table)
            
        # ### AUTHOR PAPER - SQL INSERTIONS # ###
        author_paper_table = author_paper.authors.apply(pd.Series) \
            .merge(author_paper, left_index = True, right_index = True) \
            .drop(["authors"], axis = 1) \
            .melt(id_vars = ['title'], value_name = "author") \
            .drop("variable", axis = 1) \
            .dropna()
        
        #remove espaçamento nos nomes, se houver
        #author_paper_table = pd.DataFrame(author_paper_table.author.apply(lambda x: x.strip())) \
        #    .merge(author_paper_table[['title']], left_index = True, right_index = True)
    
        for index, row in author_paper_table.iterrows():
            title = row[0] #TEM QUE TROCAR CASO REMOVA ESPAÇAMENTO
            author = row[1] #TEM QUE TROCAR CASO REMOVA ESPAÇAMENTO
    
            query = 'SELECT id FROM papers WHERE title = "{}"'.format(title)
            cur.execute(query)
            title_id = cur.fetchone()[0]
            query = 'SELECT id FROM authors WHERE author = "{}"'.format(author)
            cur.execute(query)
            author_id = cur.fetchone()[0]
    
            query = "INSERT INTO author_paper VALUES ({}, {})".format(title_id,author_id)
            cur.execute(query)
            conn.commit()
            
        # # build networks
        # ### authors
    
        def plot_networks(table, aggregator, grouped_id):
            G=nx.Graph()
            df = pd.read_sql_query('SELECT * FROM {}'.format(table),conn)
            labels={}
            for index,row in df.iterrows():
                G.add_node(row[0])
                labels[row[0]]=row[1]
        
            author_paper = pd.read_sql_query('SELECT * FROM author_paper',conn)
            author_paper = author_paper.sort_values(by='title_id')
        
            graph = list(author_paper.groupby([aggregator])[grouped_id].apply(list))
            for group in graph:
                if len(group)<2: continue
                for i in range(0,len(group)-1):
                    for j in range(i+1,len(group)):
                        G.add_edge(group[i],group[j])
        
            pos=nx.spring_layout(G, k=0.2, weight=1, iterations=50)
            plt.figure(3,figsize=(12,12)) 
            nx.draw_networkx(G, pos, labels=labels, alpha=0.7)
            plt.axis('off')
            file = "static/{}_graph.png".format(table)
            plt.savefig(file)
        plot_networks('authors', 'title_id', 'author_id')
        plot_networks('papers', 'author_id', 'title_id')