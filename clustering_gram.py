from txt_process_util import concatWordsSort

from collections import Counter
from clustering_gram_util import populateNgramStatistics
from clustering_gram_util import clusterByNgram
from clustering_gram_util import mergeGroups
from clustering_gram_util import extractNotClusteredItems
from clustering_gram_util import assignToMergedClusters
from clustering_gram_util import mergeWithPrevBatch

def cluster_gram_freq(list_pred_true_words_index, batchNo, dictri_keys_selectedClusters_prevBatch={}, dicbi_keys_selectedClusters_prevBatch={}, not_clustered_inds_prevBatch=[], seen_list_pred_true_words_index=[]):
  dic_uniGram_to_textInds={}
  dic_biGram_to_textInds={}
  dic_triGram_to_textInds={}
  uni_std_csize_offset=50000
  bi_std_csize_offset=1000000
  tri_std_csize_offset=100000  
  i=-1
  for pred_true_words_index in list_pred_true_words_index:
    i+=1
    words=pred_true_words_index[2]
    for j in range(len(words)):
      dic_uniGram_to_textInds.setdefault(words[j],[]).append(i) 
      for k in range(j+1,len(words)):
        dic_biGram_to_textInds.setdefault(concatWordsSort([words[j], words[k]]),[]).append(i)
        for l in range(k+1, len(words)):
          dic_triGram_to_textInds.setdefault(concatWordsSort([words[j], words[k], words[l]]),[]).append(i)		

  uni_std,uni_mean,uni_max,uni_min=populateNgramStatistics(dic_uniGram_to_textInds, 1)
  bi_std,bi_mean,bi_max,bi_min=populateNgramStatistics(dic_biGram_to_textInds, 1)
  tri_std,tri_mean,tri_max,tri_min=populateNgramStatistics(dic_triGram_to_textInds, 1)  
  
  dic_used_textIds={}
  dic_used_textIds, max_group_sum_tri, texts_clustered_by_tri, dictri_keys_selectedClusters=clusterByNgram(dic_triGram_to_textInds,tri_mean, tri_mean+tri_std+tri_std_csize_offset, dic_used_textIds, list_pred_true_words_index)
  
  dic_used_textIds, max_group_sum_bi, texts_clustered_by_bi, dicbi_keys_selectedClusters=clusterByNgram(dic_biGram_to_textInds, bi_mean+bi_std, bi_mean+bi_std+bi_std_csize_offset, dic_used_textIds, list_pred_true_words_index)
 
  print("###")
  print("tri", len(dic_triGram_to_textInds), "total cls#",len(dictri_keys_selectedClusters), tri_min, tri_max, tri_mean, tri_std, "texts_clustered_by_tri", texts_clustered_by_tri, "max_group_sum_tri", max_group_sum_tri, max_group_sum_tri/texts_clustered_by_tri)
  print("bi", len(dic_biGram_to_textInds), "total cls#",len(dicbi_keys_selectedClusters), bi_min, bi_max, bi_mean, bi_std, "texts_clustered_by_bi", texts_clustered_by_bi, "max_group_sum_bi", max_group_sum_bi, max_group_sum_bi/texts_clustered_by_bi) 
  
  
  print("mergekeys###")
  max_group_sum_tri, texts_clustered_by_tri, dictri_keys_selectedClusters=mergeGroups(dictri_keys_selectedClusters, 2, list_pred_true_words_index)
  max_group_sum_bi, texts_clustered_by_bi, dicbi_keys_selectedClusters=mergeGroups(dicbi_keys_selectedClusters, 1, list_pred_true_words_index)
  
  print("tri", len(dic_triGram_to_textInds), "merged total cls#",len(dictri_keys_selectedClusters), tri_min, tri_max, tri_mean, tri_std, "texts_clustered_by_tri", texts_clustered_by_tri, "max_group_sum_tri", max_group_sum_tri, max_group_sum_tri/texts_clustered_by_tri)
  print("bi", len(dic_biGram_to_textInds), "merged total cls#",len(dicbi_keys_selectedClusters), bi_min, bi_max, bi_mean, bi_std, "texts_clustered_by_bi", texts_clustered_by_bi, "max_group_sum_bi", max_group_sum_bi, max_group_sum_bi/texts_clustered_by_bi)
  
  #merge with prev batcches
  #dictri_keys_selectedClusters=mergeWithPrevBatch(dictri_keys_selectedClusters, dictri_keys_selectedClusters_prevBatch)
  #dicbi_keys_selectedClusters=mergeWithPrevBatch(dicbi_keys_selectedClusters, dicbi_keys_selectedClusters_prevBatch)  
  
  #merge with prev batcches
  
  print("###txtIds not in merged clusters###")
  not_clustered_inds=extractNotClusteredItems(list_pred_true_words_index, [dictri_keys_selectedClusters, dicbi_keys_selectedClusters])
  
  print("###assign non clustered to merged clusters###")
  new_dicTriMerged_keys_selectedClusters, not_clustered_inds_tri=assignToMergedClusters(list_pred_true_words_index, not_clustered_inds, dictri_keys_selectedClusters, 2)
  #new_dicBiMerged_keys_selectedClusters, not_clustered_inds_bi=assignToMergedClusters(list_pred_true_words_index, not_clustered_inds_tri, dicbi_keys_selectedClusters, 2)
  
  return [new_dicTriMerged_keys_selectedClusters, dicbi_keys_selectedClusters, not_clustered_inds_tri]
  #return [dictri_keys_selectedClusters_batch, ]
    
  
    
  
    
  
  
  