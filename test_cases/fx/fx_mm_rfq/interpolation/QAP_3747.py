import logging
import time
from pathlib import Path
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs

client = 'Argentina1'
account = 'Argentina1_1'
client_tier = 'Argentina'
symbol = "EUR/USD"
security_type_swap = "FXSWAP"
security_type_fwd = "FXFWD"
security_type_spo = "FXSPO"
settle_date_spo = spo()
settle_date_w1 = wk1()
settle_date_w2 = wk2()
settle_type_spo = "0"
settle_type_w1 = "W1"
settle_type_w2 = "W2"
currency = "EUR"
settle_currency = "USD"
qty = '1000000'
side = "1"
leg1_side = "2"
leg2_side = "1"
venue_msr = 'MSR'
mic_msr = 'MS-RFQ'
venue_ms = 'MS'
mic_ms = 'MS-SW'
api = Stubs.api_service


def change_venue_status_ms(case_id, health, metric):
    modify_venue_params = {
        "venueID": "MS",
        "alive": 'true',
        "venueStatusMetric": [
            {
                "venueMetricType": "LUP",
                "enableMetric": health,
                "metricErrorThreshold": metric,
                "metricWarningThreshold": metric
            }
        ]
    }
    api.sendMessage(
        request=SubmitMessageRequest(
            message=bca.message_to_grpc('ModifyVenueStatus', modify_venue_params, 'rest_wa314luna'),
            parent_event_id=case_id))


def change_venue_status_msr(case_id, health, metric):
    modify_venue_params = {
        "venueID": "MSR",
        "alive": 'true',
        "venueStatusMetric": [
            {
                "venueMetricType": "LUP",
                "enableMetric": health,
                "metricErrorThreshold": metric,
                "metricWarningThreshold": metric
            }
        ]
    }
    api.sendMessage(
        request=SubmitMessageRequest(
            message=bca.wrap_message(modify_venue_params, 'ModifyVenueStatus', 'rest_wa314luna'),
            parent_event_id=case_id))


def send_swap_and_filled(case_id):
    # Precondition
    change_venue_status_ms(case_id, 'true', '-1')
    change_venue_status_msr(case_id, 'true', '-1')
    time.sleep(3)
    params_swap = CaseParamsSellRfq(client, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                    orderqty=qty, leg1_ordqty=qty, leg2_ordqty=qty,
                                    currency=currency, settlcurrency=settle_currency,
                                    leg1_settltype=settle_type_w1, leg2_settltype=settle_type_w2,
                                    settldate=settle_date_spo, leg1_settldate=settle_date_w1,
                                    leg2_settldate=settle_date_w2,
                                    symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                    securitytype=security_type_swap, leg1_securitytype=security_type_fwd,
                                    leg2_securitytype=security_type_fwd,
                                    securityid=symbol, account=account)
    # Step 1
    rfq = FixClientSellRfq(params_swap)
    rfq.send_request_for_quote_swap()
    # Step 2
    rfq.verify_quote_reject(text="no bid forward points for client tier `2600011' on EUR/USD WK2 on QUODFX")

    change_venue_status_ms(case_id, 'false', '0')
    change_venue_status_msr(case_id, 'false', '0')


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        send_swap_and_filled(case_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
