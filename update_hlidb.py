import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
import tkinter.messagebox
from PIL import ImageTk, Image
from prettytable import PrettyTable
import itertools
from tabulate import tabulate
from PIL import Image, ImageTk
import webbrowser

import mysql.connector
from googletrans import Translator
from textblob import TextBlob
import speech_recognition as sr
from nltk import word_tokenize, pos_tag
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from geotext import GeoText
from word2number import w2n

from time import ctime
import time
import os
import sys
from gtts import gTTS

import pyttsx3

import nltk



lemmatizer = WordNetLemmatizer()
AttrList=['name','names','rollno','serialno','age','city','live','lives','studying','studies','study','class','grade',
              'residence','girls','girl','female','boys','boy','male','enrolled','admission','admitted','serial','roll','cities']
WhereList=['where','whose','जिनका', 'जिसका','जो',' जिनके' ]
CreateList=['create','make','build','construct','generate','design','table']


'''===================================================SQL==================================================================='''
def Run():
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="root@123",database="Student")
    mycursor=mydb.cursor()
    fetch_text = text1.get("sel.first", "sel.last") #'1.0', 'end-1c'
    lbx.insert(END," ")
    lbx.insert(END,"-------------------------------------------------------------------------------------------------------------------------------------")
    if "show" in fetch_text:
        try:
            
            mycursor.execute(" "+fetch_text)
            lbx.insert(END,"Tables are as follows : ")
            lbx.insert(END," ")
            for x in mycursor:
                print(x)
                lbx.insert(END,x)
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Check your syntax!")
                lbx.insert(END,"Check your syntax!")
            else:
                print("Error: {}".format(err))
                lbx.insert(END, "Error: {}".format(err))
            
    if "desc" in fetch_text:
        try:

            mycursor.execute(" "+fetch_text)
            for x in mycursor:
                print(x)
                lbx.insert(END,x)
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Check your syntax!")
                lbx.insert(END,"Check your syntax!")
            else:
                print("Error: {}".format(err))
                lbx.insert(END, "Error: {}".format(err))
        
    

    if "create" in fetch_text:
        try: #new block added
            mycursor.execute(" "+fetch_text)
            print(mycursor.rowcount+1,"Table created")
            lbx.insert(END,mycursor.rowcount+1,"Table created")
        except mysql.connector.Error as err:
            lbx.insert(END,err)
            print(err)
            #lbx.insert(END,"Error Code:", err.errno)
            #lbx.insert(END,"SQLSTATE", err.sqlstate)
            #lbx.insert(END,"Message : ", err.msg)
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Check your syntax!")
                lbx.insert(END,"Check your syntax!")
            else:
                print("Error: {}".format(err))
                lbx.insert(END, "Error: {}".format(err))
    
        
    if "alter" in fetch_text:
        try:
            mycursor.execute(" "+fetch_text)
            print(mycursor.rowcount+1,"Table created")
            lbx.insert(END,mycursor.rowcount+1,"Table altered")
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Check your syntax!")
                lbx.insert(END,"Check your syntax!")
            else:
                print("Error: {}".format(err))
                lbx.insert(END, "Error: {}".format(err))
    

    if "insert" in fetch_text or "Insert" in fetch_text:
        try: 
            mycursor.execute(" "+fetch_text)
            mydb.commit()
            #lbx.insert(END,mycursor.rowcount+1,"Data inserted")
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            print("DataError or IntegrityError")
            print(err)
            lbx.insert(END,"DataError or IntegrityError")
            lbx.insert(END,err)
        except mysql.connector.ProgrammingError as err:
            print("Programming Error")
            print(err)
            lbx.insert(END,"Programming Error")
            lbx.insert(END, err)
        except mysql.connetor.Error as err:
            print(err)
            lbx.insert(END, err)
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Check your syntax!")
                lbx.insert(END,"Check your syntax!")
            else:
                print("Error: {}".format(err))
                lbx.insert(END, "Error: {}".format(err))
    

    if "delete" in fetch_text or "Delete" in fetch_text:
        try:
            
            mycursor.execute(" "+fetch_text)
            mydb.commit()
            lbx.insert(END,mycursor.rowcount+1,"data deleted")
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Check your syntax!")
                lbx.insert(END,"Check your syntax!")
            else:
                print("Error: {}".format(err))
                lbx.insert(END, "Error: {}".format(err))

    if "update" in fetch_text:
        try:
            
            mycursor.execute(" "+fetch_text)
            mydb.commit()
            lbx.insert(END,mycursor.rowcount+1,"Data updated")
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Check your syntax!")
                lbx.insert(END,"Check your syntax!")
            else:
                print("Error: {}".format(err))
                lbx.insert(END, "Error: {}".format(err))
    


        
    if "select" in fetch_text or "Select" in fetch_text:
        try:
            T = fetch_text.split() #new line added
            lst1 = ['id','roll_no','name','age','class','address','registration_date','gender']#new line added
            lst2 = [value for value in T if value in lst1]#new line added
            top=Toplevel()
            top.geometry("1000x500")
            top.configure(bg='white')
            l6=Label(top,text="Output of the query",bg="black",fg="white",padx=10,pady=10)
            l6.pack(fill="x")
            text2 = scrolledtext.ScrolledText(top, height=10,width=100)
            text2.pack(pady=40)
            mycursor.execute(" "+fetch_text)
            myresult=mycursor.fetchall()
            if "*" in fetch_text: # new line added
                tb = tabulate(myresult,lst1, tablefmt="psql", numalign="left")# new line added
                text2.insert(INSERT, ""+tb)
            else:
                tb = tabulate(myresult,lst2, tablefmt="psql", numalign="left")#new line added
                text2.insert(INSERT, ""+tb)
                
            #lbx.insert(END,tb)  #changed x to tb
            
            #x=Label(top,text=tb,font="Times 14",pady=30,padx=30,bg="gold")
            #x.grid(row=0,column=0,padx=2,pady=2)
            #x.pack()
            
                
        except mysql.connector.ProgrammingError as err:
            if errorcode.ER_NO_SUCH_TABLE == err.errno:
                lbx.insert(END,"No table exists")
                print("No table exists")
            else:
                lbx.insert(END,"Table Exists")
                lbx.insert(END,err)
                print("Table Exists")
                print(err)
        except mysql.connector.Error as err:
            lbx.insert(END,err)
            print(err)
        except mysql.connector.Error as err:
            lbx.insert(END,"Some other error")
           # lbx.insert(END,)
            lbx.insert(END,err)
        '''except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Check your syntax!")
                lbx.insert(END,"Check your syntax!")
            else:
                print("Error: {}".format(err))
                lbx.insert(END, "Error: {}".format(err))'''


    

    if "drop" in fetch_text:
        try:
            mycursor.execute(" "+fetch_text)
            lbx.insert(END,mycursor.rowcount+1,"Table droped")
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Check your syntax!")
                lbx.insert(END,"Check your syntax!")
            else:
                print("Error: {}".format(err))
                lbx.insert(END, "Error: {}".format(err))


