"""
Project: Supporting Secure Dynamic Alert Zones Using Searchable Encryption and Graph Embedding
Description: This study addresses privacy concerns in location-based alerts by using Hidden Vector Encryption (HVE) and proposes a graph embedding technique to enhance performance. The researchers introduce three heuristics that significantly improve computational overhead compared to existing methods. Experimental evaluations demonstrate the effectiveness of the proposed solutions.
Author: Sina Shaham, Gabriel Ghinita, Cyrus Shahabi
Code: Initial Version
"""


# Import necessary libraries and modules

import numpy as np
from random import randrange
from scipy.optimize import linear_sum_assignment
import numpy as np
import logicmin
import matplotlib.pyplot as plt 
import time
import random


class Grid(object):
    def __init__(self):
        self.nx =0
        self.ny =0
        self.IDs = list()
        self.IDsEncoded = list()
        self.Prob = []
        
    
    def GenGrid(self,cellY,cellX):
        self.nx = cellX
        self.ny = cellY
        self.Prob = np.zeros((self.nx,self.ny)) 
        
        self.IDs = [[0 for col in range(self.nx)] for row in range(self.ny)]
        self.IDsEncoded = [['' for col in range(self.nx)] for row in range(self.ny)]
        
        
    def GenIDs(self):
        for row in range(self.ny):
            for col in range(self.nx):
                self.IDs[row][col] = self.nx*row +col
        
        
 

           
        
        
    """
    Here are the basic and previous approaches.
    """
    #This function encodes the data based on BaseLine encoding
    def encodeBaseline(self):
        for row in range(self.ny):
            for col in range(self.nx):
                codeLength = (self.ny)*(self.nx)
                tmp = str()
                for i in range(codeLength):
                    if i==self.IDs[row][col]:    
                        tmp = tmp+'1'
                    else:
                        tmp=tmp+'0'
                self.IDsEncoded[row][col] = tmp


    def genZonesUniform(self,CovAve):
        NumAlertCells = int(np.ceil((CovAve/100)*(self.nx)*(self.ny)))
        AlertCells = list()
        
        for i in range(NumAlertCells):
            x = self.IDsEncoded[randrange(self.nx)][randrange(self.nx)]
            while x in AlertCells:
                x = self.IDsEncoded[randrange(self.nx)][randrange(self.nx)]
            AlertCells.append(x)    
        
        return AlertCells


    def genZonesHalfNormal(self,CovAve,mu,sigma,dict_assigned):
        NumAlertCells = int(np.ceil((CovAve/100)*(self.nx)*(self.ny)))
        AlertCells = list()
        tmp = list(dict_assigned.values())
        
        for i in range(NumAlertCells):
            RandNum = abs(np.random.normal(mu, sigma))
            targetIndex = np.argmin(abs(RandNum-np.array(tmp)))
            targetCode = list(dict_assigned.keys())[targetIndex]
            
            x = targetCode
            while x in AlertCells:
                RandNum = abs(np.random.normal(mu, sigma))
                targetIndex = np.argmin(abs(RandNum-np.array(tmp)))
                x = list(dict_assigned.keys())[targetIndex]     
