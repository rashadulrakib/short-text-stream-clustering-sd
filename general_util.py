from groupTxt_ByClass import groupItemsBySingleKeyIndex

def print_by_group(listtuple_pred_true_text, grIndex):
  dic_tupple_class=groupItemsBySingleKeyIndex(listtuple_pred_true_text, grIndex)
  for label, pred_true_txts in sorted(dic_tupple_class.items()):
    Print_list_pred_true_text(pred_true_txts)
  print("total groups=", len(dic_tupple_class))	
  
def Print_list_pred_true_text(listtuple_pred_true_text):
  for pred_true_text in listtuple_pred_true_text:
    print(pred_true_text)

def readlistWholeJsonDataSet(datasetName):
  file1=open(datasetName,"r")
  lines = file1.readlines()
  file1.close()
  list_pred_true_words_index=[]
  i=-1  
  for line in lines:
    line=line.strip()  
    n = eval(line)
    id=str(n['Id']).strip()  
    true=str(n['clusterNo']).strip()
    words=str(n['textCleaned']).strip().split(' ')
    if len(true)==0 or len(words)==0:
      continue
    i+=1 	  
    list_pred_true_words_index.append([-1, true, words, i])
  return list_pred_true_words_index
  
def readDicWholeJsonDataSet(datasetName):
  file1=open(datasetName,"r")
  lines = file1.readlines()
  file1.close()
  dic_id_trueWords={}
  for line in lines:
    line=line.strip()  
    n = eval(line)
    id=str(n['Id']).strip()  
    true=str(n['clusterNo']).strip()
    words=str(n['textCleaned']).strip().split(' ')
    if len(true)==0 or len(words)==0:
      continue 	
    dic_id_trueWords[id]=[true, words]
  return dic_id_trueWords