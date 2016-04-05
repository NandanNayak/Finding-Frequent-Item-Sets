import re
import itertools
import sys
#Define all macros
fileName=sys.argv[1]
hashTable={}
bitVector={}
singletonIdx=0
pair=2
items={}
freqItems=[]
freqItemsCurItr=[]
support=int(sys.argv[2])
bucketSize=int(sys.argv[3])
weight=0
my_dict={}
bitVector=[]
isPrint=False
bitMapSize=0


#Define all functions
def getVal(item,my_d):
    if item in my_d:
        return my_d[item]

def addWeights(d,basket):
    global weight
    for item in basket:
        if item not in d:
            d[item]=weight
            weight+=1    

def updateHashTable(line,my_dict,size):
    global hashTable    
    v1=v2=total=0    
    items = [list(x) for x in itertools.combinations(line, size)]
    if isPrint==True:
        print "UpdateHashTable"
        print items
    for key in items:
        total=0
        for item in key:
            v1=getVal(item,my_dict)            
            total+=v1
        total=total%bucketSize
        if isPrint==True:
            print "%s - %d"%(key,total)
        hashTable[total]+=1

def printMemSize(items,_pass):
    if _pass==0:
        print "memory for item counts: %d"%((8+_pass*4)*len(items))
    else:
        print "memory for candidates counts of size %d : %d"%(_pass+1,(8+_pass*4)*(len(items)))

def printMemSizeHashTable(candidateType):
    print "memory for hash table counts for size %d itemsets: %d"%(candidateType,4*len(hashTable))

def generateFreqCandidates(items):
    global freqItemsCurItr
    temp=[]
    freqItemsCurItr=[]
    for key in items:
        if items[key]>=support:
            freqItemsCurItr.append(key)
            freqItems.append(key)
    freqItems.sort()    
    freqItemsCurItr.sort()
    for tuples in freqItemsCurItr:        
        temp.append(list(tuples))
    freqItemsCurItr=temp
    
    return freqItemsCurItr

def updateFreqItems(items):
    global freqItems
    freqItems.append(items)
    if isPrint==True:
        print "FreqItems:"
        print freqItems

def printFreqItems(Idx):
    global freqItems
    print freqItems[Idx]

def generateHashTable(size):
    global hashTable
    for i in range(size):
        hashTable[i]=0

def generateCandidates(candidates,_pass):
    candidateItems = list(itertools.combinations(candidates,_pass+1))
    return candidateItems
    
            

def countCandidatesAndFillHashTable(_pass):
    global items
    global my_dict #Has weights for each item in the basket
    global freqItems
    flag=False
    weight=-1
    my_file= open(fileName,"r+")
    #***Counting Candidates***#
    for line in my_file:
        line = re.sub(r'\n',"",line)
        basket = line.split(',')
        basket.sort()
        if isPrint==True:
            print "New Line"        
            print basket
        if (_pass==0):                    
            addWeights(my_dict,basket)
        #else:
            #print freqItems
            #candidateItems=generateCandidates(freqItems[0],_pass)
        itemsInBasket = list(itertools.combinations(basket,_pass+1))
        if isPrint==True:
            print itemsInBasket                    
        for item in itemsInBasket:
            if (_pass!=0):
                item_1=list(itertools.combinations(item,_pass))
                for key in item_1:
                    if key in freqItems:
                        flag=True
                    else:
                        flag=False
                        break
                if flag==True:
                    if item in items:
                        items[item]+=1
                    else:
                        items[item]=1
            else:
                if item in items:
                    items[item]+=1
                else:
                    items[item]=1        
        updateHashTable(basket,my_dict,_pass+2)        
    my_file.close()

def generateBitVector():
    global bitVector
    global bitMapSize
    bitVector=[]
    flag=False
    for i in range(bucketSize):
        if hashTable[i]>=support:
            bitVector.append(1)
            flag=True
        else:
            bitVector.append(0)
    if isPrint==True:
        print "BitVector:%d"%(flag)
        print bitVector
    #print "bitmap size : %d"%(len(bitVector))
    bitMapSize=len(bitVector)
    return flag
    

def isNextPassPossible(_pass):
    global items
    global freqItemsCurItr
    bitVectorFlag=False
    if isPrint==True:
        print "isFreqCandidatePresent:"
    print "frequent item sets of size %d : "%(_pass),
    print generateFreqCandidates(items)
    bitVectorFlag=generateBitVector()
    if isPrint==True:
        print "BitVector:%d"%(bitVectorFlag)
    if isPrint==True:
        print "Len of Freq Items : %d"%(len(freqItems[_pass-1]))
    if (len(freqItemsCurItr)>0 and bitVectorFlag==True):
        if isPrint==True:
            print "isNextPassPossible : True"
        return True
    else:
        if isPrint==True:
            print "isNextPassPossible : False"
        return False
    

def cls():
    print "\n" *100

#Generating items-singletons
#def __main__():
if __name__ == '__main__':
    #global my_dict
    #global hash    
    #cls()
    _pass=0
    size=0
    while (_pass==0 or isNextPassPossible(_pass)==True):
        print "\nPASS : %d"%(_pass+1)
        items={}    
        generateHashTable(bucketSize)
        countCandidatesAndFillHashTable(_pass)
        #fillHashTable()
        if isPrint==True:
            print "my_dict:"
            print my_dict
        if _pass!=0:
            size=_pass-1
            print "memory for frequent itemsets of size %d : %d"%(_pass,(8+size*4)*len(freqItemsCurItr))
            print "bitmap size : %d"%(bitMapSize)
        if len(items)!=0:
            printMemSize(items,_pass)
            #print items
            printMemSizeHashTable(_pass+2)
            print hashTable
        _pass+=1



    
    
