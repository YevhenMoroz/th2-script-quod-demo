import logging
from datetime import datetime
from rule_management import RuleManager
from stubs import Stubs
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

# from win_gui_modules.aggregated_rates_wrappers import PlaceRFQRequest, RFQTileOrderSide, ModifyRFQTileRequest
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.client_pricing_wrappers import BaseTileDetails
from win_gui_modules.quote_wrappers import QuoteDetailsRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    act = Stubs.fix_act
    ar_service = Stubs.win_act_aggregated_rates_service
    common_act = Stubs.win_act
    event_store = Stubs.event_store
    verifier = Stubs.verifier
    simulator = Stubs.simulator

    seconds, nanos = bca.timestamps()  # Store case start time
    case_name = "QAP-2129"
    case_id = bca.create_event(case_name, report_id)

    case_params = {
        'TraderConnectivity': 'gtwquod5-fx',
        'Account': 'MMCLIENT1',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD5',
    }
    # session_id = set_session_id()
    # set_base(session_id, case_id)
    # base_request = get_base_request(session_id, case_id)
    # base_details = BaseTileDetails(base=base_request)
    #
    # work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
    # password = Stubs.custom_config['qf_trading_fe_password_303']
    # user = Stubs.custom_config['qf_trading_fe_user_303']
    # prepare_fe(case_id, session_id, work_dir, user, password)
    #
    # execution_id = bca.client_orderid(4)
    # qrb = QuoteDetailsRequest(base=base_request)
    # qrb.set_extraction_id(execution_id)
    # qrb.request()

    reusable_params = {
        'Account': case_params['Account'],
        'Side': 1,
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXSPOT'
            },
        'SettlDate': tsd.spo(),
        'SettlType': '0'
        }

    # RFQ parameters for receive Status New
    rfq_params_new = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
            **reusable_params,
            'Currency': 'EUR',
            'QuoteType': '1',
            'OrderQty': 16000001,
            'OrdType': 'D',
            'ExpireTime': reusable_params['SettlDate'] + '-23:59:00.000',
            'TransactTime': (datetime.utcnow().isoformat())}]
        }

    # RFQ parameters for receive Status Expired
    rfq_params_expired = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
            **reusable_params,
            'Currency': 'EUR',
            'QuoteType': '1',
            'OrderQty': 1000000,
            'OrdType': 'D',
            'ExpireTime': reusable_params['SettlDate'] + '-23:59:00.000',
            'TransactTime': (datetime.utcnow().isoformat())}]
        }

    # RFQ parameters for receive Status Terminated
    rfq_params_terminated = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
            **reusable_params,
            'Currency': 'EUR',
            'QuoteType': '1',
            'OrderQty': 1000000,
            'OrdType': 'D',
            'ExpireTime': reusable_params['SettlDate'] + '-23:59:00.000',
            'TransactTime': (datetime.utcnow().isoformat())}]
        }

    # RFQ parameters for receive Status Rejected
    rfq_params_rejected = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
            **reusable_params,
            'Currency': 'EUR',
            'QuoteType': '1',
            'OrderQty': 0,
            'OrdType': 'D',
            'ExpireTime': reusable_params['SettlDate'] + '-23:59:00.000',
            'TransactTime': (datetime.utcnow().isoformat())}]
        }

    # RFQ parameters for receive Status Canceled
    rfq_params_canceled = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
            **reusable_params,
            'Currency': 'EUR',
            'QuoteType': '1',
            'OrderQty': 1000000,
            'OrdType': 'D',
            'ExpireTime': reusable_params['SettlDate'] + '-23:59:00.000',
            'TransactTime': (datetime.utcnow().isoformat())}]
        }

    # act.sendMessage(
    #         bca.convert_to_request(
    #                 'Send RFQ_New',
    #                 case_params['TraderConnectivity'],
    #                 case_id,
    #                 bca.message_to_grpc('QuoteRequest', rfq_params_new, case_params['TraderConnectivity'])
    #                 ))
    #
    # act.placeQuoteFIX(
    #         bca.convert_to_request(
    #                 'Send RFQ_Expired',
    #                 case_params['TraderConnectivity'],
    #                 case_id,
    #                 bca.message_to_grpc('QuoteRequest', rfq_params_expired, case_params['TraderConnectivity'])
    #                 ))
    #
    # act.placeQuoteFIX(
    #         bca.convert_to_request(
    #                 'Send RFQ_Rejected',
    #                 case_params['TraderConnectivity'],
    #                 case_id,
    #                 bca.message_to_grpc('QuoteRequest', rfq_params_rejected, case_params['TraderConnectivity'])
    #                 ))
    #
    # quote_canceled = act.placeQuoteFIX(
    #     bca.convert_to_request(
    #         'Send RFQ_Canceled',
    #         case_params['TraderConnectivity'],
    #         case_id,
    #         bca.message_to_grpc('QuoteRequest', rfq_params_canceled, case_params['TraderConnectivity'])
    #         ))
    #
    # # logger.info(quote_canceled.response_messages_list[0].fields['QuoteReqID'].simple_value)
    #
    # cancel_quote_params = {
    #     'QuoteReqID': quote_canceled.response_messages_list[0].fields['QuoteReqID'].simple_value,
    #     'QuoteCancelType': 5,
    #     'QuoteID': quote_canceled.response_messages_list[0].fields['QuoteID'].simple_value
    # }
    #
    # act.sendMessage(
    #     bca.convert_to_request(
    #         'Send QuoteCancel',
    #         case_params['TraderConnectivity'],
    #         case_id,
    #         bca.message_to_grpc('QuoteCancel', cancel_quote_params, case_params['TraderConnectivity'])
    #         ))

    # Send RFQ_Terminated
    rfq_term = act.placeQuoteFIX(
            bca.convert_to_request(
                    'Send RFQ_Terminated',
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params_terminated, case_params['TraderConnectivity'])
                    ))

    # quote_params = {
    #     **reusable_params,
    #     'QuoteReqID': rfq_term.response_messages_list[0].fields['QuoteID'],
    #     'Product': 4,
    #     'OfferPx': '35.0012',
    #     'OfferSize': rfq_params_terminated['NoRelatedSymbols'][0]['OrderQty'],
    #     'QuoteID': '*',
    #     'OfferSpotRate': '35.001',
    #     'ValidUntilTime': '*',
    #     'Currency': 'EUR',
    #     'QuoteType': 1,
    #     'OfferForwardPoints': 0.0002
    #     }
    #
    # verifier.submitCheckRule(
    #         bca.create_check_rule(
    #                 'Quote Received',
    #                 bca.filter_to_grpc('Quote', quote_params, rfq_params_terminated['QuoteReqID']),
    #                 rfq_term.checkpoint_id,
    #                 case_params['TraderConnectivity'],
    #                 case_id
    #                 )
    #         )
    # NewOrderSingle params for Quote Filled
    order_params = {
        **reusable_params,
        'QuoteID': rfq_term.response_messages_list[0].fields['QuoteID'],
        'ClOrdID': bca.client_orderid(9),
        'OrdType': 'D',
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': rfq_params_terminated['NoRelatedSymbols'][0]['OrderQty'],
        'Price': rfq_term.response_messages_list[0].fields['OfferPx'].simple_value,
        # 'Product': 4,
        'TimeInForce': 4
        }

    # Send NewOrderSingle for Quote Filled
    send_order = act.placeOrderFIX(
            bca.convert_to_request(
                    "Send NewOrderSingle",
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('NewOrderSingle', order_params, case_params['TraderConnectivity'])
                    ))

    er_pending_params = {
        'Side': reusable_params['Side'],
        'Account': reusable_params['Account'],
        'ClOrdID': order_params['ClOrdID'],
        'OrderQty': order_params['OrderQty'],
        'LeavesQty': order_params['OrderQty'],
        'TimeInForce': order_params['TimeInForce'],
        'OrdType': order_params['OrdType'],
        'Price': rfq_term.response_messages_list[0].fields['OfferPx'].simple_value,
        'OrderID': send_order.response_messages_list[0].fields['OrderID'].simple_value,
        'NoParty': [
            {'PartyRole': 36, 'PartyID': 'gtwquod5', 'PartyIDSource': 'D'}
            ],
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityIDSource': 8,
            'SecurityID': 'EUR/USD',
            'SecurityExchange': 'XQFX'
            },
        'SettlCurrency': 'USD',
        'Currency': 'EUR',
        'HandlInst': 1,
        'AvgPx': 0,
        'QtyType': 0,
        'LastQty': 0,
        'CumQty': 0,
        'LastPx': 0,
        'OrdStatus': 'A',
        'ExecType': 'A',
        'ExecID': '*',
        'TransactTime': '*',
        'Product': 4,
        'OrderCapacity': 'A'
        }

    verifier.submitCheckRule(
            bca.create_check_rule(
                    'Execution Report for NewOrderSingle',
                    bca.filter_to_grpc('ExecutionReport', er_pending_params, ['ClOrdID', 'OrdStatus', 'ExecType']),
                    send_order.checkpoint_id,
                    case_params['TraderConnectivity'],
                    case_id
                    )
            )

    er_filled_params = {
        'Side': reusable_params['Side'],
        'Account': reusable_params['Account'],
        'SettlDate': reusable_params['SettlDate'],
        'TradeDate': datetime.utcnow().strftime('%Y%m%d'),
        'SettlType': reusable_params['SettlType'],
        'ClOrdID': order_params['ClOrdID'],
        'OrderQty': order_params['OrderQty'],
        'LeavesQty': 0,
        'TimeInForce': order_params['TimeInForce'],
        'OrdType': order_params['OrdType'],
        'Price': rfq_term.response_messages_list[0].fields['OfferPx'].simple_value,
        'OrderID': send_order.response_messages_list[0].fields['OrderID'].simple_value,
        'NoParty': [
            {'PartyRole': 36, 'PartyID': 'gtwquod5', 'PartyIDSource': 'D'}
            ],
        'Instrument': {
            'SecurityType': 'FXSPOT',
            'Symbol': 'EUR/USD',
            'SecurityIDSource': 8,
            'SecurityID': 'EUR/USD',
            'SecurityExchange': 'XQFX'
            },
        'SettlCurrency': 'USD',
        'Currency': 'EUR',
        'HandlInst': 1,
        'AvgPx': rfq_term.response_messages_list[0].fields['OfferPx'].simple_value,
        'QtyType': 0,
        'LastQty': order_params['OrderQty'],
        'CumQty': order_params['OrderQty'],
        'LastPx': rfq_term.response_messages_list[0].fields['OfferPx'].simple_value,
        'OrdStatus': 2,
        'ExecType': 'F',
        'ExecID': '*',
        'TransactTime': '*',
        'Product': 4,
        'LastSpotRate': 35.001,
        'OrderCapacity': 'A',

        }

    verifier.submitCheckRule(
            bca.create_check_rule(
                    'Receive ExecutionReport Filled',
                    bca.filter_to_grpc('ExecutionReport', er_filled_params, ['ClOrdID', 'OrdStatus', 'ExecType']),
                    send_order.checkpoint_id,
                    case_params['TraderConnectivity'],
                    case_id
                    )
            )
    # execution_id = bca.client_orderid(4)
    # qrb = QuoteDetailsRequest(base=base_request)
    # qrb.set_extraction_id(execution_id)
    # qrb_quote_req_id = ExtractionDetail('quoteRequestBook.id', 'Id')
    # qrb_user = ExtractionDetail('quoteRequestBook.id', 'User')
    # qrb_status = ExtractionDetail('quoteRequestBook.status', 'Status')
    # qrb_quote_status = ExtractionDetail('quoteRequestBook.quotestatus', 'QuoteStatus')
    # qrb.add_extraction_details([qrb_quote_req_id, qrb_user, qrb_status, qrb_quote_status])
    #
    #
    # call(ar_service.getQuoteRequestBookDetails, qrb.request())
    # call(common_act.verifyEntities, verification(execution_id, 'checking QRB', [
    #     verify_ent('QRB Id', qrb_quote_req_id.name, rfq_params['QuoteReqID']),
    #     verify_ent('QRB User', qrb_user.name, case_params['TraderConnectivity']),
    #     verify_ent('QRB Status', qrb_status.name, "New"),
    #     # verify_ent('QRB QuoteStatus', qrb_quote_status.name, "")
    # ]))

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
