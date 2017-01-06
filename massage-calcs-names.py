"""
prepare calcs names json for upload
"""

import argparse
from functools import wraps
import inspect
import json
from language_tags import tags
import logging
import os
from polyglot.text import Text as Polytext
from polyglot.detect import Detector as Polydetector
import re
import string
import sys
import traceback
import unicodedata
from unidecode import unidecode

DEFAULT_LOG_LEVEL = logging.WARNING
POSITIONAL_ARGUMENTS = [
    ['-l', '--loglevel', logging.getLevelName(DEFAULT_LOG_LEVEL),
        'desired logging level (' +
        'case-insensitive string: DEBUG, INFO, WARNING, or ERROR'],
    ['-v', '--verbose', False, 'verbose output (logging level == INFO)'],
    ['-w', '--veryverbose', False,
        'very verbose output (logging level == DEBUG)'],
]
NOPUNCT = str.maketrans(
    {key: None for key in string.punctuation if key != "-"})
PERIODS = {
    'mediaeval/byzantine': 'mediaeval-byzantine',
    'modern': 'modern'
}
ROMAN_LETTERS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')


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
    dest = args.destination

    # read in the name data
    names = json.load(open(src, 'r'))
    logger.info('read {} names from {}'.format(len(names), src))

    complete_names = {}
    for k, v in names.items():

        logger.debug('\n\n--------------------------------------------------')
        logger.debug('Processing {}'.format(k))

        attested = unicodedata.normalize('NFC', v['attested'])
        compatibility = unicodedata.normalize('NFKC', v['attested'])
        if attested != compatibility:
            logger.warning(
                'Possible Unicode weirdness: canonical (NFC) form "{}" '
                'does not match compatibility (NFCK) form "{}". Using '
                'NFC for ATTESTED name.'.format(attested, compatibility))
        if len(attested) == 0:
            logger.warning(
                'No ATTESTED value was provided in {}. It will be left blank.'
                ''.format(k))

        language = v['language']
        if language == '':
            logger.error(
                'No language was specified in input data so '
                '{} will be ignored.'
                ''.format(k))
            continue
        if not tags.check(language):
            logger.error(
                '"{}" does not validate as an IANA language code. {} will be '
                'ignored'.format(language, k))
            continue

        romanized = unicodedata.normalize('NFC', v['transliterated'])
        compatibility = unicodedata.normalize('NFKC', v['transliterated'])
        if romanized != compatibility:
            logger.warning(
                'Possible Unicode weirdness: canonical (NFC) form "{}" '
                'does not match compatibility (NFCK) form "{}". Using '
                'NFC for ROMANIZED name.'.format(romanized, compatibility))
        if romanized == '':
            if len(attested) > 0:
                logger.info(
                    'No ROMANIZED form was provided in {}. Trying to create '
                    'one...'
                    ''.format(k))
                compatibility = unicodedata.normalize('NFKD', attested)
                try:
                    # get script subtag that is explicit in the tag
                    iana_script = tags.tag(language).script.format
                except AttributeError:
                    # there was no explicit script subtag
                    try:
                        # get default script subtag (suppress script)
                        iana_script = tags.language(language).script
                    except:
                        raise
                iana_script = str(iana_script)
                if iana_script == 'Latn':
                    romanized = attested
                    logger.info(
                        '...ATTESTED form {} is already in Latin script, so '
                        'it will be copied verbatim to ROMANIZED'
                        ''.format(attested))
                else:
                    text = Polytext(compatibility)
                    romanized = ' '.join(text.transliterate('en'))
                    romanized = string.capwords(romanized)
                    logger.info(
                        '... created ROMANIZED form "{}" using the '
                        '"polyglot" package'.format(romanized))
            else:
                logger.error(
                    'Absence of both ATTESTED and ROMANIZED forms mean we '
                    'cannot add this name. Ignoring {}.'.format(k))
                continue

        banalized = unicodedata.normalize(
            'NFC', unidecode(
                unicodedata.normalize('NFKD', romanized)))
        if banalized != romanized:
            logger.warning(
                'adding banalized form "{}" to romanized "{}"'
                ''.format(banalized, romanized))
            romanized = ', '.join((romanized, banalized))
        slug = sluggify(banalized)

        details = v['details']

        periods = [p for p in v['periods'] if p != '']
        if len(periods) == 0:
            logger.warning(
                'No time period(s) were specified for "{}" ({}).'
                ''.format(
                    '{} ({})'.format(attested, romanized), k))
        else:
            periods = [PERIODS[p] for p in periods]

        pid = v['pid']
        if len(pid) == 0:
            logger.error('No pid was specified. Ignoring {}.'
                         ''.format(k))
            continue

        references = []
        for i in range(1, 3):
            title = v['ref{}'.format(i)]
            url = v['ref{}url'.format(i)]
            if len(title) != 0:
                references.append(
                    {
                        'formatted_citation': title,
                        'access_uri': url,
                        'type': 'citesAsEvidence'
                    })

        logger.debug(
            '\n'.join(
                [
                    '\nKey attributes:',
                    '  attested: {}'.format(attested),
                    '  romanized: {}'.format(romanized),
                    '  banalized: {}'.format(banalized),
                    '  slug: {}'.format(slug),
                    '  language: {}'.format(language),
                    '  pid: {}'.format(pid)
                ]))

        attributes = {
            'romanized': romanized,
            'language': language,
            'periods': periods,
            'referenceCitations': references
        }
        if len(details) > 0:
            attributes['details'] = details
        if len(attested) > 0:
            attributes['attested'] = attested

        path = 'Name::/places/{}/{}'.format(pid, slug)

        directives = {}
        for ak, av in attributes.items():
            directives[ak] = {
                'mode': 'replace',
                'values': av
            }

        complete_names[path] = directives

    complete_names = {
        'updates': [{k: v} for k, v in complete_names.items()]
        }

    json.dump(complete_names, open(dest, 'w'), indent=4,
              ensure_ascii=False, sort_keys=True)


def sluggify(raw):
    """make a slug from raw string"""
    chopped = raw.lower().translate(NOPUNCT).split()
    cooked = '-'.join(chopped).encode('ascii', 'xmlcharrefreplace')
    return (cooked.decode('ascii'))


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
