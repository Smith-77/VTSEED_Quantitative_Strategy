import src.Holding as hd


class Holdings:

    def __init__(self, max_holdings: int):
        self._max_holdings = max_holdings
        self._holdings_dict: dict[str, hd.Holding] = {}

    def get_max_holdings(self):
        return self._max_holdings

    def get_current_holdings_number(self):
        return len(self._holdings_dict)

    def add_holding(self, ticker: str, date_bought, date_first_bought, price, repeat=False, exchange='NYSE', stop_loss=.1, multiplier=1): # TODO: What is stop_loss?
        # Replace date_first_bought if it's already present in holdings
        
        assert ticker not in self._holdings_dict.keys()

        # Create new holding
        new_holding = hd.Holding(ticker, exchange, date_bought, date_first_bought, price, stop_loss, repeat, multiplier)
        self._holdings_dict[ticker] = new_holding

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
        old_dict = self._holdings_dict
        self._holdings_dict = {}
        for result in rawResults:
            (date_bought, ticker, price) = result
            repeat = False
            if ticker in old_dict.keys():
                repeat = True 
            if repeat:
                self.add_holding(ticker, date_bought, old_dict[ticker].date_first_bought, price, repeat)
            else:
                self.add_holding(ticker, date_bought, date_bought, price, repeat)
        

    def replace_holding(self, new_holding: hd.Holding, old_holding_ticker: str):
        # TODO
        pass

    def ticker_in_holdings(self, holding_ticker: str):
        return holding_ticker in self._holdings_dict

    def get_holdings_tickers(self):
        return set(self._holdings_dict.keys())

    def get_holdings(self):
        return self._holdings_dict.values()
