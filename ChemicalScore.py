#Predicting Food's Effects on Cancers Based on Chemical's Effects on Gene Expression
#															Wilburt Tam
#															BIMM 185
#
#Input: Cancer cell expression data from medicalgenomics.org
#		Chemical expression data from Food functionality database and ArrayExpress
#		Chemical content being analyzed of various foods from USDA database
#
#Output: Score of each chemical based on gene expression
#		 Predicted foods effective against cancer based on chemical score

import numpy

#names of cancer cell lines with each cancer in order according to cancer_expression.txt
test = ['Acute_Lymphoblastic_Leukemia','Acute_Myeloid_Leukemia','Acute_T_Cell_Lymphoblastic_Leukemia',\
'Adenocarcinoma','Amelanotic_Skin_Melanoma','Anaplastic_Carcinoma','B-Cell_Neoplasm',\
'Blast_Phase_Chronic_Myelogenous_Leukemia','Brain_Glioblastoma','Bronchogenic_Carcinoma','Burkitt_Lymphoma',\
'Carcinoma','Choriocarcinoma','Chronic_Lymphocytic_Leukemia','Chronic_Myelogenous_Leukemia',\
'Clear_Cell_Adenocarcinoma','Colon_Carcinoma','Colorectal_Adenocarcinoma','Cutaneous_T_Cell_Lymphoma',\
'Erythroleukemia','Esophageal_Carcinoma','Fibrosarcoma','Glioblastoma','Hepatocellular_Carcinoma','Hodgkin_Lymphoma',\
'Large_Cell_Lung_Carcinoma','Leiomyoblastoma','Leiomyosarcoma','Liposarcoma','Lung_Adenocarcinoma',\
'Lung_Atypical_Carcinoid_Tumor','Lung_Carcinoma','Lymphoma','Medulloblastoma','Melanoma','Mesothelioma','Myeloid_Leukemia',\
'Myeloma','Neuroblastoma','Non-Hodgkin_Lymphoma','Osteosarcoma','Ovarian_Serous_Adenocarcinoma',\
'Papillary_Lung_Adenocarcinoma','Plasma_Cell_Myeloma','Retinoblastoma','Rhabdomyosarcoma','Sarcomas','Small_Cell_Carcinoma',\
'Small_Cell_Lung_Carcinoma','Squamous_Cell_Carcinoma','Synovial_Sarcoma','T-Cell_Lymphoma','Wilms_Tumor']
#chemical list being analyzed
chemicals = ['calcitriol.txt', 'cholesterol.txt', 'Daidzein.txt', 'folate.txt', 'Genistein.txt', 'omega-3.txt', 'Phloridzin.txt',\
			'Quercetin.txt', 'vitamin_c.txt']

def readCancerExpress():
	#read cancer expression data
	output = {}
	dog = open('cancer_expression.txt')
	for line in dog:
		expression = []
		loc = line.find('	')+1
		currGene = line[:line.find('	')]
		while True:
			if line.find('	',loc) == -1:
				working = line[loc:len(line)-1]
				if len(working) > 2: expression.append(working)
				else: expression.append(0.0)
				break
			working = line[loc:line.find('	',loc)]
			if working == '':
				expression.append(0.0)
				loc = loc+1
				continue
			expression.append(working)
			loc = line.find('	', loc)+1
		output[currGene] = expression
	dog.close()
	return output

def readChemicalExpress():
	#read chemical expression data
	output = {}
	for data in chemicals:
		genedict = {}	#keys:gene	#values:logbase(2) fold change
		cat = open(data)
		#store chemical values into dictionary
		for line in cat:
			gene, value = line[:line.find('	')], line[line.find('	')+1:]
			if len(gene) < 2 or len(value) < 2: continue
			if value != '\n': value = float(value[:len(value)-1])
			genedict[gene] = value
		output[data] = genedict
	return output

def readFoodContent():
	cat = open('Food.csv')
	output = {}	#keys:chemical	#values:dict with food as key and content(ug/100ug) as value
	content = {} #keys:food	#values:chemical content(ug/100ug)
	temp = []	#for listing foods
	switch = 0
	currChem = ''
	for line in cat:
		#get food list to be printed in summary
		if line.find('##') != -1: continue
		elif line.find('>') != -1 and switch == 0: switch = 1
		if switch == 0: 
			temp.append(line[:len(line)-1])
			continue
		
		#read food chemical content
		if line.find('>') != -1:
			if switch != 1:
				output[currChem] = content
				content = {}
			currChem = line[1:len(line)-2]
			switch = 2
			continue
		content[line[:line.find('	')]] = line[line.find('	')+1:len(line)-1]
	output[currChem] = content
	#print food list
	for i in temp: print i
	return output

