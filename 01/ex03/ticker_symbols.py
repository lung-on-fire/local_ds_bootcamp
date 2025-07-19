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
        ticker = sys.argv[1]
        print(get_company(ticker, COMPANIES), get_price(ticker, STOCKS))
    return

def get_company(ticker_name, companies_dict):
    company_out = "Unknown ticker"
    ticker_name = ticker_name.lower()
    for company_name, ticker_n in companies_dict.items():
        if ticker_n.lower() == ticker_name:
            company_out = company_name
    return company_out

def get_price(ticker_name, stocks_dict):
    price_out = ""
    ticker_name = ticker_name.lower()
    for key in stocks_dict:
        if key.lower() == ticker_name:
            price_out = stocks_dict[key]
    return price_out

if __name__ == '__main__':
    main()