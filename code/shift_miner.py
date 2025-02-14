import nltk
from nltk.corpus import brown
from nltk import word_tokenize, pos_tag, RegexpParser
from nltk.corpus import treebank
import pandas as pd
from nltk.corpus import sinica_treebank
from nltk.tree import Tree
from nltk.corpus import conll2000
import json
import numpy as np
import re
import os

nltk.download('punkt')
nltk.download('treebank')
nltk.download('sinica_treebank')
nltk.download('conll2000')
treebank = nltk.corpus.treebank

mpp_sents = []

with open('mpp_mine_out.json', 'r') as fp:
  for line in fp:
    mpp_sents.append(json.loads(line))
  fp.close()

selects = np.random.choice(len(mpp_sents), 500, replace=False)
with open('mpp_mine_out_rand.json', 'w') as ap:
  for a in selects:
    lines = []
    for p in mpp_sents:
      if p['id'] == a:
        lines.append(p)
    for ab in lines:
      line = json.dumps(ab) + '\n'
      ap.write(line)
  ap.close()

def load_parsed_trees_from_file(file_path):
  with open(file_path, 'r') as file:
    data = file.read()

  tree_strings = re.split(r'\n(?=\()', data.strip())

  trees = []
  for tree_str in tree_strings:
    try:
      tree = Tree.fromstring(tree_str)
      trees.append(tree)
    except ValueError as e:
      print(f"Error parsing tree: {e}")
      print(f"Tree string: {tree_str}")

  return trees

def load_all_trees_from_directory(directory_path):
  all_trees = []
  count = 0
  for root, _, files in os.walk(directory_path):
    for file in files:
      if file.endswith('.prd'):
        file_path = os.path.join(root, file)
        trees = load_parsed_trees_from_file(file_path)
        all_trees.extend(trees)
        count += len(trees)

      if count % 1000 == 0:
        print(f"Loaded {count} trees!")

  return all_trees

directory_path = 'wsj/'
all_trees = load_all_trees_from_directory(directory_path)

#============================THIS IS FOR HNPS============================
verbs = []
ob = []
fc = []

def tree_to_sentence(tree):
    return ' '.join(tree.leaves())

def get_items(tree):
  finalcon = None
  obj = None
  sbj = None
  vrb_fnd = False
  obj_fnd = False
  verb = []
  for stree in tree:
    for sstree in stree:
      if type(sstree) is Tree and sstree.label() == 'NP-SBJ':
        sbj = ' '.join(sstree.leaves())
      elif type(sstree) is Tree and (sstree.label().startswith('VB') or sstree.label().startswith('VP')):
        if type(sstree[0]) is str:
          verb.append(sstree[0])
        for ssstree in sstree:
          if type(ssstree) is Tree:
            if ssstree.label().startswith('VB') or ssstree.label().startswith('VP'):
              if type(ssstree[0]) is str:
                verb.append(ssstree[0])
            elif ssstree.label().startswith('NP') and obj_fnd is False:
              obj = tree_to_sentence(ssstree)
              obj_fnd = True
            elif ssstree.label().startswith('PP'):
              finalcon = tree_to_sentence(ssstree)
      elif type(sstree) is Tree and sstree.label().startswith('NP') and not sbj and vrb_fnd is False:
        sbj = tree_to_sentence(sstree)
      elif type(sstree) is Tree and sstree.label().startswith('PP'):
        finalcon = tree_to_sentence(sstree)
  return sbj, verb, obj, finalcon

hnps_sents = {}
count = 0

for tree in all_trees:
  #=======Extracting Constituents======
  subj, verb, obj, finalcon = get_items(tree)

  if verb != []:
    verb = ' '.join(pd.unique(verb))

  #====================================
  #=========Constructing Sents=========
  if subj and obj and finalcon and verb != []:
    if obj in finalcon:
      finalcon = finalcon.replace(obj, '')
    og_n = f"{subj} {verb} {obj} {finalcon}."
    og_s = f"{subj} {verb} {finalcon} {obj}."
    patt = ["\*[uUtTaA]\*", "\*-[0-9]+", "-[0-9]+", "\*ICH", "\*", "-lrb-", "-rrb-", "-lcb-", "-rcb-"]
    rep_n = og_n
    rep_s = og_s
    for i in patt:
      rep_n = re.sub(i, ' ', rep_n)
      rep_s = re.sub(i, ' ', rep_s)
    normal = rep_n.replace(' ,', ',').replace(" '", "'").replace(' .', '.').replace('`', '').replace(' %', '%').replace('$ ', '$').replace('   ', ' ').replace('  ', ' ').lower()
    shifted = rep_s.replace(' ,', ',').replace(" '", "'").replace(' .', '.').replace('`', '').replace(' %', '%').replace('$ ', '$').replace('   ', ' ').replace('  ', ' ').lower()
    normal = normal[0].upper() + normal[1:]
    shifted = shifted[0].upper() + shifted[1:]
    if normal != shifted and len(normal) == len(shifted):
      norm_d = {'id': count, 'sentence': normal, 'shifted': False, 'subj': subj, 'verb': verb, 'np': obj, 'final con': finalcon, 'adjectives': [], 'prepositions': [], 'weight': 0, 'qual': True}
      shif_d = {'id': count, 'sentence': shifted, 'shifted': True, 'subj': subj, 'verb': verb, 'np': obj, 'final con': finalcon, 'adjectives': [], 'prepositions': [], 'weight': 0, 'qual': True}
      hnps_sents[count] = [norm_d, shif_d]
      count += 1
  #=====================================
