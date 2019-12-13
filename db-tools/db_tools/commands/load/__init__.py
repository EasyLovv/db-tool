from pathlib import Path

import click

from .load_encounter import EncounterProcess
from .load_patient import PatientProcess
from .load_procedure import ProcedureProcess
from .load_observation import ObservationProcess
from ..base import call

patient_file = 'Patient.ndjson'
encounter_file = 'Encounter.ndjson'
procedure_file = 'Procedure.ndjson'
observation_file = 'Observation.ndjson'


@call.command(name="load", help="THe command to load the data files from provided directory, process it, "
                                "and push it to the database")
@click.argument(
    'folder',
    type=str,
    # help='The path to the folder where data files located.'
)
@click.pass_context
def load(ctx, folder: str):
    folder = Path(folder)
    with open(folder / patient_file, 'r') as patient_input:
        patient_processor = PatientProcess(patient_input,
                                           ctx.obj['engine'],
                                           ctx.obj['threads'],
                                           ctx.obj['bulk_size'])
        patient_processor.run()

    patient_processor.print_result()

    with open(folder / encounter_file, 'r') as encounter_input:
        encounter_processor = EncounterProcess(encounter_input,
                                               ctx.obj['engine'],
                                               ctx.obj['threads'],
                                               ctx.obj['bulk_size'],
                                               patient_mapping=patient_processor.source_id_mapping)

        encounter_processor.run()

    encounter_processor.print_result()

    with open(folder / procedure_file, 'r') as procedure_input:
        procedure_processor = ProcedureProcess(procedure_input,
                                               ctx.obj['engine'],
                                               ctx.obj['threads'],
                                               ctx.obj['bulk_size'],
                                               prepare_mapping=False,
                                               patient_mapping=patient_processor.source_id_mapping,
                                               encounter_mapping=encounter_processor.source_id_mapping)

        procedure_processor.run()

    procedure_processor.print_result()

    with open(folder / observation_file, 'r') as observation_input:
        observation_processor = ObservationProcess(observation_input,
                                                   ctx.obj['engine'],
                                                   ctx.obj['threads'],
                                                   ctx.obj['bulk_size'],
                                                   prepare_mapping=False,
                                                   patient_mapping=patient_processor.source_id_mapping,
                                                   encounter_mapping=encounter_processor.source_id_mapping)

        observation_processor.run()

    observation_processor.print_result()
