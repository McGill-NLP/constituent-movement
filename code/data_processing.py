import pandas as pd 
import json
import numpy as np 

modelnames = ['gpt2', 'gpt2_med', 'gpt2_large', 'gpt2_xl', 'llama_3', 'llama_3_chat', 'babyopt', 'babyllama', 'mistral_0.3', 'mistral_0.3_chat', 'olmo', 'olmo_chat']


def inspect_data(df, index=0):
    for column in df.columns:
        print(f"{column}: {df[column].iloc[index]}")



############################
########### HNPS ###########
############################

# Synthetic data:
hnps_synth = pd.read_json("synthetic_data/hnps_collective_sum_data.json", lines=True)

hnps_synth['syll_ratio'] = hnps_synth['np syll'] / hnps_synth['final con syll']
hnps_synth['wordlength_ratio'] = hnps_synth['np len'] / hnps_synth['final con len']
hnps_synth['mods_ratio'] = hnps_synth['obj phrasal weight']
hnps_synth_shifted = hnps_synth[hnps_synth['shifted']==True]
hnps_synth_unshifted = hnps_synth[hnps_synth['shifted']==False]
hnps_synth_processed = hnps_synth_shifted.drop(columns=['shifted', 'sentence'])
hnps_synth_processed['sentence_shifted'] = hnps_synth_shifted['sentence'].to_list()
hnps_synth_processed['sentence_nonshifted'] = hnps_synth_unshifted['sentence'].to_list()
hnps_synth_processed['adjectives'] = hnps_synth_processed['adjectives'].apply(lambda x: str(x))
hnps_synth_processed['prepositions'] = hnps_synth_processed['prepositions'].apply(lambda x: str(x))

for modelname in modelnames:
    hnps_synth_processed[f'{modelname}_score'] = hnps_synth_unshifted[f'{modelname} sum sentence score'].to_numpy() - hnps_synth_shifted[f'{modelname} sum sentence score'].to_numpy()
    hnps_synth_processed = hnps_synth_processed.drop(columns=[f"{modelname} sum sentence score", f"{modelname} sentence token length", f"{modelname} sentence score"])

for modelname in modelnames:
    rename_dict = {f"{modelname}_token": f"{modelname} obj tokens"}
    hnps_synth_processed = hnps_synth_processed.rename(columns=rename_dict)
    hnps_synth_processed[f"{modelname}_token_ratio"] = hnps_synth_processed[f"{modelname} obj tokens"] / hnps_synth_processed[f"{modelname} final con tokens"]

hnps_synth_processed = hnps_synth_processed.drop(columns=[column for column in hnps_synth_processed.columns if 'distilgpt2' in column])
hnps_synth_processed.to_csv("processed_data/hnps_synth.csv", index=False)


# Mined data:
hnps_mined = pd.read_json("mined_data/hnps_mined_collective_sum_data.json", lines=True)

hnps_mined['syll_ratio'] = hnps_mined['np syll'] / hnps_mined['final con syll']
hnps_mined['wordlength_ratio'] = hnps_mined['np len'] / hnps_mined['final con len']
hnps_mined['shifted'] = hnps_mined['shifted'].apply(lambda x: {"True": True, "False": False}[x])
hnps_mined_shifted = hnps_mined[hnps_mined['shifted']==True]
hnps_mined_unshifted = hnps_mined[hnps_mined['shifted']==False]
hnps_mined_processed = hnps_mined_shifted.drop(columns=['shifted', 'sentence'])
hnps_mined_processed['sentence_shifted'] = hnps_mined_shifted['sentence'].to_list()
hnps_mined_processed['sentence_nonshifted'] = hnps_mined_unshifted['sentence'].to_list()

for modelname in modelnames:
    hnps_mined_processed[f'{modelname}_score'] = hnps_mined_unshifted[f'{modelname} sum sentence score'].to_numpy() - hnps_mined_shifted[f'{modelname} sum sentence score'].to_numpy()
    hnps_mined_processed = hnps_mined_processed.drop(columns=[f"{modelname} sum sentence score", f"{modelname} sentence token length", f"{modelname} sentence score"])