def score(cancer, chem):
	output = {}	#chemical:list(scores(index based on text))
	for currChem, genedict in chem.iteritems(): #chemical:dict(gene:value)
		chemScore = [0]*len(test)
		count = [0]*len(test)
		for gene, value in genedict.iteritems():	#gene:value
			#save expression of cancers for a certain gene if it exists
			currGene = []
			if gene in cancer: currGene = cancer[gene]
			else: continue
			#go through each gene and update score
			for i, j in enumerate(currGene):
				cancerScore = float(j)
				if abs(cancerScore) > 0.5:
					tempScore = float(value)/cancerScore
					if abs(tempScore) < 0.5: continue
					if tempScore > 1: 
						tempScore = 1
					elif tempScore < -1: 
						tempScore = -1
					chemScore[i] -= (tempScore)
					count[i] += 1
				else: continue
		for i,j in enumerate(count): 
			if j == 0: continue
			chemScore[i] = chemScore[i]/j
		output[currChem] = numpy.array(chemScore)
		print currChem
		print chemScore
	return output

def food(chemScore, foodDict):
	output = {}	#keys:food	#values:list of scores with index based on test
	for chemical, foodD in foodDict.iteritems():	#chemical:[food:content]
		for food, content in foodD.iteritems():		#food:content
			workingScore = chemScore[chemical]*float(content)
			if food in output: output[food] += workingScore
			else: output[food] = workingScore
	return output

def bestandworst(FoodScores):
	output = {}	#key:cancer	#values:list[best, bestscore, worst, worstscore]
	for i in range(len(test)):
		best, worst = '',''
		bestscore, worstscore = -9999,9999
		for food, scores in FoodScores.iteritems():
			if scores[i] > bestscore:
				bestscore = scores[i]
				best = food
			elif scores[i] < worstscore:
				worstscore = scores[i]
				worst = food
		bestworst = [best, bestscore, worst, worstscore]
		output[test[i]] = bestworst
	return output

def main():
	#print summary
	dummy = ['-']*70					
	print 'cancers:'
	print ''.join(dummy)		
	for i in range(0, len(test), 5):
		for j in range(0, 5):
			if i+j > len(test)-2:
				print test[i+j]
				break
			if j != 4:
				print test[i+j], ',',
			else:
				print test[i+j]
		print
	print '\n'+'\n'
	print 'chemical files:'
	print ''.join(dummy)
	for i in chemicals: print i
	print '\n' + '\n'
	print 'food list:'
	print ''.join(dummy)
	
	
	CancerExpress = readCancerExpress()	#keys:Gene	#values:list with logbase(2) fold change
	ChemDict = readChemicalExpress()	#keys:chemical	#values:dict with gene as key and expression as value
	FoodDict = readFoodContent()	#keys:chemical	#values:dict with food as key and content(ug/100ug) as value
	#ToPrint
	ChemScores = score(CancerExpress, ChemDict)	#keys:chemical	#values:list of scores with index based on test
	FoodScores = food(ChemScores, FoodDict)	#keys:food	#values:list of scores with index based on test
	last = bestandworst(FoodScores)	#key:cancer	#values:list[best, bestscore, worst, worstscore]
	#print
	dog = open('FinalOutput.txt', 'w')
	dog.write('\t'.join(map(str,test))+'\n'*2)
	dog.write('Chemical Scores'+'\n'+('-'*15)+'\n')
	for i, j in ChemScores.iteritems():
		dog.write('>'+i+'\n')
		dog.write('\t'.join(map(str,j))+'\n')
	dog.write('\n'*3+'Food Scores'+'\n'+('-'*11)+'\n')
	for i, j in FoodScores.iteritems():
		dog.write('>'+i+'\n')
		dog.write('\t'.join(map(str,j))+'\n')
	dog.write('\n'*3+'Best Food: Worst Food'+'\n'+('-'*11)+'\n')
	for i, j in last.iteritems():
		dog.write('>'+i+'\n')
		dog.write('best:'+str(j[0])+' bestscore:'+str(j[1])+'	worst:'+str(j[2])+'	worstscore:'+str(j[3])+'\n')
					
if __name__ == '__main__':
	main()
