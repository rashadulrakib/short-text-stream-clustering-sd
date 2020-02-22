import statistics
from collections import Counter
import numpy as np

def mergeWithPrevBatch(dic_keys_selectedClusters, dic_keys_selectedClusters_prevBatch):
  if len(dic_keys_selectedClusters_prevBatch)==0:
    return dic_keys_selectedClusters
  new_dic_keys_selectedClusters={} 	
  #print("mergeWithPrevBatch", len(dic_keys_selectedClusters_prevBatch))  

  for key, txtInds in dic_keys_selectedClusters.items():
    new_dic_keys_selectedClusters[key]=txtInds
	
  for key, prev_txtInds in dic_keys_selectedClusters_prevBatch.items():
    if key in new_dic_keys_selectedClusters:
      new_txtInds = new_dic_keys_selectedClusters[key]
      combined_txtInds=list(set(prev_txtInds+new_txtInds))
      new_dic_keys_selectedClusters[key]=combined_txtInds
    else:
      new_dic_keys_selectedClusters[key]=prev_txtInds	
      	  
  	
  return new_dic_keys_selectedClusters	

def findCloseCluster_GramKey(keys_list, word_arr, minMatch):
  closeKey_Lexical=None
  maxCommonLength=0
  
  for key in keys_list:
    set1=set(key.split(' '))
    set2=set(word_arr)
    common=set1.intersection(set2)
    if len(common)>=minMatch and len(common)>maxCommonLength:
      maxCommonLength=len(common)
      #arr =list(common)
      #arr.sort()	  
      closeKey_Lexical=key	  
  
  return closeKey_Lexical

def assignToMergedClusters(list_pred_true_words_index, not_clustered_inds,dicMerged_keys_selectedClusters, minMatch):
  #new_dicMerged_keys_selectedClusters={} #key =[txtInds w.r.t to sublist list_pred_true_words_index]
  new_not_clustered_inds=[]
  keys_list=list(dicMerged_keys_selectedClusters.keys())
  for txtInd in not_clustered_inds:
    item=list_pred_true_words_index[txtInd]
    word_arr=item[2]
    closeKey_Lexical=findCloseCluster_GramKey(keys_list, word_arr, minMatch)
    if closeKey_Lexical==None:
      new_not_clustered_inds.append(txtInd)
    else:
      #print("list before close key", dicMerged_keys_selectedClusters[closeKey_Lexical])  
      print("closeKey_Lexical", closeKey_Lexical+",", list_pred_true_words_index[txtInd])	  
      new_list=dicMerged_keys_selectedClusters[closeKey_Lexical]
      new_list.append(txtInd)      	  
      dicMerged_keys_selectedClusters[closeKey_Lexical]=new_list
      for lid in new_list:
        print("new_list,", list_pred_true_words_index[lid])	  
      #print("list after close key", dicMerged_keys_selectedClusters[closeKey_Lexical])

  texts_clustered_sum=0
  max_group_sum=0
  for mergedKey, txtInds in dicMerged_keys_selectedClusters.items():
    #txtInds=list(set(txtInds))	
    #print("mergedKey->", mergedKey, txtInds)	
    texts_clustered_sum+=len(txtInds)
    true_label_list=[]
    for txtInd in txtInds:
      true_label_list.append(list_pred_true_words_index[txtInd][1])
      #print(list_pred_true_words_index[txtInd])		
    max_group_sum+=max(Counter(true_label_list).values())

  	
	
  print("\nnew_not_clustered_inds", len(new_not_clustered_inds), max_group_sum, texts_clustered_sum, max_group_sum/texts_clustered_sum, "old_not_clustered_inds", len(not_clustered_inds)) 	
  return [dicMerged_keys_selectedClusters, new_not_clustered_inds]

def extractNotClusteredItems(list_pred_true_words_index, list_dic_keys_selectedClusters):
  not_clustered_inds=[]
  
  list_clustered_inds=[]
  for dic_keys_selectedClusters in list_dic_keys_selectedClusters:
    for gramkey, txtInds in dic_keys_selectedClusters.items():
      list_clustered_inds.extend(txtInds)
  list_clustered_inds=set(list_clustered_inds)
  
  for i in range(len(list_pred_true_words_index)):
    if i in list_clustered_inds:
      continue
    not_clustered_inds.append(i)
    print("not clustered", list_pred_true_words_index[i])

  print("len(not_clustered_inds)", len(not_clustered_inds))	
  	  
  return not_clustered_inds

def mergeGroups(dicgram_keys_selectedClusters, matchCount, list_pred_true_words_index):
  max_group_sum=0
  texts_clustered_sum=0
  new_dic_keys_selectedClusters={}
  dic_used_key={}  
  keys=list(dicgram_keys_selectedClusters.keys())
  #print("keys", keys) 
  
  for i in range(len(keys)):
    #print("list(dic_used_key.keys())", list(dic_used_key.keys()))
    if keys[i] in list(dic_used_key.keys()):	
      continue	
    list_used_keys=[] 	  
    dic_used_key[keys[i]]=1	
    for j in range(i+1, len(keys)):
      if keys[j] in list(dic_used_key.keys()):	
        continue	
      seti=set(keys[i].split(' '))
      setj=set(keys[j].split(' '))
      commonWords=seti.intersection(setj)
      if len(commonWords)==matchCount:
        dic_used_key[keys[j]]=1
        list_used_keys.append(keys[j])			
    		
    if len(list_used_keys)>0:
      
      list_used_keys.append(keys[i])
      #list_key_words=[] 	  
      list_key_values=[]	  
      for key in list_used_keys:
        #list_key_words.extend(key.split(' '))
        list_key_values.extend(dicgram_keys_selectedClusters[key])
      #list_key_words.sort()
      #list_key_words=set(list_key_words)	  
      #mergedKey=' '.join(list_key_words)
      #new_dic_keys_selectedClusters[mergedKey]=list_key_values	  
      new_dic_keys_selectedClusters[keys[i]]=list_key_values	  	  
      #print(mergedKey)	  
    else:
      new_dic_keys_selectedClusters[keys[i]]=dicgram_keys_selectedClusters[keys[i]]  
    
  for mergedKey, txtInds in new_dic_keys_selectedClusters.items():
    #txtInds=list(set(txtInds))	
    print("mergedKey->", mergedKey, txtInds)	
    texts_clustered_sum+=len(txtInds)
    true_label_list=[]
    for txtInd in txtInds:
      true_label_list.append(list_pred_true_words_index[txtInd][1])
      print(list_pred_true_words_index[txtInd])		
    max_group_sum+=max(Counter(true_label_list).values())	        		
      	  
  return [max_group_sum, texts_clustered_sum, new_dic_keys_selectedClusters]

def clusterByNgram(dic_gram_to_textInds, minSize, maxSize, dic_used_textIds, list_pred_true_words_index):
  print("-----gram calculation---------")  
  #find clusters based on gram
  dicgram_keys_selectedClusters={}
  dicgram_clusterSizes={}
  dicgram_keys_selectedNonEmptyClusters={}
  for gram, txtInds in dic_gram_to_textInds.items():
    size=len(dic_gram_to_textInds[gram])
    if size not in dicgram_clusterSizes: dicgram_clusterSizes[size]=0	
    dicgram_clusterSizes[size]+=1   
    if size>=minSize and size<=maxSize:
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
    for txtInd in dicgram_keys_selectedClusters[selectedClustersKeysList[i]]:	
      print(list_pred_true_words_index[txtInd])
      true_label_list.append(list_pred_true_words_index[txtInd][1])	  
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