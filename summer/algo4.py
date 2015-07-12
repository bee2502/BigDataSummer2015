from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import util
import csv
import decimal as dec
import os


def get_sim(data,tweet) :
	vectorizer = TfidfVectorizer()
	X = vectorizer.fit_transform(data)
	i=data.index(tweet)
	v=cosine_similarity(X, X[i:i+1])
	return str(sum(v[0])/len(v[0]))
	
def similarity_matrix(file_path,data,tweets) :
	file_name=os.path.basename(file_path)
	file_name=file_name.rstrip(".txt")
	file_name="results/new/"+file_name+"_SIM_MATRIX.csv"
	vectorizer = TfidfVectorizer()
	X = vectorizer.fit_transform(data)
	with open(file_name, "a+") as fp :
     		writeFile = csv.writer(fp)
		for tweet in tweets :
			i=data.index(tweet)
			sim=cosine_similarity(X, X[i:i+1])
			writeFile.writerow(sim)
	
		
		


dec.getcontext().prec = 10
topics=["HTC","Uber","Samsung","Beyonce","Obama"]
for topic in topics :
	outfile="results/new/"+topic+"_VectorSpaceModelResults.csv"
	infile1="data/tagged_data/data_"+topic+".txt"
	data=util.txtTolist(infile1)
	size=len(data)
	"""
	print "Calculating for Clustering Results"
	k=[5,10,25,50,100]
	dataStrip=[]
	for ki in k :
		sim=[]
		infile2="results/new/"+topic+"/KMEANS/"+topic+"_TOP100_k_means"+str(ki)+".txt"
		tweets=util.txtTolist(infile2)
		sim.append(infile2)
		for tweet in tweets :
			sim.append(get_sim(data,tweet))
		dataStrip.append(sim)
		similarity_matrix(infile2,data,tweets)
	"""
	dataStrip=[]
	print "Calculating for Random 100 results"
	sim=[]
	tweets=data[0:100]
	infile2=topic+"_RANDOM_TOP100"
	sim.append(infile2)
	for tweet in tweets :
		sim.append(get_sim(data,tweet))
	dataStrip.append(sim)
	similarity_matrix(infile2,data,tweets)
	"""
	print "Calculating for RANKING_ALGO TOP_100 results"
	sim=[]
	infile2="results/new/"+topic+"/TOP100_RANKING_"+str(topic)+".txt"
	tweets=util.txtTolist(infile2)
	sim.append(infile2)
	for tweet in tweets :
		sim.append(get_sim(data,tweet))
	dataStrip.append(sim)
	similarity_matrix(infile2,data,tweets)

	print "Calculating for ASPECT RANKING_ALGO TOP_100 results"
	sim=[]
	infile2="results/new/"+topic+"/ASPECT_RANKING/GREEDY1_"+str(topic)+".txt"
	tweets=util.txtTolist(infile2)
	sim.append(infile2)
	for tweet in tweets :
		sim.append(get_sim(data,tweet))
	dataStrip.append(sim)
	similarity_matrix(infile2,data,tweets)


	sim=[]
	infile2="results/new/"+topic+"/ASPECT_RANKING/GREEDY3_"+str(topic)+".txt"
	tweets=util.txtTolist(infile2)
	sim.append(infile2)
	for tweet in tweets :
		sim.append(get_sim(data,tweet))
	dataStrip.append(sim)
	similarity_matrix(infile2,data,tweets)


	dataStrip=zip(*dataStrip)
	with open(outfile,"w+") as fp :
		writeFile = csv.writer(fp)
		for i in range(0,len(dataStrip)) :
			writeFile.writerow(dataStrip[i])



for tweet in tweets :
		sim.append(get_sim(data,tweet))
	sim_all=[dec.Decimal(0)]*(size+1)
	sim_all[0]=infile2
	for sim_i in sim :
		sim_i=[dec.Decimal(tok)/dec.Decimal(100) for tok in sim_i]
		for i in range(0,len(sim_i)) :
			sim_all[i+1]=sim_all[i+1]+sim_i[i]
	sim_all=[ str(sim) for sim in sim_all]
	dataStrip.append(sim_all)
"""
