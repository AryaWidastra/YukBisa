import json
import numpy as np
import pandas as pd

class HandleofCSV: 
    def __init__(self,File_name):
        self.File_name = File_name
        df = pd.read_csv(File_name)
        self.data = {}
        for i in df:
            self.data[i] = df[i].tolist()
        self.dataFrame = df
    def CSVtoJson (self,FileJson):
        df = pd.read_csv(self.File_name)
        daf = []
        for i in range(len(df)):
            row = {}
            for j in df:
                try :
                    a = float(df[j][i])
                except:
                    a = str(df[j][i]) 
                row[j] = a
            daf.append(row)
        with open("{}.json".format(FileJson), "w") as write_file:
            json.dump(daf,write_file)

class HandleofJson:
    def __init__(self,File_name):
        self.File_name = File_name
        with open(File_name, "r") as read_file:
            self.data = json.load(read_file)
        ran = {}
        key_list = list(self.data[0].keys())
        for key in key_list:
            ran[key] = []
        for i in self.data:
            for key in key_list:
                ran[key].append(i[key])
        self.dataFrame = pd.DataFrame(ran)
    def JsonToCSV(self,FileCSV):
        self.dataFrame.to_csv('{}.csv'.format(FileCSV), index=False) 
