import logging
from pathlib import Path

from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs

client = 'Argentina1'
account = 'Argentina1_1'
client_tier = 'Argentina'
symbol = "GBP/USD"
security_type_swap = "FXSWAP"
security_type_fwd = "FXFWD"
security_type_spo = "FXSPO"
settle_date_spo = spo()
settle_date_w1 = wk1()
settle_date_w2 = wk2()
settle_type_spo = "0"
settle_type_w1 = "W1"
settle_type_w2 = "W2"
currency = "USD"
settle_currency = "GBP"
qty = '1000000'
side = "1"
leg1_side = "2"
leg2_side = "1"
venue_msr = 'MSR'
mic_msr = 'MS-RFQ'
venue_ms = 'MS'
mic_ms = 'MS-SW'
api = Stubs.api_service




def change_venue_status_msr(case_id, health, metric):
    modify_params_MSR = {
        "tradingStatus": "T",
        "GTDHolidayCheck": "false",
        "algoIncluded": "false",
        "supportBrokerQueue": "false",
        "supportStatus": "false",
        "supportQuoteBook": "false",
        "autoRFQTimeout": 5000,
        "multilegReportType": "M",
        "clQuoteReqIDFormat": "#20d",
        "MIC": "MS-RFQ",
        "supportOrderBook": "false",
        "supportReverseCalSpread": "false",
        "timeZone": "GMT Standard Time",
        "venueName": "MSR",
        "venueShortName": "MS",
        "MDSource": "MF",
        "shortTimeZone": "GMT",
        "tradingPhase": "OPN",
        "clOrdIDFormat": "#20d",
        "supportIntradayData": "false",
        "tradingPhaseProfileID": 123,
        "supportPublicQuoteReq": "false",
        "venueID": "MSR",
        "supportMarketDepth": "false",
        "supportTrade": "true",
        "venueVeryShortName": "M",
        "settlementRank": 7,
        "feedSource": "QUOD",
        "clientVenueID": "MS-RFQ",
        "supportMovers": "false",
        "supportQuote": "false",
        "supportTimesAndSales": "false",
        "supportTickers": "false",
        "routeVenueID": "MSR",
        "venueType": "LIT",
        "supportNews": "false",
        "supportMarketTime": "false",
        "holdFIXShortSell": "false",
        "regulatedShortSell": "false",
        "generateBidOfferID": "false",
        "generateQuoteMsgID": "false",
        "supportTermQuoteRequest": "false",
        "supportQuoteCancel": "true",
        "supportSizedMDRequest": "false",
        "venueQualifier": "RFS",
        "supportDiscretionInst": "false",
        "supportBrokenDateFeed": "true",
        "weekendDay": None,
        "venueOrdCapacity": [
            {
                "ordCapacity": "P"
            },
            {
                "ordCapacity": "A"
            },
            {
                "ordCapacity": "G"
            },
            {
                "ordCapacity": "L"
            },
            {
                "ordCapacity": "W"
            },
            {
                "ordCapacity": "R"
            },
            {
                "ordCapacity": "I"
            },
            {
                "ordCapacity": "O"
            }
        ],
        "venuePhaseSession": [
            {
                "supportMinQty": "false",
                "tradingPhase": "OPN",
                "tradingSession": "NotD",
                "venuePhaseSessionPegPriceType": [],
                "venuePhaseSessionTypeTIF": [
                    {
                        "supportDisplayQty": "false",
                        "timeInForce": "FOK",
                        "ordType": "LMT"
                    },
                    {
                        "supportDisplayQty": "false",
                        "timeInForce": "FOK",
                        "ordType": "MKT"
                    },
                ],
            }
        ]
    }
    api.sendMessage(
        request=SubmitMessageRequest(message=bca.message_to_grpc('ModifyVenue', modify_params_MSR, 'rest_wa314luna'),
                                     parent_event_id=case_id))
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

def change_venue_status_ms(case_id, health, metric):
    modify_params_MS = {
        "tradingStatus": "T",
        "GTDHolidayCheck": "false",
        "algoIncluded": "true",
        "supportBrokerQueue": "false",
        "supportStatus": "false",
        "supportQuoteBook": "false",
        "MIC": "MS-SW",
        "supportOrderBook": "false",
        "supportReverseCalSpread": "false",
        "timeZone": "GMT Standard Time",
        "venueName": "MS",
        "venueShortName": "MS",
        "MDSource": "TEST",
        "shortTimeZone": "GMT",
        "tradingPhase": "OPN",
        "clOrdIDFormat": "#20d",
        "clQuoteReqIDFormat": "#20d",
        "supportIntradayData": "false",
        "tradingPhaseProfileID": 123,
        "supportPublicQuoteReq": "false",
        "venueID": "MS",
        "supportMarketDepth": "true",
        "supportTrade": "true",
        "venueVeryShortName": "M",
        "settlementRank": 7,
        "feedSource": "QUOD",
        "clientVenueID": "MS-SW",
        "supportMovers": "false",
        "supportQuote": "false",
        "supportTimesAndSales": "true",
        "supportTickers": "false",
        "venueType": "LIT",
        "supportNews": "false",
        "supportMarketTime": "false",
        "holdFIXShortSell": "false",
        "regulatedShortSell": "false",
        "multilegReportType": "M",
        "generateBidOfferID": "false",
        "generateQuoteMsgID": "false",
        "supportTermQuoteRequest": "true",
        "supportQuoteCancel": "true",
        "weekendDay": None,
        "supportSizedMDRequest": "false",
        "venueQualifier": "ESP",
        "supportDiscretionInst": "false",
        "supportBrokenDateFeed": "true",
        "venueOrdCapacity": [
            {
                "ordCapacity": "O"
            },
            {
                "ordCapacity": "I"
            },
            {
                "ordCapacity": "R"
            },
            {
                "ordCapacity": "A"
            },
            {
                "ordCapacity": "P"
            },
            {
                "ordCapacity": "G"
            },
            {
                "ordCapacity": "W"
            }
        ],
        "venuePhaseSession": [
            {
                "supportMinQty": "false",
                "tradingPhase": "OPN",
                "tradingSession": "NotD",
                "venuePhaseSessionPegPriceType": [],
                "venuePhaseSessionTypeTIF": [
                    {
                        "supportDisplayQty": "false",
                        "timeInForce": "FOK",
                        "ordType": "LMT"
                    },
                    {
                        "supportDisplayQty": "false",
                        "timeInForce": "FOK",
                        "ordType": "MKT"
                    },
                ],
            }
        ]
    }
    api.sendMessage(
        request=SubmitMessageRequest(message=bca.message_to_grpc('ModifyVenue', modify_params_MS, 'rest_wa314luna'),
                                     parent_event_id=case_id))

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
            message=bca.message_to_grpc('ModifyVenueStatus', modify_venue_params, 'rest_wa314luna'),
            parent_event_id=case_id))


def send_swap_and_filled(case_id):
    #Precondition
    change_venue_status_ms(case_id, 'true', '-1')
    change_venue_status_msr(case_id, 'true', '-1')

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
    rfq.verify_quote_pending_swap(). \
        verify_quote_reject()



def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        send_swap_and_filled(case_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        change_venue_status_ms(case_id, 'true', '-1')
        change_venue_status_msr(case_id, 'true', '-1')
