import pandas as pd
from minicons import scorer
import os
from huggingface_hub import login
import json

login(token=mytoken)
auth_token = os.getenv(mytoken)

models = {'gpt2_large':'gpt2-large', 'gpt2_xl':'gpt2-xl', 'llama_3':'meta-llama/Meta-Llama-3-8B', 'llama_3_chat':'meta-llama/Meta-Llama-3-8B-Instruct', 'mistral_0.3':'mistralai/Mistral-7B-v0.3', 'mistral_0.3_chat':'mistralai/Mistral-7B-Instruct-v0.3', 'babyllama':'babylm/babyllama-100m-2024', 'babyopt':'babylm/opt-125m-strict-2023', 'olmo':'allenai/OLMo-7B-0724-hf', 'olmo_chat':'allenai/OLMo-7B-0724-Instruct-hf'} 

for m_nick in models:
    mpp_data = pd.read_json('old_mpp_data.json', lines=True)
    mpp_out_file = f'mpp_{m_nick}_mean_scores.json'
    if mpp_out_file.exists():
        mpp_output = open(mpp_out_file, 'a')
        mpp_df = pd.read_json(mpp_out_file)
        last_line = mpp_df.iloc(-1)['sentence']
        mpp_data = mpp_data.iloc[:mpp_data[mpp_data['sentence'] == last_line].index[0] + 1]
    else:
        mpp_output = open(mpp_out_file, 'w')
    m_name = models[m_nick]
    m_scorer = scorer.IncrementalLMScorer(m_name, 'cuda')
    for i,r in mpp_data.iterrows():
        text = r['sentence']
        score = m_scorer.sequence_score(text)[0] #Sum reduction: lambda x: x.sum(0).item()
        r[f'{m_nick}_score'] = score
        json_line = json.dumps(r.to_json())
        mpp_output.write(json_line + "\n")
    mpp_output.close()
    print(f'Done scoring with {m_nick}!')
