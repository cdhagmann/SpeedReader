Book = '2 Nephi'
Chapter = 31


def BoM_chapter(Book, Chapter):
	with open('BoM.txt','r') as f:
		marker = False
		start = 10000000000
		for idx, line in enumerate(f):
			if all([marker == True, idx - start > 5, 'Chapter' in line]):
				end = idx - 3
				break
			elif line == '{} {}\n'.format(Book, Chapter):
				start = idx + 2
				marker = True
	
	filename = ''.join(str(c) for c in Book + str(Chapter) + '.txt' if str(c) != ' ')
	with open('BoM.txt','r') as f, open(filename,'w') as g:
		for idx, line in enumerate(f):
			if start <= idx <= end:
				if line != '\n':
					if len(line) == 1:
						g.write(line)
					elif not any(c.isdigit() for c in line.split()[-1]):
						g.write(line)
			elif idx > end:
				break
			else:
				pass
				
	return filename			