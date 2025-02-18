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


#====================GENERATING DA DATA====================

pivots = {
     "gave": [{"his roommate": [["sweet", "friendly", "college"], ["from Dubai"]], 
               "his sister": [["older", "step"], ["in college", "in Arkansas"]], 
               "his friend": [["good", "trusted", "longtime"], ["with the medical degree", "from Michigan"]]},
              {"a gift": [["pricey", "birthday"], ["with a card"]],
               "the documents": [["important", "personal"], ["with his full name", "from his medical visit"]],
               "flowers": [["beautiful", "pink"], ["with trimmed stems", "from the nursery in town", "with a lace wrap"]],
               "a car": [["new", "red", "sports"], ["with drivers assistance", "for safe commuting"]]}],
     "sent": [{"his roommate": [["sweet", "friendly", "college"], ["from Dubai"]], 
               "his sister": [["older", "step"], ["in college", "in Arkansas"]], 
               "his friend": [["good", "trusted", "longtime"], ["with the medical degree", "from Michigan"]],
               "his family": [["large", "religious", "extended"], ["from the farms", "in the plains", "in Kansas"]],
               "his wife": [["estranged", "unfaithful"], ["from Vegas", "with the gambling addiction"]]}, 
              {"a gift": [["pricey", "birthday"], ["with a card"]],
               "the documents": [["important", "personal"], ["with his full name", "from his medical visit"]],
               "flowers": [["beautiful", "pink"], ["with trimmed stems", "from the nursery in town", "with a lace wrap"]],
               "a car": [["new", "red", "sports"], ["with drivers assistance", "for safe commuting"]],
               "a letter": [["serious", "long", "written"], ["with bank information", "for the financial account", "for the house"]],
               "a message": [["short", "polite", "notice"], ["about his travel in Europe", "from his work"]]}],
     "mailed": [{"his roommate": [["sweet", "friendly", "college"], ["from Dubai"]], 
                 "his sister": [["older", "step"], ["in college", "in Arkansas"]], 
                 "his friend": [["good", "trusted", "longtime"], ["with the medical degree", "from Michigan"]],
                 "his family": [["large", "religious", "extended"], ["from the farms", "in the plains", "in Kansas"]],
                 "his wife": [["estranged", "unfaithful"], ["from Vegas", "with the gambling addiction"]]}, 
                {"a gift": [["pricey", "birthday"], ["with a card"]],
                 "the documents": [["important", "personal"], ["with his full name", "from his medical visit"]],
                 "flowers": [["beautiful", "pink"], ["with trimmed stems", "from the nursery in town", "with a lace wrap"]],
                 "a car": [["new", "red", "sports"], ["with drivers assistance", "for safe commuting"]],
                 "a letter": [["serious", "long", "written"], ["with bank information", "for the financial account", "for the house"]],
                 "a message": [["short", "polite", "notice"], ["about his travel in Europe", "from his work"]]}], 
     "shipped": [{"his roommate": [["sweet", "friendly", "college"], ["from Dubai"]], 
                  "his sister": [["older", "step"], ["in college", "in Arkansas"]], 
                  "his friend": [["good", "trusted", "longtime"], ["with the medical degree", "from Michigan"]]}, 
                 {"a gift": [["pricey", "birthday"], ["with a card"]],
                  "the documents": [["important", "personal"], ["with his full name", "from his medical visit"]],
                  "flowers": [["beautiful", "pink"], ["with trimmed stems", "from the nursery in town", "with a lace wrap"]],
                  "a car": [["new", "red", "sports"], ["with drivers assistance", "for safe commuting"]]}],
     "played": [{"his friend": [["good", "childhood"], ["from France", "with an interest in film"]],
                 "his roommate": [["new", "visiting", "exchange"], ["from Korea", "with his professor"]],
                 "his mom": [["sweet", "supportive", "caring"], ["with a film degree", "from North Carolina"]]}, 
                {"a video": [["long", "amateur", "comedy"], ["for a class"]],
                 "his presentation": [["detailed", "persuasive", "PowerPoint"], ["on his research", "for his thesis", "on chemistry"]],
                 "a movie": [["low-budget", "novice", "studio"], ["with a plot"]],
                 "a song": [["new", "energetic", "danceable", "pop"], ["with a really good chorus", "from his favorite record label"]]}],
     "showed": [{"his friend": [["good", "childhood"], ["from France", "with an interest in film"]],
                 "his roommate": [["new", "visiting", "exchange"], ["from Korea", "with his professor"]],
                 "his mom": [["sweet", "supportive", "caring"], ["with a film degree", "from North Carolina"]],
                 "the group": [["large", "crowded", "tour"], ["with bags", "with maps", "from America"]],
                 "his sister": [["tall", "older", "step"], ["with an art history degree", "from Michigan"]]}, 
                {"a video": [["long", "amateur", "comedy"], ["for a class"]],
                 "his presentation": [["detailed", "persuasive", "PowerPoint"], ["on his research", "for his thesis", "on chemistry"]],
                 "a movie": [["low-budget", "novice", "studio"], ["with a plot"]],
                 "a song": [["new", "energetic", "danceable", "pop"], ["with a really good chorus", "from his favorite record label"]],
                 "the piece": [["famous", "large", "art"],["with the picture", "of a woman"]],
                 "the painting": [["impressive", "grand", "Monet"], ["with the lilies", "of the lake"]],
                 "the building": [["tall", "Baroque", "church"], ["with the dome", "by the famous artist", "from Italy"]],
                 "his outfit": [["expensive", "handmade", "tailored", "silk"], ["from the designer", "for the gala", "for the evening"]]}],
     "wrote": [{"his family": [["large", "religious", "extended"], ["from the farms", "in the plains", "in Kansas"]],
                "his wife": [["estranged", "unfaithful"], ["from Vegas", "with the gambling addiction"]]}, 
               {"a letter": [["serious", "long", "written"], ["with bank information", "for the financial account", "for the house"]],
                "a message": [["short", "polite", "notice"], ["about his travel in Europe", "from his work"]]}],
     "drafted": [{"his family": [["large", "religious", "extended"], ["from the farms", "in the plains", "in Kansas"]],
                  "his wife": [["estranged", "unfaithful"], ["from Vegas", "with the gambling addiction"]]}, 
                 {"a letter": [["serious", "long", "written"], ["with bank information", "for the financial account", "for the house"]],
                  "a message": [["short", "polite", "notice"], ["about his travel in Europe", "from his work"]]}],
     "sells": [{"immigrants": [["fresh", "American"], ["with college degrees", "in politics", "from Texas"]],
                "students": [["wealthy", "college"], ["with jobs", "at the campus", "in the city"]]},
               {"houses": [["large", "modern", "vacation"], ["from a famous architect", "from the 80s"]],
                "apartments": [["small", "cheap", "studio"], ["with balconies", "on the main street", "in downtown"]],
                "cars": [["exotic", "sports"], ["with loud exhausts", "from Japan"]]}],
     "rents": [{"immigrants": [["fresh", "American"], ["with college degrees", "in politics", "from Texas"]],
                "students": [["wealthy", "college"], ["with jobs", "at the campus", "in the city"]]},
               {"houses": [["large", "modern", "vacation"], ["from a famous architect", "from the 80s"]],
                "apartments": [["small", "cheap", "studio"], ["with balconies", "on the main street", "in downtown"]],
                "cars": [["exotic", "sports"], ["with loud exhausts", "from Japan"]]}],
     "leases": [{"immigrants": [["fresh", "American"], ["with college degrees", "in politics", "from Texas"]],
                 "students": [["wealthy", "college"], ["with jobs", "at the campus", "in the city"]]},
                {"houses": [["large", "modern", "vacation"], ["from a famous architect", "from the 80s"]],
                 "apartments": [["small", "cheap", "studio"], ["with balconies", "on the main street", "in downtown"]],
                 "cars": [["exotic", "sports"], ["with loud exhausts", "from Japan"]]}],
     "brought": [{"his friend": [["loyal", "best"], ["in the sports club", "in Ohio"]],
                  "Mary": [["friendly"], ["from the dorms", "in the college"]]}, 
                 {"soup": [["warm", "chicken"], ["with vegetables", "from his kitchen"]],
                  "his guitar": [["old", "cheap", "black"], ["from his rock band", "from his childhood"]],
                  "a novel": [["long", "raunchy", "romance"], ["with a special chapter", "from the event"]]}],
     "left": [{"his friend": [["loyal", "best"], ["in the sports club", "in Ohio"]],
               "Mary": [["friendly"], ["from the dorms", "in the college"]]}, 
              {"soup": [["warm", "chicken"], ["with vegetables", "from his kitchen"]],
               "his guitar": [["old", "cheap", "black"], ["from his rock band", "from his childhood"]],
               "a novel": [["long", "raunchy", "romance"], ["with a special chapter", "from the event"]]}],
     "cooked": [{"the man": [["poor", "sick", "homeless"], ["on the street", "with a limp"]],
                 "his mother": [["old", "sick", "disabled"], ["at the care home", "in Miami", "with Alzheimers"]],
                 "his family": [["large", "hungry"], ["of ten", "with extended relatives", "from Mississippi"]],
                 "his friend": [["loyal", "best"], ["in the sports club", "in Ohio"]],
                 "Mary": [["friendly"], ["from the dorms", "in the college"]]}, 
                {"soup": [["warm", "chicken"], ["with vegetables", "from his kitchen"]],
                 "a feast": [["grand", "hearty", "celebratory"], ["of pie", "with chicken", "from the farm"]]}],
     "prepared": [{"the man": [["poor", "sick", "homeless"], ["on the street", "with a limp"]],
                   "his mother": [["old", "sick", "disabled"], ["at the care home", "in Miami", "with Alzheimers"]],
                   "his family": [["large", "hungry"], ["of ten", "with extended relatives", "from Mississippi"]],
                   "his friend": [["loyal", "best"], ["in the sports club", "in Ohio"]],
                   "Mary": [["friendly"], ["from the dorms", "in the college"]]},
                  {"soup": [["warm", "chicken"], ["with vegetables", "from his kitchen"]],
                   "a feast": [["grand", "hearty", "celebratory"], ["of pie", "with chicken", "from the farm"]]}],
     "made": [{"the man": [["poor", "sick", "homeless"], ["on the street", "with a limp"]],
               "his mother": [["old", "sick", "disabled"], ["at the care home", "in Miami", "with Alzheimers"]],
               "his family": [["large", "hungry"], ["of ten", "with extended relatives", "from Mississippi"]],
               "his friend": [["loyal", "best"], ["in the sports club", "in Ohio"]],
               "Mary": [["friendly"], ["from the dorms", "in the college"]]},
              {"soup": [["warm", "chicken"], ["with vegetables", "from his kitchen"]],
               "a feast": [["grand", "hearty", "celebratory"], ["of pie", "with chicken", "from the farm"]]}],
     "built": [{"his parents": [["kind", "old", "disabled"], ["from Bulgaria"]],
                "the citizens": [["injured", "homeless"], ["without shelter", "in a city", "in the Midwest"]],
                "the children": [["young", "poor", "orphaned"], ["from the disaster", "in his town"]],
                "his brother": [["unemployed", "sick", "younger"], ["with cancer", "from the mines"]]}, 
               {"a house": [["beautiful", "big", "suburban"], ["with a deck", "for fishing by the lake"]],
                "an app": [["automated", "intelligent", "assistant"], ["with a direct line to 911", "for helping disabled people"]],
                "a boat": [["big", "fast", "green", "speed"], ["with powered engines", "for driving on the water"]]}],
     "constructed": [{"his parents": [["kind", "old", "disabled"], ["from Bulgaria"]],
                      "the citizens": [["injured", "homeless"], ["without shelter", "in a city", "in the Midwest"]],
                      "the children": [["young", "poor", "orphaned"], ["from the disaster", "in his town"]],
                      "his brother": [["unemployed", "sick", "younger"], ["with cancer", "from the mines"]]},
                     {"a house": [["beautiful", "big", "suburban"], ["with a deck", "for fishing by the lake"]],
                      "an app": [["automated", "intelligent", "assistant"], ["with a direct line to 911", "for helping disabled people"]],
                      "a boat": [["big", "fast", "green", "speed"], ["with powered engines", "for driving on the water"]]}]
}

