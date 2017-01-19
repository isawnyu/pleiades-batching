"""
validate, normalize, and augment Pleiades names data for batch upload create
"""

from arglogger import arglogger
import argparse
import inspect
import csv
from csv_utilities import CSV_DIALECTS, read_csv, test_csv
import json
import logging
from names import PleiadesName
import os
from os.path import abspath, basename, realpath, splitext
from pprint import pformat
import re
import sys
import traceback

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
    ['-a', '--abstract', False, 'generate summaries'],
    ['-e', '--encoding', 'utf-8', 'csv file encoding']
]

SUPPORTED_EXTENSIONS = ['.csv', '.json']


@arglogger
def read_file(fname: str, dialect: None, encoding='utf-8'):
    src_fname, src_ext = splitext(fname)
    func_s = 'read_{}'.format(src_ext[1:])
    return globals()[func_s](fname, dialect, encoding)


@arglogger
def read_json(fname: str, dialect: None, encoding='utf-8'):
    raise NotImplementedError('JSON input file support is not yet available.')


@arglogger
def test_file(src: str, dialect_arg=None, encoding='utf-8'):
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
        return globals()[func_s](src, dialect_arg, encoding)
    else:
        raise ValueError(
            'Input filename has an unsupported extension ({}). Only these '
            'are supported: {}.'
            ''.format(src, SUPPORTED_EXTENSIONS))


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
    logger.debug('reading src')
    src = abspath(realpath(args.source))
    logger.debug('src: {}'.format(src))
    dialect = test_file(src, encoding=args.encoding)
    src_data, field_names = read_file(src, dialect, encoding=args.encoding)
    logger.debug('reading time_periods')
    time_periods = abspath(realpath(args.time_periods))
    logger.debug('time_periods: {}'.format(time_periods))
    dialect = test_file(time_periods, encoding=args.encoding)
    tpp, field_names = read_file(time_periods, dialect, encoding=args.encoding)
    time_periods = {}
    for tp in tpp:
        logger.debug('tp: {}'.format(repr(tp)))
        term = tp['term']
        nameid = tp['nameid']
        try:
            time_periods[nameid].append(term)
        except KeyError:
            time_periods[nameid] = [term]
    logger.debug('time_periods: {}'.format(repr(time_periods)))
    dest = abspath(realpath(args.destination))
    names = []
    for item in src_data:
        logger.debug(pformat(item))
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
        try:
            periods = time_periods[nameid]
        except KeyError:
            logger.warning('No time periods defined for {}'.format(nameid))
        else:
            pn.time_periods = periods
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
            'time_periods',
            type=str,
            help='filepath to which to write the JSON result')
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
