import pandas as pd
import fitz
from Levenshtein import distance as lev
import os

from my_distance import jaccard
from my_mask import process_mask


def analyze_file(name, phrase, lev_rate, target_directory):
  doc = fitz.open(os.path.join('data/',name))
  phrase_split = phrase.split()
  l = len(phrase)
  page_count = 0
  info = []
  
  for page in doc:
    page_count+=1
    
    text_list = page.get_text('words')      

    # text = [word for word in text if len(word)>1]
    mask = [[]]

    for w in text_list:
      word = w[4]
      len_w = len(word)

      if word in phrase_split:
            r = fitz.Rect(w[:4])  # make rect from word bbox
            info.append({'filename': name.split('/')[-1], 
                         'page': page_count, 
                         'Jaccard': '-', 
                         'Levenshtein': '0', 
                         'subject': word, 
                         'description': 'perfectly suitable'})
            
            mask.append([1,r])
      else:
            flag = False # is there a word in source code
            for word2 in phrase_split:
                if (len(word2)-len(word)) > 7:
                    continue
                else:
                    dist = lev(word,word2)/len_w
                    
                    if dist < lev_rate:
                        if len(word) == len(word2): descr = 'Symbol is changed: ' + word + ' and ' + word2
                        else: descr = "Different word's lenght: " + word + ' and ' + word2
                        
                        info.append({'filename': name.split('/')[-1], 
                                     'page': page_count, 
                                     'Jaccard': str(jaccard(word, word2)), 
                                     'Levenshtein': str(lev(word,word2)), 
                                     'subject': word, 
                                     'description': descr})

                        mask.append([1,r])
                        flag = True
                        break
                if flag:
                    break

            if not(flag):
                mask.append([0,0])
                

    mask = mask[1:]

    # mask = process_mask(mask, mask_threshold)
    for exist, rect in mask:
      if exist: 
          annot = page.add_highlight_annot([rect])
          annot.update()

  doc.save(os.path.join(target_directory,f'{name}_highlighted.pdf'))
  return info