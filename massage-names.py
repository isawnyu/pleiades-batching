"""
validate, normalize, and augment Pleiades names data for batch upload create
"""

from arglogger import arglogger
import argparse
import inspect
import csv
import json
import logging
from names import PleiadesName
import os
from os.path import abspath, basename, realpath, splitext
from pprint import pformat
import re
import sys
import traceback

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

DEFAULT_LOG_LEVEL = logging.WARNING
POSITIONAL_ARGUMENTS = [
    ['-l', '--loglevel', '',
        'desired logging level (' +
        'case-insensitive string: DEBUG, INFO, WARNING, or ERROR'],
    ['-v', '--verbose', False, 'verbose output (logging level == INFO)'],
    ['-w', '--veryverbose', False,
        'very verbose output (logging level == DEBUG)'],
    ['-r', '--romanize', False, 'generate full romanized forms'],
    ['-s', '--sluggify', False, 'generate slugs'],
    ['-d', '--dialect', '', 'CSV dialect to use (default: sniff)'],
    ['-a', '--abstract', False, 'generate summaries']
]

SUPPORTED_EXTENSIONS = ['.csv', '.json']


@arglogger
def read_file(fname: str, dialect: None):
    src_fname, src_ext = splitext(fname)
    func_s = 'read_{}'.format(src_ext[1:])
    return globals()[func_s](fname, dialect)


@arglogger
def read_csv(fname: str, dialect):
    logger_name = ':'.join(
        (basename(__file__), __name__, sys._getframe().f_code.co_name))
    logger = logging.getLogger(logger_name)
    raw = []
    with open(fname, 'r') as f:
        reader = csv.DictReader(f, dialect=dialect)
        for row in reader:
            raw.append(row)
    logger.info(
        'read {} rows of data from CSV file {}'
        ''.format(len(raw), fname))
    cooked = []
    for item in raw:
        logger.debug(pformat(item))
        d = {k: v for k, v in item.items() if v is not None}
        d = {k: v for k, v in d.items() if normalize_space(v) != ''}
        cooked.append(d)
    return cooked


@arglogger
def read_json(fname: str):
    raise NotImplementedError('JSON input file support is not yet available.')


@arglogger
def test_file(src: str, dialect=None):
    """Test if this is a file we can do something with."""
    src_fname, src_ext = splitext(src)
    if src_ext == '.file':
        raise ValueError(
            'Source filename has an invalid extension: ".file".')
    elif src_ext in ['', '.']:
        raise ValueError(
            'Source filename {} needs an extension from the list {}.'
            ''.format(src, SUPPORTED_EXTENSIONS))
    elif src_ext in SUPPORTED_EXTENSIONS:
        func_s = 'test_{}'.format(src_ext[1:])
        return globals()[func_s](src, dialect)
    else:
        raise ValueError(
            'Input filename has an unsupported extension ({}). Only these '
            'are supported: {}.'
            ''.format(src, SUPPORTED_EXTENSIONS))


@arglogger
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


@arglogger
def test_csv(fname: str, dialect_arg=None):
    """Test if a file object points to valid CSV file."""
    logger_name = ':'.join(
        (basename(__file__), __name__, sys._getframe().f_code.co_name))
    logger = logging.getLogger(logger_name)
    with open(fname, 'r') as f:
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
                logger.debug('trying dialect: {}'.format(dialect_name))
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


@arglogger
def test_json(fname: str, **kwargs):
    raise NotImplementedError('JSON input file support is not yet available.')


def normalize_space(v: str):
    return ' '.join(v.split()).strip()


