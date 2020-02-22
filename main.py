from general_util import readlistWholeJsonDataSet
from clustering_sd import cluster_sd
from clustering_gram import cluster_gram_freq
from collections import Counter

list_pred_true_words_index=readlistWholeJsonDataSet("News")


batchSize=2000
allTexts=len(list_pred_true_words_index)

batchNo=-1

dictri_keys_selectedClusters_currentBatch={}
dicbi_keys_selectedClusters_currentBatch={}
not_clustered_inds_currentBatch=[]

for start in range(0,allTexts,batchSize): 
  batchNo+=1
  end= start+batchSize if start+batchSize<allTexts else allTexts  
  print(start, end)
  sub_list_pred_true_words_index=list_pred_true_words_index[start:end]
  print(len(sub_list_pred_true_words_index))
  #cluster_sd(sub_list_pred_true_words_index)
  dictri_keys_selectedClusters_currentBatch, dicbi_keys_selectedClusters_currentBatch, not_clustered_inds_currentBatch=cluster_gram_freq(sub_list_pred_true_words_index, batchNo, dictri_keys_selectedClusters_currentBatch, dicbi_keys_selectedClusters_currentBatch, not_clustered_inds_currentBatch, list_pred_true_words_index[0:end])
  

#temp evaluation
texts_clustered_sum=0
max_group_sum=0
for mergedKey, txtInds in dictri_keys_selectedClusters_currentBatch.items():
  #txtInds=list(set(txtInds))	
  #print("mergedKey->", mergedKey, txtInds)	
  texts_clustered_sum+=len(txtInds)
  print("txtInds-main", len(txtInds), txtInds)   
  true_label_list=[]
  for txtInd in txtInds:
    true_label_list.append(list_pred_true_words_index[txtInd][1])	
    max_group_sum+=max(Counter(true_label_list).values())
  print("true_label_list", len(true_label_list), true_label_list)	
	
'''for mergedKey, txtInds in dicbi_keys_selectedClusters_currentBatch.items():
  #txtInds=list(set(txtInds))	
  #print("mergedKey->", mergedKey, txtInds)	
  texts_clustered_sum+=len(txtInds)
  true_label_list=[]
  for txtInd in txtInds:
    true_label_list.append(list_pred_true_words_index[txtInd][1])	  
    max_group_sum+=max(Counter(true_label_list).values())	'''
	
print("\nfinal not_clustered_inds", len(not_clustered_inds_currentBatch), max_group_sum, texts_clustered_sum, max_group_sum/texts_clustered_sum, "main-total cls#", len(dictri_keys_selectedClusters_currentBatch))


#  
  
  