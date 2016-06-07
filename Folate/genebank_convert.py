import sys

def main():
	genbankfile = raw_input("file with genbank: ")
	cat = open(genbankfile)
	dog = open("genbank.txt", 'w')
	switch = 0
	for line in cat:
		if line.find('main') != -1:
			switch = 1
			continue
		if switch == 0 or line.find('Reporter') != -1:
			continue
		loc = 0
		for i in range(2):
			loc = line.find('	', loc) + 1
		gen = line[loc:]
		if len(gen) < 3:
			continue
		dog.write(gen)
	cat.close()
	dog.close()
if __name__ == '__main__':
	main()
