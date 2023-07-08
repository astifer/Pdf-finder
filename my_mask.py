def process_mask(row_mask, t=4):
  '''
  Убирает все последовательности единиц короче <t>
  Если есть один нуль между единицами, кастует его к единице
  '''

  n = len(row_mask)
  post_mask = [0]*(n)
  hold = t # длина условного эталона - 3
  c=0

  for i in range(n):
    if row_mask[i]:
      c+=1
    else:
      if c >= hold:
        for j in range(i,i-c,-1): post_mask[j]=1
        c = 0

  for i in range(1,n-1):
    if post_mask[i]==0 and post_mask[i-1]==1 and post_mask[i+1]==1:
      post_mask[i]=1

  return post_mask