from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

from txt_process_util import createBinaryWordCooccurenceMatrix

def clusterByConnectedComponentWordCooccurIndex(pred_true_txt_inds):
  _components=0,
  newPred_OldPred_true_text_inds=[]
  
  
  word_binGraph, dic_word_index, docWords=createBinaryWordCooccurenceMatrix(pred_true_txt_inds)
  word_graph = csr_matrix(word_binGraph)
  
  _components, word_preds = connected_components(csgraph=word_graph, directed=False, return_labels=True)
  
  for i in range(len(pred_true_txt_inds)):
    pred_true_text_ind=pred_true_txt_inds[i]
    
    oldPredLabel=pred_true_text_ind[0]
    trueLabel=pred_true_text_ind[1]
    wordArr=docWords[i] 
    ind=pred_true_text_ind[3]
	
    if len(wordArr)==0:
      continue	
    wordId=dic_word_index[wordArr[0]]
    newPredLabel=word_preds[wordId]	
    
    newPred_OldPred_true_text_inds.append([newPredLabel, oldPredLabel, trueLabel, wordArr, ind])

  return [_components, newPred_OldPred_true_text_inds]