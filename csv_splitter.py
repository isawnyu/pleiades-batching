"""
A script for splitting CSV field values containing comma-delimited lists.
"""

from arglogger import arglogger
import argparse
from copy import deepcopy
from csv_utilities import test_csv, read_csv, write_csv
import inspect
import logging
from normalize_space import normalize_space
import os
from os.path import abspath, basename, realpath
import re
import sys
import traceback

DEFAULT_LOG_LEVEL = logging.WARNING
POSITIONAL_ARGUMENTS = [
    ['-l', '--loglevel', logging.getLevelName(DEFAULT_LOG_LEVEL),
        'desired logging level (' +
        'case-insensitive string: DEBUG, INFO, WARNING, or ERROR'],
    ['-v', '--verbose', False, 'verbose output (logging level == INFO)'],
    ['-w', '--veryverbose', False,
        'very verbose output (logging level == DEBUG)'],
    ['-k', '--key', '', 'name of field to use as key'],
    ['-e', '--encoding', 'utf-8', 'CSV file character encoding (utf-8)'],
    ['-s', '--streamline', False, 'skip empty rows']
]


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
    logger.debug('src: "{}"'.format(src))
    dialect = test_csv(src, encoding=args.encoding)
    logger.debug('dialect: "{}"'.format(repr(dialect)))
    src_data, field_names = read_csv(src, dialect, args.encoding)
    logger.debug('field_names: {}'.format(repr(field_names)))
    logger.debug('rows: {}'.format(len(src_data)))
    if args.key not in field_names:
        raise ValueError(
            'specified key field ({}) not in CSV fieldnames ({})'
            ''.format(args.key, repr(field_names)))
    dest_data = []
    field_names = []
    for i, item in enumerate(src_data):
        field_names.extend(item.keys())
        field_names = list(set(field_names))
        logger.debug('ITEM {}'.format(i))
        try:
            field_value = item[args.field]
        except KeyError:
            logger.debug(
                'specified field ({}) is empty in this row; appending: {}.'
                ''.format(args.field, repr(item)))
            dest_data.append(item)
        else:
            if ',' in field_value:
                logger.info(
                    'specified field ({}) contains delimiter: splitting "{}".'
                    ''.format(args.field, field_value))
                d = {}
                d[args.key] = item[args.key]
                splits = [normalize_space(v) for v in field_value.split(',')]
                d = deepcopy(item)
                d[args.field] = splits[0]
                dest_data.append(d)
                logger.debug(
                    'appending primary derivative: {}'
                    ''.format(repr(d)))
                for j, split in enumerate(splits[1:]):
                    d = {}
                    d[args.key] = item[args.key]
                    d[args.field] = split
                    dest_data.append(d)
                    logger.debug(
                        'appending derivative {}: {}'
                        ''.format(j+1, repr(d)))
            else:
                logger.debug(
                    'specified field ({}) does not contain delimiter'
                    ''.format(repr(item)))
                dest_data.append(item)
    if args.streamline:
        dest_data = [item for item in dest_data if len(item.keys()) > 1]
    write_csv(dest, field_names=field_names, data=dest_data)


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
        parser.add_argument('source', type=str, help="csv file to clean up")
        parser.add_argument('field', type=str, help="field to split")
        parser.add_argument('destination', type=str, help="csv file to output")
        # example positional argument
        # parser.add_argument(
        #     'foo',
        #     metavar='N',
        #     type=str,
        #     nargs='1',
        #     help="foo is better than bar except when it isn't")
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
