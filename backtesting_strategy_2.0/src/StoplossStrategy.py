import src.StoplossType as slt

class StoplossStrategy:

    def  __init__(self, type:slt.StoplossType, maxDrop=0.1, trailing_days=None):
        # Determine stoploss type
        self._type = type
            
        # Check for errors
        if (type == slt.StoplossType.NONE or type == slt.StoplossType.ABSOLUTE) and trailing_days != None:
            raise Exception("Error creating stoploss strategy. Ensure trailng_days is set to None if strategy type is NONE or ABSOLUTE")
        elif type == slt.StoplossType.TRAILING:
            if trailing_days == None or not isinstance(trailing_days, int) or trailing_days < 1:
                raise Exception("Error creating stoploss strategy. Ensure trailng_days is set to a positive integer if strategy type TRAILING")
        self._stoploss_type = type

        # TODO: check an appropriate maximumd rop has been entered
        self._max_drop = maxDrop
        self._trailing_days = trailing_days

    def get_stoploss_type(self):
        return self._stoploss_type

    def get_max_drop(self):
        return self._max_drop

    def get_trailing_days(self):
        return self._trailing_days

    



