def concatWordsSort(words):
  words.sort()
  combinedWord=' '.join(words)
  return combinedWord  

def createBinaryWordCooccurenceMatrix(listtuple_pred_true_text_ind):
  binGraph=[]
  uniqueWordList=set()  
  docWords=[]  
  for i in range(len(listtuple_pred_true_text_ind)):
    words=listtuple_pred_true_text_ind[i][2]
    uniqueWordList.update(words)
    docWords.append(words)
  
  dic_word_index={}
  i=-1 
  for word in uniqueWordList:
    i=i+1
    dic_word_index[word]=i	
   	
  m=len(uniqueWordList)	
  binGraph = [[0] * m for i in range(m)]
  for words in docWords:
    for i in range(1,len(words)):	  
      id1=dic_word_index[words[i-1]]
      id2=dic_word_index[words[i]]
      binGraph[id1][id2]=1 	      	  
   
  return [binGraph, dic_word_index, docWords] 