'''==========================================CODE==================================================='''

def form_selectquery(text):
    print("Inside Select_Query")
    ps = PorterStemmer()
    select_query=[]
    print(text)
    comment=text
    "if statements for executing commands"
    for i in range(0,len(comment)):   
            token_comment = word_tokenize(comment[i])
            #print(token_comment)
            tagged_comment = pos_tag(token_comment)
            #print([(word, tag) for word, tag in tagged_comment])
            for word, tag in tagged_comment:
                if ((tag=='NNP' or tag=='NN' and word=='show' or word=='describe') or word=='show' or word=='tell'):
                    #print(word,'Select')
                    select_query.append('Select')
                if word in AttrList:
                    if(word=='live'):
                        word='city'
                    if(word=='female' or word=='girls' or word=='girl'or word=='male' or word=='boys' or word=='boy'):
                        word='gender'
                    if(word=='enrolled' or word=='admission'):
                        word='registration_date'
                    if(word=='studying' or word=='studies' or word=='study' or word=='class' or word=='grade'):
                        word='class'
                    if(word=='serial' or word=='roll' or word=='no.'):
                        word='roll_no'
                    #print(ps.stem(word))
                    select_query.append(lemmatizer.lemmatize(word))

##               if(select_query[0]!='Select'):
##                    select_query.insert(0,'Select')
                            
            select_query.append('from Student;');
            print(select_query)
            query = ' '.join(map(str, select_query))
            if(query=='Select from Student;'):
                print("FINAL QUERY--> Select * from Student;")
                text1.insert(END,'Select * from Student;')
            else:
                print("FINAL QUERY--> ",query)
                text1.insert(END,query)


