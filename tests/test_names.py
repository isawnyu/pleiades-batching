from names import PleiadesName
from nose.tools import raises, assert_equal, assert_true, assert_false
from vocabularies import VOCABULARIES

PID_404 = '1'  # doesn't exist
PID_200 = '857359'  # Trapezus https://pleiades.stoa.org/places/857359

# Pleiades IDs (pid)
# ---------------------------------------------------------------------------
@raises(TypeError)
def test_instantiation_pid_none():
    pn = PleiadesName()


@raises(ValueError)
def test_instantiation_pid_empty():
    pn = PleiadesName('', language='en', attested='Moontown', summary='foo')


@raises(ValueError)
def test_instantiation_pid_bad():
    pn = PleiadesName(
        '5fid&', language='en', attested='Moontown', summary='foo')


@raises(ValueError)
def test_instantiation_pid_404():
    pn = PleiadesName(PID_404, language='en', attested='Moontown', summary='foo')


def test_instantiation_pid_good():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en')
    assert_equal(PID_200, pn.pid)


# association certainty
# ---------------------------------------------------------------------------
@raises(ValueError)
def test_association_certainty_empty():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        association_certainty='')


@raises(ValueError)
def test_association_certainty_bad():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        association_certainty='foo')


def test_association_certainty_good():
    vocab = VOCABULARIES['association_certainty']
    for k in vocab.keys():
        pn = PleiadesName(
            PID_200,
            summary='foo',
            attested='Moontown',
            language='en',
            association_certainty=k)
        assert_equal(k, pn.association_certainty)


# all vocabularies (other than language)
# ---------------------------------------------------------------------------
def test_vocabs_all_good():
    for v_key, vocab in VOCABULARIES.items():
        if v_key == 'language':
            continue
        for k in vocab.keys():
            kwargs = {
                v_key: k,
                'summary': 'foo',
                'attested': 'Moontown',
                'language': 'en',
            }
            pn = PleiadesName(PID_200, **kwargs)


# attested and romanized forms
# ---------------------------------------------------------------------------
@raises(ValueError)
def test_attested_and_romanized_blank():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='en')


def test_attested_good():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='el',
        attested='Αθήνα')
    assert_equal('Αθήνα', pn.attested)


def test_romanized_good_ascii():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='el',
        romanized='Athena')


def test_romanized_good_ascii_commas():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='el',
        romanized='Athena, AQHNA')


def test_romanized_good_extended():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='mul',
        romanized='Català, Français, Kurdî, Română, Slovenščina, Türkçe')


def test_romanized_good_combining():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='el',
        romanized='Athēna')


@raises(ValueError)
def test_romanized_nonlatin():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='el',
        romanized='Ελληνικά')


# language
# ---------------------------------------------------------------------------
@raises(ValueError)
def test_language_bad():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='barbaric nonsense')


def test_language_all_good():
    vocab = VOCABULARIES['language']
    for k in vocab.keys():
        kwargs = {
            'language': k,
            'summary': 'foo',
            'romanized': 'Moontown',
        }
        pn = PleiadesName(PID_200, **kwargs)


# URL slugs
# ---------------------------------------------------------------------------
@raises(ValueError)
def test_slug_bad_mixed_case():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='Moontown')


@raises(ValueError)
def test_slug_exists():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='trapezus')


def test_slug_good_lower_case():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='moontown')


@raises(ValueError)
def test_slug_bad_punctuation():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='moontown-road_turkeys')


@raises(ValueError)
def test_slug_bad_whitespace():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='moontown road')


def test_slug_good_hyphen():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='moontown-road')


def test_slug_good_alphanumeric():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='moontown-3-road')


@raises(ValueError)
def test_slug_bad_non_latin():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='Αθήνα')


# completeness
def test_complete():
    pn = PleiadesName(
        PID_200,
        attested='Moontown',
        language='en',
        romanized='Moontown',
        slug='moontown',
        summary='A test name for Pleiades.')
    assert_true(pn.complete())


def test_incomplete():
    pn = PleiadesName(
        PID_200,
        attested='Moontown',
        language='en',
        romanized='Moontown',
        summary='A test name for Pleiades.')
    assert_false(pn.complete())
