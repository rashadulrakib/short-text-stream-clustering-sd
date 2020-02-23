from sent_vecgenerator import generate_sent_vecs_toktextdata
from scipy.spatial import distance
import sys

def findCloseCluster_GramKey_lexical(keys_list, word_arr, minMatch):
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
  

def findCloseCluster_GramKey_Semantic(keys_list, word_arr, minMatch, wordVectorsDic):
  closeKey_Semantic=None
  sent_vec=generate_sent_vecs_toktextdata([word_arr], wordVectorsDic, 300)[0]
  min_dist=sys.float_info.max  
  for key in keys_list:
    key_words=key.split(' ')  
    key_vec=generate_sent_vecs_toktextdata([key_words], wordVectorsDic, 300)[0]
    eu_dist=distance.euclidean(sent_vec, key_vec)
    if min_dist>eu_dist:
      min_dist=eu_dist	
      closeKey_Semantic=key	  
    	
    	

  
  return closeKey_Semantic  
  