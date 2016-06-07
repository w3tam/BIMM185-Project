
cat = open("GSM735959_sample_table.txt")
dog = open("identifier_list.txt", "w")

for line in cat:
	if line.find('VALUE') != -1:
		continue
	text = line[:line.find('	')]+'\n'
	dog.write(text)
cat.close()
dog.close()
