import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules import infra_pb2
from grpc_modules import verifier_pb2


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = case_params['act_box']
    event_store = case_params['event_store_box']
    verifier = case_params['verifier_box']

    seconds, nanos = bca.timestamps()  # Store case start time

# Prepare user input
    reusable_order_params = {   # This parameters can be used for ExecutionReport message
        'Account': case_params['Account'],

    }
    instrument_fx = {
        'Symbol': 'EUR/USD'
        # 'SecurityID': 'SE0000818569',
        # 'SecurityIDSource': '4',
        # 'SecurityExchange': 'XSTO'
    }


    specific_order_params = {   # There are reusable and specific for submition parameters
        **reusable_order_params,
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{'Side': '1', 'Currency': 'EUR', 'QuoteType': '1',
                                            'OrderQty': '6000000', 'SettlDate': '20200817', 'OrdType': 'D',
                                            'ExpireTime': '20200813-10:04:48.498',
                                            'TransactTime': (datetime.utcnow().isoformat()),
                                            'Instrument': instrument_fx}]
    }
    logger.debug("Send new order with ClOrdID = {}".format(specific_order_params['QuoteReqID']))
    # ut = Utils()
    # my_message = ut.build_value(message_type='QuoteRequest', content=specific_order_params)
    # print(bca.message_to_grpc('QuoteRequest', specific_order_params))
    enter_order = act.placeQuoteFIX(
        bca.convert_to_request(
            'Send QuoteRequest',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            # DRAFT.dirty_message
            bca.message_to_grpc('QuoteRequest', specific_order_params)
            # ut.build_value(message_type='QuoteRequest', content=specific_order_params)
        ))

    bca.create_event(event_store, case_name, case_params['case_id'], report_id)  # Create sub-report for case
    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))