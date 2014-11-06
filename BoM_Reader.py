from SpeedReader2 import speed_reader

Books = ['1 Nephi', '2 Nephi', 'Jacob', 'Enos', 'Jarom', 'Omni',
		 'Words of Mormon', 'Mosiah', 'Alma', 'Helaman', '3 Nephi',
		 '4 Nephi', 'Mormon', 'Ether', 'Moroni']
Chapters = [22,33,7,1,1,1,1,29,63,16,30,1,9,15,10]

bom = dict(zip(Books,Chapters))

reference = lambda b, c: '{} {}'.format(b,c)

Chapter_list = list(reference(b,c) for b in Books for c in range(1, bom[b] + 1))

def BoM_chapter(Book, Chapter, numofchapters=1):
	ref = reference(Book, Chapter)
	
	start_flag = reference(Book, Chapter) + '\n'
	end_flag = Chapter_list[Chapter_list.index(ref) + numofchapters] + '\n'
	
	filename = ''.join(str(c) for c in Book + str(Chapter) + '.txt' if str(c) != ' ')
	
	with open('BoM.txt','r') as f, open(filename,'w') as g:
		line = ''
		
		while next(f) != start_flag:
			pass
		while line != end_flag:
			line = next(f)
			if line != '\n':
				if len(line) == 1:
					g.write(line)
				elif not any(c.isdigit() for c in line.split()[-1]):
					g.write(line)
			
	return filename

	
def BoM_reader(book='', chapter=None, speed=None, numofchapters=1, weighted=True, columnmode=True, columnsize=45):	
	if book not in Books:
		book = book.replace('First','1').replace('Second','2').replace('Third','3').replace('Fourth','4')
		while book not in Books:
			if book in Chapter_list:
				parsed = book.split()
				chapter = int(parsed.pop())
				book = ' '.join(parsed)
			else:
				book = raw_input('In which book of The Book of Mormon would you like to read? ').strip()
				book = book.replace('First','1').replace('Second','2').replace('Third','3').replace('Fourth','4')
	
	if chapter is None or reference(book, chapter) not in Chapter_list:
		if bom[book] == 1:
			chapter = 1
		else:
			while reference(book, chapter) not in Chapter_list: 
				chapter = int(raw_input('Which chapter in {} would you like to read [Last chapter: {}]? '.format(book,bom[book])).strip())
	
	if speed is None:
		speed = float(raw_input('How fast do you want to read in words per minute? ').strip())
	
	speed_reader(BoM_chapter(book, chapter, numofchapters), speed, weighted, columnmode, columnsize)
	
	
	return  
	
BoM_reader('2 Nephi',31,500, columnsize=25)