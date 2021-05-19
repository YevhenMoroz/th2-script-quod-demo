class requests:

    #DEFAULT COMMON VALUE:
    connectivity = 'fix-qsesp-303'
    md_req_id =  '',
    cl_ord_id =  '',
    account = 'CLIENT1'
    handl_instr = '1'
    side = '1'
    order_qty = 1000000
    ord_type = '2'
    time_in_force = '4'
    currency = 'EUR'
    settl_currency = 'USD'
    settl_type = 0
    settl_date =  '',
    symbol = 'EUR/USD'
    security_type = 'FXSPOT'
    security_id_source = '8'
    security_id = 'EUR/USD'
    security_exchange = 'XQFX'
    product = '8'
    instrument = {
        'Symbol': symbol,
        'SecurityType': security_type,
        'SecurityIDSource': security_id_source,
        'SecurityID': security_id,
        'SecurityExchange': security_exchange
    }

    #PARAMS FOR SUBSCRIBING
    case_params = {
        'Connectivity': connectivity,
        'MDReqID':  md_req_id,
        'ClOrdID':  cl_ord_id,
        'Account': account,
        'HandlInst': handl_instr,
        'Side': side,
        'OrdType': ord_type,
        'TimeInForce': time_in_force,
        'Currency': currency,
        'SettlCurrency': settl_currency,
        'SettlType': settl_type,
        'SettlDate': settl_date,
        'Instrument' : instrument,
        'Product': product,
    }

    def __init__(self, connectivity=connectivity,
                 md_req_id=md_req_id,
                 cl_ord_id=cl_ord_id,
                 account=account,
                 handl_instr=handl_instr,
                 side=side,
                 order_qty=order_qty,
                 ord_type=ord_type,
                 time_in_force=time_in_force,
                 currency=currency,
                 settl_currency=settl_currency,
                 settl_type=settl_type,
                 settl_date=settl_date,
                 product=product,
                 symbol=symbol,
                 security_type=security_type,
                 security_id_source=security_id_source,
                 security_id=security_id,
                 security_exchange=security_exchange,
                 ):
        self.connectivity=connectivity
        self.md_req_id=md_req_id
        self.cl_ord_id=cl_ord_id
        self.account=account
        self.handl_instr= handl_instr
        self.side=side
        self.order_qty=order_qty
        self.ord_type=ord_type
        self.time_in_force=time_in_force
        self.currency=currency
        self.settl_currency=settl_currency
        self.settl_type=settl_type
        self.settl_date=settl_date
        self.product=product
        self.symbol=symbol
        self.security_type=security_type
        self.security_id_source=security_id_source
        self.security_id=security_id
        self.security_exchange=security_exchange




    #EXECUTION REPORT VALUES:
    orderCapacity = 'A'

    # This parameters can be used for ExecutionReport message
    reusable_order_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': case_params['Side'],
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': orderCapacity,
        'Currency': case_params['Currency'],
        'Instrument': {
            'Symbol': case_params['Instrument']['Symbol'],
            'SecurityIDSource': case_params['Instrument']['SecurityIDSource'],
            'SecurityID': case_params['Instrument']['SecurityID'],
            'SecurityExchange': case_params['Instrument']['SecurityExchange']
        }
    }





    md_params = {
        'SenderSubID': case_params['Account'],
        'MDReqID': case_params['MDReqID'],
        'SubscriptionRequestType': '1',
        'MarketDepth': '0',
        'MDUpdateType': '0',
        'NoMDEntryTypes': [{'MDEntryType': '0'}, {'MDEntryType': '1'}],
        'NoRelatedSymbols': [
            {
                'Instrument': {
                'Symbol': case_params['Instrument']['Symbol'],
                        'SecurityType': case_params['Instrument']['SecurityType']
                    },
                    'SettlDate': case_params['SettlDate'],
                    'SettlType': case_params['SettlType']
                }
            ],
        'Product': case_params['Product']
        }