for modelname in modelnames:
    hnps_mined_processed[f"{modelname}_token_ratio"] = hnps_mined_processed[f"{modelname} np tokens"] / hnps_mined_processed[f"{modelname} final con tokens"]


hnps_mined_processed = hnps_mined_processed.drop(columns=[column for column in hnps_mined_processed.columns if 'distilgpt2' in column])
hnps_mined_processed.to_csv("processed_data/hnps_mined.csv", index=False)


# Human data:
hnps_human = pd.read_json("human_study/hnps_hs_data_sum.json", lines=True)

hnps_human['syll_ratio'] = hnps_human['np syll'] / hnps_human['final con syll']
hnps_human['wordlength_ratio'] = hnps_human['np len'] / hnps_human['final con len']
hnps_human['mods_ratio'] = hnps_human['obj phrasal weight']
hnps_human_shifted = hnps_human[hnps_human['shifted']==True]
hnps_human_unshifted = hnps_human[hnps_human['shifted']==False]
hnps_human_processed = hnps_human_shifted.drop(columns=['shifted', 'sentence'])
hnps_human_processed['sentence_shifted'] = hnps_human_shifted['sentence'].to_list()
hnps_human_processed['sentence_nonshifted'] = hnps_human_unshifted['sentence'].to_list()
hnps_human_processed['adjectives'] = hnps_human_processed['adjectives'].apply(lambda x: str(x))
hnps_human_processed['prepositions'] = hnps_human_processed['prepositions'].apply(lambda x: str(x))
for modelname in modelnames:
    hnps_human_processed[f'{modelname}_score'] = hnps_human_unshifted[f'{modelname} sum sentence score'].to_numpy() - hnps_human_shifted[f'{modelname} sum sentence score'].to_numpy()
    hnps_human_processed = hnps_human_processed.drop(columns=[f"{modelname} sum sentence score", f"{modelname} sentence token length", f"{modelname} sentence score"])

for modelname in modelnames:
    rename_dict = {f"{modelname}_token": f"{modelname} obj tokens"}
    hnps_human_processed = hnps_human_processed.rename(columns=rename_dict)
    hnps_human_processed[f"{modelname}_token_ratio"] = hnps_human_processed[f"{modelname} obj tokens"] / hnps_human_processed[f"{modelname} final con tokens"]

hnps_human_processed['raw_responses'] = hnps_human_processed['response'].apply(lambda x: eval(x))
hnps_human_processed['mean_human_response'] = hnps_human_processed['raw_responses'].apply(lambda x: np.mean(x))
hnps_human_processed['raw_responses'] = hnps_human_processed['response'].apply(lambda x: str(x)) # keep it but as a string since CSV
hnps_human_processed = hnps_human_processed.drop(columns=[column for column in hnps_human_processed.columns if 'distilgpt2' in column])
hnps_human_processed = hnps_human_processed.drop(columns=['response'])

hnps_human_processed.to_csv("processed_data/hnps_human.csv", index=False)



#############################
########### PM ##############
#############################

# Synthetic data:
pm_synth = pd.read_json("synthetic_data/vrb_prt_collective_sum_data.json", lines=True)
pm_synth['shifted'] = pm_synth['shifted'].apply(lambda x: {True: False, False: True}[x]) # Needed to be flipped for schema consistency

