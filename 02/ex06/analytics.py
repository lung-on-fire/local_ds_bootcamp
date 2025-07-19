import sys, os
import logging
import requests
from random import randint
import sys
from random import randint


logger = logging.getLogger(__name__)
logging.basicConfig(filename='analytics.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')
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
                        logging.info('The file was read')
                    else:
                        self.data = [list(map(int, line.strip('\n').split(','))) for line in lines[0:]]
                        logging.info('The file was read')
                    return self.data
            
            except Exception as error:
                print(f'Error! {error}')
                sys.exit(1)  

    def send_telegram_message(self):

        self.token = '7635404400:AAF4SC-DVMhFkM5_tl93_pnMp6ssVJNfWEM'
        self.chat_id = '784232671'
        self.telegram_url = f'https://api.telegram.org/bot{self.token}/sendMessage'

        if os.path.isfile("report.txt"):
             message = "The report has been successfully created"
        else:
             message = "The report has not been created due to an error"
        
        payload = {'chat_id': self.chat_id, 'text': message}
        response = requests.post(self.telegram_url,data=payload)

        if response.status_code == 200:
             logging.info('Telegram message was sent')
        else:
             logging.info('Telegram message was not sent')    
    
    class Calculations:         
                def __init__(self, data):
                    self.data = data
                
                def counts(self):
                     self.heads = 0
                     self.tails = 0
                     if self.data is None:
                         sys.exit(1)
                     else:
                         for elem in self.data:
                            if elem == [1, 0]:
                                self.heads += 1 
                            elif elem == [0, 1]:
                                self.tails += 1
                         logging.info('The number of heads and tails was calculated')
                         return self.heads, self.tails
                
                def fractions(self, heads, tails):
                     heads_perc = heads/(heads + tails)
                     tails_perc = tails/(heads + tails)
                     logging.info('The percentage of heads and tails was calculated')
                     return heads_perc, tails_perc


    class Analytics(Calculations):
        def predict_random(self, num_of_steps):
            predictions = []
            for _ in range(num_of_steps):
                heads = randint(0,1)
                tails = 1 - heads
                predictions.append([heads, tails])
            logging.info(f'{num_of_steps} random predictions were done')
            return predictions

        def predict_last(self, data):
            logging.info('The last prediction was done')
            return data[-1] if data else None
        
        def save_file(self, data, filename, ext = "txt"):
            with open(f"{filename}.{ext}", 'w') as file:
                 file.write(data)
            logging.info('The report was saved in %s', f"{filename}.{ext}")
