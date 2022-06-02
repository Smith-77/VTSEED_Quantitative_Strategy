import src.StoplossType as slt

class StoplossStrategy:

    def  __init__(self, ):
        self._stoploss_type = slt.StoplossType.NONE
        self._trailing_days = None

    def set_stoploss_type(self, stoploss_type: slt.StoplossType, trailing_days: int = None):
        if (stoploss_type == slt.StoplossType.NONE or stoploss_type == slt.StoplossType.ABSOLUTE) and trailing_days != None:
            return False
        elif stoploss_type == slt.StoplossType.TRAILING:
            if trailing_days == None or not isinstance(trailing_days, int) or trailing_days < 1:
                return False
        self._stoploss_type = stoploss_type
        self._trailing_days = trailing_days
        return True

    def get_trailing_days(self):
        return self._trailing_days

    def get_stoploss_type(self):
        return self._stoploss_type

    



