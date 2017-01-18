"""Construct and validate data for Pleiades name resources.

Defines the class PleiadesName, whose attributes and methods constitute the
full capabilities of this module.

"""
import bleach
import html2text
import inspect
from language_tags import tags as language_tags
import logging
from polyglot.detect import Detector as LanguageDetector
from polyglot.transliteration import Transliterator
from pprint import pprint
import re
import requests
from requests.exceptions import ConnectionError
import requests_cache
import string
import sys
import unicodedata
from unidecode import unidecode
from urllib.error import URLError
from vocabularies import VOCABULARIES, UNICODE_RANGES

requests_cache.install_cache(backend='memory')
requests_cache.clear()

# polyglot is overly chatty with warnings; shut it up
logging.getLogger('polyglot.detect.base').setLevel('CRITICAL')

RX_PID = re.compile('^\d+$')
RX_SLUG = re.compile('^[a-z\-\d]+$')
RX_ROMANIZED = r''
for k, v in UNICODE_RANGES.items():
    if 'latin' in k or k == 'combining_diacritical_marks':
        RX_ROMANIZED += r'{}-{}'.format(*v)
RX_ROMANIZED = re.compile('^[{}]*$'.format(RX_ROMANIZED))
PLEIADES_BASE_URL = 'https://pleiades.stoa.org'
PLEIADES_PLACES_URL = '/'.join((PLEIADES_BASE_URL, 'places'))
NONZERO = [
    'pid',
    'association_certainty',
    'language',
    'name_type',
    'romanized',
    'slug',
    'summary',
    'transcription_accuracy',
    'transcription_completeness',
]
NOPUNCT = str.maketrans(
    {key: None for key in string.punctuation if key != "-"})
ALLOWED_TAGS = bleach.ALLOWED_TAGS
ALLOWED_TAGS.extend(['p'])


