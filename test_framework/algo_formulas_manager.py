class AlgoFormulasManager:
    @staticmethod
    def calc_ticks_offset_minus(price: float, offset_qty: int, tick: float):
        return price - tick * offset_qty

    @staticmethod
    def calc_ticks_offset_plus(price: float, offset: int, tick: float):
        return price + tick * offset

    @staticmethod
    def calc_bps_offset_minus(price: float, offset_qty: int):
        return price - price / 10000 * offset_qty

    @staticmethod
    def calc_bps_offset_plus(price: float, offset_qty: int):
        return price + price / 10000 * offset_qty
