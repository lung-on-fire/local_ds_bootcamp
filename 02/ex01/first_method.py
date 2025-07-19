##class Research:
    ##def __init__(self):
        ##with open('data.csv', 'r') as file:
            ##self.data = file.read()
    
    ##def file_reader(self):
        ##return self.data
    

class Research:
        def file_reader(self):
            with open('data.csv', 'r') as file:
                 self.data = file.read()
                 return self.data
    

if __name__ == '__main__':
    self = Research()
    print(Research.file_reader(self))