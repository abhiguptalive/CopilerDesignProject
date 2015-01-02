import sys
from SLRparse import parse 

mainList=[]
ruleList=[]
parseTable=[]
sr=[]
def main():
	
	r=0
	
	
	f=open(sys.argv[1],'r')
	rule=f.readline()
	while rule:
		r+=1
		rule=rule.strip()
		ruleList.append(rule)
		rule=f.readline()
	s=''.join(['S1: ',ruleList[0].split(':')[0].strip(),' $'])
	ruleList.insert(0,s)
	print("Grammer list:",ruleList)
	alpha=alphabet()
	print("Terminal and nonterminal:",alpha)
	automaton(alpha)
	print("States:")
	j=0
	for i in mainList:
		print("I{}: ".format(j),i)
		j+=1
		
	print("\n\nParsing Table:")
	j=0
	print("\t\t",end="")
	for ele in alpha:
	
		print(ele,"\t",end="")
		
	print()
	print("*****************************************************************************************")
	print()
#	print("-----------------------------------------------------------------------------------------")
	
	for i in parseTable:
		print("{}\t|\t".format(j),end="")
		for ind in i:
			if ind is 0:
				ind =""
			print(ind,"\t",end="")
		#print("{}\t|\t".format(j),i)
		print()
		print("-------------------------------------------------------------------------------------")
		j+=1
	
	inpt=input("Enter string to be parsed (Leave space between each term (Ex: id * id)):")
	parse(inpt,parseTable,alpha,ruleList)


def alphabet():
	alpha=[]
	for gra in ruleList:
		gra=gra.split(':')[1].strip()
		l=gra.split(' ')
		for i in l:
			if i not in alpha:
				if i.isupper():
					alpha.append(i)								
				else:
					alpha.insert(0,i)
	return alpha


def automaton(alpha):
	
	I0=[ruleList[0]]
	I0=appendS(I0)	
	mainList.append(I0)
	i=0;
	while i<len(mainList):
		state(mainList[i],alpha)
		i+=1
	slrptable(alpha)
	
def state(I,alpha):
	l=[]
	flag=0
	for a in alpha:
		subl=[]
		f=0
		for r in I:
			if r.split(':')[1].strip().split(' ')[0]==a:
				if a is '$':
				        f=1
				elif r in ruleList:
					s=r.split(':')[0]+': '+' '.join(r.split(' ')[2:])+' /{}'.format(ruleList.index(r))
					subl.append(s)
				else:
					s=r.split(':')[0]+': '+' '.join(r.split(' ')[2:])
					subl.append(s)				
				
		if len(subl)>0:
			subl=appendS(subl)		
			if subl not in mainList:			
				mainList.append(subl)

		if f==0:
			l.append(subl)
		else:
			l.append(['A'])
			
			
	ptable(l,alpha)
	
				
	
	
	
def ptable(l,alpha):
	
	p=len(parseTable)
	parseTable.append([])
	if all(i==[] for i in l):
		sr.append(0)
		rule=mainList[p][0]
		rule=rule.split('/')[1].strip()
		for i in range(0,len(alpha)):
			if len(parseTable[p])<(alpha.index('$')+1):
				parseTable[p].append('r'+rule)
			else:
				parseTable[p].append(0)
	else:
		sr.append(1)

		for i in l:
			
			if i == ['A']:
				parseTable[p].append('accept')
			elif i == []:
				parseTable[p].append(0)
			else:
				if len(parseTable[p])<(alpha.index('$')+1):
					parseTable[p].append('s'+str(mainList.index(i)))
				else:
					parseTable[p].append(mainList.index(i))

		
	
	
def slrptable(alpha):
	for st in mainList:
		flag=0
		for s in st:
			if s.split(':')[1].split('/')[0].strip()=='':
				rule=s.split('/')[1]
				flag=1
				break;
		if(flag==1):
			for i in range(0,((alpha.index('$')+1))):
				if isinstance(parseTable[mainList.index(st)][i],int):
					parseTable[mainList.index(st)][i]='r'+rule	
	
def appendS(s):
	for j in range(1,len(ruleList)):
			i=s[(len(s)-1)]
			a=i.split(':')[1].strip()
			a=a.split(' ')[0]
			for r in ruleList:
				if r.split(':')[0].strip() == a:
					s.append(r)
	return s
	


num=0
main()
