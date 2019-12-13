import calendar
from typing import Dict
from collections import namedtuple

from db_tools.database import Encounter
from .tools import safe_get_value, safe_get_date, BaseProcess, ConvertException

day_stat = namedtuple('day_stat', ['day', 'visit_amount'])


class EncounterProcess(BaseProcess):
    _model = Encounter

    _result_template = {
        'days_visit': {i: 0 for i in range(7)}
    }

    def process_stat(self, entity: Dict):
        super().process_stat(entity)
        for i in range(entity['start_date'].weekday(), entity['end_date'].weekday() + 1):
            self._result['days_visit'][i] += 1

    def print_result(self):
        super().print_result()
        most_popular: day_stat = None
        least_popular: day_stat = None
        for day, visit_amount in self._result['days_visit'].items():

            if most_popular is None or most_popular.visit_amount < visit_amount:
                most_popular = day_stat(day, visit_amount)

            if least_popular is None or least_popular.visit_amount > visit_amount:
                least_popular = day_stat(day, visit_amount)

        print(f"The most popular day is {calendar.day_name[most_popular.day]}")
        print(f"The least popular day is {calendar.day_name[least_popular.day]}")

    def entry_convert(self, raw_entry: Dict) -> Dict:
        if 'id' not in raw_entry or not raw_entry['id']:
            raise ConvertException("There is no required 'id' field in provided entry.")

        patient_source_id = safe_get_value(raw_entry, 'subject', 'reference')[8:]
        if patient_source_id not in self._context['patient_mapping']:
            raise ConvertException(f"The patient with source_id={patient_source_id} does not exist.")

        start_date = safe_get_date(raw_entry, 'period', 'start')
        if start_date is None:
            raise ConvertException(f"Not valid start_date")

        end_date = safe_get_date(raw_entry, 'period', 'end')
        if end_date is None:
            raise ConvertException(f"Not valid end_date")

        yield dict(
            source_id=raw_entry['id'],
            patient_id=self._context['patient_mapping'][patient_source_id],
            start_date=start_date,
            end_date=end_date,
            type_code=safe_get_value(raw_entry, 'type', 0, 'coding', 0, 'code'),
            type_code_system=safe_get_value(raw_entry, 'type', 0, 'coding', 0, 'system')
        )