#            print('tmp: '+str(tmp))
#            print('RandNum: '+str(RandNum))
#            print('targetIndex: '+str(targetIndex))
#            print('x: '+str(x))
            AlertCells.append(x)    
        return AlertCells
    
    



          

    def func_sigmoid(self,a, b, x):
       '''
       Returns array of a horizontal mirrored normalized sigmoid function
       Output a value between 0 and 1
       Function parameters a = center; b = width
       '''
       s= 1/(1+np.exp(-b*(x-a)))
       return s # normalize function to 0-1

   
    #This is the main one distribution function used in our paper
    def initial_probability_assingment_sigmoid(self,seed,a,b):
        
        print("a: "+ str(a))
        print("b: "+ str(b))      

        print("here is the b")
        
        for row in range(self.ny):
            for col in range(self.nx):
                self.Prob[row,col] = self.func_sigmoid(a, b, randrange(1,seed)/seed)

        Var_dummy = np.max(self.Prob)
        
        for row in range(self.ny):
            for col in range(self.nx):
                self.Prob[row,col] = int(seed*(self.Prob[row,col]/Var_dummy))
















                



    def gen_alertedCells_basedOn_probabilities(self,CovAve,dict_assigned):
        NumAlertCells = int(np.ceil((CovAve/100)*(self.nx)*(self.ny)))
        AlertCells = list()
        Dvalues = list(dict_assigned.values())
        Dkeys = list(dict_assigned.keys())
        acc = [sum(Dvalues[0:i+1]) for i in range(len(Dvalues))]

        
        for i in range(NumAlertCells):

            rnd  = randrange(1,sum(Dvalues))
            rndIndex = -1    
            if rnd<=acc[0]:
                rndIndex = 0
            else:
                for j in range(1,len(acc)):
                    if rnd<=acc[j]:
                        rndIndex = j
                        break
            if rndIndex==-1:
                print('error')

            x = Dkeys[rndIndex]
            while x in AlertCells:
                rnd  = randrange(1,sum(Dvalues))
                rndIndex = -1    
                if rnd<=acc[0]:
                    rndIndex = 0
                else:
                    for j in range(1,len(acc)):
                        if rnd<=acc[j]:
                            rndIndex = j
                            break
                if rndIndex==-1:
                    print('error')
                
                x = Dkeys[rndIndex]
                
            AlertCells.append(x)    
            
            
        return AlertCells









    def gen_alertedCells_basedOn_probabilities_noise(self,
                                                     dict_assigned,
                                                     noise_perc, 
                                                     seed,
                                                     NumAlertCells):
        
        AlertCells = list()
        Dvalues = list(dict_assigned.values())
        

        upper_noise_limit  = int((noise_perc/100)*seed)
        if upper_noise_limit==0:
            upper_noise_limit=1

        Dvalues = [i+randrange(0,upper_noise_limit) for i in Dvalues]


        for i in range(len(Dvalues)):
            if Dvalues[i]>(seed-1):
                Dvalues[i] = Dvalues[i] -seed        
        
        
        Dkeys = list(dict_assigned.keys())
        acc = [sum(Dvalues[0:i+1]) for i in range(len(Dvalues))]

        
        
        
        
        
        for i in range(NumAlertCells):

            rnd  = randrange(1,sum(Dvalues))
            rndIndex = -1    
            if rnd<=acc[0]:
                rndIndex = 0
            else:
                for j in range(1,len(acc)):
                    if rnd<=acc[j]:
                        rndIndex = j
                        break
            if rndIndex==-1:
                print('error')

            x = Dkeys[rndIndex]
            while x in AlertCells:
                rnd  = randrange(1,sum(Dvalues))
                rndIndex = -1    
                if rnd<=acc[0]:
                    rndIndex = 0
                else:
                    for j in range(1,len(acc)):
                        if rnd<=acc[j]:
                            rndIndex = j
                            break
                if rndIndex==-1:
                    print('error')
                
                x = Dkeys[rndIndex]
                
            AlertCells.append(x)    
            
        if len(AlertCells)<NumAlertCells:
            print("error")
            
        return AlertCells  






    def gen_alertedCells_basedOn_probabilities_StateSpace(self,
                                                          dict_assigned,
                                                          noise_perc, 
                                                          seed,
                                                          NumAlertCells,
                                                          twoCell,
                                                          twoCellProbs,
                                                          twoCellIDs):
        
        
        
        AlertCells = list()
        Dvalues = twoCellProbs

        upper_noise_limit  = int((noise_perc/100)*seed)
        if upper_noise_limit==0:
            upper_noise_limit=1

        Dvalues = [i+randrange(0,upper_noise_limit) for i in Dvalues]


        for i in range(len(Dvalues)):
            if Dvalues[i]>(seed-1):
                Dvalues[i] = Dvalues[i] -seed        
        
        acc = [sum(Dvalues[0:i+1]) for i in range(len(Dvalues))]

        
        
        

        rnd  = randrange(1,sum(Dvalues))
        rndIndex = -1    
        if rnd<=acc[0]:
            rndIndex = 0
        else:
            for j in range(1,len(acc)):
                if rnd<=acc[j]:
                    rndIndex = j
                    break
        if rndIndex==-1:
            print('error')
        
        
        
        
        
        
        dictKeys = list(dict_assigned.keys())
        dictValues = list(dict_assigned.values())

        for i in list(twoCellIDs[rndIndex]):
            Index = dictValues.index(i)
            AlertCells.append(dictKeys[Index])
            
            
            
            
            
        return AlertCells  











    def gen_alertedCells_basedOn_probabilities_StateSpace_comparison(self,
                                                          dict_assigned_IDbased,
                                                          noise_perc, 
                                                          seed,
                                                          NumAlertCells,
                                                          oneCell,
                                                          oneCellProbs,
                                                          oneCellIDs):


        AlertCells = list()
        Dvalues = oneCellProbs

        acc = [sum(Dvalues[0:i+1]) for i in range(len(Dvalues))]
        for i in range(NumAlertCells):
        
        
        
        
        
            rnd  = randrange(1,sum(Dvalues))
            rndIndex = -1    
            if rnd<=acc[0]:
                rndIndex = 0
            else:
                for j in range(1,len(acc)):
                    if rnd<=acc[j]:
                        rndIndex = j
                        break
            if rndIndex==-1:
                print('error')
            
        
        
        
        
            dictKeys = list(dict_assigned_IDbased.keys())
            dictValues = list(dict_assigned_IDbased.values())
            


            
            Index = dictValues.index(oneCellIDs[rndIndex])
            x = dictKeys[Index]
            
            
            
            while x in AlertCells:
                rnd  = randrange(1,sum(Dvalues))
                rndIndex = -1    
                if rnd<=acc[0]:
                    rndIndex = 0
                else:
                    for j in range(1,len(acc)):
                        if rnd<=acc[j]:
                            rndIndex = j
                            break
                if rndIndex==-1:
                    print('error')        
            
            
                Index = dictValues.index(oneCellIDs[rndIndex])
                x = dictKeys[Index]        
