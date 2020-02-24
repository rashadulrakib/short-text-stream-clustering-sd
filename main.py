from general_util import readlistWholeJsonDataSet
from clustering_sd import cluster_sd
from clustering_gram import cluster_gram_freq
from collections import Counter
from clustering_gram_util import filterClusters
from clustering_gram_util import assignToClusterBySimilarity
from evaluation_util import evaluateByGram
from dictionary_util import combineTwoDictionary
from word_vec_extractor import extractAllWordVecs
from print_cluster_evaluation import appendResultFile
import os
from evaluation import Evaluate
from read_pred_true_text import ReadPredTrueText

gloveFile = "/home/owner/PhD/dr.norbert/dataset/shorttext/glove.42B.300d/glove.42B.300d.txt"
wordVectorsDic={}
#wordVectorsDic = extractAllWordVecs(gloveFile, 300)

list_pred_true_words_index=readlistWholeJsonDataSet("Tweets")
fileName="Tweets_clusters"
fileName_to_assigned="Tweets_clusters_to-assign"

if os.path.exists(fileName):
  os.remove(fileName)
if os.path.exists(fileName_to_assigned):
  os.remove(fileName_to_assigned)  




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
  
  #texts in cluster and texts not in cluster should be =2000
  dictri_keys_selectedClusters_currentBatch, dicbi_keys_selectedClusters_currentBatch, not_clustered_inds_currentBatch, dic_combined_keys_selectedClusters, new_sub_list_pred_true_words_index=filterClusters(dictri_keys_selectedClusters_currentBatch, dicbi_keys_selectedClusters_currentBatch, sub_list_pred_true_words_index, list_pred_true_words_index[0:end])
  
  not_clustered_inds_seen_batch.extend(not_clustered_inds_currentBatch)
  
  appendResultFile(new_sub_list_pred_true_words_index, fileName)
  
  if batchNo>=1: # and batchNo%2==0:
    dic_preds, new_not_clustered_inds_seen_batch=assignToClusterBySimilarity(not_clustered_inds_seen_batch, list_pred_true_words_index[0:end], dic_combined_keys_selectedClusters, wordVectorsDic)
	
    #appendResultFile(new_not_clustered_inds_seen_batch, fileName)
    appendResultFile(new_not_clustered_inds_seen_batch, fileName_to_assigned)	
    	
	
    #new_comb=combineTwoDictionary(dic_preds,dic_combined_keys_selectedClusters, False)	
    #evaluateByGram(new_comb, list_pred_true_words_index[0:end])	
    not_clustered_inds_seen_batch=[]

listtuple_pred_true_text=ReadPredTrueText(fileName)
Evaluate(listtuple_pred_true_text)	
      
  