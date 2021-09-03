from custom import basic_custom_actions as bca
from quod_qa.fx.fx_wrapper.common import check_order_status, prepeare_tif
from stubs import Stubs
import time


class FixClientSellRfq():
    fix_act = Stubs.fix_act
    verifier = Stubs.verifier
    quote = None
    case_params_sell_rfq = None
    new_order = None
    quote_response = None
    price = ''
    quote_id = ''

    def __init__(self, case_params_sell_rfq):
        self.case_params_sell_rfq = case_params_sell_rfq

    # ACTIONS

    # Send RFQ
    def send_request_for_quote(self, expire_time=''):
        self.case_params_sell_rfq.prepare_rfq_params()
        if expire_time != '':
            self.case_params_sell_rfq.rfq_params['NoRelatedSymbols'][0]['ExpireTime'] = expire_time
        print('RFQ', self.case_params_sell_rfq.rfq_params)
        self.quote = self.fix_act.placeQuoteFIX(
            bca.convert_to_request(
                'Send Request For Quote',
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('QuoteRequest', self.case_params_sell_rfq.rfq_params,
                                    self.case_params_sell_rfq.connectivityRFQ)
            ))
        return self

    def send_request_for_quote_no_reply(self):
        self.case_params_sell_rfq.prepare_rfq_params()
        print('RFQ', self.case_params_sell_rfq.rfq_params)
        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send Request For Quote',
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('QuoteRequest', self.case_params_sell_rfq.rfq_params,
                                    self.case_params_sell_rfq.connectivityRFQ)
            ))
        return self

    # Send RFQ swap
    def send_request_for_quote_swap(self, expire_time=''):
        self.case_params_sell_rfq.prepare_rfq_params_swap()
        if expire_time != '':
            self.case_params_sell_rfq.rfq_params_swap['NoRelatedSymbols'][0]['ExpireTime'] = expire_time

        print('SWAP RFQ \t', self.case_params_sell_rfq.rfq_params_swap)

        self.quote = self.fix_act.placeQuoteFIX(
            bca.convert_to_request(
                'Send Request For Quote',
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('QuoteRequest', self.case_params_sell_rfq.rfq_params_swap,
                                    self.case_params_sell_rfq.connectivityRFQ)
            ))
        return self

    def send_request_for_quote_swap_no_reply(self):
        self.case_params_sell_rfq.prepare_rfq_params_swap()
        print('SWAP RFQ ', self.case_params_sell_rfq.rfq_params_swap)
        self.quote = self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send Request For Quote',
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('QuoteRequest', self.case_params_sell_rfq.rfq_params_swap,
                                    self.case_params_sell_rfq.connectivityRFQ)
            ))
        return self

    def send_quote_cancel(self):
        self.case_params_sell_rfq.set_quote_cancel_params()
        self.case_params_sell_rfq.quote_cancel['QuoteID'] = self.case_params_sell_rfq.quote_params['QuoteID']
        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send QuoteCancel',
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('QuoteCancel', self.case_params_sell_rfq.quote_cancel,
                                    self.case_params_sell_rfq.connectivityRFQ)
            ))
        return self

    def send_quote_response(self):
        self.case_params_sell_rfq.set_quote_response_params()
        self.case_params_sell_rfq.quote_response['QuoteID'] = self.case_params_sell_rfq.quote_params['QuoteID']
        print('Quote Responce Params    ', self.case_params_sell_rfq.quote_response)
        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send Response',
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('QuoteResponse', self.case_params_sell_rfq.quote_response,
                                    self.case_params_sell_rfq.connectivityRFQ)
            ))
        return self

    # Send New Order Single
    def send_new_order_single(self, price, side='', quote_id=''):
        tif = prepeare_tif(self.case_params_sell_rfq.timeinforce)
        self.price = price
        self.case_params_sell_rfq.order_params['Price'] = self.price
        self.case_params_sell_rfq.order_params['QuoteID'] = self.quote_id
        if quote_id != '':
            self.case_params_sell_rfq.order_params['QuoteID'] = quote_id
        if side != '':
            self.case_params_sell_rfq.order_params['Side'] = side
        print('Send an order', self.case_params_sell_rfq.order_params)

        self.new_order = self.fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                'Send new order ' + tif, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('NewOrderSingle', self.case_params_sell_rfq.order_params,
                                    self.case_params_sell_rfq.connectivityRFQ)
            ))
        # return self.new_order.checkpoint_id
        return self

    # Send New Order Multi LEg
    def send_new_order_multi_leg(self, price='', side=''):
        tif = prepeare_tif(self.case_params_sell_rfq.timeinforce)
        self.price = price
        self.case_params_sell_rfq.order_multi_leg_params['Price'] = self.price

        if price == '':
            self.case_params_sell_rfq.order_multi_leg_params.pop('Price')
        self.case_params_sell_rfq.order_multi_leg_params['QuoteID'] = self.quote_id
        if side != '':
            self.case_params_sell_rfq.order_multi_leg_params['Side'] = side
        print('Send an order', self.case_params_sell_rfq.order_multi_leg_params)

        self.new_order = self.fix_act.placeOrderMultilegFIX(
            request=bca.convert_to_request(
                'Send new order multi leg ' + tif, self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('NewOrderMultileg', self.case_params_sell_rfq.order_multi_leg_params,
                                    self.case_params_sell_rfq.connectivityRFQ)
            ))
        return self

    def send_new_order_single_timeout(self, price):
        tif = prepeare_tif(self.case_params_sell_rfq.timeinforce)
        self.case_params_sell_rfq.order_params['Price'] = price
        self.new_order = self.fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                'Send new order ' + tif, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id,
                bca.message_to_grpc('NewOrderSingle', self.case_params_sell_rfq.order_params,
                                    self.case_params_sell_rfq.connectivityRFQ), 5
            ))
        return self

    # Extract filed by name
    def extract_filed(self, field):
        extract_value = self.quote.response_messages_list[0].fields[field].simple_value
        return extract_value

    # VERIFICATION

    # Check Market Data respons was received
    def verify_quote_pending(self, offer_forward_points='', bid_forward_points='', bid_size='', offer_size='',
                             offer_px='', bid_px='', bid_spot_rate='', offer_spot_rate='', checkpoint_id_=''):
        self.case_params_sell_rfq.prepare_quote_report()
        self.quote_id = self.extract_filed('QuoteID')
        self.case_params_sell_rfq.quote_params['QuoteID'] = self.quote_id
        self.case_params_sell_rfq.quote_params['QuoteMsgID'] = self.quote_id
        # self.case_params_sell_rfq.quote_params['Account'] = self.case_params_sell_rfq.rfq_params['NoRelatedSymbols'][0]['Account']
        self.case_params_sell_rfq.quote_params.pop('Account')
        self.case_params_sell_rfq.quote_params['SettlType'] = \
            self.case_params_sell_rfq.rfq_params['NoRelatedSymbols'][0]['SettlType']
        self.case_params_sell_rfq.quote_params['SettlDate'] = \
            self.case_params_sell_rfq.rfq_params['NoRelatedSymbols'][0]['SettlDate']
        if 'Side' in self.case_params_sell_rfq.quote_params.keys() == False:
            self.case_params_sell_rfq.quote_params['OfferPx'] = '*'
            self.case_params_sell_rfq.quote_params['OfferSize'] = '*'
            self.case_params_sell_rfq.quote_params['BidPx'] = '*'
            self.case_params_sell_rfq.quote_params['BidSize'] = '*'
        if offer_forward_points != '':
            self.case_params_sell_rfq.quote_params['OfferForwardPoints'] = offer_forward_points
        if bid_forward_points != '':
            self.case_params_sell_rfq.quote_params['BidForwardPoints'] = bid_forward_points
        if bid_size != '':
            self.case_params_sell_rfq.quote_params['BidSize'] = bid_size
        if offer_size != '':
            self.case_params_sell_rfq.quote_params['OfferSize'] = offer_size
        if offer_px != '':
            self.case_params_sell_rfq.quote_params['OfferPx'] = offer_px
        if bid_px != '':
            self.case_params_sell_rfq.quote_params['BidPx'] = bid_px
        if bid_spot_rate != '':
            self.case_params_sell_rfq.quote_params['BidSpotRate'] = bid_spot_rate
        if offer_spot_rate != '':
            self.case_params_sell_rfq.quote_params['OfferSpotRate'] = offer_spot_rate

        print('RFQ pending parameters: \t', self.case_params_sell_rfq.quote_params)
        if checkpoint_id_ != '':
            checkpoint_id = checkpoint_id_
        else:
            checkpoint_id = self.quote.checkpoint_id

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Receive quote',
                bca.filter_to_grpc('Quote', self.case_params_sell_rfq.quote_params, ['QuoteReqID']),
                checkpoint_id,
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id
            )
        )
        return self

    def verify_quote_pending_swap(self, offer_swap_points='', bid_swap_points='', bid_size='', offer_size='',
                                  offer_px='', bid_px='', bid_spot_rate='', offer_spot_rate=''
                                  , leg_of_fwd_p='', leg_bid_fwd_p='', checkpoint_id_=''):
        self.case_params_sell_rfq.prepare_quote_report_swap()
        self.quote_id = self.extract_filed('QuoteID')
        self.case_params_sell_rfq.quote_params_swap['QuoteID'] = self.quote_id
        self.case_params_sell_rfq.quote_params_swap['QuoteMsgID'] = self.quote_id
        self.case_params_sell_rfq.quote_params_swap.pop('Account')
        if leg_of_fwd_p != '':
            self.case_params_sell_rfq.quote_params_swap['NoLegs'][1]['LegOfferForwardPoints'] = leg_of_fwd_p
        if leg_bid_fwd_p != '':
            self.case_params_sell_rfq.quote_params_swap['NoLegs'][1]['LegBidForwardPoints'] = leg_bid_fwd_p
        if bid_size != '':
            self.case_params_sell_rfq.quote_params_swap['BidSize'] = bid_size
        if offer_size != '':
            self.case_params_sell_rfq.quote_params_swap['OfferSize'] = offer_size
        if offer_swap_points != '':
            self.case_params_sell_rfq.quote_params_swap['OfferSwapPoints'] = offer_swap_points
        if bid_swap_points != '':
            self.case_params_sell_rfq.quote_params_swap['BidSwapPoints'] = bid_swap_points
        if offer_px != '':
            self.case_params_sell_rfq.quote_params_swap['OfferPx'] = offer_px
        if bid_px != '':
            self.case_params_sell_rfq.quote_params_swap['BidPx'] = bid_px
        if bid_spot_rate != '':
            self.case_params_sell_rfq.quote_params_swap['BidSpotRate'] = bid_spot_rate
        if offer_spot_rate != '':
            self.case_params_sell_rfq.quote_params_swap['OfferSpotRate'] = offer_spot_rate

        print('RFQ swap pending parameters: \t', self.case_params_sell_rfq.quote_params_swap)

        checkpoint_id = self.quote.checkpoint_id
        if checkpoint_id_ != '':
            checkpoint_id = checkpoint_id_

        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Receive quote',
                bca.filter_to_grpc('Quote', self.case_params_sell_rfq.quote_params_swap, ['QuoteReqID']),
                checkpoint_id,
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id
            )
        )
        return self

    def verify_quote_cancel(self):
        self.case_params_sell_rfq.prepape_quote_cancel_report()
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                "Checking QuoteCancel",
                bca.filter_to_grpc("QuoteCancel", self.case_params_sell_rfq.quote_cancel_params),
                self.quote.checkpoint_id,
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id
            )
        )
        return self

    def verify_quote_reject(self, event_name_cust='', text=''):
        self.case_params_sell_rfq.prepare_quote_reject_report()

        event_name = "Checking Quote Reject"
        if event_name_cust != '':
            event_name = event_name_cust
        if text != '':
            self.case_params_sell_rfq.quote_request_reject_params['Text'] = text
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                event_name,
                bca.filter_to_grpc("QuoteRequestReject", self.case_params_sell_rfq.quote_request_reject_params),
                self.quote.checkpoint_id,
                self.case_params_sell_rfq.connectivityRFQ,
                self.case_params_sell_rfq.case_id
            )
        )
        return self

    def verify_order_pending(self, price='', qty='', side=''):
        self.case_params_sell_rfq.prepare_order_pending_report()
        self.case_params_sell_rfq.order_pending['Price'] = self.price
        if price != '':
            self.case_params_sell_rfq.order_pending['Price'] = price
        if qty != '':
            self.case_params_sell_rfq.order_pending['OrderQty'] = qty
            self.case_params_sell_rfq.order_pending['LeavesQty'] = qty
            self.case_params_sell_rfq.order_pending['OrderID'] = self.new_order.response_messages_list[0].fields[
                'OrderID'].simple_value
        if side != '':
            self.case_params_sell_rfq.order_pending['Side'] = side

        print('pending', self.case_params_sell_rfq.order_pending)
        self.checkpoint = self.new_order.checkpoint_id
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Pending',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_pending,
                                   ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_pending_swap(self, price='', qty='', side=''):
        self.case_params_sell_rfq.prepare_order_pending_report()
        self.case_params_sell_rfq.order_pending['Price'] = self.price
        self.case_params_sell_rfq.order_pending['Side'] = self.case_params_sell_rfq.leg2_side
        if price != '':
            self.case_params_sell_rfq.order_pending['Price'] = price
        if side != '':
            self.case_params_sell_rfq.order_pending['Side'] = side
        if price == '':
            self.case_params_sell_rfq.order_pending.pop('Price')
        if qty != '':
            self.case_params_sell_rfq.order_pending['OrderQty'] = qty
            self.case_params_sell_rfq.order_pending['LeavesQty'] = qty
            self.case_params_sell_rfq.order_pending['OrderID'] = self.new_order.response_messages_list[0].fields[
                'OrderID'].simple_value

        # if 'Side' in self.case_params_sell_rfq.quote_params_swap.keys():
        #     pass
        # if side!='':
        #     self.case_params_sell_rfq.order_pending['Side'] = side

        print('pending', self.case_params_sell_rfq.order_pending)
        self.checkpoint = self.new_order.checkpoint_id
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Pending',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_pending,
                                   ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_new(self):
        self.case_params_sell_rfq.prepare_order_new_report()
        self.case_params_sell_rfq.order_new['Price'] = self.price
        self.case_params_sell_rfq.order_new['OrderID'] = self.new_order.response_messages_list[0].fields[
            'OrderID'].simple_value
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = New',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_new, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_filled(self, price='', qty='', side=''):
        self.case_params_sell_rfq.prepare_order_filled_report()
        self.case_params_sell_rfq.order_filled['Price'] = self.price
        self.case_params_sell_rfq.order_filled['LastPx'] = self.price
        self.case_params_sell_rfq.order_filled['SpotSettlDate'] = '*'
        self.case_params_sell_rfq.order_filled['AvgPx'] = self.price
        if side != '':
            self.case_params_sell_rfq.order_filled['Side'] = side
        self.case_params_sell_rfq.order_filled['LastSpotRate'] = self.price
        self.case_params_sell_rfq.order_filled['OrderID'] = self.new_order.response_messages_list[0].fields[
            'OrderID'].simple_value
        print('filled', self.case_params_sell_rfq.order_filled)

        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Filled SPOT',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_filled, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id
            ),
            timeout=1000
        )
        return self

    def verify_drop_copy(self, check_point, spot_date=''):
        self.case_params_sell_rfq.prepare_order_filled_report()
        self.case_params_sell_rfq.prepare_order_filled_taker()
        self.case_params_sell_rfq.order_filled['Price'] = self.price
        self.case_params_sell_rfq.order_filled_drop_copy['Price'] = self.price
        self.case_params_sell_rfq.order_filled['LastPx'] = self.price
        self.case_params_sell_rfq.order_filled_drop_copy['LastPx'] = self.price
        self.case_params_sell_rfq.order_filled['AvgPx'] = self.price
        self.case_params_sell_rfq.order_filled_drop_copy['AvgPx'] = self.price
        self.case_params_sell_rfq.order_filled_drop_copy['LastSpotRate'] = '*'
        self.case_params_sell_rfq.order_filled['LastSpotRate'] = '*'
        if spot_date != '':
            self.case_params_sell_rfq.order_filled_drop_copy['SpotSettlDate'] = spot_date
            self.case_params_sell_rfq.order_filled['SpotSettlDate'] = spot_date
        if self.case_params_sell_rfq.quote_params["SettlType"] != "0":
            self.case_params_sell_rfq.order_filled['LastForwardPoints'] = '*'
            self.case_params_sell_rfq.order_filled_drop_copy['LastForwardPoints'] = '*'
            self.case_params_sell_rfq.order_filled_drop_copy.pop('Account')
        if self.case_params_sell_rfq.quote_params['Side'] == "1":
            self.case_params_sell_rfq.order_filled_drop_copy['Side'] = "2"
        if self.case_params_sell_rfq.quote_params['Side'] == "2":
            self.case_params_sell_rfq.order_filled_drop_copy['Side'] = "1"
        self.case_params_sell_rfq.order_filled['OrderID'] = self.new_order.response_messages_list[0].fields[
            'OrderID'].simple_value
        print('filled', self.case_params_sell_rfq.order_filled)

        message_filters_req = [
            bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_filled_drop_copy),
            bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_filled, ['ClOrdID', 'OrdStatus'])
        ]
        pre_filter_req = bca.prefilter_to_grpc(self.case_params_sell_rfq.drop_filter_params)
        self.verifier.submitCheckSequenceRule(
            bca.create_check_sequence_rule(
                description="Check Drop Copy Execution report",
                prefilter=pre_filter_req,
                msg_filters=message_filters_req,
                checkpoint=check_point,
                connectivity=self.case_params_sell_rfq.connectivityDropCopy,
                event_id=self.case_params_sell_rfq.case_id,
                timeout=3000
            )
        )
        return self

    def verify_order_filled_swap(self, price='', qty='', side='', spot_rate='', last_spot_rate='', leg_last_px_near='',
                                 leg_last_px_far='', last_swap_points='', avg_px='', last_px=''):
        self.case_params_sell_rfq.prepare_order_swap_filled_report()
        self.case_params_sell_rfq.order_filled_swap['Price'] = self.price
        self.case_params_sell_rfq.order_filled_swap['AvgPx'] = self.price
        self.case_params_sell_rfq.order_filled_swap['LastPx'] = self.price
        self.case_params_sell_rfq.order_filled_swap['LastSwapPoints'] = self.price
        if price != '':
            self.case_params_sell_rfq.order_filled_swap['Price'] = price
            self.case_params_sell_rfq.order_filled_swap['AvgPx'] = price
            self.case_params_sell_rfq.order_filled_swap['LastPx'] = price
            self.case_params_sell_rfq.order_filled_swap['LastSwapPoints'] = price
        if price == '':
            self.case_params_sell_rfq.order_filled_swap.pop('Price')
        if spot_rate != '':
            self.case_params_sell_rfq.order_filled_swap['LastSpotRate'] = spot_rate
        if last_swap_points != '':
            self.case_params_sell_rfq.order_filled_swap['LastSwapPoints'] = last_swap_points
        if avg_px != '':
            self.case_params_sell_rfq.order_filled_swap['AvgPx'] = avg_px
        if last_px != '':
            self.case_params_sell_rfq.order_filled_swap['LastPx'] = last_px
        if leg_last_px_near != '':
            self.case_params_sell_rfq.order_filled_swap['NoLegs'][0]['LegLastPx'] = leg_last_px_near
        if leg_last_px_far != '':
            self.case_params_sell_rfq.order_filled_swap['NoLegs'][1]['LegLastPx'] = leg_last_px_far
        if side == '1':
            self.case_params_sell_rfq.order_filled_swap['Side'] = side
            self.case_params_sell_rfq.order_filled_swap['NoLegs'][0]['LegSide'] = '2'
            self.case_params_sell_rfq.order_filled_swap['NoLegs'][1]['LegSide'] = '1'
        if side == '2':
            self.case_params_sell_rfq.order_filled_swap['Side'] = side
            self.case_params_sell_rfq.order_filled_swap['NoLegs'][0]['LegSide'] = '1'
            self.case_params_sell_rfq.order_filled_swap['NoLegs'][1]['LegSide'] = '2'

        print('SWAP FILLED \t', self.case_params_sell_rfq.order_filled_swap)

        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Filled SWAP',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_filled_swap,
                                   ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id
            ),
            timeout=1000
        )
        return self

    def verify_order_filled_swap_drop_copy(self, price='', qty='', side='', spot_rate='', last_spot_rate='',
                                           leg_last_px_near='',
                                           leg_last_px_far='', last_swap_points='', avg_px='', last_px='',
                                           check_point='', spot_date=''):
        self.case_params_sell_rfq.prepare_order_swap_filled_report()
        self.case_params_sell_rfq.prepare_order_swap_filled_taker()
        self.case_params_sell_rfq.order_filled_swap['Price'] = self.price
        self.case_params_sell_rfq.order_filled_swap['AvgPx'] = self.price
        self.case_params_sell_rfq.order_filled_swap['LastPx'] = self.price
        self.case_params_sell_rfq.order_filled_swap['LastSwapPoints'] = self.price
        if spot_date != '':
            self.case_params_sell_rfq.order_filled_swap_drop_copy['SpotSettlDate'] = spot_date
            self.case_params_sell_rfq.order_filled_swap['SpotSettlDate'] = spot_date
        if price != '':
            self.case_params_sell_rfq.order_filled_swap['Price'] = price
            self.case_params_sell_rfq.order_filled_swap['AvgPx'] = price
            self.case_params_sell_rfq.order_filled_swap['LastPx'] = price
            self.case_params_sell_rfq.order_filled_swap['LastSwapPoints'] = price
        if price == '':
            self.case_params_sell_rfq.order_filled_swap.pop('Price')
        if spot_rate != '':
            self.case_params_sell_rfq.order_filled_swap['LastSpotRate'] = spot_rate
        if last_swap_points != '':
            self.case_params_sell_rfq.order_filled_swap['LastSwapPoints'] = last_swap_points
        if avg_px != '':
            self.case_params_sell_rfq.order_filled_swap['AvgPx'] = avg_px
        if last_px != '':
            self.case_params_sell_rfq.order_filled_swap['LastPx'] = last_px
        if leg_last_px_near != '':
            self.case_params_sell_rfq.order_filled_swap['NoLegs'][0]['LegLastPx'] = leg_last_px_near
        if leg_last_px_far != '':
            self.case_params_sell_rfq.order_filled_swap['NoLegs'][1]['LegLastPx'] = leg_last_px_far
        if side == '1':
            self.case_params_sell_rfq.order_filled_swap['Side'] = side
            self.case_params_sell_rfq.order_filled_swap_drop_copy['Side'] = "2"
            self.case_params_sell_rfq.order_filled_swap['NoLegs'][0]['LegSide'] = '2'
            self.case_params_sell_rfq.order_filled_swap['NoLegs'][1]['LegSide'] = '1'
            self.case_params_sell_rfq.order_filled_swap_drop_copy['NoLegs'][0]['LegSide'] = '1'
            self.case_params_sell_rfq.order_filled_swap_drop_copy['NoLegs'][1]['LegSide'] = '2'
        if side == '2':
            self.case_params_sell_rfq.order_filled_swap['Side'] = side
            self.case_params_sell_rfq.order_filled_swap_drop_copy['Side'] = "1"
            self.case_params_sell_rfq.order_filled_swap['NoLegs'][0]['LegSide'] = '1'
            self.case_params_sell_rfq.order_filled_swap['NoLegs'][1]['LegSide'] = '2'
            self.case_params_sell_rfq.order_filled_swap_drop_copy['NoLegs'][0]['LegSide'] = '2'
            self.case_params_sell_rfq.order_filled_swap_drop_copy['NoLegs'][1]['LegSide'] = '1'

        print('SWAP FILLED \t', self.case_params_sell_rfq.order_filled_swap)

        message_filters_req = [
            bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_filled_swap_drop_copy),
            bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_filled_swap, ['ClOrdID', 'OrdStatus'])
        ]
        pre_filter_req = bca.prefilter_to_grpc(self.case_params_sell_rfq.drop_filter_params)
        self.verifier.submitCheckSequenceRule(
            bca.create_check_sequence_rule(
                description="Check Drop Copy Execution report",
                prefilter=pre_filter_req,
                msg_filters=message_filters_req,
                checkpoint=check_point,
                connectivity=self.case_params_sell_rfq.connectivityDropCopy,
                event_id=self.case_params_sell_rfq.case_id,
                timeout=3000
            )
        )
        return self

    def verify_order_filled_fwd(self, price='', qty='', fwd_point='', last_spot_rate='', side=''):
        self.case_params_sell_rfq.prepare_order_filled_report()
        self.case_params_sell_rfq.order_filled['Price'] = self.price
        self.case_params_sell_rfq.order_filled['LastPx'] = self.price
        self.case_params_sell_rfq.order_filled['AvgPx'] = self.price
        self.case_params_sell_rfq.order_filled['LastSpotRate'] = '*'
        self.case_params_sell_rfq.order_filled['Price'] = self.price
        self.case_params_sell_rfq.order_filled['OrderID'] = self.new_order.response_messages_list[0].fields[
            'OrderID'].simple_value
        self.case_params_sell_rfq.order_filled['LastForwardPoints'] = '*'
        if price != '':
            self.case_params_sell_rfq.order_filled['Price'] = price
            self.case_params_sell_rfq.order_filled['LastPx'] = price
            self.case_params_sell_rfq.order_filled['AvgPx'] = price
            self.case_params_sell_rfq.order_filled['Price'] = price
        if fwd_point != '':
            self.case_params_sell_rfq.order_filled['LastSpotRate'] = last_spot_rate
            self.case_params_sell_rfq.order_filled['LastForwardPoints'] = fwd_point
        if side != '':
            self.case_params_sell_rfq.order_filled['Side'] = side

        print('Filled', self.case_params_sell_rfq.order_filled)
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Filled FORWARD',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_filled, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_rejected(self, text='', price='', qty='', side=''):
        self.case_params_sell_rfq.prepare_order_rejected_report_rfq()
        self.case_params_sell_rfq.order_rejected['OrderID'] = self.new_order.response_messages_list[0].fields[
            'OrderID'].simple_value
        self.case_params_sell_rfq.order_rejected['Price'] = self.price
        self.case_params_sell_rfq.order_rejected['Text'] = text
        if qty != '':
            self.case_params_sell_rfq.order_rejected['OrderQty'] = qty
        if side != '':
            self.case_params_sell_rfq.order_rejected['Side'] = side
        print('Order report for REJECTION ', self.case_params_sell_rfq.order_rejected)
        self.checkpoint = self.new_order.checkpoint_id
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Rejected',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_rejected,
                                   ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityRFQ, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_algo_rejected(self, text):
        self.case_params_sell_rfq.prepare_order_algo_rejected_report()
        self.case_params_sell_rfq.order_algo_rejected['Price'] = self.price
        self.case_params_sell_rfq.order_algo_rejected['Text'] = text

        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Rejected',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_rfq.order_algo_rejected,
                                   ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_rfq.connectivityESP, self.case_params_sell_rfq.case_id
            ),
            timeout=3000
        )
        return self
