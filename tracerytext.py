import tracery
from tracery.modifiers import base_english

import math
import bdgmath as m
import drawutil
import drawSvg as draw
import text
import string

rules = {
    'origin': '#hello.capitalize#, #location#!',
    'hello': ['hello', 'greetings', 'howdy', 'hey'],
    'location': ['world', 'solar system', 'galaxy', 'universe']
}

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
print(grammar.flatten("#origin#"))  # prints, e.g., "Hello, world!"    



poemRules = {
    'origin': 'T\'was #weather# and the #monster# did #verb1# and #verb2# #locphrase#.',
    'weather': ['brillig', 'cold', 'sweltering', 'steamy', 'too damned hot', 'frigid', 'dry', 'damp'],
    'monster': '#monsterdesc# #monstername#',
    'monsterdesc': ['slithey', 'lithe', 'manxsome', 'lazy'],
    'monstername': ['aardwolf', 'aboleth', 'ankheg', 'archon', 'arghest', 'basilisk', 'blink dog', 'bugbear', 'bulette', 'beholder', 'centaur', 'cockatrice', 'chimera', 'dire ape', 'dire ox', 'dire tiger', 'dragon', 'dryad', 'dwarf', 'manticore', 'eagle', 'elf', 'ettin', 'gargoyle', 'ghost', 'ghast', 'ghoul', 'giant', 'gnoll', 'gorgon', 'goblin', 'golem', 'griffin', 'grimlock', 'halfling', 'harpy', 'hobgoblin', 'hydra', 'kraken', 'lich', 'ent', 'hellhound', 'carrion crawler', 'displacer beast', 'medusa', 'mimic', 'minotaur', 'mummy', 'naga', 'nymph', 'ogre', 'ooze', 'orc', 'otyugh', 'owlbear', 'pegasus', 'phasm', 'purple worm', 'rakshasa', 'roc', 'rust monster', 'sahuagin', 'shadow', 'skeleton', 'spectre', 'sprite', 'pixie', 'giant rat', 'stirge', 'titan', 'troll', 'unicorn', 'vampire', 'wight', 'worg', 'wyvern', 'xorn', 'zombie', 'sphinx', 'kobold', 'half-elk', 'forvalaka'],
    'verb1': ['slink', 'gyre', 'loll', 'creep'],
    'verb2': ['gimball', 'salivate', 'leap', 'hunt', 'lurk'],
    'locphrase': ['in the woods', 'in the wabe', 'by the sea', 'in the dark', 'beneath the waterfall', 'in a hidden glen', 'under the mountain', 'in the hall of the mountain king', 'beneath the city', 'in the forgotten tunnels of the crypt', 'where the darkness is deep', 'atop the crumbling wizard\'s tower', 'beneath the waves', 'in the shadows']
    }

def wordWrap(s, cc):
    lines = []
    while len(s) > cc:
        firstLine = s[:cc]
        spc = firstLine.rindex(' ')
        lines.append(firstLine[:spc])
        s = s[spc+1:]
    if s:
        lines.append(s)
    return lines


def drawPoem():
    poemGrammar = tracery.Grammar(poemRules)
    poemGrammar.add_modifiers(base_english)
    poem = poemGrammar.flatten('#origin#')
    poem = poem.upper()

    print(poem)

    poemLines = wordWrap(poem, 20)

    dwg = draw.Drawing(750, 750)
    dwg.setRenderSize('75mm', '75mm')

    start = 600
    stepSize = 100
    for li, line in enumerate(poemLines):
        print (line)
        text.drawString(dwg, line, 8, 25, start - stepSize * li)

    dwg.savePng("poem.png")
    dwg.saveSvg("poem.svg")
    

if __name__ == "__main__":
    drawPoem()