def dummywhere(text):
    print('Inside Where_Query')
    count=0
    ps = PorterStemmer()
    pre_cond_query=[]
    post_cond_query=[]
    select_query=[]
    comment1=[text.lower()]
    #print(text)
    place=GeoText(text)
    #print("Printing comment",comment1)
    for i in range(0,len(comment1)):
        token_comment = word_tokenize(comment1[i])
        #print(token_comment)
    if all(word not in 'who whose whom' for word in token_comment):
        if('over' in token_comment):
            index1=token_comment.index('over')
            #print(index1)
            token_comment.insert(index1,'who')
        elif('under' in token_comment):
            index1=token_comment.index('under')
            #print(index1)
            token_comment.insert(index1,'who')
    comment=[' '.join(map(str, token_comment))]
    for i in range(0,len(comment)):
        token_comment = word_tokenize(comment[i])
        #print(token_comment)
        if('whose' in token_comment):
            index=token_comment.index('whose')
            prequery=token_comment[:index]
            print("Prequery",prequery)
            postquery=token_comment[index:(len(token_comment))]
            print("Postquery",postquery)
            
        
        elif('who' in token_comment):
            index=token_comment.index('who')
            prequery=token_comment[:index]
            print("Prequery",prequery)
            postquery=token_comment[index:(len(token_comment))]
            print("Postquery",postquery)
    
    for i in range(0,len(comment)):
            token_comment = word_tokenize(comment[i])
            tagged_comment = pos_tag(token_comment)

    
    for i in range(0,len(prequery)):
        tagged_comment1=pos_tag(prequery)
    for word, tag in tagged_comment1:
        if ((tag=='NNP' or tag=='NN' and word=='show' or word=='describe' or word=='state') or word=='show' or word=='tell' or word=='give'):
            pre_cond_query.append('Select')
        if word in AttrList:
            if(word=='live'):
                word='city'
            if(word=='female' or word=='girls' or word=='girl'or word=='male' or word=='boys' or word=='boy'):
                word='gender'
            if(word=='enrolled' or word=='admission' or word=='admitted'):
                word='registration_date'
            if(word=='studying' or word=='studies' or word=='study'):
                word='class'
            if(word=='roll' or word=='serial'  or word=='no.'):
                word='roll_no'
                
            pre_cond_query.append(lemmatizer.lemmatize((word)))
    print(pre_cond_query)
    pre_cond_query.extend(['from','Student','where'])
    if(pre_cond_query[0]!='Select'):
        pre_cond_query.insert(0,'Select')
    print("Preconditional Query: ",pre_cond_query)

    for i in range(0,len(postquery)):
        tagged_comment2=pos_tag(postquery)
    for word, tag in tagged_comment2:
        if word in AttrList:
            if(word=='live'):
                word='city'
            if(word=='female' or word=='girls' or word=='girl'or word=='male' or word=='boys' or word=='boy'):
                word='gender'
            if(word=='enrolled' or word=='admission' or word=='admitted'):
                word='registration_date'
            if(word=='studying' or word=='studies' or word=='study'):
                word='class'
            if(word=='roll' or word=='serial'  or word=='no.'):
                word='roll_no'
                
            post_cond_query.append(lemmatizer.lemmatize((word)))
            if(word=='age'):
                for word, tag in tagged_comment:
                    if(word=='less' or word=='under'):
                        post_cond_query.append('<')
                    if(word=='more' or word=='over' or word=='above'):
                        post_cond_query.append('>')
                    if(tag=='CD'):
                        post_cond_query.append(word)
                if('>' not in post_cond_query and '<' not in post_cond_query):
                    post_cond_query.insert(-1, '=')

            if(word=='roll_no'):
                for word, tag in tagged_comment:
                    if(word=='less' or word=='under'):
                        post_cond_query.append('<')
                    if(word=='more' or word=='over' or word=='above'):
                        post_cond_query.append('>')
                    if(tag=='CD'):
                        post_cond_query.append(word)
                if('>' not in post_cond_query and '<' not in post_cond_query):
                    post_cond_query.insert(-1, '=')
                    

            if(word=='city'):
                post_cond_query.extend(['='])
                if(len(place.cities)==0):
                    post_cond_query.append("'"+token_comment[-1]+"'")
                else:
                    post_cond_query.append(str(place.cities).strip('[]'))

            if(word=='gender'):
                post_cond_query.extend(['='])
                if('girls' in token_comment or 'girl' in token_comment or 'female'in token_comment):
                    post_cond_query.append("'female'")
                else:
                    post_cond_query.append("'male'")
            if(word=='name'):
                post_cond_query.append("=")
                post_cond_query.append("'"+token_comment[-1]+"'")

            if(word=='registration_date'):
                post_cond_query.extend(['='])
                for word, tag in tagged_comment:
                    if(tag=='CD'):
                        post_cond_query.append("'"+word+"'")
    print("PostConditional Query",post_cond_query)


    cond_query=pre_cond_query+post_cond_query
    condi_query = ' '.join(map(str, cond_query))
    print('FINAL QUERY--> '+condi_query)
    text1.insert(END,condi_query)


