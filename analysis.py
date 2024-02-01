from tkinter import*
import tkinter as tk
from tkinter import filedialog
from tkinter import  ttk
import  PyPDF2
import numpy as np
import  tabula
import pandas as pd
import sys
import os
import time
import re
import tabulate as tbl
import tabula
import pandas as pd
root=Tk()
#Defining Global Variable To Store Local Values On Excecution Time
file_nm=""
pagedata=[]
pagedata1=[]
totalpg=""
Operation=" "
FoundPage=[]
Start_time=time.time()
sublist=[]
var=tk.StringVar()
cld_list=['Bramhadevdada Mane Institute of Technology Solapur Belati', 
                'College of Engineering Gopalpur', 
                'Karmayogi Engineering College Shelve Pandharpur Shelve', 
                'MAEER s MIT College of Railway Engineering Research Jamgaon Barshi Barshi', 
                'N B Navale Sinhgad College of Engineering Solapur Kegaon', 
                'Shankarrao Mohite Patil Institute of Technology and Research Shankarnagar Akluj Akluj', 
                'SKN SINHGAD COLLEGE OF ENGINEERING Korti', 
                'Walchand Institute of Technology Solapur']
Dep_list=["COMPUTER SCIENCE & ENGINEERING","Master Of Computer Application"]
#Which Operation Done By User
sublist1=tk.StringVar()
def Which_OP(str1):
    global Operation
    Operation=str1
    label.configure(text=Operation)
#On Click Convert It Open File Dailog To Choose File
def openFile():
    global file_nm
    file_nm=filedialog.askopenfilename(initialdir="/",title="Select a File",filetypes=(("PDF Files","*.pdf*"),("All files","*.*")))
    Openfilenm="File Selected And File Name:"+os.path.basename(file_nm)
    Which_OP(Openfilenm)
    global fileReader
    pdfFileObj = open(file_nm, 'rb')
    fileReader = PyPDF2.PdfFileReader(pdfFileObj)
# code 1... 
# Long for loop which finds dept name and College name in all pages
# then match the dept name and college name
# append mached page no. in "pages" list var






def scanfile(clgname,deptname):
    pages=[]
    for pagenum in range(2,fileReader.numPages):
        pageObj = fileReader.getPage(pagenum)
        with open("a.txt",'w',encoding = 'utf-8') as f:
            f.write(pageObj.extractText())

        f = open("a.txt",'r',encoding = 'utf-8')
        # Boolean values to fud the appropriate pages
        pdeptname=False
        pclgname=False

        for i in range(0,4):
            tmp=f.readline()
            tmp=tmp.strip()
            for i in tmp:
                if not i.isalpha():
                    tmp=np.char.replace(tmp,i," ")

            tmp=str(tmp)
            # Removing Unwanted Spaces fron the string
            tmp1=""
            space=1
            for i in tmp:
                if space==0 and i==" ":
                    tmp1=tmp1+i
                    space=1
                elif space==1 and i==" ":
                    pass
                else:
                    tmp1=tmp1+i
                    space=0
                    
            tmp1=tmp1.lower()
            print(tmp1)
            # print(tmp.upper)
            tmp=tmp1.split()
            tmp1=[]
            for i in tmp:
                if i.isalpha():
                    tmp1.append(i)

            tmp=tmp1
            count=0
            for i in clgname:
                if i in tmp:
                    count+=1
            if count >= len(clgname)-1: 
                pclgname = True

            for i in deptname:
                if i in tmp:
                    count+=1
            if count >= len(deptname)-1:
                pdeptname = True

        if pdeptname and pclgname:
            pages.append(pagenum)
    return pages
            
# find dept, clg name and saperate them and append these 2 lines in  # pagedata var  
# from all remaining lines ... store in # pagedata1 list var using list slicing
# Convert 2 lines in page into 1 line and append in # lines list var
# saperate 2 records on same page by finding the "Name" string count on each page 
# then split all the data in # pagedata

