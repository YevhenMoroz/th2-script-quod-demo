from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime
from custom import basic_custom_actions as bca

class CaseParams:

    connectivity = 'fix-ss-308-mercury-standard'
    mdreqid = bca.client_orderid(10)
    clordid = bca.client_orderid(9)
    settldate= (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d %H:%M:%S')

    def __init__(self,account, case_id, handlinstr='1',
                 side='1',orderqty=1,ordtype='2',timeinforce='4',currency='EUR',settlcurrency='USD',
                 settltype=0, symbol='EUR/USD', securitytype='FXSPOT', securityidsource='8',
                 securityid='EUR/USD', securityexchange='XQFX', product=4):
        self.account=account
        self.case_id=case_id
        self.handlinstr=handlinstr
        self.side=side
        self.orderqty=orderqty
        self.ordtype=ordtype
        self.timeinforce=timeinforce
        self.currency=currency
        self.settlcurrency=settlcurrency
        self.settltype=settltype
        # self.settldate=settldate
        self.symbol=symbol
        self.securitytype=securitytype
        self.securityidsource=securityidsource
        self.securityid=securityid
        self.securityexchange=securityexchange
        self.product=product

