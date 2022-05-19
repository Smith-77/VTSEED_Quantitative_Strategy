import src.Holding as hd


class Holdings:

    def __init__(self, max_holdings: int):
        self._max_holdings = max_holdings
        self._holdings_dict: dict[str, hd.Holding] = {}

    def get_max_holdings(self):
        return self._max_holdings

    def get_current_holdings_number(self):
        return len(self._holdings_dict)

    def add_holding(self, new_holding: hd.Holding):
        try:
            if self.get_current_holdings_number() >= self._max_holdings or new_holding.ticker_symbol in self._holdings_dict:
                return False
            else:
                self._holdings_dict.update({new_holding.ticker_symbol: new_holding})
                return True
        except:
            return False # new_holding wasn't a Holding Object

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

    def replace_holding(self, new_holding: hd.Holding, old_holding_ticker: str):
        # TODO
        pass

    def ticker_in_holdings(self, holding_ticker: str):
        return holding_ticker in self._holdings_dict

    def get_holdings_tickers(self):
        return set(self._holdings_dict.keys())
