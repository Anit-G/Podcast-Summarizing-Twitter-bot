import os
import re
import string
# figure out the way to use pycontractions instead
import contractions
import logging
from tqdm import tqdm

logging.basicConfig(filename='Logs/text_sum.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def clean(x):

    x = re.sub("[\(\[].*?[\)\]]", "", x)
    x = re.sub('\.\.\.', "",x)
    x = re.sub('\-', '',x)
    x = re.sub('\n', '', x)
    # x = re.sub(' +', ' ', x)
    # x = re.sub('  ',' ',x)

    # remove contractions
    for word in x.split():
        x = x.replace(word,contractions.fix(word))

    x = re.sub('[%s]' % re.escape('!#%&()*+,-./:;<=>?@[\\]^_`{|}~'), '', x)
    x = ' '.join(x.split())  # Remove random spaces

    return x

def clean_up(dir_link='Data/Transcripts/',save_dir='Data/Clean_Transcripts/'):
    logger.info('Getting transcript links')
    filelist = os.listdir(dir_link)
    file_links = []
    for filename in filelist:
        if (filename.endswith('.txt')):
            file_links.append(os.path.join(dir_link,filename))
    logger.debug(f'The number of files to summarize: {len(file_links)}')

    # Clean up
    logger.info('Begin file clean up')
    for i,file in enumerate(tqdm(file_links,desc='Files')):
        with open(file,mode='r') as f:
            lines = f.readlines()
            clean_text = []
            line_lengths = []
            for line in lines:
                clean_line = clean(line)
                clean_text.append(clean_line)
                line_lengths.append(len(clean_line))

            clean_text = ' '.join(clean_text)

            logger.debug(f"Length of final text: {len(clean_text)}")
            logger.debug(f"Length of cleaned text: {sum(line_lengths)}")
            logger.info(f"NOTE: the lengths should have a difference of 501, due to \' \'.join")

            # save the clean text
            savename = f'clean{i}.txt'
            savefile = os.path.join(save_dir,savename)
            with open(savefile,'w') as textfile:
                textfile.write(clean_text)

            textfile.close()
        f.close()







