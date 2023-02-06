import src.Holding as hd
import logging

logging.basicConfig(level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(message)s',
      filename='./tmp/backtest.log',
      filemode='w')


class Holdings:

    def __init__(self, max_holdings: int):
        self._max_holdings = max_holdings
        self._cash_holdings = {} # dictionary of cashed out holdings
        self._holdings_dict: dict[str, hd.Holding] = {}

    def get_max_holdings(self):
        return self._max_holdings

    def get_non_cash_max_holdings(self):
        return len(self._cash_holdings.keys())

    def get_current_holdings_number(self):
        return len(self._holdings_dict)

    def add_holding(self, ticker: str, date_bought, date_first_bought, price, repeat=False, exchange='NYSE', stop_loss=.1, multiplier=1): # TODO: What is stop_loss?
        # Replace date_first_bought if it's already present in holdings
        
        assert ticker not in self._holdings_dict.keys()
        assert self.get_current_holdings_number() < self.get_max_holdings()

        # Create new holding
        new_holding = hd.Holding(ticker, exchange, date_bought, date_first_bought, price, stop_loss, repeat, multiplier)
        self._holdings_dict[ticker] = new_holding

    def _add_holding(self, holding: hd.Holding):
        assert holding.ticker_symbol not in self._holdings_dict.keys()
        assert self.get_current_holdings_number() < self.get_max_holdings()

        self._holdings_dict[holding.ticker_symbol] = holding

    def remove_holding(self, old_holding_ticker: str):
        try:
            if old_holding_ticker not in self._holdings_dict:
                return False
            else:
                # Throws KeyError if not there
                del self._holdings_dict[old_holding_ticker]
                return True
        except:
            return False # new_holding wasn't a Holding Object

    def updateWithSQL(self, rawResults):
        # rawResults = [(Date, Ticker, Price, etc...),...]
        # Store old holdings and reset
        old_dict = self._holdings_dict
        old_cash_holdings = self._cash_holdings
        self._holdings_dict = {}
        self._cash_holdings = {}

        # Add holdings
        for result in rawResults:
            (date_bought, ticker, price) = result
            if ticker not in old_cash_holdings.keys(): # I think I need to remove this function. Strategy should instead return either the raw SQL object or the list of parsed informatoin and hand it back to Backtester. Backtester should then probably have another function like updateResults. Honestly, the Results class is probably a poorly designed class. Maybe Backtester should take over most of its responsiblities.
                if ticker in old_dict.keys():
                    self.add_holding(ticker, date_bought, old_dict[ticker].date_first_bought, price, repeat=True)
                else:
                    self.add_holding(ticker, date_bought, date_bought, price, repeat=False)

        # Add cash holdings from before
        for holding in self._cash_holdings.values():
            holding.repeat = True
            self._add_holding(holding)
        

    def replace_holding(self, new_holding: hd.Holding, old_holding_ticker: str):
        # TODO
        pass

    def ticker_in_holdings(self, holding_ticker: str):
        return holding_ticker in self._holdings_dict

    def get_holdings_tickers(self):
        return set(self._holdings_dict.keys())

    def get_holdings(self):
        return self._holdings_dict.values()

    def get_holding(self, holding_ticker):
        if holding_ticker in self._holdings_dict:
            return self._holdings_dict[holding_ticker]
        else:
            return None

    def convert_holding_to_cash(self, holding_ticker, date_bought):
        holding = self.get_holding(holding_ticker)

        if holding:
            assert not holding.cash
            holding.cash = True
            holding.date_bought = date_bought
            assert holding_ticker not in self._cash_holdings.keys()
            self._cash_holdings[holding_ticker] = holding
            return True

        return False