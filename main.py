from general_util import readlistWholeJsonDataSet
from clustering_sd import cluster_sd
from clustering_gram import cluster_gram_freq

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
  
  