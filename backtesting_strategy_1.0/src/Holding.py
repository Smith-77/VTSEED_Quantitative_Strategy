class Holding:

    def __init__(self, ticker_symbol: str, exchange_symbol: str, date_bought, date_first_bought, price: float, stop_loss, repeat=False, multiplier = 1):
        self.ticker_symbol = ticker_symbol
        self.exchange_symbol = exchange_symbol
        self.date_bought = date_bought
        self.date_first_bought = date_first_bought
        self.price = price # TODO: Replace this and other financial metrics by functions which look it up in SQL table
        self.stop_loss = stop_loss
        self.repeat = repeat
        self.multiplier = multiplier

    def get_price(dbConn):
        # TODO
        pass

    def get_opening_price():
        # TODO
        pass

    def get_etc():
        # TODO
        pass
