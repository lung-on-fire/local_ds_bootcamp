##class Must_read:
    ##def __init__(self):
        ##with open('data.csv', 'r') as file:
            ##self.data = file.read()
            ##print(self.data)

class Must_read:
        with open('data.csv', 'r') as file:
            data = file.read()
            print(data)

if __name__ == '__main__':
    Must_read()