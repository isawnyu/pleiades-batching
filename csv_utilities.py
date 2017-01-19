"""Reusable code for working with CSV files."""

import csv
import logging
from normalize_space import normalize_space
from os.path import basename
from pprint import pformat
import sys

CSV_DIALECTS = {}
csv.register_dialect(
    'excel-quote-none',
    csv.get_dialect('excel'),
    quoting=csv.QUOTE_NONE)
csv.register_dialect(
    'unix-quote-none',
    csv.get_dialect('unix'),
    quoting=csv.QUOTE_NONE)
csv.register_dialect(
    'excel-escape-quotes',
    csv.get_dialect('excel'),
    doublequote=False)
csv.register_dialect(
    'unix-escape-quotes',
    csv.get_dialect('unix'),
    doublequote=False)
csv.register_dialect(
    'excel-quote-all',
    csv.get_dialect('excel'),
    quoting=csv.QUOTE_ALL)
csv.register_dialect(
    'unix-quote-all',
    csv.get_dialect('unix'),
    quoting=csv.QUOTE_ALL)
for dialect_name in csv.list_dialects():
    CSV_DIALECTS[dialect_name] = csv.get_dialect(dialect_name)


def read_csv(fname: str, dialect, encoding='utf-8'):
    logger_name = ':'.join(
        (basename(__file__), __name__, sys._getframe().f_code.co_name))
    logger = logging.getLogger(logger_name)
    raw = []
    with open(fname, 'r', encoding=encoding) as f:
        reader = csv.DictReader(f, dialect=dialect)
        for row in reader:
            raw.append(row)
    field_names = reader.fieldnames
    logger.info(
        'read {} rows of data from CSV file {}'
        ''.format(len(raw), fname))
    cooked = []
    for item in raw:
        logger.debug(pformat(item))
        d = {k: v for k, v in item.items() if v is not None}
        d = {k: v for k, v in d.items() if normalize_space(v) != ''}
        cooked.append(d)
    return (cooked, field_names)


def write_csv(
    fname: str,
    field_names: list,
    data: list,
    dialect='excel',
    encoding='utf-8'
):
    with open(fname, 'w', encoding=encoding) as f:
        writer = csv.DictWriter(f, fieldnames=field_names, dialect=dialect)
        writer.writeheader()
        for d in data:
            writer.writerow(d)


def dialects_match(d1, d2):
    if type(d1) == str:
        dialect1 = CSV_DIALECTS[d1]
    else:
        dialect1 = d1
    if type(d2) == str:
        dialect2 = CSV_DIALECTS[d2]
    else:
        dialect2 = d2
    attributes = {}
    for a in dir(dialect1):
        if a[0] != '_':
            attributes[a] = getattr(dialect2, a)
    attributes = {
        k: v for k, v in attributes.items() if not callable(v)}
    for k, v in attributes.items():
        if v != getattr(dialect2, k):
            return False
    return True


def test_csv(fname: str, dialect_arg=None, encoding='utf-8'):
    """Test if a file object points to valid CSV file."""
    logger_name = ':'.join(
        (basename(__file__), __name__, sys._getframe().f_code.co_name))
    logger = logging.getLogger(logger_name)
    with open(fname, 'r', encoding=encoding) as f:
        smpl = f.read(1024)
    try:
        dialect = csv.Sniffer().sniff(smpl)
    except csv.Error as exc:
        raise csv.Error(
            'Dialect detection error on file {}.'
            ''.format(fname)) from exc
    else:
        if dialect_arg is not None:
            if not dialects_match(dialect_arg, dialect):
                logger.warning(
                    'Dialect argument ({}) and sniffer result ({}) do not '
                    'match. Using dialect argument to read {}.'
                    ''.format(dialect_arg, pformat(dialect), fname))
            else:
                logger.debug('Dialect arg and sniff match!')
            return dialect_arg
        else:
            for k, v in CSV_DIALECTS.items():
                logger.debug('trying dialect: {}'.format(k))
                if dialects_match(dialect, v):
                    logger.info(
                        'CSV file {} has dialect "{}".'.format(fname, k))
                    return k
            raise IOError(
                'CSV file "{}" does not conform to any of the standard '
                'syntax dialects ({}). Test results: {}'
                ''.format(
                    fname,
                    ', '.join(CSV_DIALECTS.keys()),
                    pformat(dialect)))

