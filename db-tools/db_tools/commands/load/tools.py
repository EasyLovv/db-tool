import sys
from concurrent.futures.thread import ThreadPoolExecutor

from dateutil import parser
from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker

import json

from copy import deepcopy
from typing import Dict, TextIO

# from tqdm import tqdm
from queue import Queue

from sqlalchemy.engine import Engine


def safe_get_value(obj: Dict, *way, default=None):
    cursor = obj
    for node in way:
        try:
            cursor = cursor[node]
        except (KeyError, IndexError, AttributeError, TypeError):
            return default
    return cursor


def safe_get_date(obj: Dict, *way, default=None):
    birth_date = safe_get_value(obj, *way, default=default)
    if birth_date is not None:
        birth_date = parser.parse(birth_date).date()
    return birth_date


class CustomThreadPoolExecutor(ThreadPoolExecutor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._work_queue = Queue(self._max_workers)


class ConvertException(Exception):
    pass


class BaseProcess(object):
    _model = None
    _result_template: Dict = None
    _base_result_template: Dict = {
        'records_amount': 0,
        'failed_amount': 0
    }

    def __init__(self, input_file: TextIO, pg_engine: Engine,
                 threads_amount: int, bulk_size: int, prepare_mapping=True, **kwargs):
        self._input_file = input_file
        self._pg_engine = pg_engine
        self._threads_amount = threads_amount
        self._bulk_size = bulk_size
        self._result: Dict = None
        self._failed_amount = 0
        self._prepare_mapping = prepare_mapping
        self.source_id_mapping = None
        self._context = kwargs

    @property
    def _tbl(self) -> Table:
        return self._model.__table__

    def bulk_insert(self, bulk):
        try:
            session = sessionmaker(bind=self._pg_engine)()
            query = self._tbl.insert().values(bulk)

            if self._prepare_mapping:
                query = query.returning(self._tbl.c.id)
                response = session.execute(query).fetchall()
                self.source_id_mapping.update(dict(
                    zip((b['source_id'] for b in bulk), (r[0] for r in response))
                ))
            else:
                session.execute(query)

            session.commit()
        except Exception as e:
            print(e, file=sys.stderr)

    def process_stat(self, entity):
        self._result['records_amount'] += 1

    def print_result(self):
        print(f"Imported {self._result['records_amount']} {self._tbl.name}")
        if self._result['failed_amount'] > 0:
            print(f"Failed {self._result['failed_amount']} {self._tbl.name}")

    def entry_convert(self, raw_entry: Dict) -> Dict:
        raise NotImplementedError

    def run(self):
        print(f"\nStart loading {self._tbl.name}")
        # prepare result storage
        self.source_id_mapping = {}
        self._result = deepcopy(self._base_result_template)
        if self._result_template is not None:
            self._result.update(deepcopy(self._result_template))

        # create a thread pool executor
        with CustomThreadPoolExecutor(max_workers=self._threads_amount) as ex:
            bulk = []
            for raw_patient in self._input_file.readlines():

                try:
                    raw_patient = json.loads(raw_patient)
                except json.decoder.JSONDecodeError:
                    self._result['failed_amount'] += 1
                    continue

                entry_gen = self.entry_convert(raw_patient)
                while True:
                    try:
                        entry = next(entry_gen)
                    except ConvertException:
                        self._result['failed_amount'] += 1
                        continue
                    except StopIteration:
                        break

                    self.process_stat(entry)
                    bulk.append(entry)
                    if len(bulk) == self._bulk_size:
                        ex.submit(self.bulk_insert, bulk)
                        bulk = []

            ex.submit(self.bulk_insert, bulk)
