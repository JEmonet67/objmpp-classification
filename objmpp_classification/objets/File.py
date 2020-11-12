import pickle

class File:
    def __init__(self,path):
        self.path = path
        

    def save_binary(self,obj):
        file = open(self.path,"wb")
        pickle.Pickler(file).dump(obj)
        file.close()
