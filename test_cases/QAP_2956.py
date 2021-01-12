import logging
from copy import deepcopy
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):

    act = Stubs.fix_act
    verifier = Stubs.verifier

    seconds, nanos = bca.timestamps()  # Store case start time
    case_name = "QAP-2956"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

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
            case_id,
            bca.message_to_grpc('MarketDataRequest', subscribe_params, case_params['Connectivity'])
        ))
