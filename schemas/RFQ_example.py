import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = Stubs.fix_act
    event_store = Stubs.event_store
    verifier = Stubs.verifier

    seconds, nanos = bca.timestamps()  # Store case start time
    case_id = bca.create_event(case_name, report_id)

# Prepare user input
    reusable_order_params = {   # This parameters can be used for ExecutionReport message
        'Account': case_params['Account'],

    }
    instrument_fx = {
        'Symbol': 'EUR/TWD',
        'InstrSymbol': 'EUR/TWD',
        'SecurityType': 'FXFWD',
        # 'SecurityID': 'SE0000818569',
        # 'SecurityIDSource': '4',
        # 'SecurityExchange': 'HSBC'
    }

    specific_order_params = {   # There are reusable and specific for submition parameters
        **reusable_order_params,
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
                                            'Side': '1',
                                            'Currency': 'EUR',
                                            'QuoteType': '1',
                                            'OrderQty': '10000000',
                                            'SettlDate': '20201009',
                                            'OrdType': 'D',
                                            'ExpireTime': '20201010-16:04:48.498',
                                            'TransactTime': (datetime.utcnow().isoformat()),
                                            'Account': 'MMCLIENT1',
                                            'SettlType': 'W1',
                                            'Instrument': instrument_fx}]
    }
    logger.debug("Send new order with ClOrdID = {}".format(specific_order_params['QuoteReqID']))

    enter_order = act.placeQuoteFIX(
        bca.convert_to_request(
            'Send QuoteRequest',
            case_params['TraderConnectivity'],
            case_id,
            # DRAFT.dirty_message
            bca.message_to_grpc('QuoteRequest', specific_order_params, case_params['TraderConnectivity'])
            # ut.build_value(message_type='QuoteRequest', content=specific_order_params)
        ))

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