count = 0
dict_list = []

for verb in pivots:
  obj1_dict, obj2_dict = pivots[verb]

  for obj1 in obj1_dict:
    adjs1, preps1 = obj1_dict[obj1]
    adj1_list = list(powerset(adjs1))
    prep1_list = list(powerset(preps1))

    for obj2 in obj2_dict:
      adjs2, preps2 = obj2_dict[obj2]
      adj2_list = list(powerset(adjs2))
      prep2_list = list(powerset(preps2))

      for adj1 in adj1_list:
        for adj2 in adj2_list:
          for prep1 in prep1_list:
            for prep2 in prep2_list:

              if len(adj1) == 0:
                if len(prep1) == 0:
                  full_obj1 = obj1
                else:
                  full_obj1 = f'{obj1} {' '.join(prep1)}'
                  
              else:
                if len(prep1) == 0:
                  full_obj1 = f'{', '.join(adj1)} {obj1}'
                else:
                  full_obj1 = f'{', '.join(adj1)} {obj1} {' '.join(prep1)}'
              
              if len(adj2) == 0:
                if len(prep2) == 0:
                  full_obj2 = obj2
                else:
                  full_obj2 = f'{obj2} {' '.join(prep2)}'
                  
              else:
                if len(prep2) == 0:
                  full_obj2 = f'{', '.join(adj2)} {obj2}'
                else:
                  full_obj2 = f'{', '.join(adj2)} {obj2} {' '.join(prep2)}'
              
              shifted_sentence = f'John {verb} {full_obj1} {full_obj2}.'
              unshifted_sentence = f'John {verb} {full_obj2} to {full_obj1}.' ### Note 'to' vs. 'for' is variable depending on object/verb
              data = [unshifted_sentence, shifted_sentence]
              unshifted_data = {'id': count, 'sentence': unshifted_sentence, 'shifted': False, 'subject': 'John', 'verb': verb, 'obj1': obj1, 'adjs1': adj1, 'preps1': prep1, 'obj2': obj2, 'adjs2': adj2, 'preps2': prep2}
              shifted_data = {'id': count, 'sentence': shifted_sentence, 'shifted': True, 'subject': 'John', 'verb': verb, 'obj1': obj1, 'adjs1': adj1, 'preps1': prep1, 'obj2': obj2, 'adjs2': adj2, 'preps2': prep2}
              dict_list.append(unshifted_data)
              dict_list.append(shifted_data)
              count += 1