pm_synth['syll_ratio'] = pm_synth['noun syll'] / pm_synth['prt syll']
pm_synth['wordlength_ratio'] = pm_synth['np len'] / pm_synth['prt len']
pm_synth['mods_ratio'] = pm_synth['np phrasal weight']
pm_synth_shifted = pm_synth[pm_synth['shifted']==True]
pm_synth_unshifted = pm_synth[pm_synth['shifted']==False]
pm_processed = pm_synth_shifted.drop(columns=['shifted', 'sentence'])
pm_processed['sentence_shifted'] = pm_synth_shifted['sentence'].to_list()
pm_processed['sentence_nonshifted'] = pm_synth_unshifted['sentence'].to_list()
pm_processed['adjectives'] = pm_processed['adjectives'].apply(lambda x: str(x))
pm_processed['prepositions'] = pm_processed['prepositions'].apply(lambda x: str(x))
for modelname in modelnames:
    pm_processed[f'{modelname}_score'] = pm_synth_unshifted[f'{modelname} sum sentence score'].to_numpy() - pm_synth_shifted[f'{modelname} sum sentence score'].to_numpy()
    pm_processed = pm_processed.drop(columns=[f"{modelname} sum sentence score", f"{modelname} sentence token length", f"{modelname} sentence score"])

pm_processed = pm_processed.drop(columns=["prt tokens"])
for modelname in modelnames:
    pm_processed[f"{modelname}_token_ratio"] = pm_processed[f"{modelname}_token"] # This is because the token count is always 1 for the verb particles in the dataset, check below
    pm_processed = pm_processed.drop(columns=[f"{modelname}_token"])

'''
# Verifying that n_tokens is always 1 for verb particles in the dataset:
from transformers import AutoTokenizer
import os
HF_AUTH_TOKEN = os.getenv('HF_AUTH_TOKEN')

unique_particles = np.unique(pm_synth.particle)
modelname_to_fullname = {"gpt2": "gpt2", "gpt2_med": "gpt2-medium", "gpt2_large": "gpt2-large", "gpt2_xl": "gpt2-xl", "llama_3": "meta-llama/Meta-Llama-3-8B", "llama_3_chat": "meta-llama/Meta-Llama-3-8B-Instruct", "babyopt": "babylm/opt-125m-strict-small-2023", "babyllama": "timinar/baby-llama-58m", "mistral_0.3": "mistralai/Mistral-7B-v0.3", "mistral_0.3_chat": "mistralai/Mistral-7B-Instruct-v0.3", "olmo": "allenai/OLMo-7B-hf", "olmo_chat": "allenai/OLMo-Instruct-7B-hf"}
for modelname in modelnames:
    try:
        tokenizer = AutoTokenizer.from_pretrained(modelname_to_fullname[modelname], use_auth_token=HF_AUTH_TOKEN)
        tokenized_lengths = [len(tokenizer.encode(f" {particle}", add_special_tokens=False)) for particle in unique_particles]
        print(f"{modelname}: {tokenized_lengths}")
    except:
        continue
'''

pm_processed = pm_processed.drop(columns=[column for column in pm_processed.columns if 'distilgpt2' in column])
pm_processed.to_csv("processed_data/pm_synth.csv", index=False)


# Mined data:
pm_mined = pd.read_json("mined_data/vrb_prt_mined_collective_sum_data.json", lines=True)
# Mined pm data doesn't need shifted/unshifted to be flipped
pm_mined['syll_ratio'] = pm_mined['np syll'] / pm_mined['prt syll']
pm_mined['wordlength_ratio'] = pm_mined['np len'] / pm_mined['prt len']
pm_mined['shifted'] = pm_mined['shifted'].apply(lambda x: {"True": True, "False": False}[x])
pm_mined_shifted = pm_mined[pm_mined['shifted']==True]
pm_mined_unshifted = pm_mined[pm_mined['shifted']==False]
pm_mined_processed = pm_mined_shifted.drop(columns=['shifted', 'sentence'])
pm_mined_processed['sentence_shifted'] = pm_mined_shifted['sentence'].to_list()
pm_mined_processed['sentence_nonshifted'] = pm_mined_unshifted['sentence'].to_list()
pm_mined_processed = pm_mined_processed.drop(columns=["prt tokens"])
pm_mined_processed = pm_mined_processed.drop(columns=[column for column in pm_mined_processed.columns if 'distilgpt2' in column])
for modelname in modelnames:
    pm_mined_processed[f'{modelname}_score'] = pm_mined_unshifted[f'{modelname} sum sentence score'].to_numpy() - pm_mined_shifted[f'{modelname} sum sentence score'].to_numpy()
    pm_mined_processed = pm_mined_processed.drop(columns=[f"{modelname} sum sentence score", f"{modelname} sentence token length", f"{modelname} sentence score"])

