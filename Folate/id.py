
cat = open("GSM1057752_sample_table.txt")
dog = open("identifier_list.txt", "w")

for line in cat:
	if line.find('VALUE') != -1:
		continue
	if line[0] == 'A':
		text = line[:line.find('	')]+'\n'
		dog.write(text)
cat.close()
dog.close()
