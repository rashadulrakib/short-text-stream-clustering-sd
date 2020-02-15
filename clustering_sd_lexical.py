from cluster_file_connected_component import clusterByConnectedComponentWordCooccurIndex
from general_util import print_by_group

def cluster_sd_lexical(list_pred_true_words_index):

  print("cluster_sd_lexical", len(list_pred_true_words_index))

  _components, newPred_OldPred_true_words_inds=clusterByConnectedComponentWordCooccurIndex(list_pred_true_words_index)
  print(_components)
  print_by_group(newPred_OldPred_true_words_inds, 2)    
    
    
  
  #for i in range(len(idList)):
  #  for j in range(i+1,len(idList)):
  #    print(sub_dic_id_trueWords[idList[i]], sub_dic_id_trueWords[idList[j]])
      	  
  