#                print("x: " + str(x))
#                1/0
            
            AlertCells.append(dictKeys[Index])
        
            
        
        if len(AlertCells)<NumAlertCells:
            print("error")
    
        
    
        return AlertCells      
            
            


###################################  Initialize     #########################################







"""
This is the initialization scripts for all the following algorithms.
"""

# This is used to find the eigenvalues and eigen vectors
import scipy.linalg as la
import copy

##########

#this function is actually called from an outside program Alert zone generator
def minBinaryDict(dict_assigned, AlertCells):
    t = logicmin.TT(len(AlertCells[0]),1)
    tmp = list(dict_assigned.keys())
    for i in tmp:
        if i in AlertCells:
            t.add(i,'1')
        else:
            t.add(i,'0')
    sols = t.solve()
    #x is the output string minimzed using 
    x = sols.printN()
    return x

################

    

def countOnes(str1):
    CounterOne = 0
    for i in range(len(str1)):
        if str1[i] =='1':
            CounterOne+=1
    return CounterOne

################

def plot_prob_dist(grid):
    probList = list(np.reshape(grid.Prob,-1))  
    a = [i/1000 for i in probList]
    plt.plot(range(len(probList)),sorted(a),'*')
    plt.xlabel('Cells') 
    plt.ylabel('Probabilities') 
    plt.title('Probabilities assigned to the grid cells') 
    plt.show() 
    
        
