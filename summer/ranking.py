import util

import urllib
import json
from decimal import Decimal, getcontext
import math
import csv


def frequency(aspects) :
	allaspects , frequency =[] , []
	for aspect_tweet in aspects :
		for aspect in aspect_tweet :
			if aspect in allaspects :
				ind=allaspects.index(aspect)			
				frequency[ind][1]=frequency[ind][1]+1
			else :
				x=[ aspect , 1]
				allaspects.append(aspect)
				frequency.append(x)

	return frequency

def hits(topic) :
	link="http://in.search.yahoo.com/search?p="+topic	
	results = urllib.urlopen(link)
	data=results.read()	
	start=data.find("Next</a><span>")
	data_endpart=data[start:] 
	end=data_endpart.find("results") 
	result=data[start+14:start+end-1]
	x=str(result).replace(',','')
	try :
		a=math.log(long(x),2)
	except ValueError:
		a=0
	return a

def get_pmi(num,hits_a,hits_t) :
	den=hits_a+hits_t
	if den!=0 :
		ratio=34.000000+num-den
	else :
		ratio=0
	return ratio

def pmi_list(aspects,target,file_path) :
	pmi , pmis=[] , [] 
	hits_t=hits(target)
	for i in range(0,len(aspects)) :
		num=hits(target+'+'+aspects[i])
		hits_a=hits(aspects[i])
		pmi=[ aspects[i] , target , float(get_pmi(num,hits_a,hits_t)) ]
		pmis.append(pmi)
		dataStrip = [ pmi[0] , pmi[2] ]	
		with open(file_path, "a+") as fp :
			writeFile = csv.writer(fp)
	   		writeFile.writerow(dataStrip)
		fp.close()
	return pmis


def hitswise(aspects,topic,file_path) :
	hits=[ [aspect[0] , hits(aspect[0] , topic , file_path)] for aspect in aspects]
	return hits



