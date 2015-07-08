import decimal as dec

#def entropy(data) :


def get_normlev_dist(word1,word2) :	
	dec.getcontext().prec = 10
	m=len(word1)
	n=len(word2) 
	x=[0]*n	
	d=[x]*m
	for i in range(0,m):
      		d[i][0]= i
        for j in range(0,n):
        	d[0][j]= j 
	for j in range(0,n) :
		for i in range(0,m) :
			if word1[i] == word2[j]:
				d[i][j] = d[i-1][j-1]             
			else:
				d[i][j] = min(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + 1) 
	
	val= dec.Decimal(d[m-1][n-1])/dec.Decimal(m*n)
	return val





def levenshtein(data) :
	dec.getcontext().prec = 10
	a=0
	for i in range(0,len(data)) :
		sum2=0
		print i
		toks1=data[i].split(' ')
		for j in range(0,len(toks1)) :
			sum1=0
			for k in range(0,len(data)) :
				sum=0
				toks2=data[k].split(' ')
				ctr=0
				for m in range(0,len(toks2)) :
					if toks1[j].isalpha() and toks2[m].isalpha() :
						l=get_normlev_dist(toks1[j],toks2[m])
						sum=sum+l
						ctr=ctr+1
				if ctr>0 :
					sum=dec.Decimal(sum)/dec.Decimal(ctr)
				sum1=sum1+sum
			sum1=dec.Decimal(sum1)/dec.Decimal(len(data))
			sum2=sum2+sum1		
		sum2=dec.Decimal(sum2)/dec.Decimal(len(toks1))
		a=a+sum2
	a=dec.Decimal(a)/dec.Decimal(len(data))
	return a