############
def DGenerator(grid_cell_size):
    #this is a particular function designed to find D[i] w.r.t '0000'
    #just works for the ones with a quite 2**2*k
    #To extend it modify it in a way to find all the combinations where it has
    # one one 

    #finds the code length here and figure outs the binaries.
    index_length = int(np.ceil(np.log2(grid_cell_size)))


    #just finds the binary codes
    binaries = ["{0:b}".format(i) for i in range(2**index_length)]
    #number of ones in each codeword
    binaryOnes = [countOnes(i) for i in binaries]

    for i in range(len(binaries)):
        while len(binaries[i])<index_length:
            binaries[i] = '0'+ binaries[i]    
            
    #here we generate the our desired list D     
    D = list()
    K = index_length
    
    for k in range(0,K+1):
        indexes = [i for i in range(len(binaryOnes)) if binaryOnes[i]==k]    
        temp = [binaries[i] for i in indexes]
        D.append(temp)
        
    # the maximum value for the counter is 
    counter = 1
    D2 = list()
    DElements = list()
    for k in range(0,K+1):
        lst = list()
        for j in D[k]:
            if counter<=grid_cell_size:
                lst.append(j)
                DElements.append(j)
                counter+=1
            else:
                break
        D2.append(lst)        
        if counter>grid_cell_size:
            break    
    return D2,DElements
    

def countOnes(str1):
    CounterOne = 0
    for i in range(len(str1)):
        if str1[i] =='1':
            CounterOne+=1
    return CounterOne


#############
def calculateH2(str_root,node_lst,dict_assigned):
    H2 = np.ones(len(node_lst))
    counter = 0
    for i in node_lst:
        PathMems = findGrayCycle(str_root,i)

        PathMems.remove(i)
        for j in range(len(PathMems)):
            H2[counter] = H2[counter]*(dict_assigned[PathMems[j]])

        counter+=1

    return H2


def findGrayCycle(str_root,str1):
    
    #find which digits are hamming bits
    hammingIndexes = []
    for i in range(len(str_root)):
        if str_root[i]!=str1[i]:
            hammingIndexes.append(i)

    #this function returns the complete gray path given the number of hamming bits        
    PathMems = completeGrayPathFromBitNumber(len(hammingIndexes))
    
    for i in range(len(PathMems)):
        x = ''
        counter = 0
        for j in range(len(str_root)):
            if j in hammingIndexes:
                x+= PathMems[i][counter]
                counter+=1
            else:
                x+= str1[j]
                
        
        PathMems[i]=x
    
    return PathMems


def completeGrayPathFromBitNumber(n):
    #this function returns the complete gray path given the number of hamming bits
    if n==0:
        return []
    else:
        n = 2**n
        result = ["{0:b}".format(i) for i in range(n)]
        index_length = int(np.ceil(np.log2(len(result))))
        for i in range(len(result)):
            while len(result[i])<index_length:
                result[i] = '0'+ result[i]    
                
        #Then, I convert them to binary here
        result = [binToGray(result[i]) for i in range(len(result))]
        
        return result


def binToGray(str1):
    res = ''
    for i in range(len(str1)):
        if i==0:
            res=res+str1[i]
        else:
            if str1[i]=='0' and str1[i-1]=='0':
                res =res +'0'
                
            if str1[i]=='0' and str1[i-1]=='1':
                res =res +'1'     
                
            if str1[i]=='1' and str1[i-1]=='0':
                res =res +'1'
                
            if str1[i]=='1' and str1[i-1]=='1':
                res =res +'0'
    return res
##########
#############





def findH1(probList,m):
    """
    This function finds the top maximum m probabilities from the list of probs
    and removes them from the list. Basically H1 in the Hungarian algorithm.
    """    
    H1 = []
    
    for i in range(m):
        H1.append(max(probList)) #append largest element to list of results
        probList.remove(max(probList)) 
        
    return probList, H1

