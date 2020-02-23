from collections import Counter

def evaluateByGram(dic_gramkeys_txtInds, seen_list_pred_true_words_index):
  texts_clustered_sum=0
  max_group_sum=0
  #bigger_clusters_tri=0
  #bigger_clusters_bi=0
  for mergedKey, txtInds in dic_gramkeys_txtInds.items():
    texts_clustered_sum+=len(txtInds)
    #if len(txtInds)>1: bigger_clusters_tri+=1  
    #print("txtInds-main", len(txtInds), txtInds)   
    true_label_list=[]
    for txtInd in txtInds:
      true_label_list.append(seen_list_pred_true_words_index[txtInd][1])	
    max_group_sum+=max(Counter(true_label_list).values())
    #print("true_label_list", len(true_label_list), true_label_list)
  
  print("batch-eval", max_group_sum, texts_clustered_sum, "accuracy", max_group_sum/texts_clustered_sum)