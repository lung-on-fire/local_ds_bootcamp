import sys

def main():
    COMPANIES = {
  'Apple': 'AAPL',
  'Microsoft': 'MSFT',
  'Netflix': 'NFLX',
  'Tesla': 'TSLA',
  'Nokia': 'NOK'
  }
    
    STOCKS = {
  'AAPL': 287.73,
  'MSFT': 173.79,
  'NFLX': 416.90,
  'TSLA': 724.88,
  'NOK': 3.37
  }
    if len(sys.argv) !=2:
        sys.exit()
    else:
        company = sys.argv[1]
        print(get_price(company, COMPANIES, STOCKS))
    return


def get_price(company_name, companies_dict, stocks_dict):
    price_out = "Unknown company"
    company_name = company_name.lower()
    for key in companies_dict:
        if key.lower() == company_name:
            price_out = stocks_dict[companies_dict[key]]
    return price_out

if __name__ == '__main__':
    main()