def getdetails(pages,slist):
    for page in pages:
        pagedata1=[]
        pageObj = fileReader.getPage(page)
        with open("a.txt",'w',encoding = 'utf-8') as f:
            f.write(pageObj.extractText())
        f = open("a.txt",'r',encoding = 'utf-8')
        page=f.readlines()
        # length=len(page)
        
        for line in page:
            if "Seat" in line:
                sflag=page.index(line)
                break
                
        for i in range(sflag,len(page)):
            if len(page[i])>5:
                pagedata1.append(page[i])

    

        # Convert 2 lines in page into 1 line and append in # lines list var
        # line mismatch found in below code.. # namecount var used to count them..
        # break the loop at which 2nd name encountered
        lines=[]
        length=len(pagedata1)
        for i in range(0,length-1,2):
        #     print("i:=",i)
            line=pagedata1[i]+pagedata1[i+1]
            line=line.strip()
        #     print(line,"\n**")
            lines.append(line)


        # split data on single page into 2 records
        indx=0
        for i in range(len(lines)):
            if "Name" in lines[i]:
        #         print(i)
                if i==0:
                    pass
                else:  
                    indx=i
                    break



        # Remove exctra spaces " " and "|"
        # Finally extend the data in # lines list var in # pagedta list var 
        pagedata1=[]
        # Remove exctra spaces " " and store in # pagedata1 list var
        for line in lines:
            space=1
            tmp1=""
            for i in line:
                if space==0 and i==" ":
                    tmp1=tmp1+i
                    space=1
                elif space==1 and i==" ":
                    pass
                else:
                    tmp1=tmp1+i
                    space=0
            pagedata1.append(tmp1)

        lines=[]
        # Remove pipes "|" and store in # lines list var
        for line in pagedata1:
            for i in line:
                if i=="|":
                    line=np.char.replace(line,i,"")
            line=str(line)
            line=line.split()
            lines.append(line)
#             print(line,"\n**")
        # pagedata.extend(lines)
        # print(type(pagedata))
        # for i in pagedata:   
        #     print(i,"\n**")



        # Finally spliting 2 records in single page in  2 different rec1,rec2 var 
        if indx!=0:
            rec1=lines[:indx]
            rec2=lines[indx:]
#             print(len(rec1))
#             print(len(rec2))
#             print(rec1)
#             print("**",rec2)
            exctract(rec1,slist)
            exctract(rec2,slist)
            
        else:
            exctract(lines,slist)

        
def exctract(rec,sbjlist):
    stdetails=[]
    #print(sbjlist)
    submark=sbjlist.copy()
    name=''
    seat=None
    sgpa=None
    status=None
    grand=None
    percent=None
    for i in rec:
        for j in range(len(i)):
            if "Seat" in i[j]:
                seat=i[j+2]

            if "Name" in i[j]:
                while(i[j+1].isalpha()):
                    name+=i[j+1]+' '
                    j+=1

            if "SGPA" in i[j]:
                sgpa=i[j+1]

            if "Status" in i[j]:
                status=i[j+1]

            if "Grand" in i[j]:
                ma=i[j+2].split('/')[0]
                if '+' in ma:
                    ma=ma.split("+")
                    grand=int(ma[0])+int(ma[1])
                else:
                    grand=int(ma)
                
            if "Percentage" in i[j]:
                percent=i[j+1]
                
    for i in sbjlist:
        for j in rec:
            for k in range(len(j)):
                if j[k]==i and j[k+1] not in ['TH','PR']: 
                    ma=j[k+11]
                    if '*' in ma:
                        ma=np.char.replace(ma,'*',"")
                        ma=str(ma)
                        submark[sbjlist.index(i)]=int(ma)
                    elif '$' in ma:
                        ma=np.char.replace(ma,'$',"")
                        ma=str(ma)
                        ma=ma.split("+")
                        submark[sbjlist.index(i)]=int(ma[0])+int(ma[1])
                    else:
                        submark[sbjlist.index(i)]=int(j[k+11])

    stdetails.append(seat)
    stdetails.append(name)
    stdetails.extend(submark)
    stdetails.append(grand)
    stdetails.append(float(sgpa))
    stdetails.append(float(percent))
    stdetails.append(status)
    records.append(stdetails)


#function for sorting students records by subject marks for all subjects
# for k in range(0,len(sblist)+1):
def analyze(sblist):
    #print(records)
    for k in range(0,len(sblist)+1):
        temprec=records.copy()
        for i in range(0,len(temprec)-1):
            maxvalindx=i
            for j in range(i+1,len(temprec)):
                if int(temprec[j][k+2]) > int(temprec[maxvalindx][k+2]):
                    maxvalindx=j
        #     print(temprec[j])
            tmplst=temprec[maxvalindx]
            temprec[maxvalindx]=temprec[i]
            temprec[i]=tmplst
        if k== len(sblist):
            analyzeddata.append(['total:'])
        else:
            analyzeddata.append([sblist[k]])
        for i in temprec:
            analyzeddata.append(i)

#print(analyzeddata)    
    
#*********** all functions finished********
import PyPDF2
import numpy as np
#import tabulate

pages = []

