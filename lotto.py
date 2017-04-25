#!/usr/bin/python

# record ecarts / from all frequency
# Find balls behaviour- avg occurrence and last / across n frequency

# Avoid overlapping scenario - Define iteration pattern rotating 

# Add uk lottery

# Calibrate / Backtest

# deal with 1/12 small numbers - account for rule changes 50%
# apply other slices
# apply with dates

from datetime import date
import numpy as np

#draw="euro"
draw="uk"

# Logic :
#	- store all in text file and load
#	- do with list flat and with date / balls
#	- produce n reduce set based on filtering
#	- apply projections - + day ...
#	- count nb occurence each ball in earch serie
#	- order ball within the serie 1-n (least to most)
#	- apply weights
#	- select balls with highest score
#

#############################################
# Load list with dates 
#############################################

seq=0
Ldraw=[]

if draw=="euro":
	maxball=51
	f=open("file_draw.txt","r")
	for line in f:
		day=line.rsplit(sep=',')[0]
		str_date=line.rsplit(sep=',')[1]
		dt_draw=date(int(str_date.rsplit(sep='/')[2]), \
    			int(str_date.rsplit(sep='/')[1]), \
     			int(str_date.rsplit(sep='/')[0]))
		ball1=line.rsplit(sep=',')[2]
		ball2=line.rsplit(sep=',')[3]
		ball3=line.rsplit(sep=',')[4]
		ball4=line.rsplit(sep=',')[5]
		ball5=line.rsplit(sep=',')[6]
		small1=line.rsplit(sep=',')[7]
		small2=line.rsplit(sep=',')[8]
		Ldraw=Ldraw+[[dt_draw,int(ball1),int(ball2),int(ball3),int(ball4),int(ball5),int(small1),int(small2)]]
		Ldraw.sort(reverse=True)	# order draw from recent to first

if draw=="uk":
	maxball=60
	f=open("file_uk.txt","r")
	for line in f:
		str_date=line.rsplit(sep=',')[0]
		ball1=line.rsplit(sep=',')[1]
		ball2=line.rsplit(sep=',')[2]
		ball3=line.rsplit(sep=',')[3]
		ball4=line.rsplit(sep=',')[4]
		ball5=line.rsplit(sep=',')[5]
		ball6=line.rsplit(sep=',')[6]
		ball7=line.rsplit(sep=',')[7]
		Ldraw=Ldraw+[[str_date,int(ball1),int(ball2),int(ball3),int(ball4),int(ball5),int(ball6),int(ball7)]]

f.close()

######################################
# flat list load
######################################

seq=0
Lflat=[]; Sflat=[]; Sflat0=[]; Sflat1=[]

if draw=="euro":
	for line in Ldraw: 
		Lflat=Lflat+[line[1],line[2],line[3],line[4],line[5]]
		Sflat0=Sflat0+[line[6],line[7]]

# 11 introduced after 720 balls		- count 10 add 1
	cpt=0;seq=0
	for i in Sflat0:
		Sflat1=Sflat1+[Sflat0[i]]
		cpt=cpt+1;seq=seq+1
		if seq==9:
			seq=0;
			Sflat1=Sflat1+[11]	
	
# 12 introduced after 1920 balls	- count 11 add 1
	cpt=0;seq=0
	for i in Sflat1:
		Sflat=Sflat+[Sflat1[i]]
		cpt=cpt+1;seq=seq+1
		if seq==10:
			seq=0;
			Sflat=Sflat+[11]	

if draw=="uk":
	for line in Ldraw: 
		Lflat=Lflat+[line[1],line[2],line[3],line[4],line[5],line[6],line[7]]

#############################################
# Count occurences
#############################################

def find(listnum,start,end):
	num=[]
	for i in range(start,end):
		cpt=0
		for j in listnum:
			if i==j:
				cpt=cpt+1
		num=num+[[cpt,i]]
	num.sort(key=None,reverse=False)			# least occurence first
	list=[]; x=1
	for i in num: list=list+[[x,i[1]]] ; x=x+1		# assign 1-n order
	return list

############################################
# Record gap with last appearance
############################################

def gap(listnum,start,end):
	num=[]	
	for i in range(start,end):
		cpt=1
		for j in listnum:
			if i==j:
				num=num+[[cpt,i]]
				break
			cpt=cpt+1
	num.sort(key=None,reverse=False)			# least gap first
	list=[]; x=1
	for i in num: list=list+[[x,i[1]]] ; x=x+1		# assign 1-n order
	return list
	


# Generate lists 1/1 , 2/2 , 3/3 , 4/4

def generate(listnum,steps):
	num=[]
	start=1;stop=1;cpt=0
	for i in listnum:
		if start<=steps:
			num=num+[listnum[cpt]]
			start=start+1
			stop=1
		else:
			if stop<=steps:
				stop=stop+1
			else:
				start=1

		cpt=cpt+1
	return num

Lflat2=generate(Lflat,2)
Lflat3=generate(Lflat,3)
Lflat4=generate(Lflat,4)
Lflat5=generate(Lflat,5)

Sflat2=generate(Sflat,2)

Lflat6=Lflat[400:]

if draw=="euro":
	Sflat6=Sflat[400:]

list1=find(Lflat,1,maxball)
list2=find(Lflat2,1,maxball)
list3=find(Lflat3,1,maxball)
list4=find(Lflat4,1,maxball)
list5=find(Lflat5,1,maxball)
list6=find(Lflat6,1,maxball)

list11=gap(Lflat,1,maxball)
list12=gap(Lflat6,1,maxball)

#list12=gap(Lflat2,1,51)

if draw=="euro":
	slist1=find(Sflat,1,13)
	slist6=find(Sflat6,1,13)
	slist11=gap(Sflat,1,13)
	slist12=gap(Sflat6,1,13)

# assign 1-n per order , apply weight , sort

score=[]

for i in range(1,maxball):
	cpt=0
	#for combine in [list1,list2,list3,list4,list5,list11,list12]:
	for combine in [list1,list6,list11,list12]:
		for j in combine:
			if j[1]==i:
				cpt=cpt+j[0]
	score=score+[[cpt,i]]

score.sort()

print(score)

if draw=="euro":
	score=[]
	for i in range(1,13):
		cpt=0
		for combine in [slist1,slist6,slist11,slist12]:
			for j in combine:
				if j[1]==i:
					cpt=cpt+j[0]
		score=score+[[cpt,i]]
	score.sort()
	print(score)




