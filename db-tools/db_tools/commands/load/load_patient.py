from typing import Dict

from db_tools.database import Patient
from .tools import safe_get_value, BaseProcess, ConvertException, safe_get_date


class PatientProcess(BaseProcess):
    _model = Patient
    race_url = "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race"
    ethnicity_url = "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity"
    _result_template = {
        'gender_stat': {}
    }

    def process_stat(self, entity: Dict):
        super().process_stat(entity)
        self._result['gender_stat'][entity['gender']] = self._result['gender_stat'].get(entity['gender'], 0) + 1

    def print_result(self):
        super().print_result()
        for gender, amount in self._result['gender_stat'].items():
            print(f"There are {amount} '{gender}'")

    def entry_convert(self, raw_entry: Dict) -> Dict:

        # find race
        race = filter(lambda x: x.get('url', '') == self.race_url,
                      safe_get_value(raw_entry, 'extension', default=[]))
        race = next(race, None)

        # find ethnicity
        ethnicity = filter(lambda x: x.get('url', '') == self.ethnicity_url,
                           safe_get_value(raw_entry, 'extension', default=[]))
        ethnicity = next(ethnicity, None)

        if 'id' not in raw_entry:
            raise ConvertException("There is no required 'id' field in provided entry.")

        yield dict(
            source_id=raw_entry['id'],
            birth_date=safe_get_date(raw_entry, 'birthDate'),
            gender=safe_get_value(raw_entry, 'gender'),
            country=safe_get_value(raw_entry, 'address', 0, 'country'),
            race_code=safe_get_value(race, 'valueCodeableConcept', 'coding', 0, 'code'),
            race_code_system=safe_get_value(race, 'valueCodeableConcept', 'coding', 0, 'system'),
            ethnicity_code=safe_get_value(ethnicity, 'valueCodeableConcept', 'coding', 0, 'code'),
            ethnicity_code_system=safe_get_value(ethnicity, 'valueCodeableConcept', 'coding', 0, 'system'),
        )