for modelname in modelnames:
    pm_mined_processed[f"{modelname}_token_ratio"] = pm_mined_processed[f"{modelname} obj token"]

pm_mined_processed.to_csv("processed_data/pm_mined.csv", index=False)


# Human data:
pm_human = pd.read_json("human_study/vrb_prt_hs_data_sum.json", lines=True)
pm_human['shifted'] = pm_human['shifted'].apply(lambda x: {True: False, False: True}[x])

pm_human['syll_ratio'] = pm_human['noun syll'] / pm_human['prt syll']
pm_human['wordlength_ratio'] = pm_human['np len'] / pm_human['prt len']
pm_human['mods_ratio'] = pm_human['np phrasal weight']
pm_human_shifted = pm_human[pm_human['shifted']==True]
pm_human_unshifted = pm_human[pm_human['shifted']==False]
pm_human_processed = pm_human_shifted.drop(columns=['shifted', 'sentence'])
pm_human_processed['sentence_shifted'] = pm_human_shifted['sentence'].to_list()
pm_human_processed['sentence_nonshifted'] = pm_human_unshifted['sentence'].to_list()
pm_human_processed['adjectives'] = pm_human_processed['adjectives'].apply(lambda x: str(x))
pm_human_processed['prepositions'] = pm_human_processed['prepositions'].apply(lambda x: str(x))
for modelname in modelnames:
    pm_human_processed[f'{modelname}_score'] = pm_human_unshifted[f'{modelname} sum sentence score'].to_numpy() - pm_human_shifted[f'{modelname} sum sentence score'].to_numpy()
    pm_human_processed = pm_human_processed.drop(columns=[f"{modelname} sum sentence score", f"{modelname} sentence token length", f"{modelname} sentence score"])

for modelname in modelnames:
    pm_human_processed[f"{modelname}_token_ratio"] = pm_human_processed[f"{modelname}_token"]
    pm_human_processed = pm_human_processed.drop(columns=[f"{modelname}_token"])

pm_human_processed['raw_responses'] = pm_human_processed['response'].apply(lambda x: eval(x))
pm_human_processed['mean_human_response'] = pm_human_processed['raw_responses'].apply(lambda x: np.mean(x))
pm_human_processed = pm_human_processed.drop(columns=[column for column in pm_human_processed.columns if 'distilgpt2' in column])
pm_human_processed = pm_human_processed.drop(columns=['response', 'prt tokens'])

pm_human_processed.to_csv("processed_data/pm_human.csv", index=False)




#############################
########### DA ##############
#############################

# Synthetic data:
da_synth = pd.read_json("synthetic_data/dative_alt_collective_sum_data.json", lines=True)
da_synth['shifted'] = da_synth['shifted'].apply(lambda x: {True: False, False: True}[x]) # Needed to be flipped for schema consistency
da_synth['syll_ratio'] = da_synth['obj1 syll'] / da_synth['obj2 syll']
da_synth['wordlength_ratio'] = da_synth['obj1 len'] / da_synth['obj2 len']
da_synth['mods_ratio'] = da_synth['obj1 phrasal weight'] / da_synth['obj2 phrasal weight']
da_synth_shifted = da_synth[da_synth['shifted']==True]
da_synth_unshifted = da_synth[da_synth['shifted']==False]
da_synth_processed = da_synth_shifted.drop(columns=['shifted', 'sentence'])
da_synth_processed['sentence_shifted'] = da_synth_shifted['sentence'].to_list()
da_synth_processed['sentence_nonshifted'] = da_synth_unshifted['sentence'].to_list()
da_synth_processed['adj1'] = da_synth_processed['adj1'].apply(lambda x: str(x))
da_synth_processed['adj2'] = da_synth_processed['adj2'].apply(lambda x: str(x))
da_synth_processed['preps1'] = da_synth_processed['preps1'].apply(lambda x: str(x))
da_synth_processed['preps2'] = da_synth_processed['preps2'].apply(lambda x: str(x))
for modelname in modelnames:
    da_synth_processed[f'{modelname}_score'] = da_synth_unshifted[f'{modelname} sum sentence score'].to_numpy() - da_synth_shifted[f'{modelname} sum sentence score'].to_numpy()
    da_synth_processed = da_synth_processed.drop(columns=[f"{modelname} sum sentence score", f"{modelname} sentence token length", f"{modelname} sentence score"])

