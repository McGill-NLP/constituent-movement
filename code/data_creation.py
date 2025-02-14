import json
import numpy as np
from itertools import chain, combinations

### From https://docs.python.org/3/library/itertools.html#itertools-recipes
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

#====================GENERATING HNPS DATA====================

pivots = {['met', 'saw', 'noticed']: [['at the park', 'in the store', 'after the party'],
          	{'the man': [['tall', 'rugged', 'mysterious'], ['with the axe', 'from the forest']], 'her friend': [['old', 'sweet', 'estranged'], ['from high school']], 'the girl': [['short', 'thin', 'quiet'], ['in the line']]}],
          ['awarded', 'presented', 'gifted', 'gave']: [['for the competition', 'at the ceremony', 'to the team'],
          	{'a present': [['wrapped', 'birthday'], ['with red ribbon', 'in a white box']], 'a trophy': [['shiny', 'gold', 'winning'], ['with her name', 'for her performance']], 'a check': [['large', 'expensive'], ['of $50k', 'from the hosts', 'from the organization']]}],
          ['baked', 'made', 'prepared']: [['for the party', 'over the weekend', 'in the kitchen'],
          	{'muffins': [['fresh', 'vegan', 'blueberry'], ['with white frosting', 'with egg substitute']], 'a cake': [['multilevel', 'blue', 'vanilla', 'sponge'], ['with her name', 'in green frosting', 'with pink bows']]}],
          ['took', 'enjoyed', 'completed', 'taught']: [['at the college', 'at her university', 'during the day'],
          	{'courses': [['fascinating', 'strenuous'], ['for her graduate program', 'on astronomy', 'under the famous professor', 'from NASA']]}],
          ['brought']: [['to the meeting', 'to the party', 'when she arrived'],
          	{'food': [['traditional', 'Argentinian', 'street'], ['from their restaurant']], 'an air': [['anticipated', 'important', 'energetic'], ['of excitement']], 'drinks': [['cold', 'sweet', 'alcoholic'], ['from the bodega', 'in her bag']]}]}

count = 0
dict_list = []

for verbs in pivots:
	set = pivots[verbs]
	final_cons, nouns = set
	for fc in final_cons:
		for noun in nouns:
			args = nouns[noun]
			adjs, preps = args
			adj_list = list(powerset(adjs))
			prep_list = list(powerset(preps))
			for verb in verbs:
				for adj in adj_list:
					for prep in prep_list:
						if len(adj) == 0:
							if len(prep) == 0:
								unshifted_sentence = f'Melissa {verb} {noun} {fc}.'
								shifted_sentence = f'Melissa {verb} {fc} {noun}.'
							else:
								unshifted_sentence = f'Melissa {verb} {noun} {' '.join(prep)} {fc}.'
								shifted_sentence = f'Melissa {verb} {fc} {noun} {' '.join(prep)}.'
						else:
							if len(prep) == 0:
								unshifted_sentence = f'Melissa {verb} {', '.join(adj)} {noun} {fc}.'
								shifted_sentence = f'Melissa {verb} {fc} {', '.join(adj)} {noun}.'
							else:
								unshifted_sentence = f'Melissa {verb} {', '.join(adj)} {noun} {' '.join(prep)} {fc}.'
								shifted_sentence = f'Melissa {verb} {fc} {', '.join(adj)} {noun} {' '.join(prep)}.'
						unshifted_data = {'id': count, 'sentence': unshifted_sentence, 'shifted': False, 'subject': 'Melissa', 'verb': verb, 'noun': noun, 'adjectives': adj, 'prepositions': prep, 'final_con': fc, 'final_con_type': 'pp'}
						shifted_data = {'id': count, 'sentence': shifted_sentence, 'shifted': True, 'subject': 'Melissa', 'verb': verb, 'noun': noun, 'adjectives': adj, 'prepositions': prep, 'final_con': fc, 'final_con_type': 'pp'}
						dict_list.append(unshifted_data)
						dict_list.append(shifted_data)
						count += 1

