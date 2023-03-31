import datetime
from copy import deepcopy
from typing import Dict, Union

from test_framework.data_sets.constants import TradingPhases





class PhaseTime():
    def __init__(self, start_time: datetime.datetime, end_time: Union[int, datetime.datetime], phase: TradingPhases):
        """

        """
        self._start_time = start_time
        if type(end_time) == datetime.datetime:
            self._end_time = end_time
            self._duration = int((end_time - start_time).total_seconds() / 60)
        elif type(end_time) == int:
            self._end_time = self.start_time + datetime.timedelta(minutes=end_time)
            self._duration = end_time
        self._trading_phase = phase

    # region start_time getter/setter
    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value
    # endregion

    # region end_time getter/setter
    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        self._end_time = value
    # endregion

    # region trading_phase getter/setter
    @property
    def trading_phase(self):
        return self._trading_phase

    @trading_phase.setter
    def trading_phase(self, value: TradingPhases):
        self._trading_phase = value
    # endregion

    # region duration getter/setter
    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value
    # endregion

    def get_phase_datetime(self) -> Dict[str, Union[str, datetime.datetime]]:
        final_result = dict()
        final_result["beginTime"] = self.start_time
        final_result["endTime"] = self.end_time
        final_result["submitAllowed"] = "True"
        final_result["submitAllowed"] = "True"


        if self.trading_phase == TradingPhases.Open:
            final_result["tradingPhase"] = "OPN"
            final_result["standardTradingPhase"] = "OPN"
        elif self.trading_phase == TradingPhases.PreOpen:
            final_result["tradingPhase"] = "POP"
            final_result["standardTradingPhase"] = "PRE"
        elif self.trading_phase == TradingPhases.PreClosed:
            final_result["tradingPhase"] = "PCL"
            final_result["standardTradingPhase"] = "PCL"
        elif self.trading_phase == TradingPhases.AtLast:
            final_result["tradingPhase"] = "TAL"
            final_result["standardTradingPhase"] = "TAL"
        elif self.trading_phase == TradingPhases.Closed:
            final_result["tradingPhase"] = "CLO"
            final_result["standardTradingPhase"] = "CLO"
        elif self.trading_phase == TradingPhases.Expiry:
            final_result["tradingPhase"] = "EXA"
            final_result["standardTradingPhase"] = "EXA"
            final_result["expiryCycle"] = "EVM"
        return final_result

    def get_phase_time(self):
        #TODO
        raise ValueError("Not Done")