@arglogger
def main(args):
    """
    main function
    """
    logger_name = ':'.join(
        (basename(__file__), __name__, sys._getframe().f_code.co_name))
    logger = logging.getLogger(logger_name)
    src = abspath(realpath(args.source))
    dest = abspath(realpath(args.destination))

    dialect = test_file(src)
    src_data = read_file(src, dialect)
    names = []
    for item in src_data:
        nameid = item['nameid']
        d = {k: v for k, v in item.items() if k != 'nameid'}
        logger.debug(pformat(d))
        try:
            pn = PleiadesName(**d)
        except (TypeError, ValueError) as exc:
            try:
                title = item['romanized']
            except:
                title = item['attested']
            logger.critical(
                'validate-name:{}: Pleiades name creation failed because of '
                'inadequate or inappropriate input '
                'data in nameid={} ({}). Details: {}'
                ''.format(nameid, nameid, title, exc))
            continue
        if args.romanize:
            try:
                pn.generate_romanized()
            except ValueError as exc:
                try:
                    title = item['romanized']
                except:
                    title = item['attested']
                logger.critical(
                    'generate-romanized:{}: Pleiades name creation failed '
                    'during attempted romanization '
                    'for nameid={} ({}). Details: {}'
                    ''.format(nameid, nameid, title, exc))
                continue
        if args.sluggify:
            try:
                pn.generate_slug()
            except ValueError as exc:
                try:
                    title = item['romanized']
                except:
                    title = item['attested']
                logger.critical(
                    'generate-slug:{}: Pleiades name creation failed during '
                    'slug generation '
                    'for nameid={} ({}). Details: {}'
                    ''.format(nameid, nameid, title, exc))
                continue
        if args.abstract:
            print('boom')
            pn.generate_summary()
        arguments = dir(pn)
        arguments = [a for a in arguments if a[0] != '_']
        arguments = [a for a in arguments if not callable(getattr(pn, a))]
        d = {}
        for a in arguments:
            d[a] = getattr(pn, a)
        d['nameid'] = nameid
        d = {k: v for k, v in d.items() if v != ''}
        logger.debug(pformat(d))
        names.append(d)
    with open(dest, 'w') as f:
        json.dump(names, f, ensure_ascii=False, sort_keys=True, indent=4)


if __name__ == "__main__":
    log_level = DEFAULT_LOG_LEVEL
    log_level_name = logging.getLevelName(log_level)
    logging.basicConfig(level=log_level)
    try:
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        for p in POSITIONAL_ARGUMENTS:
            d = {
                'help': p[3]
            }
            if type(p[2]) == bool:
                if p[2] is False:
                    d['action'] = 'store_true'
                    d['default'] = False
                else:
                    d['action'] = 'store_false'
                    d['default'] = True
            else:
                d['default'] = p[2]
            parser.add_argument(
                p[0],
                p[1],
                **d)
        parser.add_argument(
            'source',
            type=str,
            help='JSON file of data from massage-iip-places.py')
        parser.add_argument(
            'destination',
            type=str,
            help='filepath to which to write the JSON result')
        args = parser.parse_args()
        if args.loglevel != '':
            args_log_level = re.sub('\s+', '', args.loglevel.strip().upper())
            try:
                log_level = getattr(logging, args_log_level)
            except AttributeError:
                logging.error(
                    "command line option to set log_level failed "
                    "because '%s' is not a valid level name; using %s"
                    % (args_log_level, log_level_name))
        elif args.veryverbose:
            log_level = logging.DEBUG
        elif args.verbose:
            log_level = logging.INFO
        log_level_name = logging.getLevelName(log_level)
        logging.getLogger().setLevel(log_level)
        fn_this = inspect.stack()[0][1].strip()
        title_this = __doc__.strip()
        logging.info(': '.join((fn_this, title_this)))
        if log_level != DEFAULT_LOG_LEVEL:
            logging.warning(
                "logging level changed to %s via command line option"
                % log_level_name)
        else:
            logging.info("using default logging level: %s" % log_level_name)
        logging.debug("command line: '%s'" % ' '.join(sys.argv))
        main(args)
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
    except SystemExit as e:  # sys.exit()
        raise e
    except Exception as e:
        print("ERROR, UNEXPECTED EXCEPTION")
        print(str(e))
        traceback.print_exc()
        os._exit(1)
