import sys
import time
from string import punctuation
import os

def htime(s):
    if s < 60:
        H,M,S = 0,0,s
    elif s < 3600:
        H,M,S = 0, int(float(s) / 60), s % 60
    else:
        S = s % 60
        s -= S
        
        H = int(float(s) / 3600)
        s -= float(H) * 3600
        
        M = int(float(s) / 60)
        s -= float(M) * 60

        assert s < 1
        
    return (H,M,S)

def ptime(s):
	H, M, S = htime(s)

	h = '' if H == 0 else '{}h '.format(H)
	m = '' if M == 0 else '{}m '.format(M)
	s = '' if S == 0 else '{}s '.format(int(round(S,0)))
	return h + m + s  

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


						
def line_creator(words, pause, columnmode, columnsize):
	line, p, subcount = '', 0 ,0
	if columnmode:
		while len(line) < columnsize:
			word = next(words)
			line = ' '.join([line,word])
			p += pause(word)
			subcount += 1
	else:
		word = next(words)
		line = word
		p += pause(word)	
		subcount += 1
			
	return line, p, subcount
	
	
def pause_screen():
	prep_screen()
	print centered('Paused')
	print centered('Hit ENTER to continue')
	print centered('Type quit to exit')			
	print centered('Type speed to change speed\n')
	
	response = raw_input()
	prep_screen()
	
	if response == 'quit':
		return False
	elif 'speed' in response:
		speed = float(raw_input('How fast do you want to read in words per minute? ').strip())
		prep_screen()
		return speed
	else:
		return True

		
def start_screen(filename, speed):
	if speed is None:
		speed = float(raw_input('How fast do you want to read in words per minute? ').strip())

	wc, wl = 0, 0

	for word in word_gen(filename):
		wc += 1
		wl += len(word)
	else:
		awl = wl/float(wc)
		a = wc / sum(max(len(w)/awl, 1) for w in word_gen(filename))
		
	tot_time = 60./speed * wc

	prep_screen()
	
	print centered('# of words: ' + str(wc))
	print centered('Estimated Time: ' + ptime(tot_time))
	print centered('Hit any key to start')
	raw_input()
	
	prep_screen()

	
	return a, awl, speed	

def end_screen(count, total_time):
	prep_screen()
	
	print centered('Finished')
	print
	
	print centered('Words read: ' + str(count))
	print centered('Time spent: ' + str(total_time))
	print centered('Reading speed: {} wpm\n'.format(int(round(count/total_time * 60,0))))


	
def speed_reader(filename, speed=None, weighted=True, columnmode=False, columnsize=20):
	total_time, count = 0, 0
	a, awl, speed = start_screen(filename, speed)

	if speed > 400 and weighted:
		pause = lambda word: 60./(speed/a) * max(len(word)/awl, 1)
	else:
		pause = lambda word: 60.0/speed
		
	words = word_gen(filename)	

	t1 = time.time()
	while True:
		try:
			line, p, subcount = line_creator(words, pause, columnmode, columnsize)
			cPrinter(line)
			count += subcount
			time.sleep(p)
		except KeyboardInterrupt:
			t2 = time.time()
			total_time += t2 - t1
			
			speed = pause_screen()
			
			if not speed:
				break
			elif type(speed) == 'float':
				if speed >= 400 and weighted:
					pause = lambda word: 60./(speed/a) * max(len(word)/awl, 1)
				else:
					pause = lambda word: 60.0/speed

			t1 = time.time()
			continue
		except StopIteration:
			break
	
	t2 = time.time()
	total_time += t2 - t1
	prep_screen()
	
	end_screen(count, total_time)