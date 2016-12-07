"""
prepare iip names and locations json for upload (after places uploaded)
"""

import argparse
from functools import wraps
import inspect
import json
import logging
import os
import re
import string
import sys
import traceback
import unidecode

DEFAULT_LOG_LEVEL = logging.WARNING
POSITIONAL_ARGUMENTS = [
    ['-l', '--loglevel', logging.getLevelName(DEFAULT_LOG_LEVEL),
        'desired logging level (' +
        'case-insensitive string: DEBUG, INFO, WARNING, or ERROR'],
    ['-v', '--verbose', False, 'verbose output (logging level == INFO)'],
    ['-w', '--veryverbose', False,
        'very verbose output (logging level == DEBUG)'],
]
RXKEYNAME = re.compile(r'^(Name|Location)::/places/<([^>]+)>$')
TRANSLATOR = str.maketrans(
    {key: None for key in string.punctuation if key != "-"})


def arglogger(func):
    """
    decorator to log argument calls to functions
    """
    @wraps(func)
    def inner(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        logger.debug("called with arguments: %s, %s" % (args, kwargs))
        return func(*args, **kwargs)
    return inner


@arglogger
def main(args):
    """
    main function
    """
    logger = logging.getLogger(sys._getframe().f_code.co_name)
    src = args.source
    pids = args.pid_json
    dest = args.destination

    source = json.load(open(src, 'r'))
    logger.info('read {} source data from {}'.format(len(source), src))
    pid_pairs = json.load(open(pids, 'r'))
    logger.info('read {} pid pairs from {}'.format(len(pid_pairs), pids))

    ready_subordinates = []
    for obj in source['subordinates']:
        path = list(obj.keys())[0]
        m = RXKEYNAME.match(path)
        content_type = m.group(1)
        ptitle = m.group(2)
        pid = pid_pairs[ptitle]
        title = obj[path]['title']['values']
        print('place {} ({}): {} {}'
              ''.format(pid, ptitle, content_type, title))
        # if content_type == 'Name':
        #     slug = sluggify(name)
        # else:
        slug = sluggify(title)
        print('\tslug: "{}"'.format(slug))
        real_path = '{}::/places/{}/{}'.format(content_type, pid, slug)
        ready_subordinates.append(
            {real_path: obj[path]})

    ready_subordinates = {'updates': ready_subordinates}

    json.dump(ready_subordinates, open(dest, 'w'), indent=4,
              ensure_ascii=False, sort_keys=False)


def sluggify(raw):
    """make a slug from raw string"""
    return ('-'.join(unidecode.unidecode(raw).lower().translate(TRANSLATOR).split()))


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
        parser.add_argument('source', type=str,
                            help='JSON file of data from massage-iip-places.py')
        parser.add_argument('pid_json', type=str,
                            help='JSON file of PIDS and corresponding titles')
        parser.add_argument('destination', type=str,
                            help='filepath to which to write the JSON result')
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
