import sys
from decimal import Decimal, getcontext
import csv
import math

import extract
import util
import aspect
import ranking
import algo
import clean
import measures


PATH_TO_RAW_DATA="data/raw_data"
PATH_TO_CLEAN_DATA="data/clean_data"
PATH_TO_RESULTS="results"

# utf-8 encoding to include emoticons etc all kinds of spl chars found in tweets		
reload(sys)  
sys.setdefaultencoding('utf8')

topics=["HTC" , "Obama","Beyonce","Samsung","Uber"]
"""
print "\n  EXTRACTING TWITTER DATA   \n"
util.createFilePath(PATH_TO_RAW_DATA)
extract.getTweets(topics,PATH_TO_RAW_DATA,5000)
"""
print("\n  PROCESSING DATA - CLEANING AND POS TAGGING  \n")
util.createFilePath(PATH_TO_CLEAN_DATA)
clean.process(PATH_TO_RAW_DATA,PATH_TO_CLEAN_DATA,topics)


print("\n EXTRACTING TOP-K TWEETS FROM DATA  \n")

for topic in topics :
	
	print topic
	dataFile=PATH_TO_CLEAN_DATA+"/data_"+topic+".txt"
	tweets=util.txtTolist(dataFile)
	
	k=[5,10,25,50,100]
	
	for ki in k :
		topk="TOP_"+str(ki)
		CosineSimilarityVSM=[]

		method="ALL_TWEETS"
		outPath=PATH_TO_RESULTS+"/"+topic+"/"+topk+"/"+method
		util.createFilePath(outPath)
		val=measures.entropy(tweets)
		print(topic+topk+method+" Entropy : "+str(val))
	
		method="RANDOM_TWEETS"
		outPath=PATH_TO_RESULTS+"/"+topic+"/"+topk+"/"+method
		util.createFilePath(outPath)
		results=tweets[0:ki]
		rfile=outPath+"/"+topic+"_"+topk+"_"+method+".txt"
		print rfile
		util.listTotxt(rfile,results,"w+")

		val=measures.entropy(results)
		print(topic+" "+topk+method+" Entropy : "+str(val))
		measures.get_ParaphraseSim(tweets,rfile,outPath,topic,ki)
		CosineSimilarityVSM.append(measures.get_VSMsim(rfile,tweets,results))
		outFile=outPath+"/"+topic+"_"+topk+"_"+method+"_VSMSimilarityMatrix.csv"
		measures.writeCosineSimMatrix(outFile,tweets,results)
		ind=outPath.rfind("/")
		outFile=outPath[0:ind]+"/"+topic+"_"+topk+"_"+method+"_Doc2vecSimilarityMatrix.csv"
		measures.writeDoc2vecSimMatrix(outFile,tweets,results,True)
		
		# UNSUPERVISED CLUSTERING USING KMEANS		
		n_clusters=[5,10,25,50,100]
		for n in n_clusters :
			if ki>=n :
				method="KMEANS_"+str(n)	
				outPath=PATH_TO_RESULTS+"/"+topic+"/"+topk+"/"+method
				util.createFilePath(outPath)
				rfile=outPath+"/"+topic+"_"+topk+"_"+method+".txt"
				print rfile
				algo.Clustering(rfile,tweets,n,topic,ki)
			
				results=util.txtTolist(rfile)
				val=measures.entropy(results)
				print(topic+" "+topk+method+" Entropy : "+str(val))
				measures.get_ParaphraseSim(tweets,rfile,outPath,topic,ki)
				CosineSimilarityVSM.append(measures.get_VSMsim(rfile,tweets,results))
				outFile=outPath+"/"+topic+"_"+topk+"_"+method+"_VSMSimilarityMatrix.csv"
				measures.writeCosineSimMatrix(outFile,tweets,results)
				ind=outPath.rfind("/")
				outFile=outPath[0:ind]+"/"+topic+"_"+topk+"_"+method+"_Doc2vecSimilarityMatrix.csv"
				measures.writeDoc2vecSimMatrix(outFile,tweets,results,False)

		#RANKING ALGORITHM
		method="RANKING"
		outPath=PATH_TO_RESULTS+"/"+topic+"/"+topk+"/"+method
		util.createFilePath(outPath)
		rfile=outPath+"/"+topic+"_"+topk+"_"+method+".txt"
		print rfile
		results=algo.ranker(rfile,tweets,topic.lower(),ki)
		
		val=measures.entropy(results)
		print(topic+" "+topk+method+" Entropy : "+str(val))
		measures.get_ParaphraseSim(tweets,rfile,outPath,topic,ki)
		CosineSimilarityVSM.append(measures.get_VSMsim(rfile,tweets,results))
		outFile=outPath+"/"+topic+"_"+topk+"_"+method+"_VSMSimilarityMatrix.csv"
		measures.writeCosineSimMatrix(outFile,tweets,results)
		ind=outPath.rfind("/")
		outFile=outPath[0:ind]+"/"+topic+"_"+topk+"_"+method+"_Doc2vecSimilarityMatrix.csv"
		measures.writeDoc2vecSimMatrix(outFile,tweets,results,False)

		#ASPECT RANKING ALGORITHM
		method="ASPECT_RANKING"
		outPath=PATH_TO_RESULTS+"/"+topic+"/"+topk+"/"+method
		util.createFilePath(outPath)
		rfile=outPath+"/"+topic+"_"+topk+"_GreedyAspectRankingNormal.txt"
		results=aspect.GreedyAspectRanking(rfile,tweets,topic,ki)
		
		val=measures.entropy(results)
		print(topic+" "+topk+method+" Entropy : "+str(val))
		measures.get_ParaphraseSim(tweets,rfile,outPath,topic,ki)
		CosineSimilarityVSM.append(measures.get_VSMsim(rfile,tweets,results))
		outFile=outPath+"/"+topic+"_"+topk+"_"+method+"_VSMSimilarityMatrix.csv"
		measures.writeCosineSimMatrix(outFile,tweets,results)
		ind=outPath.rfind("/")
		outFile=outPath[0:ind]+"/"+topic+"_"+topk+"_"+method+"_Doc2vecSimilarityMatrix.csv"
		measures.writeDoc2vecSimMatrix(outFile,tweets,results,False)


		outPath=PATH_TO_RESULTS+"/"+topic+"/"+topk
		util.createFilePath(outPath)
		outFile=outPath+"/"+topic+"_"+topk+"_DocwiseCosineSimilarityVSM.csv"
		CosineSimilarityVSM=zip(*CosineSimilarityVSM)
		with open(outFile,"w+") as fp :
			writeFile = csv.writer(fp)
			for i in range(0,len(CosineSimilarityVSM)) :
				writeFile.writerow(CosineSimilarityVSM[i])


