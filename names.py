from language_tags import tags
import logging
from polyglot.detect import Detector as LanguageDetector
import re
import sys
from vocabularies import VOCABULARIES, UNICODE_RANGES

RX_PID = re.compile('^\d+$')
RX_SLUG = re.compile('^[a-z\-\d]+$')
RX_ROMANIZED = r''
for k, v in UNICODE_RANGES.items():
    if 'latin' in k or k == 'combining_diacritical_marks':
        RX_ROMANIZED += r'{}-{}'.format(*v)
RX_ROMANIZED = re.compile('^[{}]+$'.format(RX_ROMANIZED))

class PleiadesName:
    """ a class for working up pleiades names
        Args:
            self
            pid
            associated_certainty:
            attested:
            details:
            language:
            ...
    """

    def __init__(self, pid: str, *,
        association_certainty: str = 'certain',
        attested: str = '',
        details: str = '',
        language: str = '',
        name_type: str = 'geographic',
        romanized: str = '',
        slug: str = '',
        summary: str = '',
        transcription_accuracy: str = 'accurate',
        transcription_completeness: str = 'complete'
        ):

        # validate argument values
        arguments = locals()
        arguments = {k: v for k, v in arguments.items() if k != 'self'}
        self.__validate_attributes(**arguments)


    def __validate_attributes(self, **kwargs):
        """ Validate standard attributes of the class """

        logger = logging.getLogger(sys._getframe().f_code.co_name)
        for k, v in kwargs.items():
            logger.debug('validating "{}": "{}"'.format(k, v))
            if k == 'pid':
                m = RX_PID.match(v)
                if not m:
                    raise ValueError(
                        'Pleiades IDs (pids) must be strings of Arabic '
                        'numeral digits. "{}" does not meet this requirement.'
                        ''.format(v))
            elif k == 'attested':
                if v == '' and kwargs['romanized'] == '':
                    raise ValueError(
                        'A Pleiades name cannot be created if both the '
                        '"attested" and "romanized" fields are blank.')
            elif k == 'details':
                pass
            elif k == 'language':
                if not tags.check(v):
                    raise ValueError(
                        '"{}" does not validate as an IANA language tag.'
                        ''.format(v))
                elif kwargs['attested'] != '':
                    detector = LanguageDetector(kwargs['attested'])
                    languages = [l.code for l in detector.languages]
                    if v not in languages:
                        logger.error(
                            'Polyglot detected {} for "{}", but provided '
                            'language code value is "{}".'
                            ''.format(
                                repr(languages),
                                kwargs['attested'],
                                v))
                        raise ValueError(
                            'The provided match for the language tag ({}) '
                            'does not match the language detected by '
                            'polyglot for the attested name form "{}."'
                            ''.format(v, kwargs['attested']))
            elif k == 'romanized':
                if v == '' and kwargs['attested'] == '':
                    raise ValueError(
                        'A Pleiades name cannot be created if both the '
                        '"attested" and "romanized" fields are blank.')
                elif v == '':
                    pass
                else:
                    m = RX_ROMANIZED.match(v)
                    if not m:
                        raise ValueError(
                            'A "romanized" Pleiades name string must only '
                            'contain "Latin" Unicode characters and combining '
                            'diacritics. "{}" does '
                            'not meet this requirement.'
                            ''.format(v))
            elif k == 'slug':
                if v != '':
                    m = RX_SLUG.match(v)
                    if not m:
                        raise ValueError(
                            'Pleiades name slugs must be strings of alpha-'
                            'numeric Roman characters. "{}" does not meet '
                            'this requirement.'.format(v))
                    else:
                        # todo: validate uniqueness in context of parent pid
                        logger.warning(
                            'NOT IMPLEMENTED: slug uniqueness validation')
            elif k == 'summary':
                if v == '':
                    raise ValueError(
                        'PleiadesName attribute "summary" must not be a zero-'
                        'length string (i.e., you must provide a "summary").')
            else:
                try:
                    vocab = VOCABULARIES[k]
                except KeyError:
                    logger.warning(
                        'There is no validation test for "{}".'.format(k))
                    raise NotImplementedError(k)
                else:
                    if v not in vocab.keys():
                        raise ValueError(
                            'PleiadesName attribute "{}" must be a string '
                            'containing a value from the list: "{}." '
                            'The provided value ("{}") does not meet this '
                            'requirement.'
                            ''.format(k, '", "'.join(vocab.keys()), v))

