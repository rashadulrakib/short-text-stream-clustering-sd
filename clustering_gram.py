from txt_process_util import concatWordsSort
from collections import OrderedDict

def cluster_gram_freq(list_pred_true_words_index):
  dic_uniGram_to_textInds={}
  #dic_text_to_uniGrams={}
  dic_biGram_to_textInds={}
  #dic_text_to_biGrams={}
  i=-1
  for pred_true_words_index in list_pred_true_words_index:
    i+=1
    words=pred_true_words_index[2]
    for j in range(len(words)):
      dic_uniGram_to_textInds.setdefault(words[j],[]).append(i)
      #dic_text_to_uniGrams.setdefault(i,[]).append(words[j])  
      for k in range(j+1,len(words)):
        dic_biGram_to_textInds.setdefault(concatWordsSort([words[j], words[k]]),[]).append(i)   	  

  #print(dic_uniGram_to_textInds)
  ordered_dic_uniGram_to_textInds = sorted(dic_uniGram_to_textInds, key = lambda key: len(dic_uniGram_to_textInds[key]))
  
  for key in ordered_dic_uniGram_to_textInds:
    print(key, dic_uniGram_to_textInds[key])
	
  print("---------") 	
  
  ordered_dic_biGram_to_textInds = sorted(dic_biGram_to_textInds, key = lambda key: len(dic_biGram_to_textInds[key]))
  
  for key in ordered_dic_biGram_to_textInds:
    print(key, dic_biGram_to_textInds[key])
	
  print("##", len(ordered_dic_uniGram_to_textInds),
  len(ordered_dic_biGram_to_textInds)) 	
     
  
  
  