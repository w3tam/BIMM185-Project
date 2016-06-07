import math

out1 = {}
out2 = {}
genes = {}

def store(meow, woof, salt):
	cat = open(meow)
	dog = open(woof)
	cheese = open(salt)
	for line in cheese:
		if line.find('From	To	Species') != -1: continue
		loc = line.find('	')
		ID = line[:loc]
		gene = line[loc+1:line.find('	', loc+1)]
		genes[ID] = gene
	for line in cat:
		if line.find('VALUE') != -1: continue
		loc = line.find('	')
		ID = line[:loc]
		value = line[loc+1:]
		if value[len(value)-1] == '\n': value = float(value[:len(value)-1])
		if ID in genes: out1[genes[ID]] = value
	for line in dog:
		if line.find('VALUE') != -1: continue
		loc = line.find('	')
		ID = line[:loc]
		value = line[loc+1:]
		if value[len(value)-1] == '\n': value = float(value[:len(value)-1])
		if ID in genes: out2[genes[ID]] = value
	cat.close()
	dog.close()
	cheese.close()

def main():
	cat = 'GSM625869_sample_table.txt'
	dog = 'GSM625870_sample_table.txt'
	cheese = 'conv_19F0ED8C02281462933935914.txt'
	store(cat, dog, cheese)
	output = open('cholesterol.txt', 'w')
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
