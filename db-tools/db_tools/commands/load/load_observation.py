from typing import Dict

from db_tools.database import Observation
from .tools import safe_get_value, safe_get_date, BaseProcess, ConvertException


class ObservationProcess(BaseProcess):
    _model = Observation

    _result_template = {
    }

    def process_stat(self, entity: Dict):
        super().process_stat(entity)

    def print_result(self):
        super().print_result()

    def entry_convert(self, raw_entry: Dict) -> Dict:
        if 'id' not in raw_entry or not raw_entry['id']:
            raise ConvertException("There is no required 'id' field in provided entry.")

        patient_source_id = safe_get_value(raw_entry, 'subject', 'reference')[8:]
        if patient_source_id not in self._context['patient_mapping']:
            raise ConvertException(f"The patient with source_id={patient_source_id} does not exist.")

        observation_date = safe_get_date(raw_entry, 'effectiveDateTime')
        if observation_date is None:
            raise ConvertException(f"Could not find the observation_date")

        encounter_source_id = safe_get_value(raw_entry, 'context', 'reference', default='')[10:]

        components = raw_entry.get('components')
        if components is None:
            components = [raw_entry]

        for component in components:

            type_code = safe_get_value(component, 'code', 'coding', 0, 'code')
            type_code_system = safe_get_value(component, 'code', 'coding', 0, 'system')
            value = safe_get_value(component, 'valueQuantity', 'value')

            if not all((type_code, type_code_system, value)):
                self._result['records_amount'] += 1
                continue

            yield dict(
                source_id=raw_entry['id'],
                patient_id=self._context['patient_mapping'][patient_source_id],
                encounter_id=self._context['encounter_mapping'].get(encounter_source_id),

                observation_date=observation_date,

                type_code=type_code,
                type_code_system=type_code_system,
                value=value,
                unit_code=safe_get_value(component, 'valueQuantity', 'unit'),
                unit_code_system=safe_get_value(component, 'valueQuantity', 'system'),
            )
