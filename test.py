import torch
from transformers import (
    AutoTokenizer,
    LEDConfig,
    LEDForConditionalGeneration,
)
import os
import nltk
tokenizer = AutoTokenizer.from_pretrained('allenai/PRIMERA')
# configuration = LEDConfig.from_pretrained('allenai/PRIMERA')
model = LEDForConditionalGeneration.from_pretrained('allenai/PRIMERA')

clean_folder = 'Data/Clean_Transcripts/'
files = os.listdir(clean_folder)
for filename in files:
    file = os.path.join(clean_folder, filename)
    with open(file, 'r') as f:
        text = str(f.readlines()[0])
        text = text.split()
        n=3000
        text_batch = [' '.join(text[i:i+n]) for i in range(0,len(text),n)]

print(len(text))

# Tokenizer
print(tokenizer.model_max_length)
print(tokenizer.max_len_single_sentence)
print(tokenizer.num_special_tokens_to_add())

print([len(tokenizer.tokenize(c)) for c in text_batch])
print([len(tokenizer(c).input_ids) for c in text_batch])
print(sum([len(tokenizer(c).input_ids) for c in text_batch]))

# Get the inputs
inputs = [tokenizer(batch, return_tensors="pt") for batch in text_batch]
outputs = []
with open('tweet.txt','a') as f:
    for input in inputs:
        output = model.generate(**input,max_new_tokens=100)
        output = tokenizer.decode(*output, skip_special_tokens=True)
        outputs.append(output)
        f.write(str(output)+'\n')
    f.close()

print(len(outputs))
print([len(x) for x in outputs])
print(max([len(x) for x in outputs]))
print(sum([len(x) for x in outputs]))
print(outputs)
