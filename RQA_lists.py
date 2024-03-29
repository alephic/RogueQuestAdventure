import random

weapon_names = ['pointy stick',
                'broadsword',
                'battleaxe',
                'mace',
                'lead pipe',
                'bo staff',
                'katana',
                'chainsaw',
                'lightsaber',
                'scissors',
                'baseball bat',
                'butcher\'s knife',
                'wrench',
                'toilet plunger',
                'spatula',
                'butterfly knife',
                'sledgehammer',
                'carrot',
                'bull whip',
                'scalpel',
                'shank',
                'banana',
                'spork',
                'cattle prod',
                'fish',
                'rapier',
                'bandsaw',
                'chopstick',
                'guitar',
                'potted plant',
                'baguette',
                'letter opener',
                'candlestick',
                'potato',
                'halberd',
                'toaster',
                'tusk',
                'sponge',
                'dirk'
                ]
weapon_traits = ['giant',
                 'telescoping',
                 'plush',
                 'toy',
                 'unusual',
                 'magic',
                 'shiny',
                 'stern',
                 'long',
                 'short',
                 'moist',
                 'limp',
                 'bumpy',
                 'spiked',
                 'swift',
                 'haunted',
                 'vintage',
                 'holy',
                 'explosive',
                 'heavy',
                 'radioactive',
                 'dull',
                 'sharpened',
                 'poisoned',
                 'rusty',
                 'dusty',
                 'flaming',
                 'laser',
                 'electrified',
                 'honed',
                 'ghostly',
                 'bloodied',
                 'grim',
                 'demonic',
                 'fabulous',
                 'ancient',
                 'grisly',
                 'evil',
                 'unholy',
                 'monstrous',
                 'deadly',
                 'girthy',
                 'brittle',
                 'massive',
                 'delicious',
                 'horrid',
                 'vengeful',
                 'metal',
                 'wooden',
                 'plastic',
                 'broken',
                 'useless',
                 'cosmic',
                 'stupid',
                 'mega',
                 'nightmarish',
                 'handy',
                 'lovely',
                 'curved',
                 'extreme',
                 'plasma',
                 'icy',
                 'dark',
                 'gnarly',
                 'awesome',
                 'radical',
                 'slender',
                 'multidimensional'
                 ]
weapon_enchantments = ['crushing',
                       'unholiness',
                       'the gods',
                       'defenestration',
                       'power',
                       'omniscience',
                       'the old gods',
                       'burning',
                       'shocking',
                       'smashing',
                       'stabbing',
                       'freezing',
                       'friendship',
                       'murder',
                       'evil',
                       'baking',
                       'harassment',
                       'violation',
                       'bad intentions',
                       'bludgeoning',
                       'blasting',
                       'incineration',
                       'groping',
                       'lightning',
                       'magic',
                       'abuse',
                       'regret',
                       'sadness',
                       'sunshine',
                       'spiders',
                       'healing',
                       'seven herbs and spices',
                       'telekenesis',
                       'phenomenal cosmic power',
                       'hitting things',
                       'dimensions',
                       'mind control',
                       'poison',
                       'bonking',
                       'good intentions',
                       'kindness',
                       'dancing',
                       'intelligence',
                       'the ancient ones',
                       'wind',
                       'circumcision',
                       'pleasure',
                       'eviscerating',
                       'slicing',
                       'dicing',
                       'decapitation',
                       'defenestration',
                       'lobotomy',
                       'lawbreaking',
                       'bad screenplays',
                       'consuming',
                       'summoning',
                       'destroying',
                       'flight',
                       'brain bursting',
                       'blood',
                       'assault',
                       'humor',
                       'wishful thinking',
                       'dark magic',
                       'girliness',
                       'manliness',
                       'testosterone',
                       'the overlord',
                       'the hero',
                       'the savior',
                       'destruction',
                       'aromatherapy',
                       'torment',
                       'angst',
                       'justice',
                       'your father',
                       'divine punishment'
                       ]
attacks = ['bludgeon',
           'stab',
           'impale',
           'slice',
           'poke',
           'whack',
           'hit',
           'shank',
           'disfigure',
           'gore',
           'thump',
           'attack',
           'macerate',
           'lacerate',
           'grind',
           'pulverize',
           'pound',
           'beat',
           'clout',
           'smack',
           'clobber',
           'wallop',
           'pound',
           'lambast',
           'assault',
           'bonk'
           ]