with open('hnps_OUTPUT.json', 'w') as fp:
    for dictionary in dict_list:
        line = json.dumps(dictionary) + '\n'
        fp.write(line)

#====================GENERATING PM DATA====================

pivots = {['gave', 'up']: 
        {'the idea': [['planned', 'ambitious', 'backup'], ['to get funding', 'for the team', 'to meet deadlines']], 'her location': [['favorite', 'winning', 'hiding'], ['in the closet', 'under the stairs', 'for the game']], 'his secret': [['shameful', 'incriminating', 'longtime'], ['about what happened', 'in his marriage', 'with his wife']], 'the race': [['annual', 'Olympic', 'running'], ['on the track', 'in the stadium', 'in Canada']]}, 
      ['put', 'out']: 
        {'the fire': [['massive', 'raging', 'hot', 'red'], ['from the cinders', 'of the fireplace', 'in the living room']], 'a statement': [['long', 'formal', 'professional', 'apologetic'], ['from his client', 'on the website', 'for the press']], 'a notice': [['daily', 'building', 'warning'], ['for the construction project', 'for the lobby']]}, 
      ['worked', 'out']: 
        {'the schedule': [['revised', 'monthly', 'work'], ['for his employees', 'in the team', 'for the summer']], 'the plan': [['secret', 'ambitious', 'foolproof'], ['to win the trophy', 'for the game', 'for the next season']], 'his idea': [['initial', 'dream', 'college'], ['to move to France', 'for school']]}, 
      ['turned', 'in']: 
        {'his gun': [['old', 'broken', 'speed'], ['with radar', 'for tracking speed', 'for illegal drivers']], 'the report': [['detailed', 'final', 'history'], ['about the effects of feudalism', 'on European global development']], 'his resignation': [['unexpected', 'formal', 'written'], ['as the president', 'for the company']]}, 
      ['backs', 'up']: 
        {'the van': [['large', 'rented', 'moving'], ['from UHaul', 'for his new home']], 'his car': [['new', 'fast', 'sports'], ['with the engine', 'for racing', 'from Germany']], 'her argument': [['strong', 'logical', 'persuasive'], ['with evidence', 'for her point', 'on the Middle East']], 'the data': [['important', 'company', 'financial'], ['for the reductions', 'for the next quarter', 'from the secretary']]}, 
      ['brought', 'up']: 
        {'his kids': [['adopted', 'young'], ['with red hair', 'from Wisconsin']], 'her error': [['minor', 'computational'], ['on the third page', 'in the report']], 'the topic': [['awkward', 'strange', 'personal'], ['of his feelings', 'of getting married']], 'his issue': [['strong', 'current', 'standing'], ['with the rules', 'on voting rights']], 'the window': [['glitchy', 'Chrome', 'browser'], ['with the questionnaire', 'with his information', 'for applying to college']]}, 
      ['pointed', 'out']: 
        {'the mistake': [['minor', 'computational'], ['on the third page', 'in the report']], 'the detail': [['specific', 'intricate', 'design'], ['in the tiles', 'on the roof', 'of the cathedral']]}, 
      ['carries', 'out']: 
        {'a survey': [['comprehensive', 'online'], ['with the participants', 'for the study', 'for analyzing mental health']], 'his experiment': [['complicated', 'dangerous', 'science'], ['for his report', 'with unstable elements']], 'the strike': [['spontaneous', 'unauthorized', 'boat'], ['ordered by the Captain', 'against the ship']], 'his plan': [['genius', 'intelligent', 'detailed'], ['to raise money', 'for saving his house', 'to recover from getting fired']]}, 
      ['called', 'off']: 
        {'his concert': [['first', 'upcoming', 'summer'], ['for fans', 'in the stadium', 'in Brazil']], 'the operation': [['secret', 'military', 'aid'], ['funded by the charity', 'to help civilians', 'in Afghanistan']], 'the meeting': [['recurring', 'collaborative', 'group'], ['to discuss updates', 'for the team', 'for the past week']], 'his wedding': [['small', 'arranged', 'family'], ['with Anne', 'in the churchouse', 'in the afternoon']]}, 
      ['hand', 'in']: 
        {'his paper': [['finished', 'English', 'term'], ['in Helvetica font', 'with updated citations', 'about American literature']], 'his reviews': [['managerial', 'performance'], ['of company research', 'for his team', 'from the past year']]}, 
      ['left', 'out']: 
        {'details': [['important', 'juicy'], ['about the events', 'of his story', 'of last night']], 'the boy': [['rude', 'unintelligent'], ['with toxic behavior']], 'the paragraph': [['short', 'inarticulate', 'ungrammatical'], ['on Western Music', 'with incorrect information']]}, 
      ['turned', 'down']: 
        {'the heat': [['warm', 'baking'], ['of the oven', 'in the kitchen', 'of the house']], 'the invitation': [['fancy', 'mailed', 'printed'], ['from the host', 'for the wedding']], 'the offer': [['enticing', 'new', 'job'], ['for the position', 'to be a programmer', 'at Google']], 'his idea': [["wife's", 'lifelong', 'dream'], ['for the renovations', 'for the bathroom', 'for the house']], 'the music': [['Spanish', 'fusion', 'jazz'], ['from the band', 'from Barcelona', 'with steel guitars']], 'her proposal': [['updated', 'quarterly', 'stock'], ['from the meeting', 'for the funds', 'for his company']]}, 
      ['set', 'up']: 
        {'the system': [['new', 'efficient', 'backup'], ['for the network', 'in the office']], 'his tent': [["family's", 'large', 'camping'], ['with more space', 'for group camping']], 'the event': [['annual', 'competitive', 'hacking'], ['for computer scientists', 'in C++', 'at the university']], 'his date': [['special', 'romantic', 'anniversary'], ['at the dock', 'on the water', 'with his girlfriend']]}, 
      ['threw', 'away']: 
        {'his relationship': [['close', 'friendly', 'longtime'], ['with Andrew', 'since third grade']], 'his idea': [['rough', 'initial', 'brainstormed'], ['for the budget cuts', 'for the next quarter', 'for the company']], 'the leftovers': [['stinky', 'moldy', 'dinner'], ['with spicy sauce', 'on the shelf', 'in the fridge']], 'the clothes': [['old', 'torn', 'school'], ['from the closet', 'in the old house']], 'the trash': [['old', 'smelly', 'rotten'], ['in the black bag', 'from his party', 'from last week']]}, 
      ['takes', 'apart']: 
        {'the remote': [['old', 'broken', 'television'], ['for the television', 'with missing parts', 'from Craiglist']], 'their argument': [['radical', 'biased', 'oppositional'], ['about the presidential candidates', 'for the next election']], 'phones': [['broken', 'old', 'Apple'], ['with special chips', 'from the warehouses', 'from Korea']], 'motorcycles': [['vintage', 'Yamaha', 'racing'], ['with dual exhausts', 'from Japan', 'from 1974']]}, 
      ['looks', 'up']: 
        {'the band': [['new', 'popular', 'rock'], ['from Sweden']], 'his question': [['complicated', 'abstract', 'algebra'], ['from his class', 'from the morning', 'on mathematics']], 'the restaurant': [['new', 'popular', 'Italian'], ['with the famous pasta', 'with tomatoes', 'from Tuscany']]}, 
      ['beats', 'up']: 
        {'his brother': [['mean', 'adopted', 'younger'], ['from Denmark', 'with red hair']], 'Michael': [['scrawny', 'annoying', 'short'], ['with the tattoo', 'from the city']], 'the bully': [['big', 'mean', 'school'], ['from Ohio', 'with red hair']], 'my friend': [['old', 'best'], ['from high school', 'in the suburbs', 'in New York']]}, 
      ['put', 'on']: 
        {'his jersey': [['favorite', 'Montreal', 'hockey'], ['with the number', 'for the goalie', 'of the Habs']], 'a jacket': [['green', 'waterproof', 'rain'], ['with a hood', 'with fleece lining']], 'his socks': [['new', 'red', 'striped'], ['with lace edges', 'from Sweden']]},
      ['cleans', 'up']: 
        {'his lunch': [['leftover', 'beef', 'sandwich'], ['from the deli', 'from last night']], 'the mess': [['big', 'dirty', 'food'], ['on the carpet', 'in the living room', 'from last night']], 'the floors': [['long', 'waxed', 'hallway'], ['in the kitchen', 'of the office', 'of the business']]}, 
      ['made', 'up']: 
        {'a story': [['captivating', 'magical', 'bedtime'], ['about a warrior', 'in the Roman Empire']], 'the lie': [['sneaky', 'white'], ['about his actions', 'from the party', 'from yesterday']], 'the recipe': [['forgotten', 'secret', 'family'], ['with instructions', 'for the sauce', 'for the famous pizza']]},
      ['picked', 'up']: 
        {'his son': [['short', 'tired', 'upset'], ['at baseball practice', 'on the field', 'behind the school']], 'the books': [['thick', 'college', 'science'], ['from the library']], 'girls': [['tall', 'attractive', 'blonde'], ['on the beach', 'playing volleyball']]},
      ['kept', 'up']: 
        {'the joke': [['funny', 'improvised', 'acting'], ['about his role', 'for the play']], 'the pace': [['steady', 'quick', 'running'], ['of 6kph', 'on the track', 'for the race']], 'his appearance': [['polished', 'professional', 'media'], ['in public', 'for the movie']]}, 
      ['brought', 'in']: 
        {'this year': [['full', 'abundant', 'productive'], ['of stock profits', 'for growing the company']], 'the suspect': [['nervous', 'guilty', 'robbery'], ['from the tech store']], 'the woman': [['dangerous', 'armed', 'criminal'], ['from the gang', 'in the neighborhood']], 'his tools': [['large', 'professional', 'carpenter'], ['for fixing walls', 'in his house']]},
      ['figured', 'out']: 
        {'the problem': [['urgent', 'technical', 'electrical'], ['with the air conditioner', 'in the living room']]},
      ['gave', 'away']: 
        {'the book': [['unread', 'college', 'psychology'], ['with chapters on cognition', 'for studying for the cognition course']], 'his toys': [['old', 'broken', 'sports'], ['for his hobbies', 'from his childhood']]}, 
      ['called', 'back']: 
        {'the student': [['young', 'eager', 'prospective'], ['with the question', 'for the course']], 'the customer': [['angry', 'waiting', 'store'], ['with the issue', 'with a product', 'from the store']], 'his friend': [['interesting', 'new', 'work'], ['from his office']]}}