def form_whereallquery(text):
    print("From all")
    ps = PorterStemmer()
    cond_query=[]
    select_query=[]
    comment=[text.lower()]
    place=GeoText(text)
    for i in range(0,len(comment)):
            token_comment = word_tokenize(comment[i])
            tagged_comment = pos_tag(token_comment)
            for word, tag in tagged_comment:
                if ((tag=='NNP' or tag=='NN' and word=='show' or word=="give" or word=='describe' or word=='state') or word=='show' or word=='tell' or word=='give'):
                    select_query.append('Select')
                    cond_query.append('Select')
                    cond_query.append('*')
                if word in AttrList:
                    if(word=='live' or word=='lives'):
                        word='city'
                    if(word=='female' or word=='girls' or word=='girl'or word=='male' or word=='boys' or word=='boy'):
                        word='gender'
                    if(word=='enrolled' or word=='admission'):
                        word='registration_date'
                    if(word=='studying' or word=='studies' or word=='study'):
                        word='class'
                    if(word=='roll' or word=='serial' or word=='no.'):
                        word='roll_no'
                        
                    if(word=='age'):
                        cond_query.extend(['from',' Student', 'where',word])
                        for word, tag in tagged_comment:
                            if(word=='less' or word=='under'):
                                cond_query.append('<')
                            if(word=='more' or word=='over' or word=='above'):
                                cond_query.append('>')
                            if(tag=='CD'):
                                cond_query.append(word)
                        if('>' not in cond_query and '<' not in cond_query):
                            cond_query.insert(-1, '=')

                    if(word=='city' or word=='residence' or word=='live'):
                        word='city';
                        cond_query.extend(['from','Student', 'where',word,'='])
                        if(len(place.cities)==0):
                            cond_query.append("'"+token_comment[-1]+"'")
                        else:
                            cond_query.append(str(place.cities).strip('[]'))

                    if(word=='gender'):
                        cond_query.extend(['from','Student', 'where',word,'='])
                        if('girls' in token_comment or 'girl' in token_comment or 'female'in token_comment):
                            cond_query.append("'female'")
                        else:
                            cond_query.append("'male'")

                    if(word=='registration_date'):
                        for word, tag in tagged_comment:
                            if(tag=='CD'):
                                cond_query.extend(['from','Student', 'where',word,'='])
                                cond_query.append("'"+word+"'")

                    if(word=='name'):
                        cond_query.extend(['from','Student', 'where',word,'='])
                        cond_query.append("'"+token_comment[-1]+"'")

                    if(word=='class'):
                        cond_query.extend(['from','Student', 'where',word,'='])
                        cond_query.append("'"+token_comment[-1]+"'")

                    if(word=='roll_no'):
                        cond_query.extend(['from',' Student', 'where',word])
                        for word, tag in tagged_comment:
                            if(word=='less' or word=='under'):
                                cond_query.append('<')
                            if(word=='more' or word=='over' or word=='above'):
                                cond_query.append('>')
                            if(tag=='CD'):
                                cond_query.append(word)
                        if('>' not in cond_query and '<' not in cond_query):
                            cond_query.insert(-1, '=')

                if(cond_query[0]!='Select'):
                    cond_query.insert(0,'Select')
    condi_query = ' '.join(map(str, cond_query))
    print('FINAL QUERY--> '+condi_query+';')
    text1.insert(END,condi_query)


