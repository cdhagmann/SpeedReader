import sys
import time
from string import punctuation
import os
from BoM_parser import BoM_chapter

def prep_screen():
	os.system('cls' if os.name=='nt' else 'clear')
	print '\n' * 20 
	
class Printer():
    def __init__(self,data):
        sys.stdout.write("\r\x1b"+data.__str__())
        sys.stdout.flush()
		
		
def centered(string, width=72):
	extra = int(width - len(string))
	left = ' ' * (extra/2) 
	right = ' ' * (extra/2 + extra%2)
	return left + string + right
	
def cPrinter(string, width=72):
	Printer(centered(string,width))
	
def word_gen(filename):
	with open(filename,'r') as f:
		for line in f:
			for word in line.split():
				if not any(c.isdigit() for c in word):
					word2 = ''.join(c for c in word if c not in punctuation)
					if word2 != '':
						yield word


def rate_determiner(speed, filename, weighted=True):
	words = lambda: word_gen(filename)
	
	word_count = sum(1 for w in words())
	avg_word_len = sum(len(w) for w in words())/float(word_count)
	
	weighted = False if speed < 400 else weighted
	
	if weighted:
		tot_time = 60./speed * word_count
		a = tot_time * speed / (60. * sum(max(len(w)/avg_word_len, 1) for w in words()))
		return lambda word: 60./(speed/a) * max(len(word)/avg_word_len, 1)
	else:
		return lambda word: 60.0/speed	

						
def speed_reader(filename, speed=None, weighted=True, columnmode = False, columnsize=20):
	if speed is None:
		speed = float(raw_input('How fast do you want to read in words per minute? ').strip())
	
	pause = rate_determiner(speed, filename, weighted)

	words = word_gen(filename)
	count = 0
	
	prep_screen()
	
	cPrinter('ARE YE READY, KIDS?')
	time.sleep(2)
	cPrinter('AYE-AYE, CAPTAIN!!')
	time.sleep(.5)
	cPrinter('')
	time.sleep(.5)
	t1 = time.time()
	while True:
		try:
			if columnmode:
				line = ''
				p = 0
				minicount = 0
				while len(line) < columnsize:
					word = next(words)
					line = ' '.join([line,word])
					p += pause(word)
					minicount += 1
				cPrinter(line)
				count += minicount
				time.sleep(p)
			else:
				word = next(words)
				cPrinter(word)
				count += 1
				time.sleep(pause(word))
		except KeyboardInterrupt:
			prep_screen()
			print centered('Paused')
			print centered('(Hit ENTER to continue, type quit to exit.)')
			try:
				response = raw_input()
				if response == 'quit':
					raise StopIteration
				prep_screen()
			except KeyboardInterrupt:
				prep_screen()
				continue
			except StopIteration:
				t2 = time.time()
				total_time = t2 - t1
				prep_screen()
				
				print centered('Words read: ' + str(count))
				print centered('Time spent: ' + str(total_time))
				print centered('Reading speed: {0:.2f} wpm'.format(count/total_time * 60))
				break
		except StopIteration:
			t2 = time.time()
			total_time = t2 - t1
			prep_screen()
			
			print centered('Words read: ' + str(count))
			print centered('Time spent: ' + str(total_time))
			print centered('Reading speed: {0:.4f} wpm'.format(count/total_time * 60))
			break
	return count/total_time * 60

def BoM_reader(book=None, chapter=None, speed=None, weighted=True, columnmode=True, columnsize=45):
	Books = ['1 Nephi', '2 Nephi', 'Jacob', 'Enos', 'Jarom', 'Omni',
			 'Words of Mormon', 'Mosiah', 'Alma', 'Helaman', '3 Nephi',
			 '4 Nephi', 'Mormon', 'Ether', 'Moroni']
	Chapters = [22,33,7,1,1,1,1,29,63,16,30,1,9,15,10]
	bom = dict(zip(Books,Chapters))
	reference = lambda b, c: '{} {}'.format(b,c)
	Chapter_list = list(reference(b,c) for b in Books for c in range(1, bom[b] + 1))

	if book is None or bok not in Books:
		while book not in Books:
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

	speed_reader(BoM_chapter(book, chapter), speed, weighted, columnmode, columnsize)

BoM_reader()	
# speed_reader(BoM_chapter('2 Nephi', 31))