import os
from huggingface_hub import login
import json
from transformers import AutoTokenizer 
import pandas as pd

mytoken="TOKEN"
login(token=mytoken)
auth_token = os.getenv(mytoken)

models = {'gpt2': 'gpt2', 'gpt2_med': 'gpt2-medium', 'gpt2_large':'gpt2-large', 'gpt2_xl':'gpt2-xl', 'llama_3':'meta-llama/Meta-Llama-3-8B', 'llama_3_chat':'meta-llama/Meta-Llama-3-8B-Instruct', 'mistral_0.3':'mistralai/Mistral-7B-v0.3', 'mistral_0.3_chat':'mistralai/Mistral-7B-Instruct-v0.3', 'babyllama':'babylm/babyllama-100m-2024', 'babyopt':'babylm/opt-125m-strict-2023', 'olmo':'allenai/OLMo-7B-0724-hf', 'olmo_chat':'allenai/OLMo-7B-0724-Instruct-hf'} 

def get_tokenized_length(entity, tokenizer):
    return len(tokenizer.encode(entity, add_special_tokens=False))

data = pd.read_json('file.json', lines=True)

for m_nick in models:
    data[f'{m_nick} sum sentence score'] = (data[f'{m_nick} sentence token length'] - 1) * data[f'{m_nick} sentence score']
    print(f'Done tokenizing with {m_nick}!')

data.to_json('out.json', orient='records', lines=True)