def form_deletequery(text):
    print("From Delete Query")
    ps = PorterStemmer()
    place=GeoText(text)
    delete_query=[]
    select_query=[]
    comment=[text.lower()]
    #print(text)
    for i in range(0,len(comment)):
        token_comment = word_tokenize(comment[i])
        #print(token_comment)
        tagged_comment = pos_tag(token_comment)
        #print([(word, tag) for word, tag in tagged_comment])

        delete_query.append('Delete')
        for word, tag in tagged_comment:
            if(word=='elder' or word=='older' or word=='under' or word=='above' or word=='below'):
                word='age'
            if word in AttrList:
                if(word=='live' or word=='lives'):
                    word='city'
                if(word=='female' or word=='girls' or word=='girl'or word=='male' or word=='boys' or word=='boy'):
                    word='gender'
                if(word=='enrolled' or word=='admission'):
                    word='registration_date'
                if(word=='studying' or word=='studies' or word=='study' or word=='class'):
                    word='class'
                if(word=='roll' or word=='serial' or word=='no.'):
                    word='roll_no'
                if(word=='age'):
                    delete_query.extend(['from',' Student', 'where',word])
                    for word, tag in tagged_comment:
                        if(word=='less' or word=='under'):
                            delete_query.append('<')
                        if(word=='more' or word=='over' or word=='above' or word=='older'):
                            delete_query.append('>')
                        if(tag=='CD'):
                            delete_query.append(word)
                    if('>' not in delete_query and '<' not in delete_query):
                        delete_query.insert(-1, '=')

            if(word=='city' or word=='residence' or word=='live'):
                word='city';
                delete_query.extend(['from','Student', 'where',word,'='])
                if(len(place.cities)==0):
                    delete_query.append("'"+token_comment[-1]+"'")
                else:
                    delete_query.append(str(place.cities).strip('[]'))

            if(word=='gender'):
                delete_query.extend(['from','Student', 'where',word,'='])
                if('girls' in token_comment or 'girl' in token_comment or 'female'in token_comment):
                    delete_query.append("'female'")
                else:
                    delete_query.append("'male'")

            if(word=='registration_date'):
                for word, tag in tagged_comment:
                    if(tag=='CD'):
                        delete_query.extend(['from','Student', 'where',word,'='])
                        delete_query.append("'"+word+"'")

            if(word=='name'):
                delete_query.extend(['from','Student', 'where',word,'='])
                delete_query.append("'"+token_comment[-1]+"'")

            if(word=='class'):
                delete_query.extend(['from','Student', 'where',word,'='])
                delete_query.append("'"+token_comment[-1]+"'")

            if(word=='roll_no'):
                delete_query.extend(['from',' Student', 'where',word])
                for word, tag in tagged_comment:
                    if(word=='less' or word=='under'):
                        delete_query.append('<')
                    if(word=='more' or word=='over' or word=='above'):
                        delete_query.append('>')
                    if(tag=='CD'):
                        delete_query.append(word)
                if('>' not in delete_query and '<' not in delete_query):
                    delete_query.insert(-1, '=')
                    
            if(delete_query[0]!='Delete'):
                delete_query.insert(0,'Delete')
    deletion_query = ' '.join(map(str, delete_query))
    if(len(deletion_query)==15):
        deletion_query=deletion_query+' from Student;'
    print('FINAL QUERY--> '+deletion_query+';')
    text1.insert(END,deletion_query)


