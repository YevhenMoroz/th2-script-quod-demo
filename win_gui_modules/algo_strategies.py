from th2_grpc_act_gui_quod.order_ticket_pb2 import TWAPStrategyParams
from th2_grpc_act_gui_quod.order_ticket_pb2 import MultilistingStrategy
from th2_grpc_act_gui_quod.order_ticket_pb2 import QuodParticipationStrategyParams


class TWAPStrategy:

    def __init__(self, strategy: TWAPStrategyParams()):
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


class MultilistingStrategy:

    def __init__(self, strategy: MultilistingStrategy()):
        self.strategy = strategy

    def set_allow_missing_trim(self, allow_missing_trim: bool):
        self.strategy.allowMissingPrim = allow_missing_trim

    def set_available_venues(self, available_venues: bool):
        self.strategy.availableVenues = available_venues

    def set_post_mode(self, post_mode: str):
        self.strategy.postMode = post_mode

    def set_spreying_weights(self, spreying_weights: str):
        self.strategy.spreyingWeights = spreying_weights


class QuodParticipationStrategy:

    def __init__(self, strategy: QuodParticipationStrategyParams()):
        self.strategy = strategy

    def set_start_date(self, from_date: str, offset: str = ""):
        setattr(self.strategy.startDate, "from", from_date)
        self.strategy.startDate.offset = offset

    def set_end_date(self, from_date: str, offset: str = ""):
        setattr(self.strategy.endDate, "from", from_date)
        self.strategy.endDate.offset = offset

    def set_percentage_volume(self, percentage_volume: str):
        self.strategy.percentageVolume = percentage_volume

    def set_aggressivity(self, aggressivity: str):
        self.strategy.aggressivity = aggressivity
