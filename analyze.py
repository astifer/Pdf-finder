import pandas as pd
import fitz
from Levenshtein import distance as lev
import os

from my_distance import jaccard
from my_mask import process_mask



def analyze_file(name, phrase, lev_rate, mask_threshold, target_directory):
  doc = fitz.open(os.path.join('data/',name))
  phrase_split = phrase.split()
  l = len(phrase)
  page_count = 0
  info = []
  
  for page in doc:
    page_count+=1
    
    text = page.get_text().split()
    text = [word for word in text if len(word)>1]

    mask = []

    for word in text:
      len_w = len(word)
      
      if word in phrase_split:
            mask.append(1)
      else:
            flag = False # is there a word in the source code
            for word2 in phrase_split:
                if (len(word2)-len(word)) > 7:
                    continue
                else:
                    dist = lev(word,word2)/len_w
                    
                    if dist < lev_rate:
                        if len(word) == len(word2): descr = 'Изменен символ: ' + word + ' and ' + word2
                        else: descr = 'Разная длина слов: ' + word + ' and ' + word2
                        
                        info.append({'filename': name.split('/')[-1], 'page': page_count, 'Jaccard': jaccard(word, word2), 'Levenshtein': lev(word,word2), 'subject': word, 'description': descr})
                        mask.append(1)
                        flag = True
                        break
                if flag:
                    break

            if not(flag):
                mask.append(0)

    mask = process_mask(mask, mask_threshold)

    for r, word in zip(mask, text):
      if r: page.add_highlight_annot(page.search_for(word))

              
  doc.save(os.path.join(target_directory,f'{name}_highlighted.pdf'))
  return info