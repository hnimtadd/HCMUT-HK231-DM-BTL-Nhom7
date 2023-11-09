import pandas as pd
import json
from py_stringmatching import utils
from py_stringmatching.similarity_measure.token_similarity_measure import TokenSimilarityMeasure


from py_stringmatching import utils
from py_stringmatching.similarity_measure.jaro import Jaro
from py_stringmatching.similarity_measure.hybrid_similarity_measure import HybridSimilarityMeasure


def jaccard_similarity(a, b):
    # convert to set
    a = set(a)
    b = set(b)
    # calucate jaccard similarity
    j = float(len(a.intersection(b))) / len(a.union(b))
    return j


def GenArray(x,_size):
    _lenArray = len(x)
    _lenRs = len(x) + _size -1
    rsArray = []
    temp_arr0 =[]
    temp_arr1=[]
    temp_arr2=[]
    temp1 = _size -1
    a = "#"

    for idx in range(0,_size-1):
        b = a
        for idx1 in range(0,temp1):
            b= b + x[idx1]
        temp_arr0.append(b)
        b=""
        a=a+"#"
        temp1-=1

    temp2 = _size -1
    c = "#"
    for idx in range(0,_size-1):
        d =""
        for idx1 in range(0,temp2):
            d= d + x[_lenArray- temp2+idx1]
        d = d + c
        temp_arr2.append(d)
        c=c+"#"
        temp2-=1
    
    for idx in range(0,_lenArray):
        if((idx + _size)>_lenArray):
            break
        e =""
        for idx1 in range(0,_size):
            e+= x[idx+idx1]
        temp_arr1.append(e)
    temp_arr0.reverse()
    return temp_arr0 + temp_arr1 + temp_arr2


class Jaccard(TokenSimilarityMeasure):
    """ Tnh Jaccard Measure
    2 sets X v Y c jaccard(X, Y) = intersection(X,Y)/union(X,Y)
    """
    def __init__(self):
        super(Jaccard, self).__init__()

    def get_raw_score(self, set1, set2):
        """
        Tnh ton Jaccard da trn overlap measure
        Bx = {#d, da, av, ve, e#}, By = {#d, da, av, v#}
        J(x,y) = 3/6
        """
        _lenX = len(set1)
        #print(_lenX)
        _lenY = len(set2)
        #print(_lenY)
        jacard_array = []
        for idx1 in range(0,_lenY):
            genY = GenArray(set2[idx1],2)
            #print(genY)
            for idx2 in range(0,_lenX):
                genX = GenArray(set1[idx2],2)
                #print(genX)
                jacard = jaccard_similarity(genX,genY)
        return jacard
    
    def get_sim_score(self, set1, set2):
        return self.get_raw_score(set1, set2)


class GeneralizedJaccard(HybridSimilarityMeasure):
    """Generalized jaccard similarity measure class.
    2 Parameters:
    sim_func (function): similarity function. Tr v trng khp gia 2 sets string
    threshold (float): Threshold value (defaults to 0.5)
    """
    def __init__(self, sim_func=Jaccard().get_raw_score, threshold=0.5):
        self.sim_func = sim_func
        self.threshold = threshold
        super(GeneralizedJaccard, self).__init__()

    def get_raw_score(self, set1, set2):
        """
        Computes the Generalized Jaccard measure between two sets.
        GJ(x,y) = Total (xi,yj) belongs to M: s(xi,yj) / (|Bx| + |By| - |M|)
        """
        # input validations
        utils.sim_check_for_none(set1, set2)
        utils.sim_check_for_list_or_set_inputs(set1, set2)
        # if exact match return 1.0
        if utils.sim_check_for_exact_match(set1, set2):
            return 1.0
        # if one of the strings is empty return 0
        if utils.sim_check_for_empty(set1, set2):
            return 0
        if not isinstance(set1, set):
            set1 = set(set1)
        if not isinstance(set2, set):
            set2 = set(set2)
        set1_x = set()
        set2_y = set()
        match_score = 0.0
        match_count = 0
        list_matches = []
        for element in set1:
            for item in set2:
                score = self.sim_func(element, item)
                if score > 1 or score < 0:
                    raise ValueError('Similarity measure should return value in the range [0,1]')
                if score > self.threshold:
                    list_matches.append((element, item, score))
        # position of first string, second string and sim score in tuple
        first_string_pos = 0
        second_string_pos = 1
        sim_score_pos = 2
        # sort the score of all the pairs
        list_matches.sort(key=lambda x: x[sim_score_pos], reverse=True)
        # select score in increasing order of their weightage,
        # do not reselect the same element from either set.
        for element in list_matches:
            if (element[first_string_pos] not in set1_x and
                element[second_string_pos] not in set2_y):
                set1_x.add(element[first_string_pos])
                set2_y.add(element[second_string_pos])
                match_score += element[sim_score_pos]
                match_count += 1
        return float(match_score) / float(len(set1) + len(set2) - match_count)

    def get_sim_score(self, set1, set2):
        return self.get_raw_score(set1, set2)
    
    def get_sim_func(self):
        """
        Get similarity function
        Returns:
        similarity function (function)
        """
        return self.sim_func
    
    def get_threshold(self):
        """
        Get threshold used for the similarity function
        Returns:
        threshold (float)
        """
        return self.threshold
    
    def set_sim_func(self, sim_func):
        """
        Set similarity function
        Args:
        sim_func (function): similarity function
        """
        self.sim_func = sim_func
        return True
    
    def set_threshold(self, threshold):
        """
        Set threshold value for the similarity function
        Args:
        threshold (float): threshold value
        """
        self.threshold = threshold
        return True


