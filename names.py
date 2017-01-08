"""Construct and validate data for Pleiades name resources.

Defines the class PleiadesName, whose attributes and methods constitute the
full capabilities of this module.

"""
from language_tags import tags as language_tags
from polyglot.detect import Detector as LanguageDetector
import re
import requests
from vocabularies import VOCABULARIES, UNICODE_RANGES

RX_PID = re.compile('^\d+$')
RX_SLUG = re.compile('^[a-z\-\d]+$')
RX_ROMANIZED = r''
for k, v in UNICODE_RANGES.items():
    if 'latin' in k or k == 'combining_diacritical_marks':
        RX_ROMANIZED += r'{}-{}'.format(*v)
RX_ROMANIZED = re.compile('^[{}]*$'.format(RX_ROMANIZED))
PLEIADES_BASE_URL = 'https://pleiades.stoa.org'
PLEIADES_PLACES_URL = '/'.join((PLEIADES_BASE_URL, 'places'))


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
        summary: str,  # cannot be zero-length
        transcription_accuracy: str = 'accurate',
        transcription_completeness: str = 'complete'
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
            summary (required): short summary explaining nature of this name
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
        if attested == '' and romanized == '':
            raise ValueError(
                'A Pleiades name cannot be created if both the '
                '"attested" and "romanized" fields are blank.')
        self.pid = pid
        self.language = language  # must be validated before attested
        self.attested = attested
        self.association_certainty = association_certainty
        self.details = details  # note that HTML is not being tested
        self.romanized = romanized
        self.slug = slug  # todo: validate uniqueness in context of parent pid
        self.transcription_accuracy = transcription_accuracy
        self.transcription_completeness = transcription_completeness

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
        m = RX_PID.match(v)
        if not m:
            raise ValueError(
                'Pleiades IDs (pids) must be strings of Arabic '
                'numeral digits. "{}" does not meet this requirement.'
                ''.format(v))
        else:
            p_url = '/'.join((PLEIADES_PLACES_URL, v, 'json'))
            r = requests.get(p_url)
            if r.status_code != requests.codes.ok:
                raise ValueError(
                    'The specified pid ({}) does not seem to exist in '
                    'Pleiades. Instead of the expected "200 OK" response, a '
                    'GET request for "{}" yielded "{}".'
                    ''.format(v, p_url, r.status_code))
            else:
                self._pid = v

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
        if self.__valid_against_vocab('association_certainty', v):
            self._association_certainty = v

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
        if not language_tags.check(v):
            raise ValueError(
                '"{}" does not validate as an IANA language tag.'
                ''.format(v))
        else:
            self._language = v

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
        if v != '':
            m = RX_SLUG.match(v)
            if not m:
                raise ValueError(
                    'Pleiades name slugs must be strings of alpha-'
                    'numeric Roman characters. "{}" does not meet '
                    'this requirement.'.format(v))
        self._slug = v  # zero-length slug is ok

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
        if self.__valid_against_vocab('transcription_accuracy', v):
            self._transcription_accuracy = v

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
        if self.__valid_against_vocab('transcription_completeness', v):
            self._transcription_completeness = v

    # internal utility methods
    # ----------------
    def __valid_against_vocab(self, vocab: str, term: str):
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
        vocab = VOCABULARIES[vocab]
        if term in vocab.keys():
            return True
        else:
            raise ValueError(
                'PleiadesName attribute "{}" must be a string '
                'containing a value from the list: "{}." '
                'The provided value ("{}") does not meet this '
                'requirement.'
                ''.format(vocab, '", "'.join(vocab.keys()), term))