with open('da_OUTPUT.json', 'w') as fp:
    for dictionary in dict_list:
        line = json.dumps(dictionary) + '\n'
        fp.write(line)


#====================GENERATING MPP DATA====================

pivots = {["went", "drove"]: 
            [{"to the event": [["annual", "charity", "auction"], ["in the convention center", "of the metropolis"]],
              "to class": [["advanced", "graduate", "economics"], ["on the second floor", "of the finance building", "in the downtown campus"]],
              "to the beach": [["warm", "sandy", "surfing"], ["on the coast", "in the countryside", "by her mother's home"]],
              "to the concert": [["crowded", "folk", "music"], ["in the stadium", "on fourth street", "in downtown"]],
              "on vacation": [["her", "yearly", "spring"], ["to the mountains", "in Canada"]]}, 
             {"in her car": [["small", "green", "electric"], ["with her favorite songs", "for her trip"]],
              "in a truck": [["big", "heavy", "loaded"], ["from the military"]],
              "with a van": [["large", "cheap", "rented"], ["with space", "for her supplies"]],
              "to the movie": [["new", "Marvel", "action"], ["in theatres", "in downtown"]],
              "to the mall": [["nearby", "old", "shopping"], ["with a food court", "with fast food"]],
              "to our class": [["morning", "advanced", "math"], ["with Mr. Jones", "in the science building"]]}],
          ["talked", "chatted"]: 
            [{"to her friend": [["sweet", "quiet", "short"], ["from college", "in Nebraska"]],
              "to the woman": [["bright", "helpful", "professional"], ["in HR", "at her job"]],
              "to Michael": [["tall", "skinny"], ["with red hair", "from HR", "in the company"]],
              "with Emily": [["her good friend"], ["and her friends", "from class"]],
              "with the man": [["tall", "attractive", "buff"], ["from her gym"]],
              "with her professor": [["favorite", "old", "science"], ["in the biology department", "at the university"]],
              "with her team": [["new", "assigned", "economics"], ["for stock predictions", "in the finance branch", "in the company"]],
              "with her boss": [["rude", "ignorant", "unprofessional"], ["from Cincinnati"]],
              "during the conference": [["annual", "academia", "charity"], ["in Nepal", "for research endeavors", "in economics"]],
              "during the meeting": [["dedicated", "internal", "complaints"], ["for speaking with HR", "about company funding", "for organized projects"]]}, 
             {"about her boss": [["rude", "narcissistic", "disrespectful"], ["with a huge salary"]],
              "about Sheila": [["mean", "noisy"], ["from the next cubicle", "three rows down", "on the second floor"]],
              "at the cafe": [["new", "local", "artisan"], ["with a patio", "with outdoor seating"]],
              "at the mall": [["nearby", "shopping"], ["with the restaurants", "with vegan food"]],
              "inside the restaurant": [["popular", "expensive", "American", "seafood"], ["on main street", "in downtown"]],
              "about the project": [["disorganized", "catastropic", "failing"], ["in the data", "for the analysis", "for the paper"]],
              "about a raise": [["large", "generous", "annual"], ["for the budget", "for her project"]]}],
          ["complained"]: 
            [{"to her friend": [["sweet", "quiet", "short"], ["from college", "in Nebraska"]],
              "to the woman": [["bright", "helpful", "professional"], ["in HR", "at her job"]],
              "with her brother": [["annoying", "younger"], ["with the red hat"]]}, 
             {"about her boss": [["rude", "narcissistic", "disrespectful"], ["with a huge salary"]],
              "about Sheila": [["mean", "noisy"], ["from the next cubicle", "three rows down", "on the second floor"]]}],
          ["walked", "biked"]: 
            [{"with Emily": [["her good friend"], ["and her friends", "from class"]],
              "without anyone else": [[], ["to have some quiet", "after a long day"]],
              "with her brother": [["annoying", "younger"], ["with the red hat"]]}, 
             {"to the movie": [["new", "Marvel", "action"], ["in theatres", "in downtown"]],
              "to the mall": [["nearby", "old", "shopping"], ["with a food court", "with fast food"]],
              "to our class": [["morning", "advanced", "math"], ["with Mr. Jones", "in the science building"]]}],
          ["met", "ate"]: 
            [{"with Emily": [["her good friend"], ["and her friends", "from class"]],
              "with the man": [["tall", "attractive", "buff"], ["from her gym"]],
              "with her professor": [["favorite", "old", "science"], ["in the biology department", "at the university"]]}, 
             {"at the cafe": [["new", "local", "artisan"], ["with a patio", "with outdoor seating"]],
              "at the mall": [["nearby", "shopping"], ["with the restaurants", "with vegan food"]],
              "inside the restaurant": [["popular", "expensive", "American", "seafood"], ["on main street", "in downtown"]]}],
          ["argued", "negotiated", "discussed"]: 
            [{"with her team": [["new", "assigned", "economics"], ["for stock predictions", "in the finance branch", "in economics"]],
              "with her boss": [["rude", "ignorant", "unprofessional"], ["from Cincinnati"]],
              "during the conference": [["annual", "academia", "charity"], ["in Nepal", "for research endeavors", "in economics"]],
              "during the meeting": [["dedicated", "internal", "complaints"], ["for speaking with HR", "about company funding", "for organized projects"]]}, 
             {"about the project": [["disorganized", "catastropic", "failing"], ["in the data", "for the analysis", "for the paper"]],
              "about a raise": [["large", "generous", "annual"], ["for the budget", "for her project"]]}]}

