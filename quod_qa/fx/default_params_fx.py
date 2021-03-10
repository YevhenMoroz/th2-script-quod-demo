from custom import tenor_settlement_date as tsd
defauot_quote_params = {
    'Side': 1,
    'Instrument': {
        'Symbol': 'EUR/USD',
        'SecurityType': 'FXSPOT'
        },
    'SettlDate': tsd.spo(),
    'SettlType': '0',
    'OrderQty': 1000000
    }

text_messages = {
    'erPending': 'Receive ExecutionReport (pending)',
    'sendQR': 'Send QuoteRequest',
    'recQ': 'Receive Quote message',
    'sendNOS': 'Send NewOrderSingle',
    'recQC': 'Receive QuoteCancel message',
    'recQRR': 'Receive QuoteRequestReject message',
    'sendNOwithID': 'Send new order with ClOrdID = {}'
    }
