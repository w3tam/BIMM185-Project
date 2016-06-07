cat = open('GSM735959_sample_table.txt')
dog = open('conv_6A71C186A2B11462412648461.txt')
output = open('omega-3.txt', 'w')

dogDict = {}

for line in dog:
	if line.find('From	To') != -1: continue
	ID = line[:line.find('	')]
	loc = line.find('	')+1
	gene = line[loc:line.find('	', loc)]
	dogDict[ID] = gene
for line in cat:
	if line.find('VALUE') != -1: continue
	ID = line[:line.find('	')]
	value = line[line.find('	')+1:]
	if value[len(value)-1] == '\n': value = value[:len(value)-1]
	if ID in dogDict:
		out = dogDict[ID] + '	' + str(value) + '\n'
		output.write(out)
dog.close()
cat.close()
output.close()
