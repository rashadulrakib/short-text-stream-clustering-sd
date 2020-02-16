from txt_process_util import concatWordsSort

from collections import Counter
from clustering_gram_util import populateNgramStatistics
from clustering_gram_util import clusterByNgram

def cluster_gram_freq(list_pred_true_words_index):
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
  dic_used_textIds, max_group_sum_tri, texts_clustered_by_tri, dictri_keys_selectedClusters=clusterByNgram(dic_triGram_to_textInds, tri_std,tri_mean, tri_std_csize_offset, dic_used_textIds, list_pred_true_words_index)
  #max_group_sum_tri, texts_clustered_by_tri, dictri_keys_selectedClusters=mergeGroups(dictri_keys_selectedClusters, 2)
  
  
  dic_used_textIds, max_group_sum_bi, texts_clustered_by_bi, dicbi_keys_selectedClusters=clusterByNgram(dic_biGram_to_textInds, bi_std,bi_mean, bi_std_csize_offset, dic_used_textIds, list_pred_true_words_index)
  #max_group_sum_bi, texts_clustered_by_bi, dicbi_keys_selectedClusters=mergeGroups(dicbi_keys_selectedClusters, 1)
  
  #dic_used_textIds, max_group_sum_uni, texts_clustered_by_uni, dicuni_keys_selectedClusters=clusterByNgram(dic_uniGram_to_textInds, uni_std,uni_mean, uni_std_csize_offset, dic_used_textIds, list_pred_true_words_index)
  	

  print("###")
  #print("uni", len(dic_uniGram_to_textInds), "total cls#",len(dicuni_keys_selectedClusters), uni_min, uni_max, uni_mean, uni_std, "texts_clustered_by_uni", texts_clustered_by_uni, "max_group_sum_uni", max_group_sum_uni, max_group_sum_uni/texts_clustered_by_uni)
  print("tri", len(dic_triGram_to_textInds), "total cls#",len(dictri_keys_selectedClusters), tri_min, tri_max, tri_mean, tri_std, "texts_clustered_by_tri", texts_clustered_by_tri, "max_group_sum_tri", max_group_sum_tri, max_group_sum_tri/texts_clustered_by_tri)
  print("bi", len(dic_biGram_to_textInds), "total cls#",len(dicbi_keys_selectedClusters), bi_min, bi_max, bi_mean, bi_std, "texts_clustered_by_bi", texts_clustered_by_bi, "max_group_sum_bi", max_group_sum_bi, max_group_sum_bi/texts_clustered_by_bi) 
    
  
    
  
  
  