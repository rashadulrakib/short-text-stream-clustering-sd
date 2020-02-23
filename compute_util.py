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