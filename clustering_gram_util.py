import statistics
from collections import Counter

def mergeGroups(dictri_keys_selectedClusters, matchCount):
  max_group_sum_tri=0
  texts_clustered_by_tri=1

  return [max_group_sum_tri, texts_clustered_by_tri, dictri_keys_selectedClusters]

def clusterByNgram(dic_gram_to_textInds, gram_std, gram_mean, gram_std_csize_offset, dic_used_textIds, list_pred_true_words_index):
  print("-----gram calculation---------")  
  #find clusters based on gram
  dicgram_keys_selectedClusters={}
  dicgram_clusterSizes={}
  dicgram_keys_selectedNonEmptyClusters={}
  for gram, txtInds in dic_gram_to_textInds.items():
    size=len(dic_gram_to_textInds[gram])
    if size not in dicgram_clusterSizes: dicgram_clusterSizes[size]=0	
    dicgram_clusterSizes[size]+=1   
    if size>=gram_mean+gram_std and size<=gram_mean+gram_std+gram_std_csize_offset:
      dicgram_keys_selectedClusters[gram]=dic_gram_to_textInds[gram]
      #print(gram, dicgram_keys_selectedClusters[gram])
  #for key, size in dicgram_clusterSizes.items():
  #  print(key, size)
	
  dicgram_keys_selectedClusters={k: v for k, v in sorted(dicgram_keys_selectedClusters.items(), key=lambda item: item[1])}
  selectedClustersKeysList=list(dicgram_keys_selectedClusters.keys())
  texts_clustered_by_gram=0 
  max_group_sum_gram=0  
  for i in range(len(selectedClustersKeysList)):
    #remove previously used textIds
    i_txtIds=dicgram_keys_selectedClusters[selectedClustersKeysList[i]]	
    new_i_txtIds=[]
    for txtId in i_txtIds:
      if txtId not in dic_used_textIds:
        new_i_txtIds.append(txtId)	  
    dicgram_keys_selectedClusters[selectedClustersKeysList[i]]=new_i_txtIds	
    	
    common_txtIds_with_Others=[]	
    for j in range(i+1, len(selectedClustersKeysList)):  
      seti=set(dicgram_keys_selectedClusters[selectedClustersKeysList[i]])
      setj=set(dicgram_keys_selectedClusters[selectedClustersKeysList[j]])
      commonIds=list(seti.intersection(setj))
      common_txtIds_with_Others.extend(commonIds)
    	  
    filtered_txt_ids_i= []	
    for txt_id in dicgram_keys_selectedClusters[selectedClustersKeysList[i]]:
      if txt_id not in common_txtIds_with_Others:
        filtered_txt_ids_i.append(txt_id)
        dic_used_textIds[txt_id]=1	
    #print("\nfiltered_txt_ids_i", len(filtered_txt_ids_i), len(dicgram_keys_selectedClusters[selectedClustersKeysList[i]]), filtered_txt_ids_i, dicgram_keys_selectedClusters[selectedClustersKeysList[i]])
    dicgram_keys_selectedClusters[selectedClustersKeysList[i]]=filtered_txt_ids_i
    texts_clustered_by_gram+=len(filtered_txt_ids_i)	
 
    true_label_list=[] 
    print("selectedClustersKeysList[i]", selectedClustersKeysList[i])    	
    for txt_id in dicgram_keys_selectedClusters[selectedClustersKeysList[i]]:	
      print(list_pred_true_words_index[txt_id])
      true_label_list.append(list_pred_true_words_index[txt_id][1])	  
    if len(true_label_list)>0: 
      max_group_sum_gram+=max(Counter(true_label_list).values())
      dicgram_keys_selectedNonEmptyClusters[selectedClustersKeysList[i]]=dicgram_keys_selectedClusters[selectedClustersKeysList[i]]	  
	
  return [dic_used_textIds, max_group_sum_gram, texts_clustered_by_gram, dicgram_keys_selectedNonEmptyClusters]	
	

def populateNgramStatistics(dic_gram_to_textInds, minTxtIndsForNgram):
  ordered_keys_gram_to_textInds = sorted(dic_gram_to_textInds, key = lambda key: len(dic_gram_to_textInds[key]))
  txtIndsSize=[]
  for key in ordered_keys_gram_to_textInds:
    #print(key, dic_gram_to_textInds[key])
    if len(dic_gram_to_textInds[key])>minTxtIndsForNgram: txtIndsSize.append(len(dic_gram_to_textInds[key]))
  size_std=statistics.stdev(txtIndsSize)
  size_mean=statistics.mean(txtIndsSize) 
  size_max=max(txtIndsSize)  
  size_min=min(txtIndsSize)
  
  return [size_std, size_mean, size_max, size_min]