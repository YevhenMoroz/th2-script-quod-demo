import idna.codec

from test_framework.fix_wrappers.FixMessageExecutionReport import FixMessageExecutionReport
from test_framework.fix_wrappers.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from test_framework.fix_wrappers.FixMessageOrderCancelReplaceRequest import FixMessageOrderCancelReplaceRequest
from test_framework.data_sets.constants import GatewaySide, Status


class FixMessageExecutionReportAlgo(FixMessageExecutionReport):

    def __init__(self, parameters: dict = None):
        super().__init__()
        super().change_parameters(parameters)

    def set_params_from_new_order_single(self, new_order_single: FixMessageNewOrderSingle, side: GatewaySide, status: Status):
        if side is GatewaySide.Buy:
            if status is Status.Pending:
                self.__set_pending_new_buy(new_order_single)
            elif status is Status.New:
                self.__set_new_buy(new_order_single)
            elif status is Status.Fill:
                self.__set_fill_buy(new_order_single)
            elif status is Status.PartialFill:
                self.__set_partial_fill_buy(new_order_single)
            elif status is Status.CancelReplace:
                self.__set_cancel_replace_buy(new_order_single)
            elif status is Status.Cancel:
                self.__set_cancel_buy(new_order_single)
            elif status is Status.Eliminate:
                self.__set_eliminate_buy(new_order_single)
            elif status is Status.Reject:
                self.__set_reject_buy(new_order_single)
            else:
                raise Exception(f'Incorrect Status')
        elif side is GatewaySide.Sell:
            if status is Status.Pending:
                self.__set_pending_new_sell(new_order_single)
            elif status is Status.New:
                self.__set_new_sell(new_order_single)
            elif status is Status.Fill:
                self.__set_fill_sell(new_order_single)
            elif status is Status.PartialFill:
                self.__set_partial_fill_sell(new_order_single)
            elif status is Status.Reject:
                self.__set_reject_sell(new_order_single)
            elif status is Status.Cancel:
                self.__set_cancel_sell(new_order_single)
            elif status is Status.Eliminate:
                self.__set_eliminate_sell(new_order_single)
            else:
                raise Exception(f'Incorrect Status')
        return self

    def set_params_from_order_cancel_replace(self, order_cancel_replace: FixMessageOrderCancelReplaceRequest, side: GatewaySide, status: Status):
        if side is GatewaySide.Sell:
            if status is Status.CancelReplace:
                self.__set_cancel_replace_sell(order_cancel_replace)
            elif status is Status.Cancel:
                self.__set_cancel_rep_sell(order_cancel_replace)
            else:
                raise Exception(f'Incorrect Status')
        return self

    def __set_pending_new_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') != 1 and new_order_single.get_parameter('OrdType') != 3:
            temp.update(Price=new_order_single.get_parameter("Price"))
        if new_order_single.get_parameter('OrdType') == 3 or new_order_single.get_parameter('OrdType') == 4:
            temp.update(StopPx=new_order_single.get_parameter('StopPx'))
        if 'DisplayInstruction' in new_order_single.get_parameters():
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty=new_order_single.get_parameter('MinQty'))
        if new_order_single.is_parameter_exist('NoStrategyParameters'):
            temp.update(NoStrategyParameters='*')
        if new_order_single.get_parameter('TargetStrategy') in ['1010', '1011'] or (new_order_single.get_parameter('TargetStrategy') == '1008' and new_order_single.is_parameter_exist('MinQty')):
            temp.update(NoParty='*')
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            TargetStrategy=new_order_single.get_parameter("TargetStrategy"),
            ExecType="A",
            OrdStatus="A",
            TransactTime='*',
            AvgPx='0',
            CumQty='0',
            ExecID='*',
            LastPx='0',
            LastQty='0',
            OrderCapacity='A',
            QtyType='0',
            OrderID='*',
            SettlDate='*',
            LeavesQty=new_order_single.get_parameter("OrderQty"),
            Instrument='*',
        )
        super().change_parameters(temp)
        return self

    def __set_new_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') != 1 and new_order_single.get_parameter('OrdType') != 3:
            temp.update(Price=new_order_single.get_parameter("Price"))
        if new_order_single.get_parameter('OrdType') == 3 or new_order_single.get_parameter('OrdType') == 4:
            temp.update(StopPx=new_order_single.get_parameter('StopPx'))
        if 'DisplayInstruction' in new_order_single.get_parameters():
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty=new_order_single.get_parameter('MinQty'))
        if new_order_single.is_parameter_exist('NoStrategyParameters') or (new_order_single.get_parameter('TargetStrategy') == '1008' and new_order_single.is_parameter_exist('MinQty')): # may edit?
            temp.update(NoStrategyParameters='*')
        if new_order_single.get_parameter('TargetStrategy') in ['1010', '1011'] or (new_order_single.get_parameter('TargetStrategy') == '1008' and new_order_single.is_parameter_exist('MinQty')):
            temp.update(
                SecondaryAlgoPolicyID='*',
                NoParty='*'
            )
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            Currency=new_order_single.get_parameter("Currency"),
            HandlInst=new_order_single.get_parameter("HandlInst"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            TargetStrategy=new_order_single.get_parameter("TargetStrategy"),
            ExecType="0",
            OrdStatus="0",
            TransactTime='*',
            AvgPx='0',
            CumQty='0',
            ExecID='*',
            LastPx='0',
            LastQty='0',
            OrderCapacity='A',
            QtyType='0',
            OrderID='*',
            SettlDate='*',
            LeavesQty=new_order_single.get_parameter("OrderQty"),
            ExecRestatementReason=4,
            Instrument='*',
        )
        super().change_parameters(temp)
        return self

    def __set_pending_new_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == '2':
            temp.update(Price = new_order_single.get_parameter("Price"))
        temp.update(
            Account=new_order_single.get_parameter("Account"),
            ClOrdID='*',
            OrdType=new_order_single.get_parameter('OrdType'),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            Text='*',
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            ExecType="A",
            OrdStatus="A",
            CumQty='0',
            ExecID='*',
            OrderID='*',
            LeavesQty='*',
            TransactTime='*',
            AvgPx='*',
            ExDestination=new_order_single.get_parameter('ExDestination')
        )
        super().change_parameters(temp)
        return self

    def __set_new_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == '2':
            temp.update(Price = new_order_single.get_parameter("Price"))
        temp.update(
            Account=new_order_single.get_parameter("Account"),
            ClOrdID='*',
            OrdType=new_order_single.get_parameter('OrdType'),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            Text='*',
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
            ExecType="0",
            OrdStatus="0",
            CumQty='0',
            ExecID='*',
            OrderID='*',
            LeavesQty='*',
            TransactTime='*',
            AvgPx='*',
            ExDestination=new_order_single.get_parameter('ExDestination')
        )
        super().change_parameters(temp)
        return self

    def __set_fill_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == '2':
            temp.update(Price = new_order_single.get_parameter("Price"))
        if 'DisplayInstruction' in new_order_single.get_parameters():
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.get_parameter('TargetStrategy') != '1008':
            temp.update(LastMkt=new_order_single.get_parameter('ExDestination'))
        if new_order_single.get_parameter('TargetStrategy') == '1011':
            temp.update(
                LastMkt='*',
                ChildOrderID='*'
            )
        if new_order_single.get_parameter('TargetStrategy') == '1008':
            if new_order_single.is_parameter_exist('MinQty'):
                temp.update(
                    LastExecutionPolicy='*',
                    LastMkt='*',
                    TargetStrategy='1008',
                    ExDestination='*',
                    SecondaryAlgoPolicyID='*',
                    ChildOrderID='*',
                )
            else:
                temp.update(
                    ReplyReceivedTime='*',
                    LastExecutionPolicy='*',
                    TradeReportingIndicator='*',
                    LastMkt='*',
                    ExDestination='*'
                )
        if new_order_single.is_parameter_exist('NoStrategyParameters') or (new_order_single.get_parameter('TargetStrategy') == '1008' and new_order_single.is_parameter_exist('MinQty')):
            temp.update(NoStrategyParameters='*')
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty='*')
        if new_order_single.get_parameter('TimeInFirce') == '6':
            temp.update(ExpireDate=new_order_single.get_parameter('ExpireDate'))
        if new_order_single.is_parameter_exist('ClientAlgoPolicyID') and new_order_single.get_parameter('ClientAlgoPolicyID') == 'QA_SORPING_1':
            temp.update(
                IClOrdIdAO='*',
                SecondaryAlgoPolicyID='*',
                LastExecutionPolicy='*',
                ShortCode='*',
            )
        if new_order_single.is_parameter_exist('TargetStrategy'):
            temp.update(TargetStrategy='*')
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastPx='*',
            LastQty=new_order_single.get_parameter('OrderQty'),
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=2,
            OrdType=new_order_single.get_parameter('OrdType'),
            Side=new_order_single.get_parameter('Side'),
            Text='*',
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            TransactTime='*',
            SettlDate='*',
            TradeDate='*',
            ExecType='F',
            LeavesQty=0,
            SecondaryOrderID='*',
            GrossTradeAmt='*',
            NoParty='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            SecAltIDGrp='*',
            QtyType=0,
            SecondaryClOrdID='*',
            Instrument='*',
            SecondaryExecID='*'
        )
        if new_order_single.get_parameter('TargetStrategy') in ['1008', '1011']:
            [temp.pop(key, None) for key in ['SecAltIDGrp', 'SecondaryClOrdID']]
        super().change_parameters(temp)
        return self

    def __set_partial_fill_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == '2':
            temp.update(Price = new_order_single.get_parameter("Price"))
        if 'DisplayInstruction' in new_order_single.get_parameters():
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.get_parameter('TargetStrategy') != '1008' and new_order_single.get_parameter('TargetStrategy') != '1011':
            temp.update(LastMkt=new_order_single.get_parameter('ExDestination'))
        if new_order_single.get_parameter('TargetStrategy') == '1008':
            if new_order_single.is_parameter_exist('MinQty'):
                temp.update(
                    LastExecutionPolicy='*',
                    LastMkt='*',
                    TargetStrategy='1008',
                    ExDestination='*',
                    SecondaryAlgoPolicyID='*',
                    ChildOrderID='*',
                )
            else:
                temp.update(
                    ReplyReceivedTime='*',
                    LastExecutionPolicy='*',
                    TradeReportingIndicator='*',
                    LastMkt='*',
                    ExDestination='*'
                )
        if new_order_single.get_parameter('TargetStrategy') == '1011':
            temp.update(
                SecondaryAlgoPolicyID='*',
                LastExecutionPolicy='*',

                LastMkt='*',
                ChildOrderID='*'
            )
        if new_order_single.is_parameter_exist('NoStrategyParameters') or (new_order_single.get_parameter('TargetStrategy') == '1008' and new_order_single.is_parameter_exist('MinQty')):
            temp.update(NoStrategyParameters='*')
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty='*')
        if new_order_single.is_parameter_exist('ClientAlgoPolicyID') and new_order_single.get_parameter('ClientAlgoPolicyID') == 'QA_SORPING':
            temp.update(
                IClOrdIdAO='*',
                SecondaryAlgoPolicyID='*',
                LastExecutionPolicy='*',
                ShortCode='*',
            )
        if new_order_single.is_parameter_exist('TargetStrategy'):
            temp.update(TargetStrategy='*')
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastPx='*',
            LastQty=new_order_single.get_parameter('OrderQty'),
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=1,
            OrdType=new_order_single.get_parameter('OrdType'),
            Side=new_order_single.get_parameter('Side'),
            Text='*',
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            TransactTime='*',
            SettlDate='*',
            TradeDate='*',
            ExecType='F',
            LeavesQty=0,
            SecondaryOrderID='*',
            GrossTradeAmt='*',
            NoParty='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            SecAltIDGrp='*',
            QtyType=0,
            SecondaryClOrdID='*',
            Instrument='*',
            SecondaryExecID='*'
        )
        if new_order_single.get_parameter('TargetStrategy') in ['1008', '1011']:
            [temp.pop(key, None) for key in ['SecAltIDGrp', 'SecondaryClOrdID']]
        super().change_parameters(temp)
        return self

    def __set_fill_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == '2':
            temp.update(Price = new_order_single.get_parameter("Price"),
                        LastPx=new_order_single.get_parameter('Price'))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            LastPx='*',
            ExecID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdType=new_order_single.get_parameter('OrdType'),
            ClOrdID='*',
            LastQty=new_order_single.get_parameter('OrderQty'),
            Text='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            OrderID='*',
            TransactTime='*',
            Side=new_order_single.get_parameter('Side'),
            AvgPx='*',
            OrdStatus=2,
            Currency=new_order_single.get_parameter('Currency'),
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            Instrument=new_order_single.get_parameter('Instrument'),
            ExecType='F',
            ExDestination=new_order_single.get_parameter('ExDestination'),
            LeavesQty=0
        )
        super().change_parameters(temp)
        return self

    def __set_partial_fill_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == '2':
            temp.update(Price = new_order_single.get_parameter("Price"),
                        LastPx=new_order_single.get_parameter('Price'))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            CumQty=new_order_single.get_parameter('OrderQty'),
            LastPx='*',
            ExecID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdType=new_order_single.get_parameter('OrdType'),
            ClOrdID='*',
            LastQty=new_order_single.get_parameter('OrderQty'),
            Text='Partial fill',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            OrderID='*',
            TransactTime='*',
            Side=new_order_single.get_parameter('Side'),
            AvgPx='*',
            OrdStatus=1,
            Currency=new_order_single.get_parameter('Currency'),
            TimeInForce=0,
            Instrument=new_order_single.get_parameter('Instrument'),
            ExecType='F',
            ExDestination=new_order_single.get_parameter('ExDestination'),
            LeavesQty=0
        )
        super().change_parameters(temp)
        return self

    def __set_reject_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == '2':
            temp.update(Price=new_order_single.get_parameter("Price"))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            Instrument='*',
            AvgPx=0,
            ClOrdID='*',
            CumQty=0,
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            LastPx=0,
            LastQty=0,
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=8,
            Side=new_order_single.get_parameter('Side'),
            Text='QATestReject',
            TimeInForce=0,
            TransactTime='*',
            OrdRejReason='*',
            ExecType=8,
            LeavesQty='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
        )
        super().change_parameters(temp)
        return self

    def __set_cancel_replace_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == '2':
            temp.update(Price = new_order_single.get_parameter("Price"))
        temp.update(
            AvgPx='*',
            ClOrdID='*',
            CumQty='*',
            ExecID='*',
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdType=new_order_single.get_parameter('OrdType'),
            OrdStatus=0,
            TimeInForce=0,
            OrigClOrdID='*',
            Side=new_order_single.get_parameter('Side'),
            Text='OCRRRule',
            TransactTime='*',
            ExecType=5,
            LeavesQty="*"
        )
        super().change_parameters(temp)
        return self

    def __set_cancel_replace_sell(self, order_cancel_replace: FixMessageOrderCancelReplaceRequest = None):
        temp = dict()
        if order_cancel_replace.get_parameter('OrdType') == '2':
            temp.update(Price = order_cancel_replace.get_parameter("Price"))
        if 'DisplayInstruction' in order_cancel_replace.get_parameters():
            temp.update(DisplayInstruction=order_cancel_replace.get_parameter('DisplayInstruction'))
        if order_cancel_replace.is_parameter_exist('ClientAlgoPolicyID'):
            temp.update(SecondaryAlgoPolicyID=order_cancel_replace.get_parameter('ClientAlgoPolicyID'))
        if order_cancel_replace.is_parameter_exist('NoStrategyParameters'):
            temp.update(NoStrategyParameters='*')
        if order_cancel_replace.is_parameter_exist('MinQty'):
            temp.update(MinQty=order_cancel_replace.get_parameter('MinQty'))
        if order_cancel_replace.get_parameter('TargetStrategy') == '1010':
            temp.update(NoParty='*')
        temp.update(
            Account=order_cancel_replace.get_parameter('Account'),
            AvgPx='*',
            ClOrdID=order_cancel_replace.get_parameter('ClOrdID'),
            CumQty='*',
            Currency=order_cancel_replace.get_parameter('Currency'),
            ExecID='*',
            HandlInst=order_cancel_replace.get_parameter('HandlInst'),
            LastPx='*',
            LastQty='*',
            OrderID='*',
            OrderQty=order_cancel_replace.get_parameter('OrderQty'),
            OrdStatus=0,
            OrdType=2,
            OrigClOrdID=order_cancel_replace.get_parameter('ClOrdID'),
            Price=order_cancel_replace.get_parameter('Price'),
            Side=order_cancel_replace.get_parameter('Side'),
            TimeInForce=order_cancel_replace.get_parameter('TimeInForce'),
            TransactTime='*',
            ExecType=5,
            LeavesQty='*',
            OrderCapacity=order_cancel_replace.get_parameter('OrderCapacity'),
            TargetStrategy=order_cancel_replace.get_parameter('TargetStrategy'),
            QtyType='*',
            ExecRestatementReason='*',
            Instrument='*',
            SettlDate='*',
            SettlType='*'
        )
        super().change_parameters(temp)
        return self

    def __set_cancel_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') != 1 and new_order_single.get_parameter('OrdType') != 3:
            temp.update(Price=new_order_single.get_parameter("Price"))
        if new_order_single.get_parameter('OrdType') == 3 or new_order_single.get_parameter('OrdType') == 4:
            temp.update(StopPx=new_order_single.get_parameter('StopPx'))
        if 'DisplayInstruction' in new_order_single.get_parameters():
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.is_parameter_exist('NoStrategyParameters') or (new_order_single.get_parameter('TargetStrategy') == '1008' and new_order_single.is_parameter_exist('MinQty')):
            temp.update(NoStrategyParameters='*')
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty=new_order_single.get_parameter('MinQty'))
        if new_order_single.get_parameter('TargetStrategy') == '1010' or (new_order_single.get_parameter('TargetStrategy') == '1008' and new_order_single.is_parameter_exist('MinQty')):
            temp.update(
                SecondaryAlgoPolicyID='*',
                NoParty='*'
            )
        if new_order_single.get_parameter('TargetStrategy') == '1011':
            temp.update(NoParty='*')
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx=0,
            ClOrdID='*',
            CumQty=0,
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastPx=0,
            LastQty=0,
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=4,
            OrdType=new_order_single.get_parameter('OrdType'),
            OrigClOrdID=new_order_single.get_parameter('ClOrdID'),
            Side=new_order_single.get_parameter('Side'),
            TimeInForce=0,
            TransactTime='*',
            SettlDate='*',
            ExecType=4,
            LeavesQty=0,
            ExecRestatementReason='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            TargetStrategy=new_order_single.get_parameter('TargetStrategy'),
            QtyType='*',
            CxlQty=new_order_single.get_parameter('OrderQty'),
            Instrument='*'
        )
        super().change_parameters(temp)
        return self

    def __set_cancel_rep_sell(self, order_cancel_replace: FixMessageOrderCancelReplaceRequest = None):
        temp = dict()
        if order_cancel_replace.get_parameter('OrdType') == '2':
            temp.update(Price=order_cancel_replace.get_parameter("Price"))
        if 'DisplayInstruction' in order_cancel_replace.get_parameters():
            temp.update(DisplayInstruction=order_cancel_replace.get_parameter('DisplayInstruction'))
        if order_cancel_replace.is_parameter_exist('MinQty'):
            temp.update(MinQty=order_cancel_replace.get_parameter('MinQty'))
        if order_cancel_replace.get_parameter('TargetStrategy') == '1010':
            temp.update(
                NoParty='*',
                SecondaryAlgoPolicyID='*'
            )
        if order_cancel_replace.get_parameter('TargetStrategy') == '1011':
            temp.update(NoParty='*')
        if order_cancel_replace.is_parameter_exist('NoStrategyParameters'):
            temp.update(NoStrategyParameters='*')
        temp.update(
            Account=order_cancel_replace.get_parameter('Account'),
            AvgPx='*',
            ClOrdID='*',
            CumQty=0,
            Currency=order_cancel_replace.get_parameter('Currency'),
            ExecID='*',
            HandlInst=order_cancel_replace.get_parameter('HandlInst'),
            LastPx=0,
            LastQty=0,
            OrderID='*',
            OrderQty=order_cancel_replace.get_parameter('OrderQty'),
            OrdStatus=4,
            OrdType=order_cancel_replace.get_parameter('OrdType'),
            OrigClOrdID=order_cancel_replace.get_parameter('ClOrdID'),
            Side=order_cancel_replace.get_parameter('Side'),
            TimeInForce=0,
            TransactTime='*',
            ExecType=4,
            LeavesQty='*',
            ExecRestatementReason='*',
            OrderCapacity=order_cancel_replace.get_parameter('OrderCapacity'),
            TargetStrategy=order_cancel_replace.get_parameter('TargetStrategy'),
            QtyType='*',
            CxlQty=order_cancel_replace.get_parameter('OrderQty'),
            Instrument='*',
            SettlDate='*',
            SettlType='*'
        )
        super().change_parameters(temp)
        return self

    def __set_cancel_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict(
            ExDestination=new_order_single.get_parameter('ExDestination'),
            AvgPx='*',
            ClOrdID='*',
            CumQty='0',
            ExecID='*',
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=4,
            OrigClOrdID='*',
            Side=new_order_single.get_parameter('Side'),
            Text='order canceled',
            TransactTime='*',
            ExecType=4,
            LeavesQty=0
        )
        super().change_parameters(temp)
        return self

    def __set_eliminate_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        temp.update(
            ExDestination=new_order_single.get_parameter('ExDestination'),
            AvgPx='*',
            ClOrdID='*',
            CumQty='0',
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            ExecID='*',
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=4,
            Side=new_order_single.get_parameter('Side'),
            TransactTime='*',
            ExecType=4,
            LeavesQty='*',
            OrdType=new_order_single.get_parameter('OrdType'),
            Text='*'
        )
        super().change_parameters(temp)
        return self

    def __set_eliminate_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') != 1 and new_order_single.get_parameter('OrdType') != 3:
            temp.update(Price=new_order_single.get_parameter("Price"))
        if new_order_single.get_parameter('OrdType') == 3 or new_order_single.get_parameter('OrdType') == 4:
            temp.update(StopPx=new_order_single.get_parameter('StopPx'))
        if 'DisplayInstruction' in new_order_single.get_parameters():
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.get_parameter('TimeInForce') == 6:
            temp.update(ExpireDate=new_order_single.get_parameter('ExpireDate'))
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty=new_order_single.get_parameter('MinQty'))
        if new_order_single.is_parameter_exist('NoStrategyParameters'):
            temp.update(NoStrategyParameters='*')
        if new_order_single.get_parameter('TargetStrategy') == '1010':
            temp.update(
                NoParty='*',
                SecondaryAlgoPolicyID='*'
            )
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx=0,
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            CumQty=0,
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastPx=0,
            LastQty=0,
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=4,
            OrdType=new_order_single.get_parameter('OrdType'),
            LastMkt='*',
            Side=new_order_single.get_parameter('Side'),
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            TransactTime='*',
            SettlDate='*',
            ExecType=4,
            LeavesQty=0,
            ExecRestatementReason='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            TargetStrategy=new_order_single.get_parameter('TargetStrategy'),
            QtyType='*',
            CxlQty=new_order_single.get_parameter('OrderQty'),
            Instrument='*'
        )
        super().change_parameters(temp)
        return self

    def __set_reject_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') == '2':
            temp.update(Price = new_order_single.get_parameter("Price"))
        if new_order_single.is_parameter_exist('ExDestination'):
            temp.update(ExDestination=new_order_single.get_parameter('ExDestination'))
        temp.update(
            AvgPx='*',
            ClOrdID='*',
            CumQty='0',
            OrdType=new_order_single.get_parameter('OrdType'),
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            ExecID='*',
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=8,
            Side=new_order_single.get_parameter('Side'),
            Text='*',
            TransactTime='*',
            ExecType=8,
            LeavesQty=0
        )
        super().change_parameters(temp)
        return self
