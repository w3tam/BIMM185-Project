import math

def store(what):
	cat = open(what)
	out = {}
	for line in cat:
		trueVal = 0.0
		if line.find('VALUE') != -1: continue
		gene = line[:line.find('	')]
		value = line[line.find('	')+1:]
		if value[len(value)-1] == '\n': trueVal = float(value[:len(value)-1])
		else: trueVal = float(value)
		out[gene] = trueVal
	return out
	
def main():
	cat = 'GSM1477406_sample_table.txt'
	dog = 'GSM1477409_sample_table.txt'
	output = open('vitamin_C.txt', 'w')
	A = store(cat)
	B = store(dog)
	for i, j in A.iteritems():
		Bval = math.pow(2, B[i])
		Aval = math.pow(2, j)
		FC = Bval/Aval
		FC = math.log(FC, 2)
		#switch = 0
		#if FC < 0: switch = 1
		#if switch == 1: FC = FC*-1
		if FC > 1: print i, FC
		out = i.upper()+'	'+str(FC)+'\n'
		output.write(out)
	output.close()

if __name__ == '__main__':
	main()

