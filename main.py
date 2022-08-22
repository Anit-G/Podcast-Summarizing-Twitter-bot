import os

from text_utils import clean_up
from transformers import pipeline
import argparse
import logging

# print(torch.__version__)
# print(torch.cuda.is_available())

logging.basicConfig(filename='Logs/text_sum.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Parsers
parser = argparse.ArgumentParser(description='Text Summarization')
parser.add_argument('--text_folder', default='Data/Transcripts/',type=str, help='path to transcript folder')
parser.add_argument('--sum_model', default='facebook/bart-large-cnn',type=str,help='link to summarization model to use')
parser.add_argument('--sum_token',default='facebook/bart-large-cnn',type=str,help='link to tokenizer to use')
parser.add_argument('--clean_folder',default='Data/Clean_Transcripts/',type=str,help='folder with cleaned transcripts')
parser.add_argument('--sum_length',default=[1,40],type=list,help='give min and max length of summary')
args = parser.parse_args()

def summarize_net(model,tokenizer):
    logger.info(f'starting summarizer:\nModel:{model}\nTokenizer:{tokenizer}')
    # Construct pipeline
    summarizer = pipeline('summarization', model=model, tokenizer=tokenizer)

    # Get the data
    clean_up(args.text_folder,args.clean_folder)

    files = os.listdir(args.clean_folder)
    for filename in files:
        file = os.path.join(args.clean_folder,filename)
        with open(file,'r') as f:
            text = str(f.readlines()[0])
            n = 900
            words = text.split()
            text_batch = [' '.join(words[i:i+n]) for i in range(0,len(words),n)]
            text = text[:4500]
            logger.debug(f"Number of words in text: {len(text.split())}")

            outputs = []
            for input in text_batch:
                output = summarizer(input,
                           min_length=args.sum_length[0],
                           max_length=args.sum_length[1],
                           do_sample=False
                           )
                outputs.append(output[0]['summary_text'])
                logger.debug(f"Number of words in output: {len(output[0]['summary_text'].split())}")

            logger.debug(f"Number of outputs: {len(outputs)}")

    return outputs


outs = summarize_net(args.sum_model,args.sum_token)