for modelname in modelnames:
    da_synth_processed[f"{modelname}_token_ratio"] = da_synth_processed[f"{modelname} obj1 tokens"] / da_synth_processed[f"{modelname} obj2 tokens"]

da_synth_processed = da_synth_processed.drop(columns=[column for column in da_synth_processed.columns if 'distilgpt2' in column])

da_synth_processed.to_csv("processed_data/da_synth.csv", index=False)


# Mined data:
da_mined = pd.read_json("mined_data/dative_alt_mined_collective_sum_data.json", lines=True)
da_mined['shifted'] = da_mined['form'].apply(lambda x: {"OD": True, "DOC": False}[x])
da_mined['syll_ratio'] = da_mined['obj1 syll'] / da_mined['obj2 syll']
da_mined['wordlength_ratio'] = da_mined['obj1 len'] / da_mined['obj2 len']
da_mined_shifted = da_mined[da_mined['shifted']==True]
da_mined_unshifted = da_mined[da_mined['shifted']==False]
da_mined_processed = da_mined_shifted.drop(columns=['shifted', 'sentence'])
da_mined_processed['sentence_shifted'] = da_mined_shifted['sentence'].to_list()
da_mined_processed['sentence_nonshifted'] = da_mined_unshifted['sentence'].to_list()
for modelname in modelnames:
    da_mined_processed[f'{modelname}_score'] = da_mined_unshifted[f'{modelname} sum sentence score'].to_numpy() - da_mined_shifted[f'{modelname} sum sentence score'].to_numpy()
    da_mined_processed = da_mined_processed.drop(columns=[f"{modelname} sum sentence score", f"{modelname} sentence token length", f"{modelname} sentence score"])

for modelname in modelnames:
    da_mined_processed[f"{modelname}_token_ratio"] = da_mined_processed[f"{modelname} obj1 tokens"] / da_mined_processed[f"{modelname} obj2 tokens"]

da_mined_processed = da_mined_processed.drop(columns=[column for column in da_mined_processed.columns if 'distilgpt2' in column])

da_mined_processed.to_csv("processed_data/da_mined.csv", index=False)


# Human data:
da_human = pd.read_json("human_study/dative_alt_hs_data_sum.json", lines=True)
da_human['shifted'] = da_human['shifted'].apply(lambda x: {True: False, False: True}[x]) # Needed to be flipped for schema consistency

da_human['syll_ratio'] = da_human['obj1 syll'] / da_human['obj2 syll']
da_human['wordlength_ratio'] = da_human['obj1 len'] / da_human['obj2 len']
da_human['mods_ratio'] = da_human['obj1 phrasal weight'] / da_human['obj2 phrasal weight']
da_human_shifted = da_human[da_human['shifted']==True]
da_human_unshifted = da_human[da_human['shifted']==False]
da_human_processed = da_human_shifted.drop(columns=['shifted', 'sentence'])
da_human_processed['sentence_shifted'] = da_human_shifted['sentence'].to_list()
da_human_processed['sentence_nonshifted'] = da_human_unshifted['sentence'].to_list()
da_human_processed['adj1'] = da_human_processed['adj1'].apply(lambda x: str(x))
da_human_processed['adj2'] = da_human_processed['adj2'].apply(lambda x: str(x))
da_human_processed['preps1'] = da_human_processed['preps1'].apply(lambda x: str(x))
da_human_processed['preps2'] = da_human_processed['preps2'].apply(lambda x: str(x))
for modelname in modelnames:
    da_human_processed[f'{modelname}_score'] = da_human_unshifted[f'{modelname} sum sentence score'].to_numpy() - da_human_shifted[f'{modelname} sum sentence score'].to_numpy()
    da_human_processed = da_human_processed.drop(columns=[f"{modelname} sum sentence score", f"{modelname} sentence token length", f"{modelname} sentence score"])

