import os
import pandas as pd

files = os.listdir('processed_data')
models = ['gpt2', 'gpt2_med', 'gpt2_large', 'gpt2_xl', 'llama_3', 'llama_3_chat', 'mistral_0.3', 'mistral_0.3_chat', 'babyopt', 'babyllama', 'olmo', 'olmo_chat']

for fp in files:
    data = pd.read_csv(f'processed_data/{fp}')
    for m in models:
        cols = [col for col in data.columns if m in col]
        data = data.drop(columns=cols)
    data.to_csv(f'base_data/base_{fp}')