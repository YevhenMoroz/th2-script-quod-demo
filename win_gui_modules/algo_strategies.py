from th2_grpc_act_gui_quod import order_ticket_pb2, order_ticket_fx_pb2


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

    def set_slice_duration_min(self, slice_duration_min: str):
        self.strategy.sliceDurationMin = slice_duration_min

    def set_child_display_qty(self, child_display_qty):
        self.strategy.childDisplayQty = child_display_qty

    def set_child_min_qty(self, child_min_qty):
        self.strategy.childMinQty = child_min_qty


class ExternalTWAPStrategy:
    def __init__(self, strategy: order_ticket_pb2.ExternalTWAPStrategyParams()):
        self.strategy = strategy

    def set_urgency(self, urgency: str):
        self.strategy.urgency = urgency

    def set_start_time(self, start_time: str):
        self.strategy.startTime = start_time

    def set_end_time(self, end_time: str):
        self.strategy.endTime = end_time


class SyntheticIcebergStrategy:
    def __init__(self, strategy: order_ticket_pb2.SyntheticIcebergParams()):
        self.strategy = strategy

    def set_low_liquidity(self, low_liquidity: bool = False):
        self.strategy.lowLiquidity = low_liquidity


class SyntheticBlockStrategy:
    def __init__(self, strategy: order_ticket_pb2.SyntheticBlockParams()):
        self.strategy = strategy

    def set_order_mode(self, order_mode: str):
        self.strategy.orderMode = order_mode


class MultilistingStrategy:

    def __init__(self, strategy: order_ticket_pb2.MultilistingStrategy()):
        self.strategy = strategy

    def set_allow_missing_trim(self, allow_missing_prim: bool):
        self.strategy.allowMissingPrim = allow_missing_prim

    def set_available_venues(self, available_venues: bool):
        self.strategy.availableVenues = available_venues

    def set_post_mode(self, post_mode: str):
        self.strategy.postMode = post_mode

    def set_spreying_weights(self, spreying_weights: str):
        self.strategy.spreyingWeights = spreying_weights


class QuodParticipationStrategy:

    def __init__(self, strategy: order_ticket_pb2.QuodParticipationStrategyParams()):
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


# FX
class FXMultilistingStrategy:

    def __init__(self, strategy: order_ticket_pb2.MultilistingStrategy()):
        self.strategy = strategy

    def set_allow_missing_trim(self, allow_missing_trim: bool):
        self.strategy.allowMissingPrim = allow_missing_trim

    def set_available_venues(self, available_venues: bool):
        self.strategy.availableVenues = available_venues

    def set_fok_exploration(self, fok_exploration: bool):
        self.strategy.fokExploration = fok_exploration

    def set_sweeping_allowed(self, sweeping_allowed: bool):
        self.strategy.sweepingAllowed = sweeping_allowed

    def set_post_mode(self, post_mode: str):
        self.strategy.postMode = post_mode

    def set_spreying_weights(self, spreying_weights: str):
        self.strategy.spreyingWeights = spreying_weights

    def set_allowed_venues(self, allowed_venues: str):
        self.strategy.allowedVenues = allowed_venues

    def set_forbidden_venues(self, forbidden_venues: str):
        self.strategy.forbiddenVenues = forbidden_venues


class FXTWAPStrategy:

    def __init__(self, strategy: order_ticket_fx_pb2.FXTWAPStrategyParams()):
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

    def set_allowed_venues(self, allowed_venues: str):
        self.strategy.allowedVenues = allowed_venues

    def set_forbidden_venues(self, forbidden_venues: str):
        self.strategy.forbiddenVenues = forbidden_venues

    def set_slice_duration(self, slice_duration: str):
        self.strategy.sliceDuration = slice_duration

    def set_reserve_quantity(self, reserve_quantity: str):
        self.strategy.reserveQuantity = reserve_quantity


class QuodSyntheticStrategy:
    def __init__(self, strategy: order_ticket_fx_pb2.FXSyntheticOrdTypeStrategy()):
        self.strategy = strategy

    def set_trigger_type(self, trig_type: str):
        self.strategy.triggerType = trig_type