count = 0
dict_list = []

for pairing in pivots:
    verb, particle = pairing
    nouns = pivots[pairing]
    for noun in nouns:
        args = nouns[noun]
        adjs, preps = args
        adj_list = list(powerset(adjs))
        prep_list = list(powerset(preps))
        for adj in adj_list:
            for prep in prep_list:
                if len(adj) == 0:
                    if len(prep) == 0:
                        unshifted_sentence = f'John {verb} {particle} {noun}.'
                        shifted_sentence = f'John {verb} {noun} {particle}.'
                    else:
                        unshifted_sentence = f'John {verb} {particle} {noun} {' '.join(prep)}.'
                        shifted_sentence = f'John {verb} {noun} {' '.join(prep)} {particle}.'
                else:
                    if len(prep) == 0:
                        unshifted_sentence = f'John {verb} {particle} {', '.join(adj)} {noun}.'
                        shifted_sentence = f'John {verb} {', '.join(adj)} {noun} {particle}.'
                    else:
                        unshifted_sentence = f'John {verb} {particle} {', '.join(adj)} {noun} {' '.join(prep)}.'
                        shifted_sentence = f'John {verb} {', '.join(adj)} {noun} {' '.join(prep)} {particle}.'
                data = [unshifted_sentence, shifted_sentence]
                unshifted_data = {'id': count, 'sentence': unshifted_sentence, 'shifted': False, 'subject': 'John', 'verb': verb, 'particle': particle, 'noun': noun, 'adjectives': adj, 'prepositions': prep}
                shifted_data = {'id': count, 'sentence': shifted_sentence, 'shifted': True, 'subject': 'John', 'verb': verb, 'particle': particle, 'noun': noun, 'adjectives': adj, 'prepositions': prep}
                dict_list.append(unshifted_data)
                dict_list.append(shifted_data)
                count += 1

