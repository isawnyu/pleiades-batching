from language_tags import tags
from polyglot.detect import Detector as LanguageDetector
import re
from vocabularies import VOCABULARIES, UNICODE_RANGES

RX_PID = re.compile('^\d+$')
RX_SLUG = re.compile('^[a-z\-\d]+$')
RX_ROMANIZED = r''
for k, v in UNICODE_RANGES.items():
    if 'latin' in k or k == 'combining_diacritical_marks':
        RX_ROMANIZED += r'{}-{}'.format(*v)
RX_ROMANIZED = re.compile('^[{}]*$'.format(RX_ROMANIZED))


class PleiadesName:
    """ a class for validating and fleshing-out a Pleiades name resource
        Args:
            self
            pid: Pleiades Identifier with which this name is associated
            associated_certainty: confidence in associating name with place(*)
            attested: name form found in witness(es)
            details: extended discussion
            language: IANA-registered language tag for attested form
            name_type: the type of name described by this resource(*)
            romanized: romanized form(s) of the attested name
            slug: a URL slug to be used to identify this name resource
            summary: short summary explaining nature of this name resource
            transcription_accuracy: assessment of accuracy of witness in
                                    transmitting this name(*)
            transcription_completeness: is the name as transmitted by the
                                        witnesses fragmentary or complete?(*)

            * - values for attributes marked with an asterisk above must be
                drawn from an appropriate Pleiades project vocabulary. These
                are imported from the "vocabularies" module.
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
        summary: str,  # cannot be zero-length
        transcription_accuracy: str = 'accurate',
        transcription_completeness: str = 'complete'
    ):
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

    # attribute: transcription_accuracy
    @property
    def transcription_accuracy(self):
        return self._transcription_accuracy

    @transcription_accuracy.setter
    def transcription_accuracy(self, v):
        if self.__valid_against_vocab('transcription_accuracy', v):
            self._transcription_accuracy = v

    # attribute: transcription_accuracy
    @property
    def transcription_accuracy(self):
        return self._transcription_accuracy

    @transcription_accuracy.setter
    def transcription_accuracy(self, v):
        if self.__valid_against_vocab('transcription_accuracy', v):
            self._transcription_accuracy = v

    # attribute: transcription_completeness
    @property
    def transcription_completeness(self):
        return self._transcription_completeness

    @transcription_completeness.setter
    def transcription_completeness(self, v):
        if self.__valid_against_vocab('transcription_completeness', v):
            self._transcription_completeness = v

    # internal utility methods
    # ----------------
    def __valid_against_vocab(self, vocab, term):
        """Internal utility method used to validate a vocabulary term"""
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
