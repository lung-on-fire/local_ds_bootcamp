import sys
import requests
from urllib.error import URLError
from bs4 import BeautifulSoup
import cProfile, pstats
from pstats import SortKey

def prepare_html(filename, ticker_name):
    try:
        url = f'https://finance.yahoo.com/quote/{ticker_name}/financials/'

        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        with open(filename, "w") as output_file:
            output_file.write(resp.text)

        with open(filename) as fp:
            soup = BeautifulSoup(fp, features="html.parser") 
        if not soup.find('div', class_='rowTitle yf-t22klz'):
            raise ValueError("Incorrect URL!")
    
    except URLError:
        raise ValueError("Error! Network error")
    
    except Exception as error:
        print(f"Error! {error}")
        sys.exit(1)

def extract_info(filename, input_field):
    result = []
    try:
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

def script_profiling_top5(profile):
    output_file = 'pstats-cumulative.txt'
    with open (output_file, "w") as file:
        p = pstats.Stats(profile, stream=file)
        p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(5)

if __name__ == "__main__":
    filename = "financial.html"
    profile = "profiling-sleep.prof"
    if len(sys.argv) != 3:
         raise ValueError ("You should provide two arguments: ticker name and requested field")
    else: 
        ticker_name = sys.argv[1]
        input_field = sys.argv[2]

        profiler = cProfile.Profile()
        profiler.enable()
        prepare_html(filename, ticker_name)
        print(extract_info(filename, input_field))
        profiler.disable()
        profiler.dump_stats(profile)
        script_profiling_top5(profile)

##top5:python3 -m cProfile -s cumulative financial_enhanced.py 'MSFT' 'Total Revenue'| head -n 11 >output.txt
 
    