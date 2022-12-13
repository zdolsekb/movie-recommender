import pandas
class MovieData:
    def __init__(self,path):
        self.path = path
        self.data = pandas.read_csv(self.path, sep='\t', encoding='ISO-8859-1')
    def get_title(self,id):
        return self.data[self.data.id == id]['title'].values[0]

