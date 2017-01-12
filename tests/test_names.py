from distutils.util import strtobool
import logging
from names import PleiadesName
from nose.tools import raises, assert_equal, assert_true, assert_false
import sys
from testconfig import config
from vocabularies import VOCABULARIES

PID_404 = '1'  # doesn't exist
PID_200 = '857359'  # Trapezus https://pleiades.stoa.org/places/857359

SKIP_HTTP_TESTS = bool(strtobool(config['error_handling']['skip_http_tests']))

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
    pn = PleiadesName(
        PID_404,
        language='en',
        attested='Moontown',
        summary='foo',
        skip_http_tests=SKIP_HTTP_TESTS)
    if SKIP_HTTP_TESTS:
        raise ValueError('Make test appear to pass.')


def test_instantiation_pid_good():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        skip_http_tests=SKIP_HTTP_TESTS)
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
        association_certainty='',
        skip_http_tests=SKIP_HTTP_TESTS)


@raises(ValueError)
def test_association_certainty_bad():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        association_certainty='foo',
        skip_http_tests=SKIP_HTTP_TESTS)


def test_association_certainty_good():
    vocab = VOCABULARIES['association_certainty']
    for k in vocab.keys():
        pn = PleiadesName(
            PID_200,
            summary='foo',
            attested='Moontown',
            language='en',
            association_certainty=k,
            skip_http_tests=SKIP_HTTP_TESTS)
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
            pn = PleiadesName(
                PID_200,
                skip_http_tests=SKIP_HTTP_TESTS,
                **kwargs)


# attested and romanized forms
# ---------------------------------------------------------------------------
@raises(ValueError)
def test_attested_and_romanized_blank():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='en',
        skip_http_tests=SKIP_HTTP_TESTS)


def test_attested_good():
    attested = 'Αθήνα'
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='el',
        attested=attested,
        skip_http_tests=SKIP_HTTP_TESTS)
    assert_equal(attested, pn.attested)


def test_romanized_good_ascii():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='el',
        romanized='Athena',
        skip_http_tests=SKIP_HTTP_TESTS)


def test_romanized_good_ascii_commas():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='el',
        romanized='Athena, AQHNA',
        skip_http_tests=SKIP_HTTP_TESTS)


def test_romanized_good_extended():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='mul',
        romanized='Català, Français, Kurdî, Română, Slovenščina, Türkçe',
        skip_http_tests=SKIP_HTTP_TESTS)


def test_romanized_good_combining():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='el',
        romanized='Athēna',
        skip_http_tests=SKIP_HTTP_TESTS)


@raises(ValueError)
def test_romanized_nonlatin():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        language='el',
        romanized='Ελληνικά',
        skip_http_tests=SKIP_HTTP_TESTS)


# language
# ---------------------------------------------------------------------------
@raises(ValueError)
def test_language_bad():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='barbaric nonsense',
        skip_http_tests=SKIP_HTTP_TESTS)


def test_language_all_good():
    vocab = VOCABULARIES['language']
    for k in vocab.keys():
        kwargs = {
            'language': k,
            'summary': 'foo',
            'romanized': 'Moontown',
        }
        pn = PleiadesName(
            PID_200,
            skip_http_tests=SKIP_HTTP_TESTS,
            **kwargs)


# URL slugs
# ---------------------------------------------------------------------------
@raises(ValueError)
def test_slug_bad_mixed_case():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='Moontown',
        skip_http_tests=SKIP_HTTP_TESTS)


@raises(ValueError)
def test_slug_exists():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='trapezus',
        skip_http_tests=SKIP_HTTP_TESTS)
    if SKIP_HTTP_TESTS:
        raise ValueError('Make test appear to pass.')


def test_slug_good_lower_case():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='moontown',
        skip_http_tests=SKIP_HTTP_TESTS)


@raises(ValueError)
def test_slug_bad_punctuation():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='moontown-road_turkeys',
        skip_http_tests=SKIP_HTTP_TESTS)


@raises(ValueError)
def test_slug_bad_whitespace():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='moontown road',
        skip_http_tests=SKIP_HTTP_TESTS)


def test_slug_good_hyphen():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='moontown-road',
        skip_http_tests=SKIP_HTTP_TESTS)


def test_slug_good_alphanumeric():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='moontown-3-road',
        skip_http_tests=SKIP_HTTP_TESTS)


@raises(ValueError)
def test_slug_bad_non_latin():
    pn = PleiadesName(
        PID_200,
        summary='foo',
        attested='Moontown',
        language='en',
        slug='Αθήνα',
        skip_http_tests=SKIP_HTTP_TESTS)


# completeness
def test_complete():
    pn = PleiadesName(
        PID_200,
        attested='Moontown',
        language='en',
        romanized='Moontown',
        slug='moontown',
        summary='A test name for Pleiades.',
        skip_http_tests=SKIP_HTTP_TESTS)
    assert_true(pn.complete())