for modelname in modelnames:
    da_human_processed[f"{modelname}_token_ratio"] = da_human_processed[f"{modelname} obj1 tokens"] / da_human_processed[f"{modelname} obj2 tokens"]

da_human_processed['raw_responses'] = da_human_processed['response'].apply(lambda x: eval(x))
da_human_processed['mean_human_response'] = da_human_processed['raw_responses'].apply(lambda x: np.mean(x))
da_human_processed = da_human_processed.drop(columns=[column for column in da_human_processed.columns if 'distilgpt2' in column])
da_human_processed = da_human_processed.drop(columns=['response'])

da_human_processed.to_csv("processed_data/da_human.csv", index=False)




#############################
########### MPP #############
#############################

# Synthetic data:
mpp_synth = pd.read_json("synthetic_data/mpp_collective_data.json", lines=True)
mpp_synth['shifted'] = mpp_synth['shifted'].apply(lambda x: {True: False, False: True}[x]) # Needed to be flipped for schema consistency

mpp_synth['syll_ratio'] = mpp_synth['obj1 syll'] / mpp_synth['obj2 syll']
mpp_synth['wordlength_ratio'] = mpp_synth['obj1 len'] / mpp_synth['obj2 len']
mpp_synth['obj1_weight'] = mpp_synth['obj1_weight']+1 # Didn't include the base object itself, unlike the other data
mpp_synth['obj2_weight'] = mpp_synth['obj2_weight']+1 # ^^
mpp_synth['mods_ratio'] = mpp_synth['obj1_weight'] / mpp_synth['obj2_weight']
mpp_shifted = mpp_synth[mpp_synth['shifted']==True]
mpp_unshifted = mpp_synth[mpp_synth['shifted']==False]
mpp_processed = mpp_shifted.drop(columns=['shifted', 'sentence'])
mpp_processed['sentence_shifted'] = mpp_shifted['sentence'].to_list()
mpp_processed['sentence_nonshifted'] = mpp_unshifted['sentence'].to_list()
mpp_processed['adj1'] = mpp_processed['adj1'].apply(lambda x: str(x))
mpp_processed['adj2'] = mpp_processed['adj2'].apply(lambda x: str(x))
mpp_processed['preps1'] = mpp_processed['preps1'].apply(lambda x: str(x))
mpp_processed['preps2'] = mpp_processed['preps2'].apply(lambda x: str(x))
for modelname in modelnames:
    mpp_processed[f'{modelname}_score'] = mpp_unshifted[f'{modelname} sum score'].to_numpy() - mpp_shifted[f'{modelname} sum score'].to_numpy()

for modelname in modelnames:
    mpp_processed[f"{modelname}_token_ratio"] = mpp_processed[f"{modelname} obj1 token length"] / mpp_processed[f"{modelname} obj2 token length"]

mpp_processed.to_csv("processed_data/mpp_synth.csv", index=False)

# Mined data:
mpp_mined = pd.read_json("mined_data/mpp_mined_collective_sum_data.json", lines=True)
# Mined mpp data doesn't need shifted/unshifted to be flipped
mpp_mined['shifted'] = mpp_mined['shifted'].apply(lambda x: {"True": True, "False": False}[x]) # does need string->bool though

