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


def file_stats(filename):
	word_count, word_len = 0, 0
	
	for word in word_gen(filename):
		word_count += 1
		word_len += len(word)
	else:
		avg_word_len = word_len/float(word_count)
	
	return word_count, avg_word_len						
						
def rate_determiner(speed, filename, wc=None, awl=None, weighted=True):
	weighted = False if speed < 400 else weighted

		
	if weighted:
		words = lambda: word_gen(filename)
		wc, awl = file_stats(filename) if wc is None or awl is None else (wc, awl)
		
		tot_time = 60./speed * wc
		a = tot_time * speed / (60. * sum(max(len(w)/awl, 1) for w in words()))
		return lambda word: 60./(speed/a) * max(len(word)/awl, 1)
	else:
		return lambda word: 60.0/speed	

						
def speed_reader(filename, speed=None, weighted=True, columnmode = False, columnsize=20):
	if speed is None:
		speed = float(raw_input('How fast do you want to read in words per minute? ').strip())

	wc, awl = file_stats(filename)
	tot_time = 60./speed * wc
	
	pause = rate_determiner(speed, filename, wc, awl, weighted)

	words = word_gen(filename)
	
	count = 0
	
	prep_screen()
	
	print centered('# of words: ' + str(wc))
	print centered('Estimated Time: ' + ptime(tot_time))
	print centered('Hit any key to start')
	raw_input()
				
	cPrinter('ARE YE READY, KIDS?')
	time.sleep(2)
	cPrinter('AYE-AYE, CAPTAIN!!')
	time.sleep(.5)
	cPrinter('')
	time.sleep(.5)
	total_time = 0
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
			t2 = time.time()
			total_time += t2 - t1
			prep_screen()
			print centered('Paused')
			print centered('Hit ENTER to continue')
			print centered('Type quit to exit')			
			print centered('Type speed to change speed\n')
			try:
				response = raw_input()
				if response == 'quit':
					raise StopIteration
				elif 'speed' in response:
					speed = float(raw_input('How fast do you want to read in words per minute? ').strip())
					pause = rate_determiner(speed, filename, wc, awl, weighted)
				prep_screen()
				t1 = time.time()
			except KeyboardInterrupt:
				prep_screen()
				continue
			except StopIteration:
				total_time += t2 - t1
				prep_screen()
				
				print centered('Finished')
				print
				
				print centered('Words read: ' + str(count))
				print centered('Time spent: ' + str(total_time))
				print centered('Reading speed: {0:.2f} wpm\n'.format(count/total_time * 60))
				

				print 
				print centered('Hit ENTER to exit')
				print centered('Type again to repeat\n')
				response = raw_input()
				if 'again' in response:
					speed = float(raw_input('How fast do you want to read in words per minute? ').strip())
					speed_reader(filename, speed, weighted, columnmode, columnsize)

				break
		except StopIteration:
			t2 = time.time()
			total_time += t2 - t1
			prep_screen()
			
			print centered('Finished')
			print
			
			print centered('Words read: ' + str(count))
			print centered('Time spent: ' + str(total_time))
			print centered('Reading speed: {0:.2f} wpm\n'.format(count/total_time * 60))
			

			print 
			print centered('Hit ENTER to exit')
			print centered('Type again to repeat\n')
			
			response = raw_input()
			if 'again' in response:
				speed = float(raw_input('How fast do you want to read in words per minute? ').strip())
				speed_reader(filename, speed, weighted, columnmode, columnsize)

			break			
		
	return count/total_time * 60