###########
def Match(H1,H2):
    #runs hungarian algorithm, it is a bit tricky here as hungarian algorithm 
    #aims minimizing     
    cost = np.zeros((len(H2),len(H1)))
    for i in range(len(H2)):
        for j in range(len(H1)):
            cost[i,j]=H1[j]*H2[i]
    #notice this important line 
    cost = np.max(cost)-cost
    row_ind, col_ind = linear_sum_assignment(cost)
    return [H1[i] for i in col_ind]    

##########
####################################
def changeBit(bit):
    if bit=='0':
        return '1'
    elif bit=='1':
        return'0'
    else: 
        1/0
        
            
def NeiWithHamDis(str_root,hamDis):
    counter = 0
    lst = list()
    
    if hamDis>len(str_root):
        print('str_root'+str(str_root))
        print('hamDis'+str(hamDis))
        print('error')
        1/0
    if hamDis==0:
        return [str_root]
    
    if hamDis==len(str_root):
        str_tmp = ''
        for i in range(len(str_root)):
            str_tmp = str_tmp + changeBit(str_root[i])
        
            
        return [str_tmp]
    else:        
        fix = str_root[0]
        
        tmp2 = NeiWithHamDis(str_root[1:],hamDis)
        lst.extend([fix+ tmp2[i]  for i in range(len(tmp2))])
        tmp2 = NeiWithHamDis(str_root[1:],hamDis-1)
        lst.extend( [changeBit(fix)+ tmp2[i]  for i in range(len(tmp2))]  )        
        return lst
    
############
def AssignGivenDepth(grid_cell_size,
                     str_root,
                     depth,
                     dict_assigned,
                     probList,
                     DElements):
    
    
    #this is a particular function designed to find D[i] w.r.t 'str_root'
    #print('str_root'+str(str_root))
    #finds the index_length here and figure outs the binaries.
    index_length = int(np.ceil(np.log2(grid_cell_size)))


    D = list()
    K = index_length

    NeiHolder = list()
    
    
    for i in range(1,depth+1):
        hamDis = i
        a = NeiWithHamDis(str_root,hamDis)
        b = list()
#        print('a: ' + str(a))

        for j in range(len(a)):
            if a[j] in DElements:
                b.append(a[j])
        if len(b)>0:
            NeiHolder.append(b)



    if len(NeiHolder)==0:
        print('str_root'+str(str_root))
        print('error')
        1/0
    

    
    #k is basically the hamming distance
    for k in range(len(NeiHolder)):
        
        #count how many of the first neighbors are not in dict_assigned
        counter =0
        tmp_lst = list()
        for i in range(len(NeiHolder[k])):
            if NeiHolder[k][i] not in dict_assigned:
                counter+=1
                tmp_lst.append(NeiHolder[k][i])
                
        if counter>0:
            probList, H1=findH1(probList,counter)
            H2 = calculateH2(str_root,tmp_lst,dict_assigned)

            tmp = Match(H1,H2)
            for i in range(len(tmp)):
                dict_assigned[tmp_lst[i]] =tmp[i]
    

    return dict_assigned




def EigenVec(p1,p2):
    vec = [p1,p2]
    vec = vec/np.sum(vec)
    
    Q = np.array([[0, vec[0], vec[1], 0],
                  [vec[0], 0, 0, vec[1]],
                  [vec[1], 0, 0, vec[0]],
                  [1, 0, 0, 0]])
    Q  = np.transpose(Q )
    
    # In results first you have the eigenvalues and then eigenvectors. So 
    # results[0] returns the eigenvalues and results[1] return eigenvectors
    results = la.eig(Q)
    EigenValues = results[0]
    EigenVectors = results[1]
    
    eigenvalue_zero_index = np.argmax(results[0])
    
    
    EigenVectors = results[1]
    
    EigenVector_EigenValueOne =EigenVectors[:,eigenvalue_zero_index]
    EigenVector_EigenValueOne = EigenVector_EigenValueOne/np.sum(EigenVector_EigenValueOne)
    
    cleaned_EigenVector_EigenValueOne = list()
    for i in range(len(EigenVector_EigenValueOne)):
        cleaned_EigenVector_EigenValueOne.append(np.real(EigenVector_EigenValueOne[i]))
    
    return cleaned_EigenVector_EigenValueOne








