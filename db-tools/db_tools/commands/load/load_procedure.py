from typing import Dict

from db_tools.database import Procedure
from .tools import safe_get_value, safe_get_date, BaseProcess, ConvertException


class ProcedureProcess(BaseProcess):
    _model = Procedure

    _result_template = {
        'types_popularity': {}
    }

    def process_stat(self, entity: Dict):
        super().process_stat(entity)
        type_code = entity['type_code']
        self._result['types_popularity'][type_code] = self._result['types_popularity'].get(type_code, 0) + 1

    def print_result(self):
        super().print_result()
        print('Most popular procedures is:')
        for num, t in enumerate(sorted(self._result['types_popularity'].items(),
                                       key=lambda item: item[1],
                                       reverse=True)):
            print(f"{t[0]}: {t[1]}")
            if num == 9:
                break

    def entry_convert(self, raw_entry: Dict) -> Dict:
        if 'id' not in raw_entry or not raw_entry['id']:
            raise ConvertException("There is no required 'id' field in provided entry.")

        patient_source_id = safe_get_value(raw_entry, 'subject', 'reference')[8:]
        if patient_source_id not in self._context['patient_mapping']:
            raise ConvertException(f"The patient with source_id={patient_source_id} does not exist.")

        procedure_date = safe_get_date(raw_entry, 'performedDateTime')
        procedure_date = procedure_date or safe_get_date(raw_entry, 'performedPeriod', 'start')
        if procedure_date is None:
            raise ConvertException(f"Could not find the procedure_date")

        type_code = safe_get_value(raw_entry, 'code', 'coding', 0, 'code')
        if type_code is None:
            raise ConvertException(f"Could not find the type_code in procedure.")

        type_code_system = safe_get_value(raw_entry, 'code', 'coding', 0, 'system')
        if type_code_system is None:
            raise ConvertException(f"Could not find the type_code_system in procedure.")

        encounter_source_id = safe_get_value(raw_entry, 'context', 'reference', default='')[10:]

        yield dict(
            source_id=raw_entry['id'],
            patient_id=self._context['patient_mapping'][patient_source_id],
            encounter_id=self._context['encounter_mapping'].get(encounter_source_id),

            procedure_date=procedure_date,

            type_code=type_code,
            type_code_system=type_code_system
        )
