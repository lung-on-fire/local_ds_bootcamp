import sys, os
class Research():
    def __init__(self):
        self.path = sys.argv[1]


    def file_reader(self):
         with open(self.path, 'r') as file:
            lines = file.readlines()
            if lines:
                header_tokens = lines[0].strip().split(',')
            try:
                if not lines:
                    raise ValueError("Empty file")
                
                elif len(header_tokens) == 1 :
                    raise ValueError("Check the header of file")          
            
                for line in lines[1:]:
                    line = line.strip()
                    if line not in ["1,0", "0,1"]:
                        raise ValueError ("Check the data of file")
                
                else:
                    file.seek(0)
                    self.data = file.read()
                    return self.data
            
            except Exception as error:
                print(f'Error! {error}')
                sys.exit(1)

def main():
    if (len(sys.argv) != 2) or not os.path.exists(sys.argv[1]) or not os.path.isfile(sys.argv[1]):
        sys.exit()
    else:
        self = Research()
        print(Research.file_reader(self))


if __name__ == '__main__':
    main()


## check: data.csv, data1.csv - ok (different type of headers with , as delimeter)
## data2.csv - example, wrong format of data (not 0 with 1)
## data3.csv - example, wrong format of header (; as delimeter)