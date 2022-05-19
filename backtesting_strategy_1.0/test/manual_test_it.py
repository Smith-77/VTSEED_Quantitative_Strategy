from src import Holdings as hds
from src import Holding as hd

new_holding = hd.Holding('abc', 1, 2, 3, 4, 5)
holdings = hds.Holdings(3)
holdings.add_holding(new_holding)
