from groupTxt_ByClass import groupItemsBySingleKeyIndex
from sklearn import metrics
import re

minIntVal = -1000000

dataFileTxtTrue = "/home/owner/PhD/dr.norbert/dataset/shorttext/data-web-snippets/stc2/Stc2TrueBody"
extClustFile = "/home/owner/PhD/dr.norbert/dataset/shorttext/data-web-snippets/stc2/Stc2Preds"
dataFilePredTrueTxt="/home/owner/PhD/MStream-master/MStream/result/NewsPredTueTextMStream_WordArr.txt"

dataFilePredTrueTxt="/home/owner/PhD/MStream-master/MStream/result/mstr-enh"

def ComputePurity(dic_tupple_class):
 totalItems=0
 maxGroupSizeSum =0
 for label, pred_true_txts in dic_tupple_class.items():
  totalItems=totalItems+len(pred_true_txts)
  #print("pred label="+label+", #texts="+str(len(pred_true_txts)))
  dic_tupple_class_originalLabel=groupItemsBySingleKeyIndex(pred_true_txts, 1)
  maxMemInGroupSize=-1000000
  maxMemOriginalLabel=""
  for orgLabel, org_pred_true_txts in dic_tupple_class_originalLabel.items():
   #print("orgLabel label="+orgLabel+", #texts="+str(len(org_pred_true_txts)))
   if maxMemInGroupSize < len(org_pred_true_txts):
    maxMemInGroupSize=len(org_pred_true_txts)
    maxMemOriginalLabel=orgLabel
  
  #print("\n")
  #print(str(label)+" purity="+str(maxMemInGroupSize/len(pred_true_txts))+", items="+str(len(pred_true_txts))+", max match#="+str(maxMemInGroupSize))
  #print_by_group(pred_true_txts)  
  maxGroupSizeSum=maxGroupSizeSum+maxMemInGroupSize
  
 purity=maxGroupSizeSum/float(totalItems)
 print("purity majority whole data="+str(purity))
 return purity


def Evaluate(listtuple_pred_true_text):
 print("evaluate total texts="+str(len(listtuple_pred_true_text)))
 preds = []
 trues = []
 for pred_true_text in listtuple_pred_true_text:
  preds.append(pred_true_text[0])
  trues.append(pred_true_text[1])
 
 score = metrics.homogeneity_score(trues, preds)  
 print ("homogeneity_score-whole-data:   %0.8f" % score)

 score=metrics.completeness_score(trues, preds)
 print ("completeness_score-whole-data:   %0.8f" % score)
 
 #score=metrics.v_measure_score(trues, preds)
 #print ("v_measure_score-whole-data:   %0.4f" % score)
 
 score = metrics.normalized_mutual_info_score(trues, preds, average_method='arithmetic' )  
 print ("nmi_score-whole-data:   %0.8f" % score)
 
 #score=metrics.adjusted_mutual_info_score(trues, preds)
 #print ("adjusted_mutual_info_score-whole-data:   %0.4f" % score)
 
 #score=metrics.adjusted_rand_score(trues, preds)
 #print ("adjusted_rand_score-whole-data:   %0.4f" % score)
 
 
 dic_tupple_class=groupItemsBySingleKeyIndex(listtuple_pred_true_text, 0)
 dic_tupple_class_true=groupItemsBySingleKeyIndex(listtuple_pred_true_text, 1)  
 print ("pred clusters="+str(len(dic_tupple_class))+", true clusters="+str(len(dic_tupple_class_true)))
 ComputePurity(dic_tupple_class)
 '''print("---Pred distribution")
 for key,value in dic_tupple_class.items():
   print(key, len(value))
 print("---True distribution")
 for key,value in dic_tupple_class_true.items():
   print(key, len(value))''' 
 

