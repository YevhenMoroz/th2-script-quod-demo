import datetime
from copy import deepcopy
from enum import Enum
from typing import Dict, Union

from test_framework.data_sets.constants import TradingPhases


class TimeSlot(Enum):
    current_phase = "current_phase"
    previous_phase = "previous_phase"
    next_phase = "next_phase"


class PhaseTime:
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

    def get_phase_datetime(self, new_standart: bool = False) -> Dict[str, Union[str, datetime.datetime]]:
        final_result = dict()
        if not new_standart:
            final_result["beginTime"] = self.start_time
            final_result["endTime"] = self.end_time
            final_result["submitAllowed"] = "True"
        else:
            final_result["phaseBeginTime"] = self.start_time.strftime("%H:%M:%S")
            final_result["phaseEndTime"] = self.end_time.strftime("%H:%M:%S")

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


class TradingPhaseManager:
    def init(self):
        self._trading_phase_sequence = list()
        super().init()

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

    # region get_phases
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
        elif phase == TradingPhases.Closed:
            return None
        else:
            raise ValueError(f"Method get_next_phase can't handle phase {phase.value} ")

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
        else:
            raise ValueError(f"Method get_previous_phase can't handle phase {phase.value} ")
    # endregion

    # region build timestamp
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

    def build_timestamps_for_trading_phase_sequence(self, phase: TradingPhases, time_slot: TimeSlot = TimeSlot.current_phase, duration=5):
            self.clean_phase()
            tm = datetime.datetime.utcnow()
            tm = tm - datetime.timedelta(seconds=tm.second, microseconds=tm.microsecond)
            if time_slot == TimeSlot.current_phase:
                current_phase = PhaseTime(
                    start_time=tm,
                    end_time=tm + datetime.timedelta(minutes=duration),
                    phase=phase
                )
            elif time_slot == TimeSlot.next_phase:
                current_phase = PhaseTime(
                    start_time=tm,
                    end_time=tm + datetime.timedelta(minutes=2),
                    phase=TradingPhaseManager.get_next_phase(phase)
                )
            else:
                raise ValueError("Action at method build_timestamps_for_trading_phase_sequence for previous phase not developed yet")
            self.add_phase(current_phase)
            self.autocomplete_next_phases(current_phase, duration)
            self.autocomplete_previous_phases(current_phase, duration)
        # endregion timestamp

    # region autocomplete phases
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
    # endregion

    def get_trading_phase_list(self, new_standard: bool = False):
        final_result = list()
        for a in self.trading_phase_sequence:
            final_result.append(a.get_phase_datetime(new_standart=new_standard))
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
trading_phase_manager = TradingPhaseManager()
# trading_phase_manager.build_default_timestamp_for_trading_phase()
trading_phase_manager.build_timestamps_for_trading_phase_sequence(TradingPhases.PreClosed, TimeSlot.next_phase, 10)
# trading_phase_manager.update_endtime_for_trading_phase_by_phase_name(TradingPhases.PreOpen, 25)

trading_phase_list = trading_phase_manager.get_trading_phase_list(new_standard=True)
print()