class PleiadesName:
    """Create, validate, and enhance data for a Pleiades name resource."""

    def __init__(
        self, pid: str, *,
        association_certainty: str = 'certain',
        attested: str = '',
        details: str = '',
        language: str,  # cannot be zero-length
        name_type: str = 'geographic',
        romanized: str = '',
        slug: str = '',
        summary: str = '',
        time_periods: list = [],
        transcription_accuracy: str = 'accurate',
        transcription_completeness: str = 'complete',
        creators: str = '',
        contributors: str = '',
        skip_http_tests=False,
        ignore_unicode_errors=False
    ):
        """Construct a PleiadesName object.

        Args:
            pid (required): Pleiades Identifier with which this name is
                associated ("the parent place")
            association_certainty*: confidence in associating name with place
            attested: name form found in witness(es)
            details: extended discussion
            language (required)*: IANA-registered language tag for attested
                form
            name_type: the type of name described by this resource
            romanized: romanized form(s) of the attested name
            slug: a URL slug to be used to identify this name resource
            summary: short summary explaining nature of this name
                resource
            transcription_accuracy*: assessment of accuracy of witness in
                transmitting this name
            transcription_completeness*: is the name as transmitted by the
                witnesses fragmentary or complete?

        * values for attributes marked with an asterisk above must be
          drawn from an appropriate Pleiades project vocabulary. These
          are imported from the "vocabularies" module.

        Exceptions raised:
            - TypeError: omission of required attributes or use of unexpected
              object types for attribute values.
            - ValueError: use of invalid values for attributes.

        """
        self._skip_http_tests = skip_http_tests
        self.pid = pid
        self.language = language
        self.attested = attested
        self.association_certainty = association_certainty
        self.details = details
        self.name_type = name_type
        self.romanized = romanized
        self.slug = slug
        self.summary = summary
        self.transcription_accuracy = transcription_accuracy
        self.transcription_completeness = transcription_completeness
        if attested == '' and romanized == '':
            raise ValueError(
                'A Pleiades name cannot be created if both the '
                '"attested" and "romanized" fields are blank.')

    # attribute: pid (ID of Pleiades place that will be parent of this name)
    @property
    def pid(self):
        """Get the vale of the object's 'pid' attribute."""
        return self._pid

    @pid.setter
    def pid(self, v: str):
        """Set the value of the object's 'pid' attribute.

        Args:
            v: value to use

        Exceptions raised:
            - ValueError: the provided string does not conform to
              restrictions on Pleiades IDs, i.e., a string of Arabic numeral
              digits.

        """
        w = self.__normalize_space(v)
        self._pid = w
        m = RX_PID.match(w)
        if not m:
            raise ValueError(
                'Pleiades IDs (pids) must be strings of Arabic '
                'numeral digits. "{}" does not meet this requirement.'
                ''.format(w))
        elif self._skip_http_tests:
            logger_name = ':'.join(
                (__name__, inspect.currentframe().f_code.co_name))
            logger = logging.getLogger(logger_name)
            logger.warning(
                'Skipping HTTP test on pid="{}".'
                ''.format(w))
        else:
            p_url = '/'.join((PLEIADES_PLACES_URL, w, 'json'))
            try:
                success = self.__fetch('pid', p_url)
            except:
                raise
            else:
                if not success:
                    raise ValueError(
                        'Pleiades pid "{}" does not seem to have a '
                        'corresponding place resource in Pleiades; therefore '
                        'it cannot be the parent pid of a name resource.'
                        ''.format(w))

    # attribute: association_certainty
    @property
    def association_certainty(self):
        """Get the value of the object's 'association_certainty' attribute."""
        return self._association_certainty

    @association_certainty.setter
    def association_certainty(self, v: str):
        """Set the value of the object's 'association_certainty' attribute.

        Args:
            v: value to use

        Exceptions raised:
            - ValueError: the provided string does not appear as a term in the
              Pleiades "association certainty" vocabulary, and is therefore
              invalid.

        """
        w = self.__normalize_space(v)
        self._association_certainty = w
        self.__valid_against_vocab('association_certainty', w)

    # attribute: attested
    @property
    def attested(self):
        """Get the value of the object's 'attested' attribute."""
        return self._attested

    @attested.setter
    def attested(self, v: str):
        """Set the value of the object's "attested" attribute.

        Args:
            v: value to use

        Exceptions raised:
            - ValueError: v is non-zero length, but when the language
              detection algorithm included in the "polyglot" package is run
              against its contents, none of the possible language matches
              identified by that algorithm corresponds to the value in the
              object's "language" attribute. NB: this is why self.__init__
              sets the "language" attribute before it sets the "attested"
              attribute.

        """
        w = self.__normalize_space(v)
        if w != '':
            normed = self.__normalize_unicode(w)
            self._attested = normed
            if normed != v:
                logger_name = ':'.join(
                    (__name__, inspect.currentframe().f_code.co_name))
                logger = logging.getLogger(logger_name)
                logger.info(
                    'Attested name form "{}" was normalized to the '
                    'Unicode canonical composition form "{}".'
                    ''.format(w, normed))
            detector = LanguageDetector(normed)
            languages = [l.code for l in detector.languages if l.code != 'un']
            if detector.reliable:
                if self.language not in languages:
                    raise ValueError(
                        'The provided value for the language tag ({}) '
                        'does not match the language detected by '
                        'polyglot for the attested name form "{}." '
                        'Possibilities include: {}.'
                        ''.format(self.language, w, '" or "'.join(languages)))
            else:
                logger_name = ':'.join(
                    (__name__, inspect.currentframe().f_code.co_name))
                logger = logging.getLogger(logger_name)
                logger.info(
                    'Skipping language verification for "{}" because polyglot '
                    'thinks its identification ("{}") is unreliable.'
                    ''.format(w, '" or "'.join(languages)))
        else:
            self._attested = w

    # attribute: details
    @property
    def details(self):
        """Get the value of the object's "details" attribute."""
        return self._details

    @details.setter
    def details(self, v: str):
        """Set the value of the object's "details" attribute."""
        w = self.__normalize_space(self.__normalize_unicode(v))
        x = bleach.clean(w, strip=True)
        x = self.__normalize_space(x)
        self._details = x
        if x != w:
            logger_name = ':'.join(
                (__name__, inspect.currentframe().f_code.co_name))
            logger = logging.getLogger(logger_name)
            logger.info(
                'Details was sanitized. Result: \n{}'.format(x))

    # attribute: language (IANA-registered language code)
    @property
    def language(self):
        """Get the value of the object's "language" attribute."""
        return self._language

    @language.setter
    def language(self, v: str):
        """Set the value of the object's "language" attribute.

        Args:
            v: value to use

        Exceptions raised:
            - ValueError: the value in v is not a valid language subtag as
              determined by the "language_tags" module.

        """
        w = self.__normalize_space(v)
        self._language = w
        if not language_tags.check(w):
            raise ValueError(
                '"{}" does not validate as an IANA language tag.'
                ''.format(w))

    # read-only attribute: language_script
    @property
    def language_script(self):
        try:
            # get script subtag that is explicit in the tag
            iana_script = language_tags.tag(self.language).script.format
        except AttributeError:
            # there was no explicit script subtag
            try:
                # get default script subtag (suppress script)
                iana_script = language_tags.language(self.language).script
            except:
                raise
        return str(iana_script)

    # attribute: name_type
    @property
    def name_type(self):
        """Get the value of the object's 'name_type' attribute."""
        return self._name_type

    @name_type.setter
    def name_type(self, v: str):
        """Set the value of the object's 'name_type' attribute.

        Args:
            v: value to use

        Exceptions raised:
            - ValueError: the provided string does not appear as a term in the
              Pleiades "name type" vocabulary, and is therefore
              invalid.

        """
        w = self.__normalize_space(v)
        self._name_type = w
        self.__valid_against_vocab('name_type', w)

    # attribute: romanized
    @property
    def romanized(self):
        """Get the value of the object's "romanized" attribute."""
        return self._romanized

    @romanized.setter
    def romanized(self, v: str):
        """Set the value of the object's 'romanized' attribute.

        Args:
            v: value to use

        Exceptions raised:
            - ValueError: the provided string does not conform to
              restrictions on Romanized name forms for Pleiades, i.e., only
              Latinate (Roman) characters, combining diacriticals, and
              associated punctuation marks may be used.

        """
        w = self.__normalize_space(v)
        if w != '':
            normed = self.__normalize_unicode(w)
            self._romanized = normed
            if normed != w:
                logger_name = ':'.join(
                    (__name__, inspect.currentframe().f_code.co_name))
                logger = logging.getLogger(logger_name)
                logger.info(
                    'Romanized name form "{}" was normalized to the '
                    'Unicode canonical composition form "{}".'
                    ''.format(w, normed))
            m = RX_ROMANIZED.match(normed)
            if not m:
                raise ValueError(
                    'A "romanized" Pleiades name string must only '
                    'contain "Latin" Unicode characters and combining '
                    'diacritics. "{}" does '
                    'not meet this requirement.'
                    ''.format(normed))
        else:
            self._romanized = w  # zero-length romanized form is ok

    # attribute: slug
    @property
    def slug(self):
        """Get the value of the object's "slug" attribute."""
        return self._slug

    @slug.setter
    def slug(self, v: str):
        """Set the value of the object's "slug" attribute.

        Args:
            v: value to use

        Exceptions raised:
            - ValueError: the provided string does not conform to
              restrictions on URL slugs for Pleiades name resources, i.e., only
              lower-case ASCII characters, hyphens, and Arabic numeral digits
              may be used.

        """
        w = self.__normalize_space(v)
        self._slug = w
        if w != '':
            m = RX_SLUG.match(w)
            if not m:
                raise ValueError(
                    'Pleiades name slugs must be strings of alpha-'
                    'numeric Roman characters. "{}" does not meet '
                    'this requirement.'.format(w))
            elif self._skip_http_tests:
                logger_name = ':'.join(
                    (__name__, inspect.currentframe().f_code.co_name))
                logger = logging.getLogger(logger_name)
                logger.warning(
                    'Skipping slug validation via HTTP for "{}".'
                    ''.format(w))
            else:
                p_url = '/'.join((PLEIADES_PLACES_URL, self.pid, w))
                try:
                    success = self.__fetch('slug', p_url)
                except:
                    raise
                else:
                    if success:
                        raise ValueError(
                            'The specified slug ({}) already exists in '
                            'Pleiades ({}).'
                            ''.format(w, p_url))

    # attribute: summary
    @property
    def summary(self):
        """Get the value of the object's "summary" attribute."""
        return self._summary

    @summary.setter
    def summary(self, v: str):
        """Set the value of the object's "summary" attribute.

        Args:
            v: value to use

        Exceptions raised:
            - ValueError: the provided string does not conform to
              restrictions on URL slugs for Pleiades name resources, i.e.,
              plain text.

        """
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_emphasis = True
        h.body_width = 0
        w = h.handle(v).strip()
        self._summary = self.__normalize_space(self.__normalize_unicode(w))
        if w != v:
            raise ValueError(
                'Value provided for summary "{}" appears not to be plain '
                'text; rather, it appears to be HTML.')

    # attribute: time_periods
    @property
    def time_periods(self):
        """Get the value of the object's "time_periods" attribute."""
        return self._time_periods

    @time_periods.setter
    def time_periods(self, periods: list):
        """Set the value of the object's "time_periods" attribute."""
        for p in periods:
            q = self.__normalize_space(p)
            try:
                self.__valid_against_vocab('time-periods', q)
            except ValueError:
                raise
            else:
                try:
                    self._time_periods.append(q)
                except ValueError:
                    self._time_periods = [q]

    # attribute: transcription_accuracy
    @property
    def transcription_accuracy(self):
        """Get the value of the object's "transcription_accuracy" attribute."""
        return self._transcription_accuracy

    @transcription_accuracy.setter
    def transcription_accuracy(self, v: str):
        """Set the value of the object's "transcription_accuracy" attribute.

        Args:
            v: value to use

        Exceptions raised:
            - ValueError: the provided string does not appear as a term in the
              Pleiades "transcription accuracy" vocabulary, and is therefore
              invalid.

        """
        w = self.__normalize_space(v)
        self._transcription_accuracy = w
        self.__valid_against_vocab('transcription_accuracy', w)

    # attribute: transcription_completeness
    @property
    def transcription_completeness(self):
        """Get the value of the "transcription_completeness" attribute."""
        return self._transcription_completeness

    @transcription_completeness.setter
    def transcription_completeness(self, v: str):
        """Set the value of the object's "transcription_completeness" attribute.

        Args:
            v: value to use

        Exceptions raised:
            - ValueError: the provided string does not appear as a term in the
              Pleiades "transcription completeness" vocabulary, and is
              therefore invalid.

        """
        w = self.__normalize_space(v)
        self._transcription_completeness = w
        self.__valid_against_vocab('transcription_completeness', w)

    # public methods
    def complete(self):
        """Test and report completeness of the name resource."""

        for field in NONZERO:
            v = getattr(self, field)
            if v == '':
                return False
        if self.attested == '' and self.romanized == '':
            return False
        return True

    def generate_romanized(self):
        """Generate a romanized form from the attested form."""

        r = []
        if self.romanized != '':
            r = [n.strip() for n in self.romanized.split(',')]
        iana_script = self.language_script
        if iana_script == 'Latn':
            if self.attested not in r:
                r.append(self.attested)
            b = unicodedata.normalize(
                'NFC', unidecode(
                    unicodedata.normalize('NFKD', self.attested)))
            if b not in r:
                r.append(b)
        else:
            try:
                transliterator = Transliterator(
                    source_lang=self.language, target_lang='en')
            except URLError:
                logger_name = ':'.join(
                    (__name__, inspect.currentframe().f_code.co_name))
                logger = logging.getLogger(logger_name)
                msg = (
                    'The "polyglot" transliteration module '
                    'encountered an error trying to do something with a URL, '
                    'so its use in romanized form creation is not possible.')
                if not self._skip_http_tests:
                    logger.error(msg)
                    raise
                else:
                    logger.warning(msg)
            else:
                t = transliterator.transliterate(self.attested)
                t = string.capwords(t)
                if t not in r:
                    r.append(t)
        self.romanized = ', '.join(r)

    def generate_slug(self):
        """Generate URL slug."""
        logger_name = ':'.join(
            (__name__, inspect.currentframe().f_code.co_name))
        logger = logging.getLogger(logger_name)
        if self.romanized == '':
            self.generate_romanized()
        names = [n.strip() for n in self.romanized.split(',')]
        logger.debug('names: {}'.format(names))
        s = unicodedata.normalize(
            'NFC', unidecode(
                unicodedata.normalize('NFKD', names[0])))
        s = s.lower().translate(NOPUNCT).split()
        s = '-'.join(s).encode('ascii', 'xmlcharrefreplace')
        self.slug = s.decode('ascii')

    def generate_summary(self):
        """Generate an abstract/summary for this name resource."""
        logger_name = ':'.join(
            (__name__, inspect.currentframe().f_code.co_name))
        logger = logging.getLogger(logger_name)
        p_url = '/'.join((PLEIADES_PLACES_URL, self.pid, 'json'))
        place = self.__fetch('pid', p_url).json()
        logger.debug('language tag: {}'.format(self.language))
        lang_desc = language_tags.description(self.language)
        if len(lang_desc) > 1 and '-' in self.language:
            lang_desc = self.language.split('-')
            script_desc = [l for l in lang_desc if len(l) == 4]
            lang_desc = [l for l in lang_desc if len(l) < 4 and l.lower() == l]
            lang_desc = language_tags.description(lang_desc[0])[0]
            script_desc = language_tags.description(script_desc[0])[0]
            lang_chunk = (
                '{}-language name in {} script'
                ''.format(lang_desc, script_desc))
        else:
            lang_desc = lang_desc[0]
            script_desc = ''
            lang_chunk = '{}-language name'.format(lang_desc)
        title = place['title']
        if title in lang_chunk:
            title_chunk = ''
        else:
            title_chunk = 'associated with {}'.format(title)
        summary = (' '.join((lang_chunk, title_chunk)))
        if summary[-1] != '.':
            summary += '.'
        self.summary = summary

    # internal utility methods
    def __fetch(self, name: str, url: str):
        """Fetch an item from the web and handle associated errors.

        Args:
            name: Name of the item being fetched (for error message purposes)
            url: URL to try to fetch

        Returns:
            True: if the response includes 200 or if a connection error occurs
                  but self.ignore_http_tests == True
            False:

        """
        try:
            r = requests.get(url)
        except ConnectionError:
            logger_name = ':'.join(
                (__name__, inspect.currentframe().f_code.co_name))
            logger = logging.getLogger(logger_name)
            if not self._skip_http_tests:
                logger.error(
                    'Encountered a web connection error trying to fetch URL '
                    '({}) for "{}".'.format(url, name))
                raise
            else:
                logger = logging.getLogger(logger_name)
                logger.warning(
                    'Ignored connection error while attempting to fetch '
                    'URL ({}) for "{}".'
                    ''.format(url, name))
                return True
        else:
            if r.status_code == requests.codes.ok:
                return r
            else:
                return False

    def __normalize_space(self, v: str):
        """Normalize space."""
        return ' '.join(v.split()).strip()

    def __normalize_unicode(self, v: str):
        """Normalize Unicode."""
        canonical = unicodedata.normalize('NFC', v)
        compatibility = unicodedata.normalize('NFKC', v)
        if canonical != compatibility:
            msg = (
                'Unicode normalization may have changed the string "{}" in '
                'an undesireable way. The canonical composition form (NFC: '
                '"{}") does not match the compatibility composition form ('
                'NFKC: "{}"). NFC is being used.')
            if self.ignore_unicode_errors:
                logger = logging.getLogger(logger_name)
                logger.warning(msg)
            else:
                raise ValueError(msg)
        return canonical

    def __valid_against_vocab(self, vocab_name: str, term: str):
        """Validate a vocabulary term.

        Args:
            vocab: Name of the vocabulary against which to validate. Must be
                   a key in the VOCABULARIES dictionary imported from the
                   vocabularies module.
            term: Vocabulary term to validate. Must be a key within the
                  vocabulary dictionary returned by VOCABULARIES[vocab].

        Returns:
            True if the term is valid for the requested vocabulary. Raises
            ValueError if not.

        """
        vocab = VOCABULARIES[vocab_name]
        if term in vocab.keys():
            return True
        else:
            raise ValueError(
                'PleiadesName attribute "{}" must be a string '
                'containing a value from the list: "{}." '
                'The provided value ("{}") does not meet this '
                'requirement.'
                ''.format(vocab_name, '", "'.join(vocab.keys()), term))
