import pandas as pd

fd=pd.read_csv("data.csv", names=["movie_id","movie_name","year","director", 'rating', ])
data_dict=fd.to_dict()

class movie(object):

    def __init__(self,dictionary):
        for key in dictionary:
            setattr(self,key,dictionary[key])


data_dict["movie_id"]= dict((v,k) for k,v in data_dict["movie_id"].items())
data_dict["movie_name"]= dict((v,k) for k,v in data_dict["movie_name"].items())

data = {
	'id' : data_dict["movie_id"],
	'name' : data_dict["movie_name"]
}

#print(data)
for i in data:
	print(i.id)
	print(i.name)
	
# x=movie(data_dict)
# print(x.movie_id)
# print(data_dict
# for i in x.movie_name:
# 	print(i)