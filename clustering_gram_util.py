import statistics

def populateNgramStatistics(dic_gram_to_textInds, minTxtIndsForNgram):
  ordered_keys_gram_to_textInds = sorted(dic_gram_to_textInds, key = lambda key: len(dic_gram_to_textInds[key]))
  txtIndsSize=[]
  for key in ordered_keys_gram_to_textInds:
    #print(key, dic_gram_to_textInds[key])
    if len(dic_gram_to_textInds[key])>1: txtIndsSize.append(len(dic_gram_to_textInds[key]))
  size_std=statistics.stdev(txtIndsSize)
  size_mean=statistics.mean(txtIndsSize) 
  size_max=max(txtIndsSize)  
  size_min=min(txtIndsSize)
  
  return [size_std, size_mean, size_max, size_min]