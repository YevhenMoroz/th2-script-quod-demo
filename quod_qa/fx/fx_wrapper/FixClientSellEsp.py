from custom import basic_custom_actions as bca
from quod_qa.fx.fx_wrapper.common import check_order_status, prepeare_tif
from stubs import Stubs
import time


class FixClientSellEsp():
    fix_act = Stubs.fix_act
    verifier = Stubs.verifier
    subscribe = None
    case_params_sell_esp = None
    new_order=None
    md_pending_response=None
    price=''


    def __init__(self, case_params_sell_esp):
        self.case_params_sell_esp=case_params_sell_esp

    #ACTIONS

    #Send MarketDataRequest subscribe method
    def send_md_request(self, event_name_custom=''):
        event_name = 'Send MDR (subscribe)'
        self.case_params_sell_esp.md_params['SubscriptionRequestType'] = '1'
        if event_name_custom!='':
            event_name=event_name_custom
        print('Market Data request parameters: ',self.case_params_sell_esp.md_params)
        self.subscribe = self.fix_act.placeMarketDataRequestFIX(
            bca.convert_to_request(
                event_name,
                self.case_params_sell_esp.connectivityESP,
                self.case_params_sell_esp.case_id,
                bca.message_to_grpc('MarketDataRequest', self.case_params_sell_esp.md_params, self.case_params_sell_esp.connectivityESP)
            ))
        return self

    #Send MarketDataRequest subscribe method timeout
    def send_md_request_timeout(self, timeout):
        self.case_params_sell_esp.md_params['SubscriptionRequestType'] = '1'
        self.subscribe = self.fix_act.placeMarketDataRequestFIX(bca.convert_to_request(
                'Send MDR (subscribe)',
                self.case_params_sell_esp.connectivityESP,
                self.case_params_sell_esp.case_id,
                bca.message_to_grpc('MarketDataRequest', self.case_params_sell_esp.md_params, self.case_params_sell_esp.connectivityESP)
            ), timeout)
        return self

    #Send MarketDataRequest unsubscribe method
    def send_md_unsubscribe(self):
        self.case_params_sell_esp.md_params['SubscriptionRequestType'] = '2'
        self.fix_act.sendMessage(
            bca.convert_to_request(
                'Send MDR (unsubscribe)',
                self.case_params_sell_esp.connectivityESP,
                self.case_params_sell_esp.case_id,
                bca.message_to_grpc('MarketDataRequest', self.case_params_sell_esp.md_params, self.case_params_sell_esp.connectivityESP)
            ))
        return self

    #Send New Order Single
    def send_new_order_single(self,price,qty='',event_name_custom =''):
        even_name = 'Send new order '
        if event_name_custom!='':
            even_name=event_name_custom
        tif = prepeare_tif(self.case_params_sell_esp.timeinforce)
        self.case_params_sell_esp.set_new_order_single_params()
        self.case_params_sell_esp.order_params['Price'] = price
        if qty!='':
            self.case_params_sell_esp.order_params['OrderQty'] = qty
        print('New Order Single parameters: ', self.case_params_sell_esp.order_params)
        self.new_order = self.fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                even_name + tif, self.case_params_sell_esp.connectivityESP, self.case_params_sell_esp.case_id,
                bca.message_to_grpc('NewOrderSingle', self.case_params_sell_esp.order_params, self.case_params_sell_esp.connectivityESP)
            ))
        return self

    def send_new_order_single_timeout(self,price):
        tif = prepeare_tif(self.case_params_sell_esp.timeinforce)
        self.case_params_sell_esp.order_params['Price'] = price
        self.new_order = self.fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                'Send new order ' + tif, self.case_params_sell_esp.connectivityESP, self.case_params_sell_esp.case_id,
                bca.message_to_grpc('NewOrderSingle', self.case_params_sell_esp.order_params, self.case_params_sell_esp.connectivityESP),5
            ))
        return self

    #Extract filed by name
    def extract_filed(self, field, band_number=1):
        if field.lower()=='price':
            self.price = self.subscribe.response_messages_list[0].fields['NoMDEntries'] \
                .message_value.fields['NoMDEntries'].list_value.values[band_number] \
                .message_value.fields['MDEntryPx'].simple_value
            print('Extracted price: ', self.price)
            return self.price
        elif field.lower()=='mdentryid':
            mdEntryId = self.subscribe.response_messages_list[0].fields['NoMDEntries'] \
                .message_value.fields['NoMDEntries'].list_value.values[band_number] \
                .message_value.fields['MDEntryID'].simple_value
            print('Extracted MD Entry ID: ', mdEntryId)
            return mdEntryId
        elif field.lower()=='mdentryforwardpoints':
            mdentryforwardpoints = self.subscribe.response_messages_list[0].fields['NoMDEntries'] \
                .message_value.fields['NoMDEntries'].list_value.values[band_number] \
                .message_value.fields['MDEntryForwardPoints'].simple_value
            print('Extracted forward points: ', mdentryforwardpoints)
            return mdentryforwardpoints


    #VERIFICATION

    # Check Market Data respons was received
    def verify_md_pending(self):
        time.sleep(3)
        self.md_pending_response = self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Receive MarketDataSnapshotFullRefresh (pending)',
                bca.filter_to_grpc('MarketDataSnapshotFullRefresh', self.case_params_sell_esp.md_subscribe_response, ['MDReqID']),
                self.subscribe.checkpoint_id,
                self.case_params_sell_esp.connectivityESP,
                self.case_params_sell_esp.case_id
            ))
        return self

    def verify_md_rejected(self,text,reason=''):
        self.case_params_sell_esp.set_md_reject_response(text)
        time.sleep(5)
        if reason=='date':
            self.case_params_sell_esp.md_reject_response.pop('MDReqRejReason')
        self.verifier.submitCheckRule(
            bca.create_check_rule(
                'Market Data Request Reject',
                bca.filter_to_grpc('MarketDataRequestReject', self.case_params_sell_esp.md_reject_response, ['MDReqID']),
                self.subscribe.checkpoint_id,
                self.case_params_sell_esp.connectivityESP,
                self.case_params_sell_esp.case_id
            )
        )
        return self

    def verify_order_pending(self,price='', qty=''):
        self.case_params_sell_esp.prepare_order_pending_report()
        self.case_params_sell_esp.order_pending['Price'] = self.price
        if price != '':
            self.case_params_sell_esp.order_pending['Price'] = price
        if qty !='':
            self.case_params_sell_esp.order_pending['OrderQty']=qty
            self.case_params_sell_esp.order_pending['LeavesQty']=qty
        self.case_params_sell_esp.order_pending['OrderID']=self.new_order.response_messages_list[0].fields['OrderID'].simple_value
        print('New Order Single pending : ', self.case_params_sell_esp.order_pending)
        self.checkpoint = self.new_order.checkpoint_id
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Pending',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_esp.order_pending, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_esp.connectivityESP, self.case_params_sell_esp.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_new(self,price='',qty=''):
        self.case_params_sell_esp.prepare_order_new_report()
        self.case_params_sell_esp.order_new['Price']=self.price
        self.case_params_sell_esp.order_new['OrderID']=self.new_order.response_messages_list[0].fields['OrderID'].simple_value
        if qty !='':
            self.case_params_sell_esp.order_new['OrderQty']=qty
            self.case_params_sell_esp.order_new['LeavesQty']=qty
        if price !='':
            self.case_params_sell_esp.order_new['Price'] = price
        print('New Order Single NEW : ', self.case_params_sell_esp.order_pending)
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = New',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_esp.order_new, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_esp.connectivityESP, self.case_params_sell_esp.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_filled(self,price='', qty='', spot_s_d=''):
        self.case_params_sell_esp.prepare_order_filled_report()
        self.case_params_sell_esp.order_filled['Price']=self.price
        self.case_params_sell_esp.order_filled['LastPx']=self.price
        self.case_params_sell_esp.order_filled['AvgPx']=self.price
        self.case_params_sell_esp.order_filled['LastSpotRate']=self.price
        self.case_params_sell_esp.order_filled['OrderID']=self.new_order.response_messages_list[0].fields['OrderID'].simple_value
        if spot_s_d!='':
            self.case_params_sell_esp.order_filled['SpotSettlDate'] = spot_s_d
        if qty !='':
            self.case_params_sell_esp.order_filled['OrderQty']=qty
            self.case_params_sell_esp.order_filled['LastQty']=qty
            self.case_params_sell_esp.order_filled['CumQty']=qty
        if price !='':
            self.case_params_sell_esp.order_filled['Price'] = price
            self.case_params_sell_esp.order_filled['LastPx'] = price
            self.case_params_sell_esp.order_filled['AvgPx'] = price
            self.case_params_sell_esp.order_filled['LastSpotRate'] = price
        print('New Order Single Filled : ', self.case_params_sell_esp.order_pending)


        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Filled SPOT',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_esp.order_filled, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_esp.connectivityESP, self.case_params_sell_esp.case_id
            ),
            timeout=3000
        )
        return self



    def verify_order_filled_fwd(self,price='', qty='',fwd_point='',last_spot_rate=''):
        self.case_params_sell_esp.prepare_order_filled_report()
        self.case_params_sell_esp.order_filled['Price']=self.price
        self.case_params_sell_esp.order_filled['LastPx']=self.price
        self.case_params_sell_esp.order_filled['AvgPx']=self.price
        self.case_params_sell_esp.order_filled['LastSpotRate']= '*'
        self.case_params_sell_esp.order_filled['Price'] = self.price
        self.case_params_sell_esp.order_filled['OrderID']=self.new_order.response_messages_list[0].fields['OrderID'].simple_value
        self.case_params_sell_esp.order_filled['LastForwardPoints'] = '*'
        if price != '':
            self.case_params_sell_esp.order_filled['Price'] = price
            self.case_params_sell_esp.order_filled['LastPx'] = price
            self.case_params_sell_esp.order_filled['AvgPx'] = price
            self.case_params_sell_esp.order_filled['Price'] = price
        if fwd_point != '':
            self.case_params_sell_esp.order_filled['LastSpotRate'] = last_spot_rate
            self.case_params_sell_esp.order_filled['LastForwardPoints'] = fwd_point



        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Filled FORWARD',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_esp.order_filled, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_esp.connectivityESP, self.case_params_sell_esp.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_rejected(self,text='',price='', qty=''):
        self.case_params_sell_esp.prepare_order_rejected_report_rfq()
        self.case_params_sell_esp.order_rejected['OrderID']=self.new_order.response_messages_list[0].fields['OrderID'].simple_value
        self.case_params_sell_esp.order_rejected['Price']=self.price
        self.case_params_sell_esp.order_rejected['Text']=text
        if qty !='':
            self.case_params_sell_esp.order_rejected['OrderQty']=qty
        if price !='':
            self.case_params_sell_esp.order_rejected['Price']=price
        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Rejected',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_esp.order_rejected, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_esp.connectivityESP, self.case_params_sell_esp.case_id
            ),
            timeout=3000
        )
        return self

    def verify_order_algo_rejected(self,text):
        self.case_params_sell_esp.prepare_order_algo_rejected_report()
        self.case_params_sell_esp.order_algo_rejected['Price']=self.price
        self.case_params_sell_esp.order_algo_rejected['Text']=text

        self.verifier.submitCheckRule(
            request=bca.create_check_rule(
                'Execution Report with OrdStatus = Rejected',
                bca.filter_to_grpc('ExecutionReport', self.case_params_sell_esp.order_algo_rejected, ['ClOrdID', 'OrdStatus']),
                self.checkpoint, self.case_params_sell_esp.connectivityESP, self.case_params_sell_esp.case_id
            ),
            timeout=3000
        )
        return self