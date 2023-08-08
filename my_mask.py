def process_mask(row_mask, t=0):
  '''
  Убирает все последовательности единиц короче <t>
  Если есть один нуль между единицами, кастует его к единице
  '''
  if t==0:
    return row_mask
  
      
  n = len(row_mask)
  post_mask = [[0,None]]*(n)
  hold = t # длина условного эталона
  c=0

  for i in range(n):
    '''
    Накапливает длину, а потом идет обратно
    '''
    if row_mask[i][0]:
      c+=1
    else:
      if c >= hold:
        for j in range(i,i-c,-1): 
          post_mask[j][0]=1
          post_mask[j][1] = row_mask[j][1]
          
        c = 0

  for i in range(1,n-1):
    if post_mask[i][0]==0 and post_mask[i-1][0]==1 and post_mask[i+1][0]==1:
      post_mask[i][0]=1
      post_mask[i][1] = row_mask[i][1]

  return post_mask