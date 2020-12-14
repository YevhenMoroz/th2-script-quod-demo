from configuration import *
from grpc import insecure_channel


class Channels:
    ui_act_channel = insecure_channel(win_act_address)
    event_store_channel = insecure_channel(event_store_address)
    verifier_channel = insecure_channel(verifier_address)
    simulator_channel = insecure_channel(simulator_address)
    fix_act_channel = insecure_channel(fix_act_address)
