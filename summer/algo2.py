from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score,silhouette_score
import numpy as np
import util
import decimal as dec
import sys

reload(sys)  
sys.setdefaultencoding('utf-8')

def get_max(data) :
	max=-99999999
	for i in range(0,len(data)):
		if data[i][1]>max :
			max=data[i][1]
	return max


def bm25(doc,topic,avgdl,datal):
	freq=doc.count(topic)
	tok=doc.split(" ")
	docl=len(tok)
	coeff=dec.Decimal(0.75*docl)/dec.Decimal(avgdl)
	num=freq*2.5
	den=dec.Decimal(freq+(1.5*(0.25+float(coeff))))
	val=dec.Decimal(num)/dec.Decimal(den)
	idf=dec.Decimal(0.5)/dec.Decimal(datal+0.5)
	result=idf*val
	return result
"""
def get_tfidf(data):


def cosval(data1,data2) :
	tok1=data1.split(" ")
	l1=len(tok1)
	tok2=data2.split(" ")
	l2=len(tok2)
	den=l1*l2
	v1=get_tfidf(data1)
	v2=get_tfidf(data2)
	size=min(len(v1),len(v2))
	sumv=0.00000
	for i in range(0,size) :
		sumv=sumv+(v1[i]*v2[i])
	result=dec.Decimal(sumv)/dec.Decimal(den)
	return result

def sim(data,i) :
	sumval=0.00000
	coeff=dec.Decimal(1)/dec.Decimal(len(data)-1)
	for j in range(0,len(data)) :
		if j!=i :
			sumval=sumval+cosval(data[i],data[j])
	result=coeff*sumval
	return result
"""

def rank_by_val(data,topic,ind):
	size=len(data)
	data1=""
	for i in range(0,size) :
		data1=data1+data[i]+" "
	tok=data1.split(" ")
	avgdl=len(tok)
	score1=[]
	score2=[]
	score3=[]
	score=[]
	rind=[]	
	for i in range(0,size) :
		x=[None]*2
		x[0]=i
		x[1]=bm25(data[i],topic,avgdl,size)
		score1.append(x)
		x[1]=1
		score2.append(x)
		x[1]=len(str(data[i]))
		score3.append(x)
	max1=get_max(score1)
	max2=get_max(score2)
	max3=get_max(score3)
	for i in range(0,size) :
		x=[None]*2
		x[0]=i
		score1[i][1]=dec.Decimal(score1[i][1])/dec.Decimal(max1)
		score2[i][1]=dec.Decimal(score2[i][1])/dec.Decimal(max2)
		score3[i][1]=dec.Decimal(score3[i][1])/dec.Decimal(max3)
		x[1]=dec.Decimal(score1[i][1]+score2[i][1]+score3[i][1])
		score.append(x)
	score=sorted(score,key=lambda x: dec.Decimal(x[1]),reverse=True)
	if ind<len(score) :
		score=score[0:ind]
	for i in range(0,len(score)) :
		rind.append(score[i][0])
	return rind

def ranker(data,topic,ind) :
	rind=rank_by_val(data,topic,ind)
	with open ("results/RANKING_index.txt","w+") as f:
		for i in range(len(rind)) :
			f.write(str(rind[i]))
			f.write("\n")
	rtweets=[]
	for i in range(0,len(rind)) :
		j=rind[i]
		rtweets.append(data[j].encode("utf-8"))
	return rtweets


def k_means_clustering(data,n_clusters,topic) :
	np.random.seed(0)
	vectorizer = TfidfVectorizer(stop_words='english')
	X = vectorizer.fit_transform(data)
	X=X.toarray()
	model = KMeans(n_clusters, init='k-means++', max_iter=500, n_init=20)
	model.fit(X)
	print(str(n_clusters)+" Clusters : Silhouette Coefficient:"+str(silhouette_score(X, model.labels_, sample_size=len(data))))
	arr=list(model.predict(X))
	
	for i in range(n_clusters) :
		if arr.count(i)==0 :
			print("Empty cluster "+str(i))
			n_clusters=int(n_clusters/2)+1
			return k_means_clustering(data,n_clusters,topic)

	# Get Clusterwise Top terms	
	order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    	terms = vectorizer.get_feature_names()
	with open("cluster_terms.csv",'w+') as f:
		for i in range(n_clusters):
			f.write("Cluster %d:\t" % i)
			for ind in order_centroids[i, :10]:
		    		f.write(' %s\t' % terms[ind])
			f.write("\n")
	f.close()
	
	#Write Tweetwise Clusters to File
	with open("results/tweetwise cluster k"+str(n_clusters)+".csv",'w+') as f:
		for i in range(0,len(arr)) :
			f.write(str(arr[i])+"\n")
	f.close()

	#Get top ranked tweets from cluster 
	ind=100/n_clusters
	zx=[]
	zy=[]
	zz=[]
	for i in range(n_clusters) :
		x=[]
		y=[]
		z=[]
		for j in range(0,len(arr)):
			if arr[j]==i :
				x.append(data[j])
				y.append(j)
		zy.append(y)
		z=rank_by_val(x,topic,ind)
		zx.append(z)
		zz.extend(z)

	with open ("results/TOP100_k_means"+str(n_clusters)+"_index.txt","w+") as f:
		for i in range(len(zx)) :
			f.write(str(zx[i]))
			f.write("\n")
		

	with open ("results/TOP100_k_means"+str(n_clusters)+".txt","w+") as f:
		for i in range(len(zz)) :
			j=zz[i]
			f.write(str(data[j]).encode("utf-8"))
			f.write("\n")
	util.listTocsv("results/cluster_tweets "+str(n_clusters)+".csv",zy)
	