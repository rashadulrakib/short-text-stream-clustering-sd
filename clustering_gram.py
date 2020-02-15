from txt_process_util import concatWordsSort
import statistics


def cluster_gram_freq(list_pred_true_words_index):
  dic_uniGram_to_textInds={}
  dic_biGram_to_textInds={}
  dic_triGram_to_textInds={}
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

  ordered_keys_uniGram_to_textInds = sorted(dic_uniGram_to_textInds, key = lambda key: len(dic_uniGram_to_textInds[key]))
  uni_value_sizes=[]
  for key in ordered_keys_uniGram_to_textInds:
    #print(key, dic_uniGram_to_textInds[key])
    if len(dic_uniGram_to_textInds[key])>1: uni_value_sizes.append(len(dic_uniGram_to_textInds[key]))
  uni_std=statistics.stdev(uni_value_sizes)
  uni_mean=statistics.mean(uni_value_sizes) 
  uni_max=max(uni_value_sizes)  
  uni_min=min(uni_value_sizes)  
	
  #print("---------") 	
  
  ordered_keys_biGram_to_textInds = sorted(dic_biGram_to_textInds, key = lambda key: len(dic_biGram_to_textInds[key]))
  bi_value_sizes=[]
  for key in ordered_keys_biGram_to_textInds:
    #print(key, dic_biGram_to_textInds[key])
    if len(dic_biGram_to_textInds[key])>1: bi_value_sizes.append(len(dic_biGram_to_textInds[key]))	
  bi_std=statistics.stdev(bi_value_sizes)
  bi_mean=statistics.mean(bi_value_sizes) 
  bi_max=max(bi_value_sizes)  
  bi_min=min(bi_value_sizes) 


  ordered_keys_triGram_to_textInds = sorted(dic_triGram_to_textInds, key = lambda key: len(dic_triGram_to_textInds[key]))
  tri_value_sizes=[]
  for key in ordered_keys_triGram_to_textInds:
    #print(key, dic_uniGram_to_textInds[key])
    if len(dic_triGram_to_textInds[key])>1: tri_value_sizes.append(len(dic_triGram_to_textInds[key]))
  tri_std=statistics.stdev(tri_value_sizes)
  tri_mean=statistics.mean(tri_value_sizes) 
  tri_max=max(tri_value_sizes)  
  tri_min=min(tri_value_sizes)  
	
  print("-----uni-gram calculation---------")     
  #find clusters based on uni
  dicUni_keys_selectedClusters={}
  dicUni_clusterSizes={}
  for uni, txtInds in dic_uniGram_to_textInds.items():
    size=len(dic_uniGram_to_textInds[uni])
    if size not in dicUni_clusterSizes: dicUni_clusterSizes[size]=0	
    dicUni_clusterSizes[size]+=1   
    if size>=uni_mean+uni_std and size<=uni_mean+uni_std+2:
      dicUni_keys_selectedClusters[uni]=dic_uniGram_to_textInds[uni]
      print(uni, dicUni_keys_selectedClusters[uni])
  for key, size in dicUni_clusterSizes.items():
    print(key, size)
	
  dic_used_textIds={}	
  dicUni_keys_selectedClusters={k: v for k, v in sorted(dicUni_keys_selectedClusters.items(), key=lambda item: item[1])}
  selectedClustersKeysList=list(dicUni_keys_selectedClusters.keys())
  texts_clustered_by_uni=0  
  for i in range(len(selectedClustersKeysList)):
    #remove previously used textIds
    i_txtIds=dicUni_keys_selectedClusters[selectedClustersKeysList[i]]	
    new_i_txtIds=[]
    for txtId in i_txtIds:
      if txtId not in dic_used_textIds:
        new_i_txtIds.append(txtId)	  
    dicUni_keys_selectedClusters[selectedClustersKeysList[i]]=new_i_txtIds	
    	
	
    common_txtIds_with_Others=[]	
    for j in range(i+1, len(selectedClustersKeysList)):  
      seti=set(dicUni_keys_selectedClusters[selectedClustersKeysList[i]])
      setj=set(dicUni_keys_selectedClusters[selectedClustersKeysList[j]])
      commonIds=list(seti.intersection(setj))
      common_txtIds_with_Others.extend(commonIds)
    	  
    filtered_txt_ids_i= []	
    for txt_id in dicUni_keys_selectedClusters[selectedClustersKeysList[i]]:
      if txt_id not in common_txtIds_with_Others:
        filtered_txt_ids_i.append(txt_id)
        dic_used_textIds[txt_id]=1	
    print("\nfiltered_txt_ids_i", len(filtered_txt_ids_i), len(dicUni_keys_selectedClusters[selectedClustersKeysList[i]]), filtered_txt_ids_i, dicUni_keys_selectedClusters[selectedClustersKeysList[i]])
    dicUni_keys_selectedClusters[selectedClustersKeysList[i]]=filtered_txt_ids_i
    texts_clustered_by_uni+=len(filtered_txt_ids_i)	
    	

    print("selectedClustersKeysList[i]", selectedClustersKeysList[i])
    	
    for txt_id in dicUni_keys_selectedClusters[selectedClustersKeysList[i]]: 
	
      print(list_pred_true_words_index[txt_id])
	
  
  print("-----bi-gram calculation---------")  
	  
  dicBi_keys_selectedClusters={}
  dicBi_clusterSizes={}
  for bi, txtInds in dic_biGram_to_textInds.items():
    size=len(dic_biGram_to_textInds[bi])
    if size not in dicBi_clusterSizes: dicBi_clusterSizes[size]=0	
    dicBi_clusterSizes[size]+=1   
    if size>=bi_mean+bi_std and size<=bi_mean+bi_std+2:
      dicBi_keys_selectedClusters[bi]=dic_biGram_to_textInds[bi]
      print(bi, dicBi_keys_selectedClusters[bi])
  for key, size in dicBi_clusterSizes.items():
    print(key, size)
	
  dic_used_textIds={}	
  dicBi_keys_selectedClusters={k: v for k, v in sorted(dicBi_keys_selectedClusters.items(), key=lambda item: item[1])}
  selectedClustersKeysList=list(dicBi_keys_selectedClusters.keys())
  texts_clustered_by_bi=0
  for i in range(len(selectedClustersKeysList)):
    #remove previously used textIds
    i_txtIds=dicBi_keys_selectedClusters[selectedClustersKeysList[i]]	
    new_i_txtIds=[]
    for txtId in i_txtIds:
      if txtId not in dic_used_textIds:
        new_i_txtIds.append(txtId)	  
    dicBi_keys_selectedClusters[selectedClustersKeysList[i]]=new_i_txtIds	
    	
	
    common_txtIds_with_Others=[]	
    for j in range(i+1, len(selectedClustersKeysList)):  
      seti=set(dicBi_keys_selectedClusters[selectedClustersKeysList[i]])
      setj=set(dicBi_keys_selectedClusters[selectedClustersKeysList[j]])
      commonIds=list(seti.intersection(setj))
      common_txtIds_with_Others.extend(commonIds)
    	  
    filtered_txt_ids_i= []
    for txt_id in dicBi_keys_selectedClusters[selectedClustersKeysList[i]]:
      if txt_id not in common_txtIds_with_Others:
        filtered_txt_ids_i.append(txt_id)
        dic_used_textIds[txt_id]=1	
    print("\nfiltered_txt_ids_i", len(filtered_txt_ids_i), len(dicBi_keys_selectedClusters[selectedClustersKeysList[i]]), filtered_txt_ids_i, dicBi_keys_selectedClusters[selectedClustersKeysList[i]])
    dicBi_keys_selectedClusters[selectedClustersKeysList[i]]=filtered_txt_ids_i
    texts_clustered_by_bi+=len(filtered_txt_ids_i)	

    print("selectedClustersKeysList[i]", selectedClustersKeysList[i])
    for txt_id in dicBi_keys_selectedClusters[selectedClustersKeysList[i]]: 
	
      print(list_pred_true_words_index[txt_id])	 


  print("-----tri-gram calculation---------")     
  #find clusters based on tri
  dicUni_keys_selectedClusters={}
  dicUni_clusterSizes={}
  for uni, txtInds in dic_uniGram_to_textInds.items():
    size=len(dic_uniGram_to_textInds[uni])
    if size not in dicUni_clusterSizes: dicUni_clusterSizes[size]=0	
    dicUni_clusterSizes[size]+=1   
    if size>=uni_mean+uni_std and size<=uni_mean+uni_std+2:
      dicUni_keys_selectedClusters[uni]=dic_uniGram_to_textInds[uni]
      print(uni, dicUni_keys_selectedClusters[uni])
  for key, size in dicUni_clusterSizes.items():
    print(key, size)
	
  dic_used_textIds={}	
  dicUni_keys_selectedClusters={k: v for k, v in sorted(dicUni_keys_selectedClusters.items(), key=lambda item: item[1])}
  selectedClustersKeysList=list(dicUni_keys_selectedClusters.keys())
  texts_clustered_by_uni=0  
  for i in range(len(selectedClustersKeysList)):
    #remove previously used textIds
    i_txtIds=dicUni_keys_selectedClusters[selectedClustersKeysList[i]]	
    new_i_txtIds=[]
    for txtId in i_txtIds:
      if txtId not in dic_used_textIds:
        new_i_txtIds.append(txtId)	  
    dicUni_keys_selectedClusters[selectedClustersKeysList[i]]=new_i_txtIds	
    	
	
    common_txtIds_with_Others=[]	
    for j in range(i+1, len(selectedClustersKeysList)):  
      seti=set(dicUni_keys_selectedClusters[selectedClustersKeysList[i]])
      setj=set(dicUni_keys_selectedClusters[selectedClustersKeysList[j]])
      commonIds=list(seti.intersection(setj))
      common_txtIds_with_Others.extend(commonIds)
    	  
    filtered_txt_ids_i= []	
    for txt_id in dicUni_keys_selectedClusters[selectedClustersKeysList[i]]:
      if txt_id not in common_txtIds_with_Others:
        filtered_txt_ids_i.append(txt_id)
        dic_used_textIds[txt_id]=1	
    print("\nfiltered_txt_ids_i", len(filtered_txt_ids_i), len(dicUni_keys_selectedClusters[selectedClustersKeysList[i]]), filtered_txt_ids_i, dicUni_keys_selectedClusters[selectedClustersKeysList[i]])
    dicUni_keys_selectedClusters[selectedClustersKeysList[i]]=filtered_txt_ids_i
    texts_clustered_by_uni+=len(filtered_txt_ids_i)	
    	

    print("selectedClustersKeysList[i]", selectedClustersKeysList[i])
    	
    for txt_id in dicUni_keys_selectedClusters[selectedClustersKeysList[i]]: 
	
      print(list_pred_true_words_index[txt_id])	  
	  
     	
     
	  
	  
  
  	

  
  
  
  
  
  
  
  
  
  print("###\nuni", len(ordered_keys_uniGram_to_textInds), len(dicUni_keys_selectedClusters), uni_min, uni_max, uni_mean, uni_std, "texts_clustered_by_uni", texts_clustered_by_uni)
  print("bi", len(ordered_keys_biGram_to_textInds), bi_min, bi_max, bi_mean, bi_std, "texts_clustered_by_bi", texts_clustered_by_bi)	  
    
  
    
  
  
  