print(f"{count} sentences found!")

#============================THIS IS FOR VRB PRT============================
verbs = []
ob = []
fc = []

def tree_to_sentence(tree):
  return ' '.join(tree.leaves())

def get_items(tree):
  sents = []
  sbj = None
  verb = []
  prt = None
  obj = None
  for stree in tree:
    for sstree in stree:
      if type(sstree) is Tree:
        if sstree.label() == 'NP-SBJ' and sbj is None:
          sbj = tree_to_sentence(sstree)
        if sstree.label().startswith('VB') or sstree.label().startswith('VP') and len(sstree) >= 3:
          if type(sstree[1]) is Tree and sstree[1].label() == 'PRT':
            prt = sstree[1][0]
            verb = sstree[0]
          if type(sstree[2]) is Tree and sstree[2].label().startswith('NP'):
              obj = tree_to_sentence(sstree[2])

              return sbj, verb, prt, obj
          for ssstree in sstree:
            if type(ssstree) is Tree:
              if ssstree.label().startswith('VB') or ssstree.label().startswith('VP'):
                if type(sstree[1]) is Tree and sstree[1].label() == 'PRT':
                  prt = sstree[1][0]
                  verb = sstree[0]
                if type(sstree[2]) is Tree and sstree[2].label().startswith('NP'):
                    obj = tree_to_sentence(sstree[2])
                    return sbj, verb, prt, obj
  return sbj, verb, prt, obj


verb_particle_sents = {}
count = 0

for tree in all_trees:
  #=======Extracting Constituents======
  subj, verb, prt, obj = get_items(tree)
  #====================================

  #=========Constructing Sents=========
  if subj and obj and prt and verb != []:
    r_subj = subj
    r_vrb = ' '.join(pd.unique(verb))
    r_prt = prt
    r_obj = obj
    patt = [r"\*[uUtTaA]\*", r"\*-[0-9]+", r"-[0-9]+", r"\*ICH", r"\*", r"-lrb-", r"-rrb-", r"-lcb-", r"-rcb-"]
    for i in patt:
      r_subj = re.sub(i, ' ', r_subj)
      r_vrb = re.sub(i, ' ', r_vrb)
      r_prt = re.sub(i, ' ', r_prt)
      r_obj = re.sub(i, ' ', r_obj)
    rep_n = f"{r_subj} {r_vrb} {r_obj} {r_prt}."
    rep_s = f"{r_subj} {r_vrb} {r_prt} {r_obj}."
    normal = rep_n.replace(' ,', ',').replace(" '", "'").replace(' .', '.').replace('`', '').replace(' %', '%').replace('$ ', '$').replace('   ', ' ').replace('  ', ' ').lower()
    shifted = rep_s.replace(' ,', ',').replace(" '", "'").replace(' .', '.').replace('`', '').replace(' %', '%').replace('$ ', '$').replace('   ', ' ').replace('  ', ' ').lower()
    if normal[0] == ' ':
      normal = normal[1:]
      shifted = shifted[1:]
    normal = normal[0].upper() + normal[1:]
    shifted = shifted[0].upper() + shifted[1:]
    if normal != shifted and len(normal) == len(shifted):
      norm_d = {'id': count, 'sentence': normal, 'shifted': False, 'subj': subj, 'verb': verb, 'particle': prt, 'obj': obj, 'adjectives': [], 'prepositions': [], 'qual': True}
      shif_d = {'id': count, 'sentence': shifted, 'shifted': True, 'subj': subj, 'verb': verb, 'particle': prt, 'obj': obj, 'adjectives': [], 'prepositions': [], 'qual': True}
      verb_particle_sents[count] = [norm_d, shif_d]
      count += 1
  #=====================================
print(f"{count} sentences found!")
for count in verb_particle_sents:
  print(f"{count} : {verb_particle_sents[count][0]['sentence']}")
  print(f"{count} : {verb_particle_sents[count][1]['sentence']}\n")

