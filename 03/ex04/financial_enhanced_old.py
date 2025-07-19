import sys
import validators
import requests
from bs4 import BeautifulSoup
import cProfile, pstats
from pstats import SortKey
def prepare_html(filename):
    try:
        if len(sys.argv) != 3:
            raise ValueError ("You should provide two arguments: ticker name and requestedman field")
        else:
            ticker_name = sys.argv[1]
            url = f'https://finance.yahoo.com/quote/{ticker_name}/financials/'
            if not is_valid_url(url):
                raise ValueError("Incorrect URL!")
            
            else:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
                resp = requests.get(url, headers=headers)
                with open(filename, "w") as output_file:
                    output_file.write(resp.text)
                #time.sleep(5)


    except Exception as error:
        print(f"Error! {error}")
        sys.exit(1)

def extract_info(filename):
    result = []
    try:
        input_field = sys.argv[2]
        with open(filename) as fp:
            soup = BeautifulSoup(fp, features="html.parser")

        title_div = soup.find('div', class_='rowTitle yf-t22klz', title=input_field)
        if not title_div:
            raise ValueError("Incorrect requested field name!")
        else:
            result.append(title_div.get_text())
            if title_div:
                parent_div = title_div.find_parent('div')
                if parent_div:
                    alt_divs = parent_div.find_next_siblings('div')
                    numbers = [div.get_text(strip=True) for div in alt_divs]
                    result.extend(numbers)

        return tuple(result)
    
    except Exception as error:
        print(f"Error! {error}")
        sys.exit(1)

#def script_profiling_top5(profile):
    #output_file = 'pstats-cumulative.txt'
    #with open (output_file, "w") as file:
        #p = pstats.Stats(profile, stream=file)
        #p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(5)

def is_valid_url(url):
    return validators.url(url)
    

if __name__ == "__main__":
    filename = "financial.html"
    profile = "profiling-sleep.prof"
    #profiler = cProfile.Profile()
    #profiler.enable()
    print(extract_info(filename))
    #profiler.disable()
    #profiler.dump_stats(profile)
    #script_profiling_top5(profile)

##top5:python3 -m cProfile -s cumulative financial_enhanced.py 'MSFT' 'Total Revenue'| head -n 11 >output.txt
    