#Import all required modules
import sys
import re
import random
import itertools
#from pypreprocessor import pypreprocessor



#Define all global variables
#define debug True
#pypreprocessor.parse()
support=int(sys.argv[2])
samplingRate=0.5
fraction=0.8
canFreqItems={}
negBorder={}
FreqItems={}
isPrint=False
filename=sys.argv[1]



def splitData(line_list,splitRatio):
    length=len(line_list)
    splitSize=int(length*splitRatio)
    splitSet=[]
    copiedSet=line_list
    while len(splitSet)<splitSize:
        range=random.randrange(len(copiedSet))
        splitSet.append(copiedSet.pop(range))
    return splitSet

#Define all functions
def getRandomSample(ratio):
    lineList=[]
    my_file=open(filename,"r+")
    for line in my_file:
        temp = re.sub(r',',' ',line)
        temp=temp.split()        
        lineList.append(temp)
    lineListLen=len(lineList)
    rand_smpl = splitData(lineList,ratio)  
    return rand_smpl

def getSupportValue(sup):
    return sup*fraction*samplingRate

def getCanFreqItemsAndNegBorder(inputList,_pass,sup):
    global canFreqItems
    global negBorder
    flag=False
    Items={}    
    for subList in inputList:
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
        else:
            if isPrint==True:
                print "_pass>1 entered"
            tempItems=list(itertools.combinations(subList,_pass))
            if isPrint==True:
                print tempItems
            for tuples in tempItems:
                temp2Items=list(itertools.combinations(tuples,_pass-1))
                for item in temp2Items:
                    if item in canFreqItems:
                        flag=True
                    else:
                        flag=False
                        break
                if flag==True:
                    tuples=tuple(sorted(tuples))
                    if tuples in Items:
                        Items[tuples]+=1
                    else:
                        Items[tuples]=1
    #print Items            
    for key in Items:
        if Items[key]>=sup:
            canFreqItems[key]=Items[key]
        else:
            negBorder[key]=Items[key]
            
    lenCanFreqItemsCurItr=len(canFreqItems)
    return canFreqItems,negBorder,lenCanFreqItemsCurItr

def getFreqItems(inputList,_pass,sup):    
    global FreqItems
    global isPrint
    flag=False
    Items={}    
    for subList in inputList:
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
        else:
            if isPrint==True:
                print "_pass>1 entered"
            tempItems=list(itertools.combinations(subList,_pass))
            if isPrint==True:
                print tempItems
            for tuples in tempItems:
                temp2Items=list(itertools.combinations(tuples,_pass-1))
                for item in temp2Items:
                    if item in FreqItems:
                        flag=True
                    else:
                        flag=False
                        break
                if flag==True:
                    tuples=tuple(sorted(tuples))
                    if tuples in Items:
                        Items[tuples]+=1
                    else:
                        Items[tuples]=1
    if isPrint==True:
        print Items
    for key in Items:
        if Items[key]>=sup:
            FreqItems[key]=Items[key]
            
    if isPrint==True:
        print "FreqItems:"
        print FreqItems
    lenFreqItemsCurItr=len(FreqItems)
    return FreqItems,lenFreqItemsCurItr
    

def getList(my_dict):
    my_list=my_dict.keys()
    my_list.sort()
    return my_list

def convertTupleToList(freqItems):
    my_list=[]    
    for tuples in freqItems:
        my_list.append(list(tuples))
    return my_list

def findMaxLenOfItem(my_list):
    size=0
    for item in my_list:
        if len(item)>size:
            size=len(item)
    return size

def extractList(my_list):
    size=1    
    maxLen=findMaxLenOfItem(my_list)
    while(size<=maxLen):
        new_list=[]
        for item in my_list:
            if len(item) == size:
                new_list.append(item)
        new_list.sort()
        print "Items of size %d : "%(size),
        print new_list
        size+=1



def compare(list1,list2):
    for item in list1:
        if item in list2:
            return True
    return False

#Main Function
if __name__ == '__main__':
    repeatToivonen=True
    noOfItr=0
    while repeatToivonen==True:
        noOfItr+=1
        repeatToivonen=False

    #Generating Frequent Items from the Sample Data
        line=getRandomSample(samplingRate)    
        sampleSupport=getSupportValue(support)#replace support with sys.argv[1]    
        _pass=1    
        lenCanFreqItemsCurItr=1
        lenCanFreqItemsPrevItr=0
        while lenCanFreqItemsCurItr!=lenCanFreqItemsPrevItr:
            lenCanFreqItemsPrevItr=lenCanFreqItemsCurItr    
            canFreqItems,negBorder,lenCanFreqItemsCurItr=getCanFreqItemsAndNegBorder(line,_pass,sampleSupport)
            _pass+=1
            
        print "Frequent Item sets from the sample :"
        canFreqItemsList=getList(canFreqItems)
        canFreqItemsList=convertTupleToList(canFreqItemsList)    
        extractList(canFreqItemsList)

        print "\nItem sets in negative border from the sample :"
        negBorderList=getList(negBorder)
        negBorderList=convertTupleToList(negBorderList)    
        extractList(negBorderList)


    #Generating Frequent Items from the Whole file**************
        line=getRandomSample(1)
        lenFreqItemsCurItr=1
        lenFreqItemsPrevItr=0     
        _pass=1
        while lenFreqItemsCurItr!=lenFreqItemsPrevItr:
            lenFreqItemsPrevItr=lenFreqItemsCurItr    
            freqItems,lenFreqItemsCurItr=getFreqItems(line,_pass,support)
            _pass+=1               

        print"******************************************"
        print "\nFrequent items in the entire data set:"    
        FreqItemList=getList(FreqItems)    
        FreqItemList=convertTupleToList(FreqItemList)    
        extractList(FreqItemList)
    #****************************************************************"""

        flag = compare(negBorderList,FreqItemList)
        print "\nIs the negative border of sample in the frequent Item List of whole data set : " + str(flag)
        repeatToivonen=flag


    print "No. of Iterations : %d"%noOfItr
    print "Fraction of transactions used : %f"%samplingRate
            
        
