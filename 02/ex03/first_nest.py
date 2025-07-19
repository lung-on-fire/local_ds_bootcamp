import sys, os
class Research():
    def __init__(self):
        self.path = sys.argv[1]
        self.data = []

    def file_reader(self):
         self.has_header = True
         with open(self.path, 'r') as file:
            lines = file.readlines()
            if lines:
                header = lines[0].strip()

            if header in ["1,0", "0,1"]:
                self.has_header = False

            try:
                if not lines or not header:
                    raise ValueError("Empty file")        
            
                for line in lines[1:]:
                    line = line.strip()
                    if line not in ["1,0", "0,1"]:
                        raise ValueError ("Check the data of file")
                
                else:
                    file.seek(0)
                    if self.has_header == True:
                        self.data = [list(map(int, line.strip('\n').split(','))) for line in lines[1:]]
                    else:
                        self.data = [list(map(int, line.strip('\n').split(','))) for line in lines[0:]]
                    return self.data
            
            except Exception as error:
                print(f'Error! {error}')
                sys.exit(1)

    
    class Calculations:
                def counts(self, data):
                     self.heads = 0
                     self.tails = 0
                     for elem in data:
                          if elem == [1, 0]:
                               self.heads += 1 
                          elif elem == [0, 1]:
                               self.tails += 1
                     return self.heads, self.tails
                
                def fractions(self, heads, tails):
                     heads_perc = heads/(heads + tails)
                     tails_perc = tails/(heads + tails)
                     return heads_perc, tails_perc
                     



def main():
    if (len(sys.argv) != 2) or not os.path.exists(sys.argv[1]) or not os.path.isfile(sys.argv[1]):
        sys.exit()
    else:
        self = Research()
        data = Research.file_reader(self)
        Calculations = Research.Calculations()
        heads, tails = Calculations.counts(data)
        heads_perc, tails_perc = Calculations.fractions(heads, tails)
        print(data)
        print(heads,tails)
        print(heads_perc, tails_perc)


if __name__ == '__main__':
    main()

##data.csv - with header
##data1.csv - w/o header