def form_countquery(text):
    print("From Count Query")
    ps = PorterStemmer()
    place=GeoText(text)
    cond_query=[]
    select_query=[]
    comment=[text.lower()]
    #print(text)
    for i in range(0,len(comment)):
            token_comment = word_tokenize(comment[i])
            #print(token_comment)
            tagged_comment = pos_tag(token_comment)
            #print('tagged comment', tagged_comment)
            #print([(word, tag) for word, tag in tagged_comment])

            cond_query.append('Select')
            cond_query.append('COUNT(*)')
            for word, tag in tagged_comment:
                if(word=='elder' or word=='older' or word=='under' or word=='above' or word=='below'):
                    word='age'
                if word in AttrList:
                    if(word=='live' or word=='lives'):
                        word='city'
                    if(word=='female' or word=='girls' or word=='girl'or word=='male' or word=='boys' or word=='boy'):
                        word='gender'
                    if(word=='enrolled' or word=='admission'):
                        word='registration_date'
                    if(word=='studying' or word=='studies' or word=='study' or word=='class'):
                        word='class'
                        #cond_query.append(lemmatizer.lemmatize((word)))
                    if(word=='roll' or word=='serial'  or word=='no.'):
                        word='roll_no'
                    if(word=='age'):
                        cond_query.extend(['from',' Student', 'where',word])
                        for word, tag in tagged_comment:
                            if(word=='less' or word=='under'):
                                cond_query.append('<')
                            if(word=='more' or word=='over' or word=='above' or word=='older'):
                                cond_query.append('>')
                            if(tag=='CD'):
                                cond_query.append(word)
                        if('>' not in cond_query and '<' not in cond_query):
                            cond_query.insert(-1, '=')

                if(word=='city' or word=='residence' or word=='live'):
                    word='city';
                    cond_query.extend(['from','Student', 'where',word,'='])
                    if(len(place.cities)==0):
                        cond_query.append("'"+token_comment[-1]+"'")
                    else:
                        cond_query.append(str(place.cities).strip('[]'))

                if(word=='gender'):
                    cond_query.extend(['from','Student', 'where',word,'='])
                    if('girls' in token_comment or 'girl' in token_comment or 'female'in token_comment):
                        cond_query.append("'female'")
                    else:
                        cond_query.append("'male'")

                if(word=='registration_date'):
                    for word, tag in tagged_comment:
                        if(tag=='CD'):
                            cond_query.extend(['from','Student', 'where',word,'='])
                            cond_query.append("'"+word+"'")

                if(word=='name'):
                    cond_query.extend(['from','Student', 'where',word,'='])
                    cond_query.append("'"+token_comment[-1]+"'")

                if(word=='class'):
                    cond_query.extend(['from','Student', 'where',word,'='])
                    cond_query.append("'"+token_comment[-1]+"'")
                if(word=='roll_no'):
                    cond_query.extend(['from',' Student', 'where',word])
                    for word, tag in tagged_comment:
                        if(word=='less' or word=='under'):
                            cond_query.append('<')
                        if(word=='more' or word=='over' or word=='above'):
                            cond_query.append('>')
                        if(tag=='CD'):
                            cond_query.append(word)

                        
                if(cond_query[0]!='Select'):
                    cond_query.insert(0,'Select')
    condi_query = ' '.join(map(str, cond_query))
    if(len(condi_query)==15):
        condi_query=condi_query+' from Student;'
    print('FINAL QUERY--> '+condi_query+';')
    text1.insert(END,condi_query)
    