# Stores the deatils after complete analysis of student data
analyzeddata=[]

# final output of program in records list in Tabular form
records=[]
sublist=[]
#sublist=['7044411','7044412','7044413','7044414','7044417','704441-3','7044415','7044416']
#sublist=['7044411','7044412','7044413']
college_list = ['Bramhadevdada Mane Institute of Technology Solapur Belati', 
                'College of Engineering Gopalpur', 
                'Karmayogi Engineering College Shelve Pandharpur Shelve', 
                'MAEER s MIT College of Railway Engineering Research Jamgaon Barshi Barshi', 
                'N B Navale Sinhgad College of Engineering Solapur Kegaon', 
                'Shankarrao Mohite Patil Institute of Technology and Research Shankarnagar Akluj Akluj', 
                'SKN SINHGAD COLLEGE OF ENGINEERING Korti', 
                'Walchand Institute of Technology Solapur']


# select a college for "college_list" var and assign to "clgname" var
clgname=college_list[0]#--------------------------------
#clgname=clgname.split(" ")#------------------------------
clg=var.get()
#print(clg)
#print(clgname)
deptname="COMPUTER SCIENCE technology".split(" ")#-----------------------
# print(deptname)
#pdfFileObj = open(file_nm, 'r')#---------------------------
#fileReader = PyPDF2.PdfFileReader(pdfFileObj)
#print(fileReader.numPages)    
# calling functions and executing program from here.........
# this  function scans the file and stores the page no in "pages" list


def Generate2Excel():
    pdfFileObj = open(file_nm, 'rb')#---------------------------
    fileReader = PyPDF2.PdfFileReader(pdfFileObj)
    #print("in generate2excel fun....")
    pages=[]
    xyz=var.get().lower()
    print("hello")
    clgname=xyz.split(" ")
    print(clgname)
    deptname=var1.get().lower().split()
    print(deptname)
    sblist=list(sublist1.get().split(","))
    #print(sblist)
    pages=scanfile(clgname,deptname)
    getdetails(pages,sblist)
    analyze(sblist)
    with open("output.txt",'w',encoding = 'utf-8') as f:
            f.write(tbl.tabulate(analyzeddata))
    read_file = pd.read_csv("output.txt","r")
    read_file.to_csv(r"NewCSV.csv")
    read_csv=pd.read_csv("NewCSV.csv","r")
    read_csv.to_excel("ToExcel.xlsx")
    print("execution completed......!")

root.title("File Convertor")
root.geometry("900x500")
Label(root,text="* Analayse PDF File Data * ",font="ar 17 bold" ,bg='grey').grid(row=3,column=6)
labl=Label(root,text="Select File :").grid(row=4,column=1)
button=Button(text="Open PDF File",command=openFile).grid(row=4,column=6)
#var=tk.StringVar()
labl=Label(root,text="Select College Name :").grid(row=6,column=1)
dropMenu1=tk.OptionMenu(root,var, *cld_list).grid(row=6, column=6)
var.set("Bramhadevdada Mane Institute of Technology")# Setting Default Value To College name
var1=tk.StringVar()
labl=Label(root,text="Select  A Department :").grid(row=7,column=1)
Dep_drop=tk.OptionMenu(root,var1,*Dep_list).grid(row=7,column=6)
var1.set("COMPUTER SCIENCE & ENGINEERING")# Setting Default Value To College Department
labl=Label(root,text="Enter Subjcet Code :").grid(row=8,column=1)
txtsub=Entry(root,width=60,textvariable=sublist1).grid(row=8,column=6)
labl=Label(root,text="Enter Code By Seperated by comma ','",font="ar 9 bold",bg="red").grid(row=9,column=6)
#button2=Button(text="Search And Show",command=Generate2Excel).grid(row=9,column=7)
button1=Button(text="Generate O/P File",command=Generate2Excel).grid(row=9,column=5)
label=Label(root,text="None")
label.grid(row=14,column=1)
labl2=Label(root,text="Operation is :",bg="Green").grid(row=11,column=1)
root.mainloop()
# print("file scanned successfully")
# "pages" var can be passed to 
# print("getdetails run successfully")
# final output of program in records list in Table form
# print(records)
# Analyze function analyze the whole data and store in "analyzeddata" list variable
# print("analyze run successfully")
# This prints the all the records in analyzeddata list variable
#for i in analyzeddata:
#    print(i)
#print(tabulate(analyzeddata,headers=["Seat No","Name","S1","S2","s3","s4","s5","s6","s7","s8","Total","SGPA","Per","sts"]))
