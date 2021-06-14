import logging
from datetime import datetime

from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from custom.tenor_settlement_date import get_expire_time
from quod_qa.fx.default_params_fx import text_messages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def send_swap_rfq(reusable_params, case_params, case_id, fix_act, ttl, qty1, qty2):
    # rfq_params = {
    #     'NoRelatedSymbols': [{
    #         **reusable_params,
    #         # 'QuoteType': '1',
    #         'OrderQty': reusable_params['OrderQty'],
    #         'OrdType': 'D',
    #         'ExpireTime': get_expire_time(ttl),
    #         'TransactTime': (datetime.utcnow().isoformat())}]
    #     }

    rfq_params = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [
            {
                'Instrument': reusable_params['Instrument'],
                'OrderQty': reusable_params['OrderQty'],
                'Currency': reusable_params['Instrument']['Symbol'][:3],
                'Account': reusable_params['Account'],
                'ExpireTime': get_expire_time(ttl),
                'NoLegs': [
                    {
                        'InstrumentLeg': {
                            'LegSymbol': reusable_params['Instrument']['Symbol'],
                            'LegSecurityType': 'FXSPOT'
                        },
                        'LegSide': 1,
                        'LegSettlType': 0,
                        'LegSettlDate': tsd.spo(),
                        'LegOrderQty': qty1
                    },
                    {
                        'InstrumentLeg': {
                            'LegSymbol': reusable_params['Instrument']['Symbol'],
                            'LegSecurityType': 'FXFWD'
                        },
                        'LegSide': 2,
                        'LegSettlType': '1W',
                        'LegSettlDate': tsd.wk1(),
                        'LegOrderQty': qty2
                    },
                ]
            }
        ]
    }
    logger.debug("Send new order with ClOrdID = {}".format(rfq_params['QuoteReqID']))

    rfq_id = fix_act.sendMessage(
            bca.convert_to_request(
                    text_messages['sendQR'],
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
                    ))

    return rfq_id