mpp_mined['syll_ratio'] = mpp_mined['prep1 syll'] / mpp_mined['prep2 syll']
mpp_mined['wordlength_ratio'] = mpp_mined['prep1 len'] / mpp_mined['prep2 len']
mpp_mined_shifted = mpp_mined[mpp_mined['shifted']==True]
mpp_mined_unshifted = mpp_mined[mpp_mined['shifted']==False]
mpp_mined_processed = mpp_mined_shifted.drop(columns=['shifted', 'sentence'])
mpp_mined_processed['sentence_shifted'] = mpp_mined_shifted['sentence'].to_list()
mpp_mined_processed['sentence_nonshifted'] = mpp_mined_unshifted['sentence'].to_list()
for modelname in modelnames:
    mpp_mined_processed[f'{modelname}_score'] = mpp_mined_unshifted[f'{modelname} sum sentence score'].to_numpy() - mpp_mined_shifted[f'{modelname} sum sentence score'].to_numpy()
    mpp_mined_processed = mpp_mined_processed.drop(columns=[f"{modelname} sum sentence score", f"{modelname} sentence token length", f"{modelname} score"])

for modelname in modelnames:
    mpp_mined_processed[f"{modelname}_token_ratio"] = mpp_mined_processed[f"{modelname} prep1 tokens"] / mpp_mined_processed[f"{modelname} prep2 tokens"]

mpp_mined_processed = mpp_mined_processed.drop(columns=[column for column in mpp_mined_processed.columns if 'distilgpt2' in column])

mpp_mined_processed.to_csv("processed_data/mpp_mined.csv", index=False)


# Human data:
mpp_human = pd.read_json("human_study/mpp_hs_data_sum.json", lines=True)
mpp_human['shifted'] = mpp_human['shifted'].apply(lambda x: {True: False, False: True}[x]) # Needed to be flipped for schema consistency

mpp_human['syll_ratio'] = mpp_human['obj1 syll'] / mpp_human['obj2 syll']
mpp_human['wordlength_ratio'] = mpp_human['obj1 len'] / mpp_human['obj2 len']
mpp_human['obj1_weight'] = mpp_human['obj1_weight']+1 # Didn't include the base object itself, unlike the other data
mpp_human['obj2_weight'] = mpp_human['obj2_weight']+1 # ^^
mpp_human['mods_ratio'] = mpp_human['obj1_weight'] / mpp_human['obj2_weight']
mpp_human_shifted = mpp_human[mpp_human['shifted']==True]
mpp_human_unshifted = mpp_human[mpp_human['shifted']==False]
mpp_human_processed = mpp_human_shifted.drop(columns=['shifted', 'sentence'])
mpp_human_processed['sentence_shifted'] = mpp_human_shifted['sentence'].to_list()
mpp_human_processed['sentence_nonshifted'] = mpp_human_unshifted['sentence'].to_list()
mpp_human_processed['adj1'] = mpp_human_processed['adj1'].apply(lambda x: str(x))
mpp_human_processed['adj2'] = mpp_human_processed['adj2'].apply(lambda x: str(x))
mpp_human_processed['preps1'] = mpp_human_processed['preps1'].apply(lambda x: str(x))
mpp_human_processed['preps2'] = mpp_human_processed['preps2'].apply(lambda x: str(x))
for modelname in modelnames:
    mpp_human_processed[f'{modelname}_score'] = mpp_human_unshifted[f'{modelname} sum score'].to_numpy() - mpp_human_shifted[f'{modelname} sum score'].to_numpy()
    mpp_human_processed = mpp_human_processed.drop(columns=[f"{modelname} sum score"])

for modelname in modelnames:
    mpp_human_processed[f"{modelname}_token_ratio"] = mpp_human_processed[f"{modelname} obj1 token length"] / mpp_human_processed[f"{modelname} obj2 token length"]

mpp_human_processed['raw_responses'] = mpp_human_processed['response'].apply(lambda x: eval(x))
mpp_human_processed['mean_human_response'] = mpp_human_processed['raw_responses'].apply(lambda x: np.mean(x))
mpp_human_processed = mpp_human_processed.drop(columns=["response"])

mpp_human_processed.to_csv("processed_data/mpp_human.csv", index=False)