monster_names = ['alligator',
                 'crocodile',
                 'drake',
                 'snake',
                 'dog',
                 'aardvark',
                 'bear',
                 'wolf',
                 'monkey',
                 'ninja',
                 'goblin',
                 'imp',
                 'orc',
                 'land shark',
                 'drop-bear',
                 'tree octopus',
                 'squid',
                 'basilisk',
                 'dragon',
                 'harpie',
                 'succubus',
                 'gorgon',
                 'hydra',
                 'slime',
                 'pegasus',
                 'unicorn',
                 'horse',
                 'thief',
                 'beholder',
                 'cat',
                 'octopus',
                 'spider',
                 'bat',
                 'moth',
                 'pony',
                 'crab',
                 'rabbit',
                 'hobgoblin',
                 'clown',
                 'wolverine',
                 'badger',
                 'troll',
                 'chimera',
                 'bee swarm',
                 'hermit crab',
                 'ghost',
                 'kraken',
                 'mask',
                 'robot',
                 'thief',
                 'wizard',
                 'fire elemental',
                 'water elemental',
                 'ice elemental',
                 'milk elemental',
                 'cow',
                 'scorpion',
                 'chef',
                 'thing',
                 'elf',
                 'fairy',
                 'fly',
                 'gnome',
                 'munchkin',
                 'jellyfish',
                 'pirahna',
                 'energy ball',
                 'beetle',
                 'wombat',
                 'sloth',
                 'penguin',
                 'horror',
                 'abomination'
                 ]
monster_colors = dict()
for monster in monster_names:
    monster_colors[monster] = random.randint(0,255)
monster_attributes = ['skeletal',
                      'robot',
                      'demon',
                      'baby',
                      'elderly',
                      'enraged',
                      'docile',
                      'evil',
                      'manic',
                      'giant',
                      'tiny',
                      'miniature',
                      'gigantic',
                      'huge',
                      'scary',
                      'posessed',
                      'mega',
                      'giga',
                      'super',
                      'nasty',
                      'blind',
                      'obese',
                      'rabid',
                      'dire',
                      'slow',
                      'magic',
                      'floating',
                      'ghostly',
                      'undead',
                      'dyslexic',
                      'abominable',
                      'ethereal',
                      'multidimensional',
                      'beastly'
                      ]
boss_titles = ['king',
               'overlord',
               'master',
               'champion',
               'wizard',
               'conqueror',
               'god',
               'president',
               'sorceror',
               'knight',
               'general',
               'warlord',
               'goddess',
               'queen',
               'dictator'
               ]
food_names = ['banana',
              'cheese slice',
              'bacon strip',
              'loaf of bread',
              'carrot',
              'cabbage',
              'cake',
              'cookie',
              'cinnamon stick',
              'box of cereal',
              'doughnut',
              'cheese danish',
              'crossaint',
              'double cheeseburger',
              'cheeseburger',
              'fried egg',
              'hard-boiled egg',
              'deviled egg',
              'scrambled egg',
              'hot dog',
              'hamburger',
              'kebab',
              'pork chop',
              'steak',
              'slice of toast',
              'tuna salad sandwich',
              'milkshake',
              'bowl of ice cream',
              'lettuce',
              'leek',
              'tomato',
              'clove of garlic',
              'chocolate bar',
              'grilled cheese sandwich',
              'slice of pizza',
              'bowl of soup',
              'can of beans',
              'grape soda',
              'bucket of fried chicken',
              'chicken wing',
              'spicy pepper',
              'potato',
              'bag of chips',
              'beer',
              'carton of milk',
              'roast duck',
              'cup o\' tea',
              'coconut',
              'pineapple',
              'pumpkin pie',
              'apple pie',
              'mushroom',
              'watermelon',
              'bag of popcorn',
              'bagel',
              'salad',
              'salmon',
              'fish stick',
              'sushi roll',
              'taco',
              'burrito',
              'strip of beef jerky',
              'bottle of ketchup',
              'cupcake',
              'muffin',
              'creme brulee',
              'perogi',
              'apple fritter',
              'lollipop'
              ]