def form_insertquery(text):
    insertquery=[]
    print("From Insert Query")
    r = sr.Recognizer()
    translator = Translator()
    with sr.Microphone() as source:
        print('Ready... from Insert')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        talk("समय समाप्त, धन्यवाद।")

    try:
        print("You said: "+r.recognize_google(audio, language='hi-IN'));
        text=r.recognize_google(audio, language='hi-IN')
        hi_blob = TextBlob(text)
        print(hi_blob.translate(to='en'))
        text2=(str(hi_blob.translate(to='en')))
        print(text2)
        comment=[text2.lower()]
        for i in range(0,len(comment)):
            token_comment = word_tokenize(comment[i])
            print(token_comment)
        insertquery.extend(["Insert","into","Student","values("])
        
        for i in range(0,len(token_comment)):
            insertquery.append(token_comment[i])
        insertquery.append(")")
        print(insertquery)
        insert_query =' '.join(map(str, insertquery))
        insert_query=insert_query.replace('mail','male')
        insert_query=insert_query.replace('boy','male')
        insert_query=insert_query.replace('boys','male')
        insert_query=insert_query.replace('girl','female')
        insert_query=insert_query.replace('girls','female')
        print("FINAL QUERY--> ",insert_query)
        text1.insert(END,insert_query)
            
        #print(w2n.word_to_num(list1[0]))
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')



'''================================INITIAL COMMANDS=========================='''
def talk(audio):
    "speaks audio passed as argument"

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[20].id)
    engine.say(audio)
    engine.runAndWait()

def greeting():
    talk('नमस्ते, आपका स्वागत हैं।')
def closinggreeting():
    talk("धन्यवाद, आपका दिन शुभ हो।")
    
def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    translator = Translator()
    with sr.Microphone() as source:
        #lbx.insert(END,'Ready...')
        print("--------------------------------------------------------------------------------")
        talk("मैं आपकी कैसे मदद कर सकती हूँ?");

        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        talk("समय समाप्त, धन्यवाद।")
        

    try:
        lbx.insert(END,"आपने कहा: "+r.recognize_google(audio, language='hi-IN'));
        text=r.recognize_google(audio, language='hi-IN')
        print("आपने कहा: "+text)
        hi_blob = TextBlob(text)
        text1=(str(hi_blob.translate(to='en')))
        comment=[text1.lower()]
        print("TOKENIZATION")
        for i in range(0,len(comment)):
                token_comment = word_tokenize(comment[i])
                print(token_comment)
                tagged_comment = pos_tag(token_comment)
                print([(word, tag) for word, tag in tagged_comment])
                if('जिनका' in hi_blob or 'जिनकी' in hi_blob or 'जो' in hi_blob or 'जिसका' in hi_blob or
                   'जिसकी' in hi_blob or 'जिन्होंने' in hi_blob or 'जिसने' in hi_blob or 'जिस' in hi_blob or 'जिन जिन' in hi_blob or 'जिनका' in hi_blob):
                    if('पूरा' in hi_blob or 'सारा' in hi_blob or 'सब' in hi_blob or'सारी' in hi_blob or 'सभी' in hi_blob):
                        form_whereallquery(text1)
                    elif('संख्या' in hi_blob or 'कितने' in hi_blob or 'कितनी' in hi_blob):
                        form_countquery(text1)
                    elif('हटाइये' in hi_blob or  'डिलीट' in hi_blob or 'निकालिये' in hi_blob or 'निकालो' in hi_blob or  'निकाल' in hi_blob or  'निकालियें' in hi_blob or 'हटा' in hi_blob):
                        form_deletequery(text1)
                    else:
                        #form_wherequery(text1)
                        dummywhere(text1)

                else:
                    for word, tag in tagged_comment:
                        if((tag=='NNP' or tag=='NN' and word=='show' or word=='describe') or word=='show' or word=='tell'):
                            form_selectquery(comment)
                if('संख्या' in hi_blob or 'कितने' in hi_blob or 'कितनी' in hi_blob):
                    form_countquery(text1)

                if('डालो' in hi_blob or  'डालिये'  in hi_blob or  'प्रवेश' in hi_blob or  'भरिये' in hi_blob or  'भर्ती' in hi_blob or  'डाल' in hi_blob or  'डालिए' in hi_blob or  'डालियेँ' in hi_blob):
                    print("Roll_No | Name  | Age | Class | Address | Registration_Date | Gender ")
                    lbx.insert(END,"Roll_No | Name  | Age | Class | Address | Registration_Date | Gender ")
                    talk("ऊपर दिखाए गए क्रम में ही डाटा डालिये")
                    form_insertquery(text1)

        unwanted_no=[':','00',':00']
        if(':' in comment or  '00' in comment or ':00' in comment):
            for i in unwanted_no:
                text1=comment.replace(i,' ')
    except sr.UnknownValueError:
        talk('माफ़ कीजिये, मैं आपको सुन नहीं पायी ')
        comment = myCommand();

    return comment