class TradingPhaseManager():
    def __init__(self):
        self._trading_phase_sequence = list()
        super().__init__()

    # region trading_phase_sequence getter/setter
    @property
    def trading_phase_sequence(self):
        return self._trading_phase_sequence

    @trading_phase_sequence.setter
    def trading_phase_sequence(self, value):
        self._trading_phase_sequence = value

    # endregion

    def add_phase(self, phase: PhaseTime):
        self.trading_phase_sequence.append(phase)

    def clean_phase(self):
        self.trading_phase_sequence = list()

    def build_default_timestamp_for_trading_phase(self):
        self.clean_phase()
        tm = datetime.datetime.now()
        self.add_phase(PhaseTime(
            start_time=datetime.datetime(year=tm.year, month=tm.month, day=tm.day, hour=6, minute=50, second=0, microsecond=0).replace(tzinfo=datetime.timezone.utc),
            end_time=datetime.datetime(year=tm.year, month=tm.month, day=tm.day, hour=7, minute=0, second=0, microsecond=0).replace(tzinfo=datetime.timezone.utc),
            phase=TradingPhases.PreOpen
        ))
        self.add_phase(PhaseTime(
            start_time=datetime.datetime(year=tm.year, month=tm.month, day=tm.day, hour=7, minute=0, second=0, microsecond=0).replace(tzinfo=datetime.timezone.utc),
            end_time=datetime.datetime(year=tm.year, month=tm.month, day=tm.day, hour=19, minute=0, second=0, microsecond=0).replace(tzinfo=datetime.timezone.utc),
            phase=TradingPhases.Open
        ))
        self.add_phase(PhaseTime(
            start_time=datetime.datetime(year=tm.year, month=tm.month, day=tm.day, hour=19, minute=0, second=0, microsecond=0).replace(tzinfo=datetime.timezone.utc),
            end_time=datetime.datetime(year=tm.year, month=tm.month, day=tm.day, hour=19, minute=10, second=0, microsecond=0).replace(tzinfo=datetime.timezone.utc),
            phase=TradingPhases.PreClosed
        ))
        self.add_phase(PhaseTime(
            start_time=datetime.datetime(year=tm.year, month=tm.month, day=tm.day, hour=19, minute=10, second=0, microsecond=0).replace(tzinfo=datetime.timezone.utc),
            end_time=datetime.datetime(year=tm.year, month=tm.month, day=tm.day, hour=19, minute=20, second=0, microsecond=0).replace(tzinfo=datetime.timezone.utc),
            phase=TradingPhases.AtLast
        ))
        self.add_phase(PhaseTime(
            start_time=datetime.datetime(year=tm.year, month=tm.month, day=tm.day, hour=19, minute=20, second=0, microsecond=0).replace(tzinfo=datetime.timezone.utc),
            end_time=datetime.datetime(year=tm.year, month=tm.month, day=tm.day, hour=23, minute=59, second=0, microsecond=0).replace(tzinfo=datetime.timezone.utc),
            phase=TradingPhases.Closed
        ))
        self.add_phase(PhaseTime(
            start_time=datetime.datetime(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=10, second=0, microsecond=0).replace(tzinfo=datetime.timezone.utc),
            end_time=datetime.datetime(year=tm.year, month=tm.month, day=tm.day, hour=10, minute=15, second=0, microsecond=0).replace(tzinfo=datetime.timezone.utc),
            phase=TradingPhases.Expiry
        ))

    @staticmethod
    def get_next_phase(phase: TradingPhases):
        if phase == TradingPhases.PreOpen:
            return TradingPhases.Open
        elif phase == TradingPhases.Open:
            return TradingPhases.PreClosed
        elif phase == TradingPhases.PreClosed:
            return TradingPhases.AtLast
        elif phase == TradingPhases.AtLast:
            return TradingPhases.Closed
        elif phase == TradingPhases.Closed.value:
            return None

    @staticmethod
    def get_previous_phase(phase: TradingPhases):
        if phase == TradingPhases.PreOpen:
            return None
        elif phase == TradingPhases.Open:
            return TradingPhases.PreOpen
        elif phase == TradingPhases.PreClosed:
            return TradingPhases.Open
        elif phase == TradingPhases.AtLast:
            return TradingPhases.PreClosed
        elif phase == TradingPhases.Closed:
            return TradingPhases.AtLast

    def build_timestamps_for_trading_phase_sequence(self, phase: TradingPhases, time_slot, duration=5):
        self.clean_phase()
        tm = datetime.datetime.now()
        tm = tm - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond)
        current_phase = PhaseTime(
            start_time=tm,
            end_time=tm + datetime.timedelta(minutes=duration),
            phase=phase
        )
        self.add_phase(current_phase)
        self.autocomplete_next_phases(current_phase, duration)
        self.autocomplete_previous_phases(current_phase, duration)

    def autocomplete_next_phases(self, start_phase: PhaseTime, duration):
        phase = start_phase.trading_phase
        current_phase = deepcopy(start_phase)
        while phase != None:
            phase = TradingPhaseManager.get_next_phase(phase)
            if phase != None:
                current_phase = PhaseTime(
                    start_time=current_phase.end_time,
                    end_time=current_phase.end_time + datetime.timedelta(minutes=duration),
                    phase=phase
                )
                self.add_phase(current_phase)

    def autocomplete_previous_phases(self, start_phase: PhaseTime, duration):
        phase = start_phase.trading_phase
        current_phase = deepcopy(start_phase)
        while phase != None:
            phase = TradingPhaseManager.get_previous_phase(phase)
            if phase != None:
                current_phase = PhaseTime(
                    start_time=current_phase.start_time - datetime.timedelta(minutes=duration),
                    end_time=current_phase.start_time,
                    phase=phase
                )
                self.add_phase(current_phase)

    def get_trading_phase_list(self):
        final_result = list()
        for a in self.trading_phase_sequence:
            final_result.append(a.get_phase_datetime())
        return final_result

    def get_phase_time_by_phase(self, phase: TradingPhases) -> PhaseTime:
        for phase_in_list in self.trading_phase_sequence:
            if phase_in_list.trading_phase == phase:
                return phase_in_list

    def update_endtime_for_trading_phase_by_phase_name(self, phase: TradingPhases, end_time: Union[int, datetime.datetime]):
        current_phase = self.get_phase_time_by_phase(phase)
        if type(end_time) == datetime.datetime:
            current_phase.end_time = end_time
            current_phase.duration = int((current_phase.end_time - current_phase.start_time).total_seconds() / 60)
        elif type(end_time) == int:
            current_phase.end_time = current_phase.start_time + datetime.timedelta(minutes=end_time)
            current_phase.duration = end_time

        self.fix_time_parameters(current_phase)

    def fix_time_parameters(self, phase: PhaseTime):
        start_phase = deepcopy(phase)
        previous_phase = start_phase
        current_phase = self.get_phase_time_by_phase(TradingPhaseManager.get_next_phase(start_phase.trading_phase))

        # next phases
        while current_phase != None:
            current_phase.start_time = previous_phase.end_time
            current_phase.end_time = current_phase.start_time + datetime.timedelta(minutes=current_phase.duration)

            previous_phase = current_phase
            current_phase = self.get_phase_time_by_phase(TradingPhaseManager.get_next_phase(current_phase.trading_phase))

        # previous phases
        current_phase = self.get_phase_time_by_phase(TradingPhaseManager.get_previous_phase(start_phase.trading_phase))
        while current_phase != None:
            current_phase.end_time = previous_phase.start_time
            current_phase.start_time = current_phase.end_time - datetime.timedelta(minutes=current_phase.duration)

            previous_phase = current_phase
            current_phase = self.get_phase_time_by_phase(TradingPhaseManager.get_previous_phase(current_phase.trading_phase))


# #Example of usage
# trading_phase_manager = TradingPhaseManager()
# trading_phase_manager.build_default_timestamp_for_trading_phase()
# trading_phase_manager.build_timestamps_for_trading_phase_sequence(TradingPhases.PreOpen, None, 5)
# trading_phase_manager.update_endtime_for_trading_phase_by_phase_name(TradingPhases.PreOpen, 25)
# trading_phase_list = trading_phase_manager.get_trading_phase_list()
