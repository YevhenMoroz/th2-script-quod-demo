class PositionCalculationManager:
    @staticmethod
    def calculate_position_buy(position_before: str, order_qty: str) -> str:
        expected_pos = int(position_before.replace(",", "")) + int(order_qty)
        return str(expected_pos)

    @staticmethod
    def calculate_position_sell(position_before: str, order_qty: str) -> str:
        expected_pos = int(position_before.replace(",", "")) - int(order_qty)
        return str(expected_pos)
