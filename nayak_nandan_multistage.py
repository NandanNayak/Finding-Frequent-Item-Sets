import re
import itertools
import sys
#Define all macros
support=int(sys.argv[2]) #Replace with Sys.argv
bucketSize=int(sys.argv[3]) #Replace this with sys.argv
isPrint=False
FreqItems=[]
Items={}
hashTable1={}
hashTable2={}
bitVector1=[]
bitVector2=[]
weight=0
my_dict={}
filename=sys.argv[1]

def addWeights(basket):
    global weight
    global my_dict
    for item in basket:
        if item not in my_dict:
            my_dict[item]=weight
            weight+=1 

def isBitSet(bitVector,val,typeTable):    
    if typeTable==1:
        val%=20
    else:
        val%=10
    if bitVector[val]==1:
        return True
    else:
        return False

def getItemCounts(inputList,_pass):    
    global FreqItems
    global isPrint
    global Items
    global bitVector1
    global bitVector2
    flag=False
    temp={}
    Items={}
    total=0
    for subList in inputList:
        subList.sort()
        if _pass==1:            
            if isPrint==True:
                print "_pass = 1 entered"
            tempItems=list(itertools.combinations(subList,_pass))
            if isPrint==True:
                print tempItems
            for tuples in tempItems:
                if tuples in Items:
                    Items[tuples]+=1
                else:
                    Items[tuples]=1
            addWeights(subList)
            
        else:
            if isPrint==True:
                print "_pass>1 entered"
            tempItems=list(itertools.combinations(subList,_pass))
            if isPrint==True:
                print tempItems
            for tuples in tempItems:
                temp2Items=list(itertools.combinations(tuples,_pass-1))
                total=0
                for item in temp2Items:
                    if item in FreqItems:
                        total+=my_dict[item[0]]                        
                        flag=True
                    else:
                        flag=False
                        break
                
                if flag==True and isBitSet(bitVector1,total,1) and isBitSet(bitVector2,total,2):
                #if flag==True:   
                    tuples=tuple(sorted(tuples))
                    if tuples in Items:
                        Items[tuples]+=1
                    else:
                        Items[tuples]=1
    
    if _pass==1:
        print "memory for item counts: %d"%((8+(_pass-1)*4)*len(Items))
    else:
        print "memory for candidates counts of size %d : %d"%(_pass,(8+(_pass-1)*4)*(len(Items)))
    if len(Items)==0:
        return False
    else:
        return True

def fill(hashTable,line,_pass,tableType):
    hashTable=initialize(hashTable)
    hashTable=update(hashTable,line,_pass,tableType)
    print "memory for hash table %d counts for size %d itemsets: %d"%(tableType,_pass+1,4*len(hashTable))
    print hashTable
    return hashTable

def readFile():
    my_file=open(filename,"r+")
    my_lines=[]
    for line in my_file:
        temp=re.sub(r',',' ',line)
        temp=temp.split()
        my_lines.append(temp)
    return my_lines

def initialize(hashTable):
    global bucketSize        
    for i in range(bucketSize):       
        hashTable[i]=0
    return hashTable

def generateTuples(line,_pass):    
    tempItems=list(itertools.combinations(line,_pass+1))
    return tempItems

def findHashValue(group,tableType):
    total=0
    for item in group:
        total+=my_dict[item]
    if tableType==1:
        total=total%20
    else:
        total=total%10
    return total

def update(hashTable,line,_pass,tableType):
    for subLine in line:
        tuples=generateTuples(subLine,_pass)
        for eachTuple in tuples:
            hashValue=findHashValue(eachTuple,tableType)
            hashTable[hashValue]+=1
    return hashTable

def findFreqItems(inDict,_pass):
    size=_pass
    for key in inDict:
        if inDict[key]>=support:
            FreqItems.append(key)
    FreqItemList=convertTupleToList(FreqItems)
    extractList(FreqItemList,_pass-1)
    

def generateBitVector(hashTable,bitVector,vecType):    
    for i in range(bucketSize):
        if hashTable[i]>=support:
            bitVector[i]=1
        else:
            bitVector[i]=0
    print "bitmap %d size: %d"%(vecType,len(bitVector))
    return bitVector

def initializeVec(Vector):    
    global bucketSize
    for i in range(bucketSize):
        Vector.append(0)
    return Vector

def convertTupleToList(freqItems):
    my_list=[]    
    for tuples in freqItems:
        my_list.append(list(tuples))
    return my_list

def extractList(my_list,size):        
    #maxLen=findMaxLenOfItem(my_list)
    #while(size<=maxLen):
    new_list=[]
    for item in my_list:
        if len(item) == size:
            new_list.append(item)
    new_list.sort()
    print "Frequent itemsets of size %d : "%(size),
    print new_list
    print "\nmemory for frequent itemsets of size %d : %d"%(size,(8+(size-1)*4)*len(new_list))
    

def findMaxLenOfItem(my_list):
    size=0
    for item in my_list:
        if len(item)>size:
            size=len(item)
    return size

if __name__=='__main__':
    _pass=1
    subPass=1
    flag=True
    bitVector1=initializeVec(bitVector1)
    bitVector2=initializeVec(bitVector2)
    while(flag==True):
        line=readFile()
        #print line
        if _pass==1:
            flag=getItemCounts(line,_pass)
            hashTable1=fill(hashTable1,line,_pass,1)
            _pass+=1
        else:            
            if subPass==1:
                findFreqItems(Items,_pass)
                bitVector1=generateBitVector(hashTable1,bitVector1,1)
                #print bitVector1
                hashTable2=fill(hashTable2,line,_pass-1,2)
                subPass=2
            else:
                subPass=1
                bitVector2=generateBitVector(hashTable2,bitVector2,2)
                #print bitVector2
                flag=getItemCounts(line,_pass)
                hashTable1=fill(hashTable1,line,_pass,1)
                _pass+=1

    FreqItemList=convertTupleToList(FreqItems)
    #extractList(FreqItemList,size)
        
        