def GrayOptimizer(grid,
                  algorithmDepth,
                  initialCellProbabilities,
                  grid_cell_size):
    
    
    
    """
    This function implements:
        1. Gray Optimizer when depth is set to maximum
        2. MSGO when 1<depth<max
        3. SGO when depth = 1
    """
    
    
    
    
    
    """
    D is really important and stores the nodes based on their hamming distance from
    the root node index (all zeros)
    """
    D,DElements= DGenerator(grid_cell_size)


    

 
    for depth in [algorithmDepth]:
        
        

        dict_assigned = {}
        #findH1 finds H1 which is basically the highest probabilities required
        initialCellProbabilities, H1=findH1(initialCellProbabilities,len(D[0]))
        #first nodes is assigned D0
        dict_assigned[D[0][0]] =H1[0]

        
    
        #length of D tells you the maximum hamming distance
        for i in range(0,len(D)):        
            #in each D[i] we want to go through the maximum ones first            
            Di_value = [dict_assigned[D[i][j]] for j in range(len(D[i]))]
            Di_value = np.array(Di_value)
            Di_value_indices = list(np.argsort(Di_value)[::-1])
        
        
            for j in range(len(D[i])):
                dict_assigned = AssignGivenDepth(grid_cell_size,D[i][Di_value_indices[j]],
                                                 depth,dict_assigned,
                                                 initialCellProbabilities,
                                                 DElements)
            
            
    return dict_assigned




















def Gen_AlertedCellsRandomly(dict_assigned,
                             NumAlertCells,
                             sample_size):
    
    """
    First we generate alert cells uniformly random for the purpose of comparison
    The result will be  hold in OtherApproaches array.
    """
    
    result = np.zeros(sample_size)
    
    for sample in range(sample_size):
        
#            NumAlertCells=2
        
        AlertCells = list()
        

        x = list(dict_assigned.keys())
        AlertCells = random.sample(x,NumAlertCells)
        
        

        """
        We are using the logic minimization tool here to generate the tokens
        """
        tmp2 = minBinaryDict(dict_assigned, AlertCells)
        counter = 0
        for i in tmp2:
            if i=='x':
                counter+=1
        result[sample]=counter
    
    OtherApproaches = np.average(result)*2+1   
    
    return OtherApproaches



def Convert_ProbsToIDs_inDictionary(grid,
                                    dict_assigned,
                                    probList):
    
    """
    This function simply returns the assinged dictionary by changing probabilities
    to IDs of cells. 
    """


    IDList = list(np.reshape(grid.IDs,-1))    
    
    dictKeys = list(dict_assigned.keys())
    dictValues = list(dict_assigned.values())
    
    Converted_dict_assigned = {}
    
    
    for i in range(len(dictKeys)):
        target_prob = dictValues[i]
        
        Index = probList.index(target_prob)        
        Converted_dict_assigned[dictKeys[i]] = IDList[Index]
        
        probList.pop(Index)
        IDList.pop(Index)
    
    dict_assigned_IDbased = copy.deepcopy(Converted_dict_assigned)       
    
    return dict_assigned_IDbased




























#################  MAIN ######################
    

grid_cell_size =28900  
grid_dimension  = int(np.sqrt(grid_cell_size))

seed = 1000

'''
Returns array of a horizontal mirrored normalized sigmoid function
Output a value between 0 and 1
Function parameters a = center; b = width
'''



a = 0.75
b = 10



