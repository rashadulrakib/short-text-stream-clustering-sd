from general_util import readlistWholeJsonDataSet
from clustering_sd import cluster_sd
from clustering_gram import cluster_gram_freq
from collections import Counter
from clustering_gram_util import filterClusters
from clustering_gram_util import assignToClusterBySimilarity
from evaluation_util import evaluateByGram
from dictionary_util import combineTwoDictionary

list_pred_true_words_index=readlistWholeJsonDataSet("News")




batchSize=2000
allTexts=len(list_pred_true_words_index)

batchNo=0

dictri_keys_selectedClusters_currentBatch={}
dicbi_keys_selectedClusters_currentBatch={}
not_clustered_inds_currentBatch=[]
not_clustered_inds_seen_batch=[]

for start in range(0,allTexts,batchSize): 
  batchNo+=1
  end= start+batchSize if start+batchSize<allTexts else allTexts  
  print(start, end)
  sub_list_pred_true_words_index=list_pred_true_words_index[start:end]
  print(len(sub_list_pred_true_words_index))
  #cluster_sd(sub_list_pred_true_words_index)
  dictri_keys_selectedClusters_currentBatch, dicbi_keys_selectedClusters_currentBatch, not_clustered_inds_currentBatch=cluster_gram_freq(sub_list_pred_true_words_index, batchNo, dictri_keys_selectedClusters_currentBatch, dicbi_keys_selectedClusters_currentBatch, not_clustered_inds_currentBatch, list_pred_true_words_index[0:end])
  
  dictri_keys_selectedClusters_currentBatch, dicbi_keys_selectedClusters_currentBatch, not_clustered_inds_currentBatch, dic_combined_keys_selectedClusters=filterClusters(dictri_keys_selectedClusters_currentBatch, dicbi_keys_selectedClusters_currentBatch, sub_list_pred_true_words_index)
  
  not_clustered_inds_seen_batch.extend(not_clustered_inds_currentBatch)
  
  if batchNo>=1: # and batchNo%2==0:
    dic_preds=assignToClusterBySimilarity(not_clustered_inds_seen_batch, list_pred_true_words_index[0:end], dic_combined_keys_selectedClusters)
    new_comb=combineTwoDictionary(dic_preds,dic_combined_keys_selectedClusters)	
    evaluateByGram(new_comb, list_pred_true_words_index[0:end])	
    not_clustered_inds_seen_batch=[]	
      
  
 
  
  
  
  
  

'''#temp evaluation
texts_clustered_sum=0
max_group_sum=0
bigger_clusters_tri=0
bigger_clusters_bi=0
for mergedKey, txtInds in dictri_keys_selectedClusters_currentBatch.items():
  #txtInds=list(set(txtInds))	
  #print("mergedKey->", mergedKey, txtInds)	
  texts_clustered_sum+=len(txtInds)
  if len(txtInds)>1: bigger_clusters_tri+=1  
  #print("txtInds-main", len(txtInds), txtInds)   
  true_label_list=[]
  for txtInd in txtInds:
    true_label_list.append(list_pred_true_words_index[txtInd][1])	
  max_group_sum+=max(Counter(true_label_list).values())
  #print("true_label_list", len(true_label_list), true_label_list)	
	
for mergedKey, txtInds in dicbi_keys_selectedClusters_currentBatch.items():
  #txtInds=list(set(txtInds))	
  #print("mergedKey->", mergedKey, txtInds)	
  texts_clustered_sum+=len(txtInds)
  if len(txtInds)>1: bigger_clusters_bi+=1   
  true_label_list=[]
  for txtInd in txtInds:
    true_label_list.append(list_pred_true_words_index[txtInd][1])	  
  max_group_sum+=max(Counter(true_label_list).values())
	
print("\nfinal not_clustered_inds", len(not_clustered_inds_currentBatch), max_group_sum, texts_clustered_sum, max_group_sum/texts_clustered_sum, "tri main-total cls#", len(dictri_keys_selectedClusters_currentBatch), "bi main-total cls#",len(dicbi_keys_selectedClusters_currentBatch), "bigger_clusters_tri", bigger_clusters_tri, "bigger_clusters_bi", bigger_clusters_bi)'''
  
  
  