#============================THIS IS FOR VRB PRT OG============================
def get_verb_particle(subtree):
    verb = None
    obj = None
    particle = None
    for child in subtree:
        if child.label().startswith('VB'):
            verb = tree_to_sentence(child)
        elif child.label() == 'NP':
            obj = tree_to_sentence(child)
        elif child.label() == 'PRT':
            particle = tree_to_sentence(child)
    return verb, obj, particle

subj = None
verb = None
obj = None
particle = None

for tree in treebank.parsed_sents():
    #=======Extracting Constituents======
    for subtree in tree:
        if subtree.label() == 'NP-SBJ':
            subj = tree_to_sentence(subtree)
        elif subtree.label() == 'VP':
            verb, obj, particle = get_verb_particle(subtree)

    if verb:
        verb = ' '.join(pd.unique(verb.split()))
    if obj:
        obj = ' '.join(obj.split())
    if particle:
        particle = ' '.join(particle.split())
    #====================================

    #=========Constructing Sents=========
    if subj and verb and obj and particle:
        normal = f"{subj} {verb} {obj} {particle}."
        normal = re.sub(r'\* |\*-\d+|\*T\*-\d+', '', normal).replace(' ,', ',').replace(" '", "'").replace(' .', '.').replace('  ', ' ').replace('`', '').lower()
        shifted = f"{subj} {verb} {particle} {obj}."
        shifted = re.sub(r'\* |\*-\d+|\*T\*-\d+', '', shifted).replace(' ,', ',').replace(" '", "'").replace(' .', '.').replace('  ', ' ').lower()

        if normal != shifted and len(normal) == len(shifted):
            #print(f"{normal}\n{shifted}\n=====================")
            verb_particle_sents[count] = [normal, shifted]
            count += 1
    #=====================================

    #=========Resetting Variables=========
    subj = None
    verb = None
    obj = None
    particle = None
    #=====================================
print(f"{len(verb_particle_sents)} sentences found!")

#============================THIS IS FOR MULTIPLE PPs============================
verbs = []
ob = []
fc = []

def tree_to_sentence(tree):
    return ' '.join(tree.leaves())

def get_items(tree):
  finalcon_list = []
  obj = None
  sbj = None
  vrb_fnd = False
  obj_fnd = False
  verb = []
  for stree in tree:
    for sstree in stree:
      if type(sstree) is Tree and sstree.label() == 'NP-SBJ':
        sbj = ' '.join(sstree.leaves())
      elif type(sstree) is Tree and (sstree.label().startswith('VB') or sstree.label().startswith('VP')):
        if type(sstree[0]) is str:
          verb.append(sstree[0])
        for ssstree in sstree:
          if type(ssstree) is Tree:
            if ssstree.label().startswith('VB') or ssstree.label().startswith('VP'):
              if type(ssstree[0]) is str:
                verb.append(ssstree[0])
            elif ssstree.label().startswith('PP'):
              finalcon_list.append(tree_to_sentence(ssstree))
      elif type(sstree) is Tree and sstree.label().startswith('NP') and not sbj and vrb_fnd is False:
        sbj = tree_to_sentence(sstree)
      elif type(sstree) is Tree and sstree.label().startswith('PP'):
        finalcon_list.append(tree_to_sentence(sstree))
  return sbj, verb, prep1, prep2

mpp_sents = {}
count = 0

for tree in all_trees:
  #=======Extracting Constituents======
  subj, verb, obj, finalcon = get_items(tree)

  if verb != []:
    verb = ' '.join(pd.unique(verb))

  #====================================
  #=========Constructing Sents=========
  if subj and obj and finalcon and verb != []:
    if obj in finalcon:
      finalcon = finalcon.replace(obj, '')
    og_n = f"{subj} {verb} {obj} {finalcon}."
    og_s = f"{subj} {verb} {finalcon} {obj}."
    patt = ["\*[uUtTaA]\*", "\*-[0-9]+", "-[0-9]+", "\*ICH", "\*", "-lrb-", "-rrb-", "-lcb-", "-rcb-"]
    rep_n = og_n
    rep_s = og_s
    for i in patt:
      rep_n = re.sub(i, ' ', rep_n)
      rep_s = re.sub(i, ' ', rep_s)
    normal = rep_n.replace(' ,', ',').replace(" '", "'").replace(' .', '.').replace('`', '').replace(' %', '%').replace('$ ', '$').replace('   ', ' ').replace('  ', ' ').lower()
    shifted = rep_s.replace(' ,', ',').replace(" '", "'").replace(' .', '.').replace('`', '').replace(' %', '%').replace('$ ', '$').replace('   ', ' ').replace('  ', ' ').lower()
    normal = normal[0].upper() + normal[1:]
    shifted = shifted[0].upper() + shifted[1:]
    if normal != shifted and len(normal) == len(shifted):
      norm_d = {'id': count, 'sentence': normal, 'shifted': False, 'subj': subj, 'verb': verb, 'np': obj, 'final con': finalcon, 'adjectives': [], 'prepositions': [], 'weight': 0, 'qual': True}
      shif_d = {'id': count, 'sentence': shifted, 'shifted': True, 'subj': subj, 'verb': verb, 'np': obj, 'final con': finalcon, 'adjectives': [], 'prepositions': [], 'weight': 0, 'qual': True}
      mpp_sents[count] = [norm_d, shif_d]
      count += 1
  #=====================================
