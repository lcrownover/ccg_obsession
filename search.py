from ccglib import ccg_obsession
import sys
import argparse

def GetArgs():
    parser = argparse.ArgumentParser(description='Get the lowest price for a given card or list of cards')
    parser.add_argument('-n', '--card_name', required=False, action='store', default=False, help='example: \'Beastmaster Ascension\'')
    parser.add_argument('-f', '--file', required=False, action='store', default=False, help='example: cardlist.txt')
    args = parser.parse_args()
    if not args.card_name and not args.file:
    	sys.exit('Did not supply card name or list')
    if args.card_name and args.file:
    	sys.exit('Please only supply a card name or a file input')
    card_name = args.card_name
    file = args.file
    return card_name, file


ccgo = ccg_obsession.Ccg_obsession()
card_list = []
card_name, file = GetArgs()
if card_name:
	card_list.append(card_name)
if file:
	with open(file, 'r') as f:
		for line in f.readlines():
			card_list.append(line.strip())

total_price = 0
unavailable_cards = []
print '\n'
for card_name in card_list:
	padding = ' ' * (40 - len(card_name))
	card_data = ccgo.search(card_name)
	if card_data == False:
		print '{}'.format(card_name)+padding+'not available'
		unavailable_cards.append(card_name)
	else:
		print '{}'.format(card_data['name'])+padding+'price: {}'.format(ccgo.format_price(card_data['price']))
		total_price += float(card_data['price'])

print '\n\ntotal price for all cards: ${}\n'.format(ccgo.format_price(total_price))

if unavailable_cards:
	print 'unavailable cards:'
	for c in unavailable_cards:
		print c