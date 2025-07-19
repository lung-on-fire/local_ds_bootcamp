#!/home/lungaria/Desktop/School21/DS_Bootcamp.Day03-1/src/ex00/shylaisa/shylaisa_env/bin/python
import os

def virtualenv_set():
    virtual_env_path = os.getenv('VIRTUAL_ENV')
    print (f"Your current virtual env is {virtual_env_path}")



##alternative: - KeyError 
##virtual_env_path = os.environ['VIRTUAL_ENV']
##print (f"Your current virtual env is {virtual_env_path}")

if __name__ == '__main__':
    virtualenv_set()