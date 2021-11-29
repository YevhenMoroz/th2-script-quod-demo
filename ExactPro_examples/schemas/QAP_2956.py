import logging
from copy import deepcopy
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules import infra_pb2
from grpc_modules.act_fix_pb2_grpc import ActFixStub
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.verifier_pb2_grpc import VerifierStub
from grpc_modules.quod_simulator_pb2_grpc import TemplateSimulatorServiceStub
from grpc_modules.simulator_pb2_grpc import ServiceSimulatorStub
from grpc_modules.infra_pb2 import Direction, ConnectionID
from grpc_modules.quod_simulator_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = ActFixStub(case_params['act'])
    event_store = EventStoreServiceStub(case_params['event-store'])
    verifier = VerifierStub(case_params['verifier'])
    rules_killer = ServiceSimulatorStub(case_params['simulator'])

    seconds, nanos = bca.timestamps()  # Store case start time
    event_request_1 = bca.create_store_event_request(case_name, case_params['case_id'], report_id)
    event_store.StoreEvent(event_request_1)

    # Create sub-report for case

    subscribe_params = {
        # 'Account': 'MMCLIENT1',
        'SenderSubID': 'MMCLIENT1',
        'MDReqID': '1111222001',
        'SubscriptionRequestType': '1',
        'MarketDepth': '0',
        'MDUpdateType': '0',
        'NoMDEntryTypes': [{'MDEntryType': '0'}, {'MDEntryType': '1'}],
        'NoRelatedSymbols': [{
            'Instrument': {
                'Symbol': 'EUR/USD',
                'Product': '4',
                # 'SettlDate': '20201223',
                # 'SecurityType': 'FXFWD'
                'SettlDate': '20201216',
                'SecurityType': 'FXSPOT'
            }}]
    }

    subscribe = act.placeMarketDataRequestFIX(
        bca.convert_to_request(
            'MarketDataRequest (subscribe)',
            case_params['Connectivity'],
            case_params['case_id'],
            bca.message_to_grpc('MarketDataRequest', subscribe_params)
        ))
