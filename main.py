import argparse
import fitz
from Levenshtein import distance as lev
import pandas as pd
import os

from analyze import analyze_file

parser = argparse.ArgumentParser(description='Find text in pdf and highlight it. \
    If there are too many folders in results you can delete all and it \
        does not crash')

parser.add_argument('phrase', type=str, help='Key phrase, which search will be for')

parser.add_argument(
    '--indir',
    type=str,
    default='data',
    help='provide a folder (default: data)'
)
parser.add_argument(
    '--mask_thres',
    type=int,
    default=0,
    help="Doesn't pay attantion to sample when a sentence less than a number(threshold) in a row (default: 0)"
)
parser.add_argument(
    '--rate',
    type=int,
    default=0.2,
    help='Rate for word comparison. The less the harder to find similar word (default: 0.2)'
)
parser.add_argument(
    '--is_make_csv',
    type=bool,
    default=True,
    help='Make csv file with mismatching words through all documents (default: True)'
)

args = parser.parse_args()
# phrase
# indir
mask_threshold = args.mask_thres
lev_rate = args.rate
# is_make_csv

print(f'we will find "{args.phrase}" in docs at folder {args.indir} \n')
print('procces...\n')

target_directory = ''
try:
    os.makedirs('results')
except:
    pass

for address, dirs, files in os.walk('results'):
    count = len(dirs)
    target_directory = "results/run_"+str(count+1)
    os.makedirs(target_directory)
    assert target_directory != '',  'Error with target directory'
    break
    
        
def make_csv(name,info):
    df = pd.DataFrame(info, columns=['filename','page','Jaccard','Levenshtein','subject','description'])
    df.to_csv(os.path.join(target_directory,f'{name}_info.csv'))

def main(phrase):
    filenames = list()
    
    for address, dirs, files in os.walk('./data'):
        filenames = files
        if len(filenames) == 0:
            print('Folder with data is empty')
            break
        break
        
    for filename in filenames:
        info = analyze_file(filename, phrase, lev_rate, mask_threshold, target_directory)
        
        if args.is_make_csv: 
            make_csv(filename, info)
        
        print(f'file "{filename}" is succecfully completed. Similar: {len(info)} positions\n')
        
main(args.phrase)

print('all complete \n')
print(f'results wrote to {target_directory}')