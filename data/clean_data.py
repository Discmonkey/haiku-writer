# coding=utf-8

import os
import json
import codecs

import argparse


parser = argparse.ArgumentParser()

parser.add_argument('input_file')
parser.add_argument('--blacklist_authors',
					help='TXT file listing authors to be removed from the input dataset.')
parser.add_argument('-o', '--output_file',
					help='Output file to write clean data to. If no output file is given '
					'then the input file will be overwritten.')

args = parser.parse_args()

blacklist_file = codecs.open(args.blacklist_authors, 'r', encoding='utf-8')
blacklist_authors = [aut.replace('\n', '').lower() for aut in blacklist_file.readlines()]

author_count = 0
authors_removed = 0
haiku_count = 0
haikus_removed = 0
data = json.load(open(args.input_file, 'r'))
for author in data.keys():
	# TODO: Need to better deal with these dumb unicodes in the author names
	if any([auth in author.lower() for auth in blacklist_authors]):
		authors_removed += 1
		haikus_removed += len(data[author]['haikus'])

		del data[author]
		continue

	haikus = []
	for haiku in data[author]['haikus']:
		haiku = [ln for ln in haiku if len(ln) > 0]

		if len(haiku) <= 1:
			haikus_removed += 1
			continue

		haikus.append(haiku)

	author_count += 1
	haiku_count += len(haikus)
	data[author]['haikus'] = haikus


output_file = args.output_file if args.output_file else args.input_file
json.dump(data, open(output_file, 'w'), indent=4)

print 'Removed {} authors and {} faulty haikus.'.format(authors_removed, haikus_removed)
print 'Dataset now has {} authors and {} haikus'.format(author_count, haiku_count)
print 'Updated {}'.format(output_file)