path_res1 = "/content/drive/MyDrive/btl/JedAI-Spark-master/JedAI-Spark-master/datasets/clean/products/walmart.csv"
dataFrame1 = pd.read_csv(path_res1, engine='python', na_filter=True).astype(str)
path_res2 = "/content/drive/MyDrive/btl/JedAI-Spark-master/JedAI-Spark-master/datasets/clean/products/amazon.csv"
dataFrame2 = pd.read_csv(path_res2, engine="python", na_filter=True).astype(str)

#para dataframe 1
_shape1 = dataFrame1.shape
_lenColumn1 = _shape1[0]
_lenRows1 = _shape1[1]

#para dataframe 2
_shape2 = dataFrame2.shape
_lenColumn2 = _shape2[0]
_lenRows2 = _shape2[1]

#header dataframe
list_header1 = [*dataFrame1]
list_header2 = [*dataFrame2]

#define class GeneralizedJaccard
genJaccard = GeneralizedJaccard()

# Run to find result string matching.
rs_data2 = []
thresHold = 0.4
setA = []
setB = []
for index in range(0,10):
    for indexRow in [3,4,5,7,8,9,14]:
        setTemp = dataFrame1[list_header1[indexRow]][index]
        setA+= setTemp.split()
    for index1 in range(0,10):
        for indexRow1 in [3,4,5,9,13,14,15]:
            setTemp1 = dataFrame2[list_header2[indexRow1]][index1]
            setB+= setTemp1.split()
        genRS = genJaccard.get_sim_score(setA,setB)
        setA = []
        setB = []
        if genRS >= thresHold:
            rs_data2.append({"ID1": dataFrame1[list_header1[0]][index],"ID2": dataFrame2[list_header2[0]][index1]})
            print({"ID1": dataFrame1[list_header1[0]][index],"ID2": dataFrame2[list_header2[0]][index1]})
    setA = []

#read file json
path_js1 = "/content/drive/MyDrive/btl/JedAI-Spark-master/JedAI-Spark-master/datasets/clean/abtBuy/dataset1.json"
path_js2 = "/content/drive/MyDrive/btl/JedAI-Spark-master/JedAI-Spark-master/datasets/clean/abtBuy/dataset2.json"

#file json dataset1 to dataFrame_json1
data_name = []
data_description = []
flag1 = 0
flag2 = 0
temp_js1 = ""
temp_js2 = ""
with open(path_js1, 'r') as JSON:
    for idx in JSON:
        data = json.loads(idx)
        #df2 = pd.DataFrame.from_dict(data, orient="index")
        for name,data_dict in data.items():
            if(name == "description"):
                flag1 = 1
                temp_js1 = data_dict
            if(name == "name"):
                flag2 = 1
                temp_js2 = data_dict
    if flag1 == 1 and flag2 == 1:
        data_description.append(temp_js1)
        data_name.append(temp_js2)
        flag1 = 0
        flag2 = 0

dataFrame_json1 = pd.DataFrame(data_name,data_description,columns=["Name, Description"])
#file json dataset2 to dataFrame_json2
data_name = []
data_description = []
flag1 = 0
flag2 = 0
temp_js1 = ""
temp_js2 = ""
with open(path_js2, 'r') as JSON:
    for idx in JSON:
        data = json.loads(idx)
        #df2 = pd.DataFrame.from_dict(data, orient="index")
        for name,data_dict in data.items():
            if(name == 'description'):
                flag1 = 1
                temp_js1 = data_dict
            if(name == 'name'):
                flag2 = 1
                temp_js2 = data_dict
        if flag1 == 1 and flag2 == 1:
            data_description.append(temp_js1)
            data_name.append(temp_js2)
            flag1 = 0
            flag2 = 0

dataFrame_json2 = pd.DataFrame(data_name,data_description,columns=["Name, Description"])
#Run to find result string matching the same as above