def test_incomplete_slug():
    pn = PleiadesName(
        PID_200,
        attested='Moontown',
        language='en',
        romanized='Moontown',
        summary='A test name for Pleiades.',
        skip_http_tests=SKIP_HTTP_TESTS)
    assert_false(pn.complete())


def test_generate_romanized_ascii():
    pn = PleiadesName(
        PID_200,
        attested='Moontown',
        language='en',
        summary='A test name for Pleiades.',
        skip_http_tests=SKIP_HTTP_TESTS)
    pn.generate_romanized()
    assert_equal(pn.romanized, 'Moontown')


def test_generate_romanized_extended():
    pn = PleiadesName(
        PID_200,
        attested='Română',
        summary='foo',
        language='ro',
        skip_http_tests=SKIP_HTTP_TESTS)
    pn.generate_romanized()
    assert_equal(pn.romanized, 'Română, Romana')


def test_generate_romanized_preset():
    pn = PleiadesName(
        PID_200,
        attested='Română',
        romanized='Română',
        summary='foo',
        language='ro',
        skip_http_tests=SKIP_HTTP_TESTS)
    pn.generate_romanized()
    assert_equal(pn.romanized, 'Română, Romana')


def test_generate_romanized_preset2():
    pn = PleiadesName(
        PID_200,
        attested='Română',
        romanized='Romana',
        summary='foo',
        language='ro',
        skip_http_tests=SKIP_HTTP_TESTS)
    pn.generate_romanized()
    assert_equal(pn.romanized, 'Romana, Română')


def test_generate_romanized_greek():
    if not SKIP_HTTP_TESTS:
        pn = PleiadesName(
            PID_200,
            attested='Αθήνα',
            summary='foo',
            language='el',
            skip_http_tests=SKIP_HTTP_TESTS)
        pn.generate_romanized()
        assert_equal(pn.romanized, 'Athina')


def test_generate_slug_ascii():
    if not SKIP_HTTP_TESTS:
        pn = PleiadesName(
            PID_200,
            attested='Moontown',
            summary='foo',
            language='en',
            skip_http_tests=SKIP_HTTP_TESTS)
        pn.generate_slug()
        assert_equal(pn.slug, 'moontown')


def test_generate_slug_ascii_spaces():
    if not SKIP_HTTP_TESTS:
        pn = PleiadesName(
            PID_200,
            attested='Moontown Road',
            summary='foo',
            language='en',
            skip_http_tests=SKIP_HTTP_TESTS)
        pn.generate_slug()
        assert_equal(pn.slug, 'moontown-road')


def test_generate_slug_banalized():
    if not SKIP_HTTP_TESTS:
        pn = PleiadesName(
            PID_200,
            attested='Română',
            summary='foo',
            language='ro',
            skip_http_tests=SKIP_HTTP_TESTS)
        pn.generate_slug()
        assert_equal(pn.slug, 'romana')


def test_generate_slug_greek():
    if not SKIP_HTTP_TESTS:
        pn = PleiadesName(
            PID_200,
            attested='Αθήνα',
            summary='foo',
            language='el',
            skip_http_tests=SKIP_HTTP_TESTS)
        pn.generate_slug()
        assert_equal(pn.slug, 'athina')


def test_summary_ascii():
    pn = PleiadesName(
        PID_200,
        attested='Moontown',
        summary='Where oh where has my little dog gone?',
        language='en',
        skip_http_tests=SKIP_HTTP_TESTS)
    assert_equal(pn.summary, 'Where oh where has my little dog gone?')


@raises(ValueError)
def test_summary_html():
    pn = PleiadesName(
        PID_200,
        attested='Moontown',
        summary='<p><b>Where oh where</b> has my little dog gone?</p>',
        language='en',
        skip_http_tests=SKIP_HTTP_TESTS)
    assert_equal(pn.summary, 'Where oh where has my little dog gone?')


def test_details_plaintext():
    d = "It's the end of the world as we know it, and I feel fine."
    pn = PleiadesName(
        PID_200,
        attested='Moontown',
        summary='foo',
        language='en',
        details=d,
        skip_http_tests=SKIP_HTTP_TESTS)
    assert_equal(d, pn.details)


def test_details_goodhtml():
    d = "<p>It's the end of the world as we know it, and I feel fine.</p>"
    pn = PleiadesName(
        PID_200,
        attested='Moontown',
        summary='foo',
        language='en',
        details=d,
        skip_http_tests=SKIP_HTTP_TESTS)
    assert_equal(d, pn.details)


@raises(ValueError)
def test_details_badhtml():
    d = ('<p style="tuttifruti">It\'s the end of the world as we know it, and '
         ' I feel fine.</p>')
    pn = PleiadesName(
        PID_200,
        attested='Moontown',
        summary='foo',
        language='en',
        details=d,
        skip_http_tests=SKIP_HTTP_TESTS)
    assert_equal(d, pn.details)