count = 0
dict_list = []

for verb in pivots:
  obj1_dict, obj2_dict = pivots[verb]

  for obj1 in obj1_dict:
    adjs1, preps1 = obj1_dict[obj1]
    adj1_list = list(powerset(adjs1))
    prep1_list = list(powerset(preps1))

    for obj2 in obj2_dict:
      adjs2, preps2 = obj2_dict[obj2]
      adj2_list = list(powerset(adjs2))
      prep2_list = list(powerset(preps2))

      for adj1 in adj1_list:
        for adj2 in adj2_list:
          for prep1 in prep1_list:
            for prep2 in prep2_list:

              if len(adj1) == 0:
                if len(prep1) == 0:
                  full_obj1 = obj1
                else:
                  full_obj1 = f'{obj1} {' '.join(prep1)}'
                  
              else:
                if len(prep1) == 0:
                  full_obj1 = f'{', '.join(adj1)} {obj1}'
                else:
                  full_obj1 = f'{', '.join(adj1)} {obj1} {' '.join(prep1)}'
              
              if len(adj2) == 0:
                if len(prep2) == 0:
                  full_obj2 = obj2
                else:
                  full_obj2 = f'{obj2} {' '.join(prep2)}'
                  
              else:
                if len(prep2) == 0:
                  full_obj2 = f'{', '.join(adj2)} {obj2}'
                else:
                  full_obj2 = f'{', '.join(adj2)} {obj2} {' '.join(prep2)}'
              
              shifted_sentence = f'John {verb} {full_obj1} {full_obj2}.'
              unshifted_sentence = f'John {verb} {full_obj2} to {full_obj1}.' ### Note 'to' vs. 'for' is variable depending on object/verb
              data = [unshifted_sentence, shifted_sentence]
              unshifted_data = {'id': count, 'sentence': unshifted_sentence, 'shifted': False, 'subject': 'John', 'verb': verb, 'obj1': obj1, 'adjs1': adj1, 'preps1': prep1, 'obj2': obj2, 'adjs2': adj2, 'preps2': prep2}
              shifted_data = {'id': count, 'sentence': shifted_sentence, 'shifted': True, 'subject': 'John', 'verb': verb, 'obj1': obj1, 'adjs1': adj1, 'preps1': prep1, 'obj2': obj2, 'adjs2': adj2, 'preps2': prep2}
              dict_list.append(unshifted_data)
              dict_list.append(shifted_data)
              count += 1

with open('mpp_OUTPUT.json', 'w') as fp:
    for dictionary in dict_list:
        line = json.dumps(dictionary) + '\n'
        fp.write(line)