with open('pm_OUTPUT.json', 'w') as fp:
    for dictionary in dict_list:
        line = json.dumps(dictionary) + '\n'
        fp.write(line)


#====================GENERATING DA DATA [TODO]====================

prepositions1 = ["with the coat", "from California"]
prepositions2 = ["in the store", "from the market", "at the park", "behind the gym", "at work", "at the event"]
verbs = ["met", "saw", "passed", "greeted"]
nouns = ["the man", "the woman", "his friend", "her friend", "his uncle", "her uncle", "his roommate", "her roommate"]
subjects = ["I", "He", "They", "She"]
adjectives = ["wealthy", "tall", "chatty", "older"]

count = 0
dict_list = []



with open('da_OUTPUT.json', 'w') as fp:
    for dictionary in dict_list:
        line = json.dumps(dictionary) + '\n'
        fp.write(line)


#====================GENERATING MPP DATA [TODO]====================



count = 0
dict_list = []
for subject in subjects:
    for verb in verbs:
        for noun in nouns:
            for mod_type in ['adj', 'pp']:
                for weight1 in [0,1,1,1,2,2,2,3,3]:
                    for weight2 in [0, 1, 1, 1, 2, 2, 2]:
                        for prep2 in prepositions2:
                            noun_split = noun.split()
                            adj_list = list(np.random.choice(adjectives, weight1, replace=False))
                            prep_list = list(np.random.choice(prepositions1, weight2, replace=False))
                            if weight1 == 0:
                                if weight2 == 0:
                                    unshifted_sentence = f"{subject} {verb} {noun} {prep2}."
                                    shifted_sentence = f"{subject} {verb} {prep2} {noun}."
                                else:
                                    unshifted_sentence = f"{subject} {verb} {noun} {' '.join(prep_list)} {prep2}."
                                    shifted_sentence = f"{subject} {verb} {prep2} {noun} {' '.join(prep_list)}."
                            else:
                                if weight2 == 0:
                                    unshifted_sentence = f"{subject} {verb} {noun_split[0]} {', '.join(adj_list)} {noun_split[1]}{prep2}."
                                    shifted_sentence = f"{subject} {verb} {prep2} {noun_split[0]} {', '.join(adj_list)} {noun_split[1]}."
                                else:
                                    unshifted_sentence = f"{subject} {verb} {noun_split[0]} {', '.join(adj_list)} {noun_split[1]} {' '.join(prep_list)} {prep2}."
                                    shifted_sentence = f"{subject} {verb} {prep2} {noun_split[0]} {', '.join(adj_list)} {noun_split[1]} {' '.join(prep_list)}."
                            data = [unshifted_sentence, shifted_sentence]
    
                            print(count)
                            print(unshifted_sentence, str(scores[0]))
                            print(shifted_sentence, str(scores[1]))
                            unshifted_data = {'id': count, 'sentence': unshifted_sentence, 'shifted': False, 'subject': subject, 'verb': verb, 'noun': noun, 'adjectives': adj_list, 'prepositions': prep_list, 'final_con': prep2, 'final_con_type': 'pp', 'score':scores[0]}
                            shifted_data = {'id': count, 'sentence': shifted_sentence, 'shifted': True, 'subject': subject, 'verb': verb, 'noun': noun, 'adjectives': adj_list, 'prepositions': prep_list, 'final_con': prep2, 'final_con_type': 'pp', 'score':scores[1]}
                            dict_list.append(unshifted_data)
                            dict_list.append(shifted_data)
                            count += 1

with open('mpp_OUTPUT.json', 'w') as fp:
    for dictionary in dict_list:
        line = json.dumps(dictionary) + '\n'
        fp.write(line)
