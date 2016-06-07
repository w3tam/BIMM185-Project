import math

out1 = {}
out2 = {}

def store(what):
	cat = open(what)
	for line in cat:
		trueVal = 0.0
		if line.find('control') != -1 or line.find('DarkCorner') != -1 or \
		 line.find('BrightCorner') != -1 or line.find('Normalized') != -1: continue
		loc = 0
		for i in range(5):
			loc = line.find('	', loc)+1
		gene = line[:line.find('	')]
		value1 = float(line[loc:line.find('	',loc)])
		for i in range(2):
			loc = line.find('	', loc)+1
		value2 = float(line[loc:line.find('	', loc)])
		out1[gene] = value1
		out2[gene] = value2
	
def main():
	cat = 'matrix.txt'
	output = open('calcitriol.txt', 'w')
	store(cat)
	count = 0
	for i, j in out1.iteritems():
		Bval = math.pow(2, out2[i])
		Aval = math.pow(2, j)
		FC = Bval/Aval
		FC = math.log(FC, 2)
		#switch = 0
		#if FC < 0: switch = 1
		#if switch == 1: FC = FC*-1
		if abs(FC) > 1: 
			print i, FC
			count += 1
		out = i.upper()+'	'+str(FC)+'\n'
		output.write(out)
	output.close()
	print count

if __name__ == '__main__':
	main()

