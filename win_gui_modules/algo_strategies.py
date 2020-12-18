from grpc_modules import order_ticket_pb2


class TWAPStrategy:

    def __init__(self, strategy: order_ticket_pb2.TWAPStrategyParams()):
        self.strategy = strategy

    def set_start_date(self, from_date: str, offset: str = ""):
        setattr(self.strategy.startDate, "from", from_date)
        self.strategy.startDate.offset = offset

    def set_end_date(self, from_date: str, offset: str = ""):
        setattr(self.strategy.endDate, "from", from_date)
        self.strategy.endDate.offset = offset

    def set_waves(self, waves: str):
        self.strategy.waves = waves

    def set_aggressivity(self, aggressivity: str):
        self.strategy.aggressivity = aggressivity

    def set_max_participation(self, max_participation: str):
        self.strategy.maxParticipation = max_participation
