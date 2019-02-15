import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
aa = pd.read_csv("tst.csv")
newtable = pd.DataFrame(aa)
newtable.set_index("name", inplace = True)
username = "e"     ##user for which prediction is being generated

old = newtable
len = old.shape[0]
old = old.replace(0,np.nan)

userarr = old.loc[username,:].values


sum = 0
#print(newtablec['0']['L'])
ind = old.index.values
j = 0
dic = {}
dics = {}
for i in (ind):
    df = pd.DataFrame(userarr)
    if (i!=username):
        temparr = old.iloc[j,:].values
        #print(temparr)
        df = pd.DataFrame(userarr).T
        df2 = (pd.DataFrame(temparr)).T
        df2.index = [1]
        
        df = df.append(df2)
        df.dropna(axis = 1,inplace=True)
        
        sim = cosine_similarity(df)[0,1]
        dic[str(i)] = float(sim)
        #print (df)
        
    j= j+1

attributeToPredict =  old.columns.values ##Can iterate over this
allcolsofuser = old.loc[username,:].values
len2 = attributeToPredict.shape[0]

old['mean'] = old.mean(axis = 1)

for k in range(len2):
    if (np.isnan(allcolsofuser[k])):
        answer = old.loc[username,'mean']
        numerator = 0
        denominator = 0
        old = old.fillna(0)
        for i in (dic.keys()):
            
            numerator = numerator + dic[i]*(old.loc[i,attributeToPredict[k]] - old.loc[i,'mean'])
            denominator = denominator + dic[i]
            answer = answer + numerator/denominator
        old.loc[username,attributeToPredict[k]] = answer

final = old.loc[username,:].values
final = np.sort(final)
final = final[::-1]
print(final)