"""
Index length is set to be equal based on the paper. Also the starting root
is set to be the index with all zeros.
"""
index_length = int(np.ceil(np.log2(grid_cell_size)))
str_root = ''
for i in range(index_length):
    str_root+='0'





"""
An object of class Grid is generated 
"""
grid = Grid()
#just write grid.Probs to get the probabilities
grid.GenGrid(grid_dimension,grid_dimension)
#this one generates IDs, Just wride grid.IDs to get them
grid.GenIDs()


"""
We have different test Gen Initial Prob check the number
All we are doing to assign a probability to the cells
"""




grid.initial_probability_assingment_sigmoid(seed,a,b)


"""
If you wanna run based on Chicago dataset use this one
GRID SIZE MUCT BE 1024
"""









"""
You can plot generator function by uncommenting the following line.
"""
plot_prob_dist(grid)




















#################################### Gray Optimizer #########################################



def plot_prob_dist(probList):
    plt.plot(range(len(probList)),sorted(probList),'*')
    plt.xlabel('Cells') 
    plt.ylabel('Numbers (Probabilities)') 
    plt.title('Probabilities assigned to the grid cells') 
    plt.show() 




probList = list(np.reshape(grid.Prob,-1))





#plot_prob_dist(probList)

#for depth in [len(str_root)]:
for depth in [1]:
    """
    This function implements:
        1. Gray Optimizer when depth is set to maximum (len(str_root))
        2. MSGO when 1<depth<max
        3. SGO when depth = 1
        
    I. First input is the grid
    II. Which algorithm you want to run?
    III. Initial probability of the cells
    IV. number of cells in the grid.
    """
    
    dict_assigned = GrayOptimizer(grid = grid,
                                  algorithmDepth = depth,
                                  initialCellProbabilities = probList,
                                  grid_cell_size = grid_cell_size)
    print("Encoding is done")
    """
    Upto here Gray Optimizer is done and we want to test the algorithm.
    """
    sec_one = time.time()   
    #sample_size = 500
    sample_size = 50

    print("grid_cell_size: "+str(grid_cell_size))
    
    
    """
    CovAve specifies the percentage of cells which are alerted.
    """
    for CovAve in [12]:
    
        NumAlertCells = int((grid_cell_size*CovAve)/100)
    

        OtherApproaches = Gen_AlertedCellsRandomly(dict_assigned,
                                                   NumAlertCells,
                                                   sample_size)
        

    
        """
        Next we generate the numbers based on the probabilities of the cells.
        """
        
        
        result = np.zeros(sample_size)
        for sample in range(sample_size):
            
            if sample%20==0:   
                print('sample: '+str(sample))
            

            noise_perc= 0
            
            AlertCells = grid.gen_alertedCells_basedOn_probabilities_noise(dict_assigned,
                                                                           noise_perc, 
                                                                           seed,
                                                                           NumAlertCells)

            tmp2 = minBinaryDict(dict_assigned, AlertCells)
            counter = 0
            for i in tmp2:
                if i=='x':
                    counter+=1
            result[sample]=counter
            
        
        temp1 = []
        for _ in range(5):
            cc = int(sample_size//5)
            NewApproaches_mem = np.average(result[_*cc:(_+1)*cc])*2+1
            Improvement_mem = ((OtherApproaches-NewApproaches_mem)/OtherApproaches)*100
            temp1.append(Improvement_mem)

        print("std   {} ".format(np.std(temp1)))
            
            



        NewApproaches = np.average(result)*2+1
        Improvement = ((OtherApproaches-NewApproaches)/OtherApproaches)*100
        print("Other approaches "+str(OtherApproaches))
        print("New Approache "+str(NewApproaches))
#        print("Improvement for NumAlertCells of " +str(NumAlertCells)+" is "+str(Improvement) )
        print("Percentage of alerted cells " +str(NumAlertCells)+" is "+str(Improvement) )
    
    sec_two = time.time()   

