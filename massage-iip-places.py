"""
prepare iip places json for upload
"""

import argparse
from functools import wraps
import inspect
import json
import logging
import os
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
    ['-a', '--alternates', '', 'json file containing alternate name info']
]
RXDD = re.compile(r'^\d+\.\d+$')
RXDMS = re.compile(r"^(\d+)°\s*(\d+)'\s*(\d+\.?\d*)''\s*([N,S,E,W])$")
LANGUAGES = {
    'arabic': 'ar',
    'hebrew': 'he',
    'english': 'en',
    'latin': 'la'
}


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
    alts = args.alternates

    # read in the place data (implies subordinate name/location data)
    places = json.load(open(src, 'r'))
    logger.info('read {} places from {}'.format(len(places), src))

    # strip out incomplete places
    logger.info('stripping out incomplete places')
    complete_places = {}
    for k, v in places.items():
        for kk, vv in v.items():
            if vv == '':
                logger.warning('OMITTED: title={}, blank={}'.format(
                    v['title'], kk))
                break
        else:
            complete_places[k] = v
    logger.info('stripped {} incomplete places'.format(
        len(places) - len(complete_places)))
    places = complete_places

    # validate lat/lon and convert DMS to DD where necessary
    logger.info('validate lat/lon and convert DMS to DD where necessary')
    complete_places = {}
    count_lat = 0
    count_lon = 0
    for k, v in places.items():
        lat = v['latitude']
        m = RXDD.match(lat)
        if m is None:
            lat = lat.replace('′', "'")
            lat = lat.replace('″', '"')
            lat = lat.replace('"', "''")
            m = RXDMS.match(lat)
            if m:
                count_lat += 1
                logger.info('CONVERTING: title={}, latitude={}'.format(
                    v['title'], lat))
                logger.debug('prior lat: {}'.format(lat))
                lat = '{}'.format(
                    float(m.group(1)) +
                    float(m.group(2))/60.0 +
                    float(m.group(3))/3600.0)
                logger.debug('post lat: {}'.format(lat))
            else:
                logger.warning(
                    'OMITTED: title={}, latitude="{}"'.format(
                        v['title'], lat))
                continue
        lon = v['longitude']
        m = RXDD.match(lon)
        if m is None:
            lon = lon.replace('′', "'")
            lon = lon.replace('″', '"')
            lon = lon.replace('"', "''")
            m = RXDMS.match(lon)
            if m:
                count_lon += 1
                logger.info(
                    'CONVERTING: title={}, longitude="{}"'.format(
                        v['title'], lon))
                logger.debug('prior lon: {}'.format(lon))
                lon = '{}'.format(
                    float(m.group(1)) +
                    float(m.group(2))/60.0 +
                    float(m.group(3))/3600.0)
                logger.debug('post lon: {}'.format(lon))
            else:
                logger.warning(
                    'OMITTED PLACE: title={}, longitude="{}"'.format(
                        v['title'], lon))
                continue
        complete_places[k] = v
        if type(lat) == str:
            lat = float(lat)
        if type(lon) == str:
            lon = float(lon)
        complete_places[k]['latitude'] = '{0:.5f}'.format(round(lat, 5))
        complete_places[k]['longitude'] = '{0:.5f}'.format(round(lon, 5))
    logger.info('stripped {} places with invalid coordinates'.format(
        len(places) - len(complete_places)))
    logger.info('converted {} latitude coordinates from DMS to DD'.format(
        count_lat))
    logger.info('converted {} longitude coordinates from DMS to DD'.format(
        count_lon))
    places = complete_places

    # read in and pre-process alternate names
    alternate_names = {}
    if alts != '':
        alternate_names_raw = json.load(open(alts, 'r'))
        logger.info('read {} alternate names from {}'
                    ''.format(len(alternate_names_raw), alts))

        # strip out incomplete alternate names

        complete_alternate_names = {}
        for k, v in alternate_names_raw.items():
            for kk, vv in v.items():
                if vv == '':
                    logger.warning(
                        'OMITTED ALTNAME: title={}, blank={}'
                        ''.format(v['title'], kk))
                    break
            else:
                complete_alternate_names[k] = v
        logger.info('stripped {} incomplete alternate names'.format(
            len(alternate_names_raw) - len(complete_alternate_names)))

        for k, v in complete_alternate_names.items():
            logger.debug('processing alternate name: "{}"'.format(k))
            d = v
            ptitle = v['parent_title']
            if ptitle in alternate_names.keys():
                alternate_names[ptitle].append(d)
            else:
                alternate_names[ptitle] = [d]

    # assemble data for upload script
    complete_places = []
    subordinates = []

    for k, v in places.items():

        # new places
        update_key = 'Place::/places/{}'.format(k)
        attributes = {
            'title': {
                'mode': 'replace',
                'values': v['title'],
                },
            'description': {
                'mode': 'replace',
                'values': ('Place in the {}, identified as an '
                           'epigraphic findspot '
                           'by the Inscriptions of Israel/Palestine project.'
                           ''.format(v['region'])
                           )
                },
            'subject': {
                'mode': 'replace',
                'values': ('IIP')
            },
            'referenceCitations': {
                'mode': 'replace',
                'values': [
                    {
                        'formatted_citation': v['place_reference'],
                        'type': 'seeFurther'
                    }
                ]
            }
        }
        complete_places.append({update_key: attributes})

        # subordinate location
        update_key = 'Location::/places/<{}>'.format(v['title'])
        if 'GeoNames' in v['location_reference']:
            positional_accuracy = 'generic-geonames-accuracy-assessment'
        elif 'GeoHack' in v['location_reference']:
            positional_accuracy = 'generic-geohack-accuracy-assessment'
        elif 'Google Earth' in v['location_reference']:
            positional_accuracy = 'google-earth-and-partners-imagery-2015'
        else:
            logger.warning(
                'Cannot set accuracy assessment for {} on {}.'
                ''.format(v['location_reference'], v['title']))
        attributes = {
            'title': {
                'mode': 'replace',
                'values': '{} Location'.format(v['location_reference']),
                },
            'description': {
                'mode': 'replace',
                'values': ('Representative point location, derived from {}.'
                           ''.format(v['location_reference']))
            },
            'geometry': {
                'mode': 'replace',
                'values':
                    'Point:[{},{}]'
                    ''.format(v['longitude'], v['latitude'])
            },
            'subject': {
                'mode': 'replace',
                'values': ('IIP')
            },
            'positional_accuracy': {
                'mode': 'replace',
                'values': positional_accuracy
            }
        }
        subordinates.append({update_key: attributes})

        # subordinate name(s)
        update_key, attributes = serialize_name(v)
        subordinates.append({update_key: attributes})
        try:
            anames = alternate_names[v['title']]
        except KeyError:
            pass
        else:
            for aname in anames:
                update_key, attributes = serialize_name(aname)
                update_key = update_key.replace(
                    aname['title'], aname['parent_title'])
                subordinates.append({update_key: attributes})

    places = {'updates': complete_places, 'subordinates': subordinates}

    json.dump(places, open(dest, 'w'), indent=4, ensure_ascii=False,
              sort_keys=False)


def serialize_name(v):
    language = LANGUAGES[v['language'].lower()]
    update_key = 'Name::/places/<{}>'.format(v['title'])
    attributes = {
        'title': {
            'mode': 'replace',
            'values': v['title']
        },
        'transliterated': {
            'mode': 'replace',
            'values': v['title']
        },
        'nameType': {
            'mode': 'replace',
            'values': 'geographic'
        },
        'language': {
            'mode': 'replace',
            'values': language
        },
        'subject': {
            'mode': 'replace',
            'values': ('IIP')
        },
        'description': {
            'mode': 'replace',
            'values': 'Name variant identified the Inscriptions of Israel/'
                      'Palestine project.'
        }
    }
    return (update_key, attributes)


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
                            help='CSV file to read and convert')
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
