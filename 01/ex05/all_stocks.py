import sys

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

def normalize_input(expression):
    return expression.strip().upper()

def main():
  
  if len(sys.argv) != 2:
        sys.exit()
  
  input_string = sys.argv[1]

  if ",," in input_string:
        sys.exit()

  expressions = input_string.split(',')

  for expression in expressions:
        normalized_expression = normalize_input(expression)
        normalized_companies = [normalize_input(company) for company in COMPANIES]

        if normalized_expression in STOCKS:
            ticker = normalized_expression
            for key, value in COMPANIES.items():
                if value == ticker:
                    company = key
                    break
            print(f"{ticker} is a ticker symbol for {company}")

        elif normalized_expression in normalized_companies:
            for key in COMPANIES:
                if normalize_input(key) == normalized_expression:
                    company = key
                    ticker = COMPANIES[company]
                    stock_price = STOCKS[ticker]
                    break
            print(f"{company} stock price is {stock_price}")

        else:
            print(f"{expression.strip()} is an unknown company or an unknown ticker symbol")

if __name__ == "__main__":
    main()
    