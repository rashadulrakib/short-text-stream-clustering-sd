def generate_sent_vecs_toktextdata(docsWords, termsVectorsDic, dim=300):
 toktextdatavecs = []
 #if len(termsVectorsDic)>0:
 # dim=len(termsVectorsDic.items) 

 for i in range(len(docsWords)): 
  words = docsWords[i]
  sum_vecs = [0] * dim
  missingCount=0  
  for word in words:
   if word in termsVectorsDic:
     for j in range(len(sum_vecs)):
       sum_vecs[j]=(sum_vecs[j]+termsVectorsDic[word][j])
   else:
     missingCount=missingCount+1   
  
  #to use   
  for j in range(len(sum_vecs)):
    sum_vecs[j]=sum_vecs[j]/(len(words)-missingCount+1)
  #end to use   
  #if missingCount>0:  
  #  print("missing Word Count="+str(missingCount)+", original len="+str(len(words)))
  toktextdatavecs.append(sum_vecs)  
    
 return toktextdatavecs
 
	
    	
    	
      
