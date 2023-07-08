def jaccard(list1, list2):
  '''
  simple jaccard distance realization
  '''
  list1, list2 = list(list1), list(list2)
  intersection = len([x1==x2 for (x1,x2) in zip(list1,list2)])
  union = (len(list1) + len(list2))
  return float(intersection)/union