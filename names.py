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
RX_ROMANIZED = re.compile('^[{}]*$'.format(RX_ROMANIZED))


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

    def __init__(
        self, pid: str, *,
        association_certainty: str = 'certain',
        attested: str = '',
        details: str = '',
        language: str,  # cannot be zero-length
        name_type: str = 'geographic',
        romanized: str = '',
        slug: str = '',
        summary: str = '',  # cannot be zero-length
        transcription_accuracy: str = 'accurate',
        transcription_completeness: str = 'complete'
    ):

        # validate argument values
        arguments = locals()
        arguments = {k: v for k, v in arguments.items() if k != 'self'}
        if attested == '' and romanized == '':
            raise ValueError(
                'A Pleiades name cannot be created if both the '
                '"attested" and "romanized" fields are blank.')
        self.__validate_attributes(**arguments)
        self.pid = pid
        self.language = language  # must be validated before attested
        self.attested = attested
        self.association_certainty = association_certainty
        self.details = details  # note that HTML is not being tested
        self.romanized = romanized
        self.slug = slug  # todo: validate uniqueness in context of parent pid
        # todo: finish setting up getter/setter for remaining attributes

    # attribute: pid (ID of Pleiades place that will be parent of this name)
    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, v):
        m = RX_PID.match(v)
        if not m:
            raise ValueError(
                'Pleiades IDs (pids) must be strings of Arabic '
                'numeral digits. "{}" does not meet this requirement.'
                ''.format(v))
        else:
            self._pid = v

    # attribute: association_certainty
    @property
    def association_certainty(self):
        return self._association_certainty

    @association_certainty.setter
    def association_certainty(self, v):
        if self.__valid_against_vocab('association_certainty', v):
            self._association_certainty = v

    # attribute: attested
    @property
    def attested(self):
        return self._attested

    @attested.setter
    def attested(self, v):
        if v != '':
            detector = LanguageDetector(v)
            languages = [l.code for l in detector.languages]
            if self.language not in languages:
                raise ValueError(
                    'The provided value for the language tag ({}) '
                    'does not match the language detected by '
                    'polyglot for the attested name form "{}."'
                    ''.format(self.language, v))
        self._attested = v  # zero-length attested is ok

    # attribute: language (IANA-registered language code)
    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, v):
        if not tags.check(v):
            raise ValueError(
                '"{}" does not validate as an IANA language tag.'
                ''.format(v))
        else:
            self._language = v

    # attribute: romanized
    @property
    def romanized(self):
        return self._romanized

    @romanized.setter
    def romanized(self, v):
        m = RX_ROMANIZED.match(v)
        if not m:
            raise ValueError(
                'A "romanized" Pleiades name string must only '
                'contain "Latin" Unicode characters and combining '
                'diacritics. "{}" does '
                'not meet this requirement.'
                ''.format(v))
        self._romanized = v  # zero-length romanized form is ok

    # attribute: slug
    @property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, v):
        if v != '':
            m = RX_SLUG.match(v)
            if not m:
                raise ValueError(
                    'Pleiades name slugs must be strings of alpha-'
                    'numeric Roman characters. "{}" does not meet '
                    'this requirement.'.format(v))
        self._slug = v  # zero-length slug is ok

    # utility methods
    # ----------------
    def __valid_against_vocab(self, vocab, term):
        if term in VOCABULARIES[vocab]:
            return True
        else:
            return False

    def __validate_attributes(self, **kwargs):
        """ Validate standard attributes of the class """

        logger = logging.getLogger(sys._getframe().f_code.co_name)
        for k, v in kwargs.items():
            logger.debug('validating "{}": "{}"'.format(k, v))
            if k == 'pid':
                pass
            elif k == 'attested':
                pass
            elif k == 'details':
                pass
            elif k == 'language':
                pass
            elif k == 'romanized':
                pass
            elif k == 'slug':
                pass
            elif k == 'summary':
                pass
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