print(f"{count} sentences found!")

#============================THIS IS FOR DATIVE ALT============================
import re
verbs = []
ob = []
fc = []

def tree_to_sentence(tree):
    return ' '.join(tree.leaves())

def get_items(tree):
  sbj = None
  verb = []
  obj1 = None
  obj2 = None
  obj3 = None
  for stree in tree:
    for sstree in stree:
      if type(sstree) is Tree:
        if sstree.label() == 'NP-SBJ':
          sbj = tree_to_sentence(sstree)
          if '*' in sbj and len(sbj) < 6:
            sbj = None
        elif sstree.label().startswith('VB') or sstree.label().startswith('VP'):
          for ssstree in sstree:
            if type(ssstree) is str:
              verb.append(ssstree)
            if type(ssstree) is Tree:
              if ssstree.label().startswith('NP') and obj1 is None:
                obj1 = tree_to_sentence(ssstree)
              elif ssstree.label().startswith('NP') and obj1 is not None and obj2 is None:
                obj2 = tree_to_sentence(ssstree)
              elif ssstree.label().startswith('PP') and obj2 is None:
                if ssstree[0] in ['for', 'to']:
                  obj2 = tree_to_sentence(ssstree)
  if obj2 is not None:
    if 'for' in obj2 or 'to' in obj2:
      obj3 = ' '.join(obj2.split()[1:])
    else:
      obj3 = obj2
      tmp = 'for ' + obj2
      obj2 = tmp
  if obj1 is not None and ('$' in obj1 or '%' in obj1 or re.match("^[0-9 ]+$", obj1)):
    obj1 = None
  if obj3 is not None and ('$' in obj3 or '%' in obj3 or re.match("^[0-9 ]+$", obj3)):
    obj3 = None
  return sbj, verb, obj1, obj2, obj3 #we maintain obj3 as the NP version, obj2 as the PP version


da_sents = {}
count = 0

for tree in all_trees:
  #=======Extracting Constituents======
  subj, verb, obj1, obj2, obj3 = get_items(tree)
  if verb != []:
    verb = ' '.join(pd.unique(verb))

  #====================================

  #=========Constructing Sents=========
  if subj and obj1 and obj2 and obj3 and verb != []:
    og_n = f"{subj} {verb} {obj1} {obj2}."
    og_s = f"{subj} {verb} {obj3} {obj1}."
    patt = ["\*[uUtTaA]\*", "\*-[0-9]+", "-[0-9]+", "\*ICH", "\*", "-lrb-", "-rrb-", "-lcb-", "-rcb-"]
    rep_n = og_n
    rep_s = og_s
    for i in patt:
      rep_n = re.sub(i, ' ', rep_n)
      rep_s = re.sub(i, ' ', rep_s)
    normal = rep_n.replace(' ,', ',').replace(" '", "'").replace('`', '').replace(' %', '%').replace('$ ', '$').replace('   ', ' ').replace('  ', ' ').replace(' .', '.').lower()
    shifted = rep_s.replace(' ,', ',').replace(" '", "'").replace('`', '').replace(' %', '%').replace('$ ', '$').replace('   ', ' ').replace(' .', '.').replace('  ', ' ').lower()
    normal = normal[0].upper() + normal[1:]
    shifted = shifted[0].upper() + shifted[1:]
    if normal != shifted:
      norm_d = {'id': count, 'sentence': normal, 'shifted': "False", 'subj': subj, 'verb': verb, 'obj1': obj1, 'obj2': obj2, 'qual': True}
      shif_d = {'id': count, 'sentence': shifted, 'shifted': "True", 'subj': subj, 'verb': verb, 'obj1': obj1, 'obj2': obj2, 'qual': True}
      da_sents[count] = [norm_d, shif_d]
      count += 1
  #=====================================
print(f"{count} sentences found!")
for count in da_sents:
  print(f"{count} : {da_sents[count][0]['sentence']}")
  print(f"{count} : {da_sents[count][1]['sentence']}\n")

with open('/content/drive/MyDrive/Shift Happens/dative_alt_mine_out.json', 'w') as ap:
  for a in da_sents:
    for ab in da_sents[a]:
      line = json.dumps(ab) + '\n'
      ap.write(line)
  ap.close()
