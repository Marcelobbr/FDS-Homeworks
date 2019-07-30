#!/usr/bin/env python
# coding: utf-8

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

###################################################
#                   PART 2
###################################################
class UpdateTools:
    def __init__(self):
        pass
    
    def update(self, results_dict, initialize=True):
        if results_dict is None: return
                   
        #initialize sql db
        sql_db = 'hw1.sqlite'
        conn = sqlite3.connect(sql_db, isolation_level=None)
        cur = conn.cursor()
        
        if initialize == True:
            for table in ['authors', 'papers', 'author_paper']:
                cur.execute("DROP TABLE IF EXISTS {}".format(table))
            queries = '''
            CREATE TABLE papers (id INT PRIMARY KEY, title TEXT UNIQUE) ;
            CREATE TABLE authors (id INT PRIMARY KEY, author TEXT UNIQUE) ;
            CREATE TABLE author_paper (title_id INT, author_id INT,
            FOREIGN KEY(title_id) REFERENCES papers(id)
            FOREIGN KEY(author_id) REFERENCES authors(id)
            );'''
            cur.executescript(queries)
            # generate blank images
            graphic_tools().plot_networks('authors', 'title_id', 'author_id', conn)
            graphic_tools().plot_networks('papers', 'author_id', 'title_id', conn)
            return
        
        # ### AUTHORS # ###
        author_paper = pd.DataFrame(results_dict, columns=['title', 'authors'])
    
        authors_table = author_paper.authors.apply(pd.Series).stack(dropna=True).reset_index(drop=True)
        authors_table = pd.DataFrame(authors_table)[0].apply(lambda x: x.strip()).unique()
        authors_table = pd.DataFrame(authors_table, columns=['author'])
        authors_table = authors_table.sort_values('author')
        authors_table = authors_table.reset_index().drop('index', axis=1)
    
        # ### PAPERS # ###
        papers_table = author_paper['title'].apply(pd.Series).reset_index(drop=True)
        papers_table = papers_table.rename(columns={0: 'title'})
    
        # ### SQL # ###        
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables_list = cur.fetchall()  
        print("\nTABLES_LIST:", tables_list, "\n")
        
        #this function builds new tables if needed (only used once during initialization)
        def build_sql_table(dataframe, table_name):  
            dataframe.to_sql(table_name, conn, index_label = "id", if_exists="replace")
            print('Table',table_name, 'was created on database', sql_db)
            
        #this function checks tables and inserts new data corresponding to user queries
        def insert_data(table, column, df_table): 
            cur.execute("SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(table))
            try: new_id = cur.fetchone()[0] + 1
            except Exception as e:
                e = str(e)
                if "'NoneType' object is not subscriptable" in e:
                    new_id = 1
        
            count = 1
            for index, row in df_table.iterrows():
                cur.execute("SELECT EXISTS(SELECT * FROM {} WHERE {} = '{}')".format(table, column, row[0]))
                is_name = cur.fetchone()[0]
                if is_name == 0: 
                    new_id += 1
                    cur.execute("INSERT INTO {} VALUES ({}, '{}')".format(table, new_id,row[0]))
                    count += 1
        
        # ### AUTHORS AND PAPERS - SQL INSERTIONS # ###
        print("\nPOPULATE AUTHORS AND PAPERS TABLES\n")
        insert_data("authors", "author", authors_table)
        insert_data("papers", "title", papers_table)
            
        # ### AUTHOR_PAPER - SQL INSERTION # ###
        author_paper_table = author_paper.authors.apply(pd.Series) \
            .merge(author_paper, left_index = True, right_index = True) \
            .drop(["authors"], axis = 1) \
            .melt(id_vars = ['title'], value_name = "author") \
            .drop("variable", axis = 1) \
            .dropna()
    
        print("\nPOPULATE AUTHOR_PAPER TABLE\n")
        for index, row in author_paper_table.iterrows():
            title = row[0] 
            author = row[1]
            #print(title)
            cur.execute('SELECT id FROM papers WHERE title = "{}"'.format(title))
            title_id = cur.fetchone()[0]
            cur.execute('SELECT id FROM authors WHERE author = "{}"'.format(author))
            author_id = cur.fetchone()[0]
            cur.execute("INSERT INTO author_paper VALUES ({}, {})".format(title_id,author_id))
            conn.commit()
        
        print('All tables were updated on database', sql_db)
            
        # # BUILD NETWORKS            
        print("\nDRAWING GRAPHS\n")
        graphic_tools().plot_networks('authors', 'title_id', 'author_id', conn)
        graphic_tools().plot_networks('papers', 'author_id', 'title_id', conn)
        print("\nGRAPHS GENERATED AND SAVED IN FOLDER\n")
        conn.close()
        
class graphic_tools:
    def __init__(self):
        pass
    
    def plot_networks(self, table, aggregator, grouped_id,conn):
        G=nx.Graph()
        df = pd.read_sql_query('SELECT * FROM {}'.format(table),conn)
        labels={}
        for index,row in df.iterrows():
            G.add_node(row[0])
            labels[row[0]]=row[1]
        author_paper = pd.read_sql_query('SELECT * FROM author_paper',conn)
        author_paper = author_paper.sort_values(by=aggregator)
    
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
        plt.clf()