import sys

def geneID(Genes):
	output = {}
	cat = open(Genes)
	for line in cat:
		if line.find('From	To	Species	Gene') != -1:
			continue
		ID = line[:line.find('	')]
		loc = line.find('	')
		gene = line[loc+1:line.find('	',loc+1)]
		output[ID] = gene
	cat.close()
	return output

def geneReport(Reporter, dic):
	cat = open(Reporter)
	switch = 0
	output = {}
	for line in cat:
		if line.find('main') != -1:
			switch = 1
			continue
		if switch == 0 or line.find('Reporter') != -1:
			continue
		loc = 0
		for i in range(4):
			loc = line.find('	', loc) + 1
		ID = line[loc:line.find('	', loc)]
		if ID == '	' or len(ID) == 0:
			continue
		report = line[:line.find('	')]
		if ID[len(ID)-1] == '\n':
			ID = ID[:len(ID)-1]
		print ID
		if report in dic:
			output[report] = dic[report].upper()
		else:
			output[report] = 0
	cat.close()
	return output

def saveFinal(dic, sample):
	cat = open(sample)
	dog = open('folate.txt', 'w')
	for line in cat:
		if line.find('VALUE') != -1:
			continue
		identifier = line[:line.find('	')]
		value = line[line.find('	')+1:]
		if identifier in dic and dic[identifier] != 0:
			gene = dic[identifier]
			working = str(gene) + '	' + str(value)
			dog.write(working)
	cat.close()
	dog.close()

def main(arg):
	Genes = arg[0]
	Reporter = arg[1]
	SAMPLE = arg[2]
	IDtoGene = geneID(Genes)
	IDtoGene = geneReport(Reporter, IDtoGene)
	saveFinal(IDtoGene, SAMPLE)

if __name__ == '__main__':
	main(sys.argv[1:])