'''=========================================TKINTER=================================================='''
new = 1
def openweb():
    webbrowser.open(url,new=new)

def callback():
    if tkinter.messagebox.askokcancel("Quit", "Do you really wish to quit?\n क्या आप इसे बंद करना चाहते हैं?"):
        closinggreeting()
        window.destroy()

greeting()
window = tk.Tk()
window.title("Hindi Language Interface to Database")
window.protocol("WM_DELETE_WINDOW", callback)
window.geometry("700x500")
tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl,width=300, height=200)
tabControl.add(tab1, text="होम/Home")
tabControl.pack(expand=1, fill="both")

tab2 = ttk.Frame(tabControl,width=300, height=200)
tabControl.add(tab2, text="डेमो/Demo")
tabControl.pack(expand=1, fill="both")
window.configure(bg='cornflower blue')
l1=tk.Label(tab2,text="अब डेटाबेस से बात करना होगा और भी सरल|",bg="black",fg="white",padx=10,pady=10)
l1.pack(fill="x")

f1 = Frame(tab2,width = 500,height=500,relief=SUNKEN)
f1.pack(side=LEFT)

load = Image.open('no button.png')
render = ImageTk.PhotoImage(load)
img = Label(f1, image=render)
img.image = render
img.pack(side=TOP)

url = "https://drive.google.com/open?id=1g5ENtl3g0_WNXpS_b27uYJoBmQuaM6QW"
Btn = Button(f1, text = "Download Video",command=openweb, width='20', bg='blue', fg='white').pack(side=BOTTOM, expand=YES)

l1=tk.Label(tab1,text="अब डेटाबेस से बात करना होगा और भी सरल|",bg="black",fg="white",padx=10,pady=10)
l1.pack(fill="x")
text1 = tk.scrolledtext.ScrolledText(tab1, height=8)

lbl = tk.Label(tab1)
text1.pack(pady=20)
lbl.pack()
print(text1.get(1.0,END))

hf = Frame(tab1)
##photo = Image.open("record1.png")  # PIL solution
##photo = photo.resize((30,30))
##photo = ImageTk.PhotoImage(photo)
  
# Resizing image to fit on button 
#photoimage = photo.subsample(3, 3) 
btn = tk.Button(hf, text="Speak", bg="black", fg="white",padx=20,pady=6,command=myCommand)
btn.grid(row=0,column=0,padx=2,pady=2)

btn4 = tk.Button(hf, text="Run", bg="black", fg="white",padx=25,pady=6, command=Run)
btn4.grid(row=0,column=1,padx=10,pady=10)


hf.grid_columnconfigure(0,weight=1)
hf.grid_columnconfigure(1,weight=1)


hf.pack(fill="x")

lbx = tk.Listbox(tab1,
              font = ("Arial",11),height=8
)
lbx.pack(expand=1, fill="both",pady=20,side=LEFT,padx=20)

sbr = tk.Scrollbar(tab1,)
sbr.pack(side=RIGHT,fill="y")

sbr.config(command=lbx.yview)
lbx.config(yscrollcommand=sbr.set)
window.mainloop()
closinggreeting()




