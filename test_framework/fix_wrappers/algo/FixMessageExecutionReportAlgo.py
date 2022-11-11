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
        elif side is GatewaySide.RBSell:
            if status is Status.Pending:
                self.__set_pending_new_rb_sell(new_order_single)
            elif status is Status.New:
                self.__set_new_rb_sell(new_order_single)
            elif status is Status.Cancel:
                self.__set_cancel_rb_sell(new_order_single)
            else:
                raise Exception(f'Incorrect Status')
        return self

    def set_params_from_order_cancel_replace(self, order_cancel_replace: FixMessageOrderCancelReplaceRequest, side: GatewaySide, status: Status):
        if side is GatewaySide.Sell:
            if status is Status.CancelReplace:
                self.__set_cancel_replace_sell(order_cancel_replace)
            elif status is Status.Cancel:
                self.__set_cancel_rep_sell(order_cancel_replace)
            elif status is Status.PartialFill:
                self.__set_cancel_rep_partial_fill_sell(order_cancel_replace)
            elif status is Status.Fill:
                self.__set_cancel_rep_fill_sell(order_cancel_replace)
            else:
                raise Exception(f'Incorrect Status')
        return self

    def set_params_from_new_order_single_for_DMA(self, new_order_single: FixMessageNewOrderSingle, status: Status):
        if status is Status.Pending:
            self.__set_pending_new_dma(new_order_single)
        elif status is Status.New:
            self.__set_new_dma(new_order_single)
        elif status is Status.Fill:
            self.__set_fill_dma(new_order_single)
        elif status is Status.PartialFill:
            self.__set_partial_fill_dma(new_order_single)
        elif status is Status.Reject:
            self.__set_reject_dma(new_order_single)
        elif status is Status.Cancel:                           
            self.__set_cancel_dma(new_order_single)
        elif status is Status.Eliminate:
            self.__set_eliminate_dma(new_order_single)
        else:
            raise Exception(f'Incorrect Status')
        return self

    def set_params_from_order_cancel_replace_for_DMA(self, order_cancel_replace: FixMessageOrderCancelReplaceRequest, status: Status):
        if status is Status.CancelReplace:
            self.__set_cancel_replace_dma(order_cancel_replace)
        elif status is Status.Cancel:
            self.__set_cancel_rep_dma(order_cancel_replace)
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
        if new_order_single.get_parameter('TargetStrategy') in ['1010', '1011', '1004', '1003'] or (new_order_single.get_parameter('TargetStrategy') == '1008' and new_order_single.is_parameter_exist('MinQty')) or new_order_single.is_parameter_exist('NoParty'):
            temp.update(NoParty='*')
        if new_order_single.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate=new_order_single.get_parameter('ExpireDate'))
        if new_order_single.is_parameter_exist('ExpireTime'):
            temp.update(ExpireTime=new_order_single.get_parameter('ExpireTime'))
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

    def __set_pending_new_dma(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') != 1 and new_order_single.get_parameter('OrdType') != 3:
            temp.update(Price=new_order_single.get_parameter("Price"))
        if new_order_single.get_parameter('OrdType') == 3 or new_order_single.get_parameter('OrdType') == 4:
            temp.update(StopPx=new_order_single.get_parameter('StopPx'))
        if 'DisplayInstruction' in new_order_single.get_parameters():
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty=new_order_single.get_parameter('MinQty'))
        if new_order_single.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate=new_order_single.get_parameter('ExpireDate'))
        if new_order_single.is_parameter_exist('ExpireTime'):
            temp.update(ExpireTime=new_order_single.get_parameter('ExpireTime'))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            Currency=new_order_single.get_parameter("Currency"),
            OrderQty=new_order_single.get_parameter("OrderQty"),
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
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
            NoParty='*',
            HandlInst='*'
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
        if new_order_single.is_parameter_exist('NoStrategyParameters') or ('ClientAlgoPolicyID' not in new_order_single.get_parameters() and new_order_single.get_parameter('TargetStrategy') not in ['1004', '1003']):
            temp.update(NoStrategyParameters='*')
        if new_order_single.get_parameter('TargetStrategy') in ['1010', '1011', '1004'] or (new_order_single.get_parameter('TargetStrategy') == '1008' and new_order_single.is_parameter_exist('MinQty')):
            temp.update(
                SecondaryAlgoPolicyID='*',
                NoParty='*'
            )
        if new_order_single.is_parameter_exist('ClientAlgoPolicyID'):
            temp.update(SecondaryAlgoPolicyID='*')
        if new_order_single.get_parameter('TargetStrategy') == '1003' or new_order_single.is_parameter_exist('NoParty'):
            temp.update(NoParty='*')
        if new_order_single.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate=new_order_single.get_parameter('ExpireDate'))
        if new_order_single.is_parameter_exist('ExpireTime'):
            temp.update(ExpireTime=new_order_single.get_parameter('ExpireTime'))
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

    def __set_new_dma(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') != 1 and new_order_single.get_parameter('OrdType') != 3:
            temp.update(Price=new_order_single.get_parameter("Price"))
        if new_order_single.get_parameter('OrdType') == 3 or new_order_single.get_parameter('OrdType') == 4:
            temp.update(StopPx=new_order_single.get_parameter('StopPx'))
        if 'DisplayInstruction' in new_order_single.get_parameters():
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty=new_order_single.get_parameter('MinQty'))
        if new_order_single.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate=new_order_single.get_parameter('ExpireDate'))
        if new_order_single.is_parameter_exist('ExpireTime'):
            temp.update(ExpireTime=new_order_single.get_parameter('ExpireTime'))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            ClOrdID=new_order_single.get_parameter("ClOrdID"),
            Currency=new_order_single.get_parameter("Currency"),
            NoParty='*',
            OrderQty=new_order_single.get_parameter("OrderQty"),
            OrdType=new_order_single.get_parameter("OrdType"),
            Side=new_order_single.get_parameter("Side"),
            TimeInForce=new_order_single.get_parameter("TimeInForce"),
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
            Instrument='*',
            HandlInst='*',
            ExecRestatementReason='*',
        )
        super().change_parameters(temp)
        return self

    def __set_pending_new_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.is_parameter_exist("Price"):
            temp.update(Price=new_order_single.get_parameter("Price"))
        if new_order_single.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate=new_order_single.get_parameter('ExpireDate'))
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
        if new_order_single.is_parameter_exist("Price"):
            temp.update(Price=new_order_single.get_parameter("Price"))
        if new_order_single.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate=new_order_single.get_parameter('ExpireDate'))
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
        if str(new_order_single.get_parameter('OrdType')) == '2':
            temp.update(Price = new_order_single.get_parameter("Price"))
        if 'DisplayInstruction' in new_order_single.get_parameters():
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.get_parameter('TargetStrategy') not in ['1008', '1011', '1010']:
            temp.update(LastMkt=new_order_single.get_parameter('ExDestination'))
        if new_order_single.is_parameter_exist("IClOrdIdTO"):
            temp.update(IClOrdIdTO=new_order_single.get_parameter("IClOrdIdTO"))
        if new_order_single.get_parameter('TargetStrategy') != '1010':
            temp.update(
                SecAltIDGrp='*',
                SecondaryClOrdID='*',
            )
        if new_order_single.get_parameter('TargetStrategy') == '1010':
            temp.update(
                LastMkt='*',
                ChildOrderID='*',
            )
        if new_order_single.get_parameter('TargetStrategy') == '1011' or new_order_single.get_parameter('TargetStrategy') == '1004':
            temp.update(
                ExDestination='*',
                LastMkt='*',
                ChildOrderID='*'
            )
        if new_order_single.is_parameter_exist('ClientAlgoPolicyID') or new_order_single.get_parameter('TargetStrategy') == '1004':
            temp.update(
                IClOrdIdAO='*',
                SecondaryAlgoPolicyID='*',
                LastExecutionPolicy='*',
                ShortCode='*',
                ExDestination='*'
            )
        if new_order_single.is_parameter_exist('IClOrdIdCO'):
            temp.update(IClOrdIdCO=new_order_single.get_parameter('IClOrdIdCO'))
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
            elif new_order_single.is_parameter_exist('ClientAlgoPolicyID'):
                temp.update(
                    LastExecutionPolicy='*',
                    LastMkt='*',
                    ExDestination='*',
                    ChildOrderID='*'
                )
            else:
                temp.update(
                    ReplyReceivedTime='*',
                    LastExecutionPolicy='*',
                    TradeReportingIndicator='*',
                    LastMkt='*',
                    ExDestination='*'
                )
        if new_order_single.is_parameter_exist('NoStrategyParameters') or ('ClientAlgoPolicyID' not in new_order_single.get_parameters() and new_order_single.get_parameter('TargetStrategy') != '1004'):
            temp.update(NoStrategyParameters='*')
        if 'ClientAlgoPolicyID' not in new_order_single.get_parameters() and new_order_single.get_parameter('TargetStrategy') == '1011':
            temp.update(
                SecondaryAlgoPolicyID='*',
                LastExecutionPolicy='*'
            )
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty='*')
        if new_order_single.get_parameter('TimeInForce') == '6':
            temp.update(ExpireDate=new_order_single.get_parameter('ExpireDate'))
        if new_order_single.is_parameter_exist('TargetStrategy'):
            temp.update(TargetStrategy='*')
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            CumQty='*',
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastPx='*',
            LastQty='*',
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
            QtyType=0,
            Instrument='*',
            SecondaryExecID='*'
        )
        if new_order_single.get_parameter('TargetStrategy') in ['1008', '1011', '1004']:
            [temp.pop(key, None) for key in ['SecAltIDGrp', 'SecondaryClOrdID']]
        super().change_parameters(temp)
        return self

    def __set_fill_dma(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if str(new_order_single.get_parameter('OrdType')) == '2':
            temp.update(Price = new_order_single.get_parameter("Price"))
        if 'DisplayInstruction' in new_order_single.get_parameters():
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty='*')
        if new_order_single.get_parameter('TimeInForce') == '6':
            temp.update(ExpireDate=new_order_single.get_parameter('ExpireDate'))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID='*',
            CumQty=new_order_single.get_parameter('OrderQty'),
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            LastPx='*',
            LastQty='*',
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=2,
            OrdType=new_order_single.get_parameter('OrdType'),
            Side=new_order_single.get_parameter('Side'),
            Text='*',
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            TransactTime='*',
            ExecType='F',
            LeavesQty=0,
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            Instrument='*',
            ExDestination=new_order_single.get_parameter('ExDestination')
        )
        super().change_parameters(temp)
        return self

    def __set_partial_fill_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if str(new_order_single.get_parameter('OrdType')) == '2':
            temp.update(Price = new_order_single.get_parameter("Price"))
        if 'DisplayInstruction' in new_order_single.get_parameters():
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.get_parameter('TargetStrategy') in ['1011', '1010'] and new_order_single.is_parameter_exist('ClientAlgoPolicyID'):
            temp.update(
                IClOrdIdAO='*',
                ShortCode='*'
            )
        if new_order_single.get_parameter('TargetStrategy') == '1008':
            if new_order_single.is_parameter_exist('MinQty'):
                temp.update(
                    LastExecutionPolicy='*',
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
                    ExDestination='*'
                )
        if new_order_single.get_parameter('TargetStrategy') in ['1011', '1010']:
            temp.update(
                SecondaryAlgoPolicyID='*',
                LastExecutionPolicy='*',
                ExDestination='*',
                ChildOrderID='*'
            )
        if new_order_single.is_parameter_exist('NoStrategyParameters') or (new_order_single.get_parameter('TargetStrategy') == '1008' and new_order_single.is_parameter_exist('MinQty')):
            temp.update(NoStrategyParameters='*')
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty='*')
        if new_order_single.is_parameter_exist('TargetStrategy'):
            temp.update(TargetStrategy='*')
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            CumQty='*',
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastPx='*',
            LastQty='*',
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=1,
            OrdType=new_order_single.get_parameter('OrdType'),
            Side=new_order_single.get_parameter('Side'),
            Text='*',
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            TransactTime='*',
            SettlDate='*',
            LastMkt='*',
            TradeDate='*',
            ExecType='F',
            LeavesQty='*',
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
        if new_order_single.get_parameter('TargetStrategy') in ['1008', '1011', '1010']:
            [temp.pop(key, None) for key in ['SecAltIDGrp', 'SecondaryClOrdID']]
        super().change_parameters(temp)
        return self

    def __set_partial_fill_dma(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if str(new_order_single.get_parameter('OrdType')) == '2':
            temp.update(Price = new_order_single.get_parameter("Price"))
        if 'DisplayInstruction' in new_order_single.get_parameters():
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty='*')
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            CumQty='*',
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastPx='*',
            LastQty='*',
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
            LeavesQty='*',
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
        super().change_parameters(temp)
        return self

    def __set_fill_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.is_parameter_exist('Price'):
            temp.update(
                Price=new_order_single.get_parameter("Price"),
                LastPx=new_order_single.get_parameter('Price')
            )
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
            Instrument='*',
            ExecType='F',
            ExDestination=new_order_single.get_parameter('ExDestination'),
            LeavesQty=0
        )
        super().change_parameters(temp)
        return self

    def __set_partial_fill_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if str(new_order_single.get_parameter('OrdType')) == '2':
            temp.update(Price = new_order_single.get_parameter("Price"),
                        LastPx=new_order_single.get_parameter('Price'))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            CumQty='*',
            LastPx='*',
            ExecID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdType=new_order_single.get_parameter('OrdType'),
            ClOrdID='*',
            LastQty='*',
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
            LeavesQty='*'
        )
        super().change_parameters(temp)
        return self

    def __set_reject_buy(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.is_parameter_exist('Price'):
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
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
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
        if new_order_single.is_parameter_exist('Price'):
            temp.update(Price=new_order_single.get_parameter("Price"))
        if new_order_single.is_parameter_exist('StopPx'):
            temp.update(StopPx=new_order_single.get_parameter("StopPx"))
        if new_order_single.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate='*')
        temp.update(
            AvgPx='*',
            ClOrdID='*',
            CumQty='*',
            ExecID='*',
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdType=new_order_single.get_parameter('OrdType'),
            OrdStatus=0,
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            OrigClOrdID='*',
            Side=new_order_single.get_parameter('Side'),
            Text='*',
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
        if order_cancel_replace.is_parameter_exist('NoStrategyParameters') or (order_cancel_replace.get_parameter('TargetStrategy') == '1008' and order_cancel_replace.is_parameter_exist('MinQty')):
            temp.update(NoStrategyParameters='*')
        if order_cancel_replace.is_parameter_exist('MinQty'):
            temp.update(MinQty=order_cancel_replace.get_parameter('MinQty'))
        if order_cancel_replace.get_parameter('TargetStrategy') == '1008' and order_cancel_replace.is_parameter_exist('MinQty'):
            temp.update(SecondaryAlgoPolicyID='*')
        if order_cancel_replace.get_parameter('TargetStrategy') in ['1010', '1011', '1008', '1004']:
            temp.update(NoParty='*')
        if order_cancel_replace.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate=order_cancel_replace.get_parameter('ExpireDate'))
        if order_cancel_replace.is_parameter_exist('StopPx'):
            temp.update(StopPx=order_cancel_replace.get_parameter('StopPx'))
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
            OrdType=order_cancel_replace.get_parameter('OrdType'),
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

    def __set_cancel_replace_dma(self, order_cancel_replace: FixMessageOrderCancelReplaceRequest = None):
        temp = dict()
        if order_cancel_replace.get_parameter('OrdType') == '2':
            temp.update(Price = order_cancel_replace.get_parameter("Price"))
        if 'DisplayInstruction' in order_cancel_replace.get_parameters():
            temp.update(DisplayInstruction=order_cancel_replace.get_parameter('DisplayInstruction'))
        if order_cancel_replace.is_parameter_exist('MinQty'):
            temp.update(MinQty=order_cancel_replace.get_parameter('MinQty'))
        if order_cancel_replace.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate=order_cancel_replace.get_parameter('ExpireDate'))
        if order_cancel_replace.is_parameter_exist('StopPx'):
            temp.update(StopPx=order_cancel_replace.get_parameter('StopPx'))
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
            OrdType=order_cancel_replace.get_parameter('OrdType'),
            OrigClOrdID=order_cancel_replace.get_parameter('ClOrdID'),
            Price=order_cancel_replace.get_parameter('Price'),
            Side=order_cancel_replace.get_parameter('Side'),
            TimeInForce=order_cancel_replace.get_parameter('TimeInForce'),
            TransactTime='*',
            ExecType=5,
            LeavesQty='*',
            OrderCapacity=order_cancel_replace.get_parameter('OrderCapacity'),
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
        if new_order_single.is_parameter_exist('NoStrategyParameters') or ('ClientAlgoPolicyID' not in new_order_single.get_parameters() and 'StrategyName' not in new_order_single.get_parameters() and new_order_single.get_parameter('TargetStrategy') != '1003'):
            temp.update(NoStrategyParameters='*')
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty=new_order_single.get_parameter('MinQty'))
        if new_order_single.get_parameter('TargetStrategy') in ['1010', '1011', '1004'] or (new_order_single.get_parameter('TargetStrategy') == '1008' and new_order_single.is_parameter_exist('MinQty')):
            temp.update(
                SecondaryAlgoPolicyID='*',
                NoParty='*'
            )
        if new_order_single.get_parameter('TargetStrategy') == '1003':
            temp.update(
                NoParty='*'
            )
        if new_order_single.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate=new_order_single.get_parameter('ExpireDate'))
        if new_order_single.is_parameter_exist('ExpireTime'):
            temp.update(ExpireTime=new_order_single.get_parameter('ExpireTime'))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID='*',
            CumQty='*',
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
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            TransactTime='*',
            SettlDate='*',
            ExecType=4,
            LeavesQty=0,
            ExecRestatementReason='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            TargetStrategy=new_order_single.get_parameter('TargetStrategy'),
            QtyType='*',
            CxlQty='*',
            Instrument='*'
        )
        super().change_parameters(temp)
        return self

    def __set_cancel_dma(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') != 1 and new_order_single.get_parameter('OrdType') != 3:
            temp.update(Price=new_order_single.get_parameter("Price"))
        if new_order_single.get_parameter('OrdType') == 3 or new_order_single.get_parameter('OrdType') == 4:
            temp.update(StopPx=new_order_single.get_parameter('StopPx'))
        if 'DisplayInstruction' in new_order_single.get_parameters():
            temp.update(DisplayInstruction=new_order_single.get_parameter('DisplayInstruction'))
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty=new_order_single.get_parameter('MinQty'))
        if new_order_single.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate=new_order_single.get_parameter('ExpireDate'))
        if new_order_single.is_parameter_exist('ExpireTime'):
            temp.update(ExpireTime=new_order_single.get_parameter('ExpireTime'))
        if new_order_single.is_parameter_exist('NoParty'):
            temp.update(NoParty='*')
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID='*',
            CumQty='*',
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
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            TransactTime='*',
            SettlDate='*',
            ExecType=4,
            LeavesQty=0,
            ExecRestatementReason='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            QtyType='*',
            CxlQty='*',
            Instrument='*'
        )
        super().change_parameters(temp)
        return self

    def __set_cancel_rep_sell(self, order_cancel_replace: FixMessageOrderCancelReplaceRequest = None):
        temp = dict()
        if order_cancel_replace.is_parameter_exist('Price'):
            temp.update(Price=order_cancel_replace.get_parameter('Price'))
        if order_cancel_replace.is_parameter_exist('StopPx'):
            temp.update(StopPx=order_cancel_replace.get_parameter('StopPx'))
        if 'DisplayInstruction' in order_cancel_replace.get_parameters():
            temp.update(DisplayInstruction=order_cancel_replace.get_parameter('DisplayInstruction'))
        if order_cancel_replace.is_parameter_exist('MinQty'):
            temp.update(MinQty=order_cancel_replace.get_parameter('MinQty'))
        if order_cancel_replace.get_parameter('TargetStrategy') == '1011' and order_cancel_replace.is_parameter_exist('ClientAlgoPolicyID'):
            temp.update(SecondaryAlgoPolicyID='*')
        if order_cancel_replace.get_parameter('TargetStrategy') == '1010' or (order_cancel_replace.get_parameter('TargetStrategy') == '1008' and order_cancel_replace.is_parameter_exist('MinQty')) or (order_cancel_replace.get_parameter('TargetStrategy') == '1004' and order_cancel_replace.is_parameter_exist('ClientAlgoPolicyID')):
            temp.update(
                NoParty='*',
                SecondaryAlgoPolicyID='*'
            )
        if order_cancel_replace.get_parameter('TargetStrategy') in ['1011']:
            temp.update(NoParty='*')
        if order_cancel_replace.is_parameter_exist('NoStrategyParameters') or (order_cancel_replace.get_parameter('TargetStrategy') == '1008' and order_cancel_replace.is_parameter_exist('MinQty')):
            temp.update(NoStrategyParameters='*')
        if order_cancel_replace.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate='*')
        temp.update(
            Account=order_cancel_replace.get_parameter('Account'),
            AvgPx='*',
            ClOrdID='*',
            CumQty='*',
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
            TimeInForce=order_cancel_replace.get_parameter('TimeInForce'),
            TransactTime='*',
            ExecType=4,
            LeavesQty='*',
            ExecRestatementReason='*',
            OrderCapacity=order_cancel_replace.get_parameter('OrderCapacity'),
            TargetStrategy=order_cancel_replace.get_parameter('TargetStrategy'),
            QtyType='*',
            CxlQty='*',
            Instrument='*',
            SettlDate='*',
            SettlType='*'
        )
        super().change_parameters(temp)
        return self

    def __set_cancel_rep_dma(self, order_cancel_replace: FixMessageOrderCancelReplaceRequest = None):
        temp = dict()
        if order_cancel_replace.is_parameter_exist('Price'):
            temp.update(Price=order_cancel_replace.get_parameter('Price'))
        if order_cancel_replace.is_parameter_exist('StopPx'):
            temp.update(StopPx=order_cancel_replace.get_parameter('StopPx'))
        if 'DisplayInstruction' in order_cancel_replace.get_parameters():
            temp.update(DisplayInstruction=order_cancel_replace.get_parameter('DisplayInstruction'))
        if order_cancel_replace.is_parameter_exist('MinQty'):
            temp.update(MinQty=order_cancel_replace.get_parameter('MinQty'))
        if order_cancel_replace.is_parameter_exist('ExpireDate'):
            temp.update(ExpireDate='*')
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
            TimeInForce=order_cancel_replace.get_parameter('TimeInForce'),
            TransactTime='*',
            ExecType=4,
            LeavesQty='*',
            ExecRestatementReason='*',
            OrderCapacity=order_cancel_replace.get_parameter('OrderCapacity'),
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

    def set_params_for_nos_eliminate_rule(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            LastPx='*',
            LastQty='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            Price=new_order_single.get_parameter('Price'),
            Currency=new_order_single.get_parameter('Currency'),
            Instrument=new_order_single.get_parameter('Instrument'),
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
        if new_order_single.get_parameter('TargetStrategy') != '1008' and new_order_single.get_parameter('TargetStrategy') != '1011':
            temp.update(LastMkt='*')
        if new_order_single.get_parameter('TargetStrategy') == '1010' or (new_order_single.is_parameter_exist('ClientAlgoPolicyID') and new_order_single.get_parameter('ClientAlgoPolicyID') in ['QA_Auto_SORPING_ME_Y', 'QA_Auto_SORPING_ME_N']):
            temp.update(
                NoParty='*',
                SecondaryAlgoPolicyID='*'
            )
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID=new_order_single.get_parameter('ClOrdID'),
            CumQty='*',
            Currency=new_order_single.get_parameter('Currency'),
            ExecID='*',
            HandlInst=new_order_single.get_parameter('HandlInst'),
            LastPx=0,
            LastQty=0,
            OrderID='*',
            OrderQty=new_order_single.get_parameter('OrderQty'),
            OrdStatus=4,
            OrdType=new_order_single.get_parameter('OrdType'),
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
            CxlQty='*',
            Instrument='*',
        )
        super().change_parameters(temp)
        return self

    def __set_eliminate_dma(self, new_order_single: FixMessageNewOrderSingle = None):
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
            Side=new_order_single.get_parameter('Side'),
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            TransactTime='*',
            SettlDate='*',
            ExecType=4,
            LeavesQty=0,
            ExecRestatementReason='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            QtyType='*',
            CxlQty=new_order_single.get_parameter('OrderQty'),
            Instrument='*',
        )
        super().change_parameters(temp)
        return self

    def set_RFQ_accept_params_new(self, nos_rfq: FixMessageNewOrderSingle):
        temp = {
            "Account": nos_rfq.get_parameter("Account"),
            "AvgPx": 0,
            "ClOrdID": "*",
            "CumQty": 0,
            "Currency": nos_rfq.get_parameter("Currency"),
            "ExecID": "*",
            "ExecInst": "uncrossing-only",
            "LastPx": 0,
            "LastQty": 0,
            "OrderID": "*",
            "OrderQty": nos_rfq.get_parameter("OrderQty"),
            "OrdStatus": 0,
            "OrdType": "P",
            "Side": nos_rfq.get_parameter("Side"),
            "TimeInForce": nos_rfq.get_parameter("TimeInForce"),
            "TransactTime": "*",
            "ExDestination": nos_rfq.get_parameter("ExDestination"),
            "ExecType": 0,
            "LeavesQty": nos_rfq.get_parameter("OrderQty"),
            "SecondaryOrderID": "*",
            "OrderCapacity": "A",
            "AccountType": "1",
            "ApplID": "1",
            "AlgoCst01": "ioi",
            "ShortCode": "14519",
            "CustomKeplerTag": "14519",
            "Instrument": "*",
            "NoParty": "*",
        }
        if nos_rfq.is_parameter_exist('Price'):
            temp.update(Price=nos_rfq.get_parameter('Price'))
        super().change_parameters(temp)
        return self

    def set_RFQ_accept_params_restated(self, er_rfq_new: FixMessageExecutionReport):
        temp = er_rfq_new.get_parameters()
        temp.update({
            "AlgoCst04": "invited",
            "ExecType": "D",
            "AlgoCst03": "VenueQuoteID_O04r2TeUXbzb",
            "ExecRestatementReason": "1",
            "QuoteType": "1",
            "LastMkt": er_rfq_new.get_parameter("ExDestination"),
        })
        super().change_parameters(temp)
        return self

    def set_RFQ_cancel_accepted(self, nos_rfq: FixMessageNewOrderSingle):
        temp = {
            "AvgPx": 0,
            "ClOrdID": "*",
            "CumQty": 0,
            "ExecID": "*",
            "LastMkt": "*",
            "LastPx": 0,
            "LastQty": 0,
            "OrderID": "*",
            "OrdStatus": 4,
            "OrdType": "P",
            "Side": nos_rfq.get_parameter("Side"),
            "TransactTime": "*",
            "ExDestination": nos_rfq.get_parameter("ExDestination"),
            "ExecType": 4,
            "LeavesQty": 1000000, # value hard-coded at th2-sim
            "OrderCapacity": "A",
            "ApplID": "1",
            "AlgoCst01": "ioi",
            "ShortCode": "18831",
            "CustomKeplerTag": "18831",
            "IClOrdIdTO": "*",
            "ChildOrderID": "*",
            "OrigClOrdID": "*",
        }
        super().change_parameters(temp)
        return self

    def set_params_full_fill_MPDark(self, MP_Dark_order: FixMessageNewOrderSingle):
        temp = {
            "Account": MP_Dark_order.get_parameter("Account"),
            "AvgPx": MP_Dark_order.get_parameter("Price"),
            "ClOrdID": "*",
            "CumQty": MP_Dark_order.get_parameter("OrderQty"),
            "Currency": MP_Dark_order.get_parameter("Currency"),
            "ExecID": "*",
            "LastPx": MP_Dark_order.get_parameter("Price"),
            "LastQty": MP_Dark_order.get_parameter("OrderQty"),
            "OrderID": "*",
            "OrdStatus": 2,
            "OrderQty": MP_Dark_order.get_parameter("OrderQty"),
            "OrdType": MP_Dark_order.get_parameter("OrdType"),
            "Side": MP_Dark_order.get_parameter("Side"),
            "Price": MP_Dark_order.get_parameter("Price"),
            "TransactTime": "*",
            "Text": "*",
            "ExDestination": "*",
            "TimeInForce": MP_Dark_order.get_parameter("TimeInForce"),
            "ExecType": "F",
            "LeavesQty": 0,
            "Instrument": "*",
            "OrderCapacity": "A",
            "ShortCode": "*",
            "SecondaryOrderID": "*",
            "LastMkt": "*",
            "QtyType": 0,
            "ChildOrderID": "*",
            "TargetStrategy": MP_Dark_order.get_parameter("TargetStrategy"),
            "SecondaryAlgoPolicyID": "*",
            "SettlDate": "*",
            "TradeDate": "*",
            "NoParty": "*",
            "HandlInst": 2,
            "LastExecutionPolicy": "*",
            "IClOrdIdAO": "*",
            "GrossTradeAmt": "*",
            "SecondaryExecID": "*",
        }
        super().change_parameters(temp)
        return self

    def __set_reject_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if str(new_order_single.get_parameter('OrdType')) == '2':
            temp.update(Price = new_order_single.get_parameter("Price"))
        if new_order_single.is_parameter_exist("NoStrategyParameters") or new_order_single.get_parameter('TargetStrategy') == '1008':
            temp.update(NoStrategyParameters='*')
        if new_order_single.get_parameter('Account') == 'KEPLER':
            temp.update(
                Account='*',
                SecondaryAlgoPolicyID='*',
                SettlDate='*',
                Currency='*',
                HandlInst='*',
                NoParty='*',
                LastPx='*',
                OrderCapacity='*',
                QtyType='*',
                ExecRestatementReason='*',
                TargetStrategy='*',
                Instrument='*',
                LastQty='*',
                Text='*'
            )
        if new_order_single.is_parameter_exist('ExDestination'):
            temp.update(ExDestination=new_order_single.get_parameter('ExDestination'))
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty=new_order_single.get_parameter('MinQty'))
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
            TransactTime='*',
            ExecType=8,
            LeavesQty=0
        )
        super().change_parameters(temp)
        return self

    def __set_reject_dma(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if str(new_order_single.get_parameter('OrdType')) == '2':
            temp.update(Price = new_order_single.get_parameter("Price"))
        if new_order_single.is_parameter_exist('ExDestination'):
            temp.update(ExDestination=new_order_single.get_parameter('ExDestination'))
        if new_order_single.is_parameter_exist('MinQty'):
            temp.update(MinQty=new_order_single.get_parameter('MinQty'))
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

    def set_MPDArk_LIST_child_par_fill(self, nos_lis_order):
        temp = {
            "Account": nos_lis_order.get_parameter("Account"),
            "AvgPx": nos_lis_order.get_parameter("Price"),
            "ClOrdID": "*",
            "CumQty": "*",
            "Currency": nos_lis_order.get_parameter("Currency"),
            "ExecID": "*",
            "LastPx": nos_lis_order.get_parameter("Price"),
            "LastQty": "*",
            "OrderID": "*",
            "OrdStatus": 1,
            "OrderQty": nos_lis_order.get_parameter("OrderQty"),
            "OrdType": nos_lis_order.get_parameter("OrdType"),
            "Side": nos_lis_order.get_parameter("Side"),
            "Price": nos_lis_order.get_parameter("Price"),
            "TransactTime": "*",
            "Text": "*",
            "ExDestination": "*",
            "TimeInForce": nos_lis_order.get_parameter("TimeInForce"),
            "ExecType": "F",
            "LeavesQty": "*",
            "Instrument": "*",
            "OrderCapacity": "A",
        }
        super().change_parameters(temp)
        return self

    def set_RFQ_reject_params(self, nos_rfq: FixMessageNewOrderSingle):
        temp = {
            "Account": nos_rfq.get_parameter("Account"),
            "AvgPx": 0,
            "ClOrdID": "*",
            "CumQty": 0,
            "Currency": nos_rfq.get_parameter("Currency"),
            "ExecID": "*",
            "ExecInst": "uncrossing-only",
            "LastPx": 0,
            "LastQty": 0,
            "OrderID": "*",
            "OrderQty": nos_rfq.get_parameter("OrderQty"),
            "OrdStatus": 8,
            "OrdType": "P",
            "Side": nos_rfq.get_parameter("Side"),
            "TimeInForce": nos_rfq.get_parameter("TimeInForce"),
            "TransactTime": "*",
            "ExDestination": nos_rfq.get_parameter("ExDestination"),
            "ExecType": 8,
            "LeavesQty": 0,
            "SecondaryOrderID": "*",
            "OrderCapacity": "A",
            "AccountType": "1",
            "AlgoCst01": "ioi",
            "ShortCode": "14519",
            "CustomKeplerTag": "14519",
            "NoParty": "*",
            "OrdRejReason": "*",
            "Text": "*",
            "AlgoCst04": 'invited'

        }
        if nos_rfq.is_parameter_exist('Price'):
            temp.update(Price=nos_rfq.get_parameter('Price'))
        super().change_parameters(temp)
        return self

    def __set_pending_new_rb_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') != 1 and new_order_single.get_parameter('OrdType') != 3:
            temp.update(Price=new_order_single.get_parameter("Price"))
        temp.update(
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
            NoStrategyParameters='*',
            NoParty='*',
            SecAltIDGrp='*'
        )
        super().change_parameters(temp)
        return self

    def __set_new_rb_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') != 1 and new_order_single.get_parameter('OrdType') != 3:
            temp.update(Price=new_order_single.get_parameter("Price"))
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
            NoStrategyParameters='*',
            NoParty='*',
            SecAltIDGrp='*'
        )
        super().change_parameters(temp)
        return self

    def __set_cancel_rb_sell(self, new_order_single: FixMessageNewOrderSingle = None):
        temp = dict()
        if new_order_single.get_parameter('OrdType') != 1 and new_order_single.get_parameter('OrdType') != 3:
            temp.update(Price=new_order_single.get_parameter("Price"))
        temp.update(
            Account=new_order_single.get_parameter('Account'),
            AvgPx='*',
            ClOrdID='*',
            CumQty='*',
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
            TimeInForce=new_order_single.get_parameter('TimeInForce'),
            TransactTime='*',
            SettlDate='*',
            ExecType=4,
            LeavesQty=0,
            ExecRestatementReason='*',
            OrderCapacity=new_order_single.get_parameter('OrderCapacity'),
            TargetStrategy=new_order_single.get_parameter('TargetStrategy'),
            QtyType='*',
            Instrument='*',
            NoStrategyParameters='*',
            NoParty='*',
            SecAltIDGrp='*'
        )
        super().change_parameters(temp)
        return self

    def __set_cancel_rep_fill_sell(self, order_cancel_replace: FixMessageOrderCancelReplaceRequest = None):
        temp = dict()
        if str(order_cancel_replace.get_parameter('OrdType')) == '2':
            temp.update(Price = order_cancel_replace.get_parameter("Price"))
        if 'DisplayInstruction' in order_cancel_replace.get_parameters():
            temp.update(DisplayInstruction=order_cancel_replace.get_parameter('DisplayInstruction'))
        if order_cancel_replace.get_parameter('TargetStrategy') not in ['1008', '1011', '1010']:
            temp.update(LastMkt=order_cancel_replace.get_parameter('ExDestination'))
        if order_cancel_replace.get_parameter('TargetStrategy') != '1010':
            temp.update(
                SecAltIDGrp='*',
                SecondaryClOrdID='*',
            )
        if order_cancel_replace.get_parameter('TargetStrategy') == '1010':
            temp.update(
                LastMkt='*',
                ChildOrderID='*',
            )
        if order_cancel_replace.get_parameter('TargetStrategy') == '1011' or order_cancel_replace.get_parameter('TargetStrategy') == '1004':
            temp.update(
                ExDestination='*',
                LastMkt='*',
                ChildOrderID='*'
            )
        if order_cancel_replace.is_parameter_exist('ClientAlgoPolicyID') or order_cancel_replace.get_parameter('TargetStrategy') == '1004':
            temp.update(
                IClOrdIdAO='*',
                SecondaryAlgoPolicyID='*',
                LastExecutionPolicy='*',
                ShortCode='*',
                ExDestination='*'
            )
        if order_cancel_replace.is_parameter_exist('IClOrdIdCO'):
            temp.update(IClOrdIdCO=order_cancel_replace.get_parameter('IClOrdIdCO'))
        if order_cancel_replace.get_parameter('TargetStrategy') == '1008':
            if order_cancel_replace.is_parameter_exist('MinQty'):
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
        if order_cancel_replace.is_parameter_exist('NoStrategyParameters') or ('ClientAlgoPolicyID' not in order_cancel_replace.get_parameters() and order_cancel_replace.get_parameter('TargetStrategy') != '1004'):
            temp.update(NoStrategyParameters='*')
        if 'ClientAlgoPolicyID' not in order_cancel_replace.get_parameters() and order_cancel_replace.get_parameter('TargetStrategy') == '1011':
            temp.update(
                SecondaryAlgoPolicyID='*',
                LastExecutionPolicy='*'
            )
        if order_cancel_replace.is_parameter_exist('MinQty'):
            temp.update(MinQty='*')
        if order_cancel_replace.get_parameter('TimeInForce') == '6':
            temp.update(ExpireDate=order_cancel_replace.get_parameter('ExpireDate'))
        if order_cancel_replace.is_parameter_exist('TargetStrategy'):
            temp.update(TargetStrategy='*')
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
            OrdStatus=2,
            OrdType=order_cancel_replace.get_parameter('OrdType'),
            Side=order_cancel_replace.get_parameter('Side'),
            Text='*',
            TimeInForce=order_cancel_replace.get_parameter('TimeInForce'),
            TransactTime='*',
            SettlDate='*',
            TradeDate='*',
            ExecType='F',
            LeavesQty=0,
            SecondaryOrderID='*',
            GrossTradeAmt='*',
            NoParty='*',
            OrderCapacity=order_cancel_replace.get_parameter('OrderCapacity'),
            QtyType=0,
            Instrument='*',
            SecondaryExecID='*',
            SettlType='*'
        )
        if order_cancel_replace.get_parameter('TargetStrategy') in ['1008', '1011', '1004']:
            [temp.pop(key, None) for key in ['SecAltIDGrp', 'SecondaryClOrdID']]
        super().change_parameters(temp)
        return self

    def __set_cancel_rep_partial_fill_sell(self, order_cancel_replace: FixMessageOrderCancelReplaceRequest = None):
        temp = dict()
        if str(order_cancel_replace.get_parameter('OrdType')) == '2':
            temp.update(Price = order_cancel_replace.get_parameter("Price"))
        if 'DisplayInstruction' in order_cancel_replace.get_parameters():
            temp.update(DisplayInstruction=order_cancel_replace.get_parameter('DisplayInstruction'))
        if order_cancel_replace.get_parameter('TargetStrategy') in ['1011', '1010'] and order_cancel_replace.is_parameter_exist('ClientAlgoPolicyID'):
            temp.update(
                IClOrdIdAO='*',
                ShortCode='*'
            )
        if order_cancel_replace.get_parameter('TargetStrategy') == '1008':
            if order_cancel_replace.is_parameter_exist('MinQty'):
                temp.update(
                    LastExecutionPolicy='*',
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
                    ExDestination='*'
                )
        if order_cancel_replace.get_parameter('TargetStrategy') in ['1011', '1010']:
            temp.update(
                SecondaryAlgoPolicyID='*',
                LastExecutionPolicy='*',
                ExDestination='*',
                ChildOrderID='*'
            )
        if order_cancel_replace.is_parameter_exist('NoStrategyParameters') or (order_cancel_replace.get_parameter('TargetStrategy') == '1008' and order_cancel_replace.is_parameter_exist('MinQty')):
            temp.update(NoStrategyParameters='*')
        if order_cancel_replace.is_parameter_exist('MinQty'):
            temp.update(MinQty='*')
        if order_cancel_replace.is_parameter_exist('TargetStrategy'):
            temp.update(TargetStrategy='*')
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
            OrdStatus=1,
            OrdType=order_cancel_replace.get_parameter('OrdType'),
            Side=order_cancel_replace.get_parameter('Side'),
            Text='*',
            TimeInForce=order_cancel_replace.get_parameter('TimeInForce'),
            TransactTime='*',
            SettlDate='*',
            LastMkt='*',
            TradeDate='*',
            ExecType='F',
            LeavesQty='*',
            SecondaryOrderID='*',
            GrossTradeAmt='*',
            NoParty='*',
            OrderCapacity=order_cancel_replace.get_parameter('OrderCapacity'),
            SecAltIDGrp='*',
            QtyType=0,
            SecondaryClOrdID='*',
            Instrument='*',
            SecondaryExecID='*',
            SettlType='*'
        )
        if order_cancel_replace.get_parameter('TargetStrategy') in ['1008', '1011', '1010']:
            [temp.pop(key, None) for key in ['SecAltIDGrp', 'SecondaryClOrdID']]
        super().change_parameters(temp)
        return self
