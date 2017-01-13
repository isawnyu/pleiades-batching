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
from os.path import abspath, realpath, splitext
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
    ['-l', '--loglevel', logging.getLevelName(DEFAULT_LOG_LEVEL),
        'desired logging level (' +
        'case-insensitive string: DEBUG, INFO, WARNING, or ERROR'],
    ['-v', '--verbose', False, 'verbose output (logging level == INFO)'],
    ['-w', '--veryverbose', False,
        'very verbose output (logging level == DEBUG)'],
    ['-r', '--romanize', False, 'generate full romanized forms'],
    ['-s', '--sluggify', False, 'generate slugs']
]

SUPPORTED_EXTENSIONS = ['.csv', '.json']


@arglogger
def read_file(fname: str):
    src_fname, src_ext = splitext(fname)
    func_s = 'read_{}'.format(src_ext[1:])
    return globals()[func_s](fname)


@arglogger
def read_csv(fname: str):
    logger = logging.getLogger(sys._getframe().f_code.co_name)
    raw = []
    with open(fname, 'r') as f:
        sample = f.read(1024)
        dialect = csv.Sniffer().sniff(sample)
        f.seek(0)
        reader = csv.DictReader(f, dialect=dialect)
        for row in reader:
            raw.append(row)
    logger.info(
        'read {} rows of data from CSV file {}'
        ''.format(len(raw), fname))
    cooked = []
    for item in raw:
        d = {k: v for k, v in item.items() if v is not None}
        d = {k: v for k, v in d.items() if normalize_space(v) != ''}
        cooked.append(d)
    return cooked


@arglogger
def read_json(fname: str):
    raise NotImplementedError('JSON input file support is not yet available.')


@arglogger
def test_file(src: str):
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
        globals()[func_s](src)
    else:
        raise ValueError(
            'Input filename has an unsupported extension ({}). Only these '
            'are supported: {}.'
            ''.format(src, SUPPORTED_EXTENSIONS))


@arglogger
def test_csv(fname: str):
    """Test if a file object points to valid CSV file."""
    logger = logging.getLogger(sys._getframe().f_code.co_name)
    with open(fname, 'r') as f:
        smpl = f.read(1024)
    try:
        dialect = csv.Sniffer().sniff(smpl)
    except csv.Error as exc:
        raise csv.Error(
            'Dialect detection error on file {}.'
            ''.format(fname)) from exc
    else:
        attributes = {}
        for a in dir(dialect):
            if a[0] != '_':
                attributes[a] = getattr(dialect, a)
        attributes = {
            k: v for k, v in attributes.items() if not callable(v)}
        match = None
        for dialect_name, dialect in CSV_DIALECTS.items():
            logger.debug('trying dialect: {}'.format(dialect_name))
            for k, v in attributes.items():
                logger.debug('\t{}: {}'.format(k, v))
                if v != getattr(dialect, k):
                    logger.debug(
                        '\t\tFAILED with {}'.format(getattr(dialect, k)))
                    match = None
                    break
                else:
                    match = dialect_name
            if match is not None:
                logger.info(
                    'CSV file {} has dialect "{}".'.format(fname, match))
                break
        if match is None:
            raise IOError(
                'CSV file "{}" does not conform to any of the standard '
                'syntax dialects ({}).'
                ''.format(fname, ', '.join(CSV_DIALECTS.keys())))


@arglogger
def test_json(fname: str):
    raise NotImplementedError('JSON input file support is not yet available.')


def normalize_space(v: str):
    return ' '.join(v.split()).strip()


@arglogger
def main(args):
    """
    main function
    """
    logger = logging.getLogger(sys._getframe().f_code.co_name)
    src = abspath(realpath(args.source))
    dest = abspath(realpath(args.destination))

    test_file(src)
    src_data = read_file(src)
    names = []
    for item in src_data:
        nameid = item['nameid']
        d = {k: v for k, v in item.items() if k != 'nameid'}
        d['summary'] = 'foo'
        logger.debug(pformat(d))
        try:
            pn = PleiadesName(**d)
        except TypeError as exc:
            raise TypeError(
                'Pleiades name creation failed because of inadequate input '
                'data in ({}). Details: {}'
                ''.format(repr(item), exc)) from exc
        pn.generate_romanized()
        pn.generate_slug()
        arguments = dir(pn)
        arguments = [a for a in arguments if a[0] != '_']
        arguments = [a for a in arguments if not callable(getattr(pn, a))]
        d = {}
        for a in arguments:
            d[a] = getattr(pn, a)
        logger.debug(pformat(d))





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
        if args.loglevel is not None:
            args_log_level = re.sub('\s+', '', args.loglevel.strip().upper())
            try:
                log_level = getattr(logging, args_log_level)
            except AttributeError:
                logging.error(
                    "command line option to set log_level failed "
                    "because '%s' is not a valid level name; using %s"
                    % (args_log_level, log_level_name))
        if args.veryverbose:
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
