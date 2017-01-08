VOCABULARIES = {
    'association_certainty': {
        'certain': 'All commentators are agreed that, in antiquity, a place was '
                   'identified or located by the name or location of interest.',
        'less-certain': 'Most commentators are at least relatively certain that, '
                        'in antiquity, a place was identified or located by the '
                        'name or location of interest.',
        'uncertain': 'Commentators do not agree that, in antiquity, a place was '
                     'identified or located by the name or location of interest.'
    },
    'name_type': {
        'unknown': '',
        'geographic': '',
        'undefined': '',
        'ethnic': ''
    },
    'transcription_accuracy': {
        'accurate': '',
        'false': '',
        'inaccurate': ''
    },
    'transcription_completeness': {
        'complete': '',
        'reconstructable': '',
        'non-reconstructable': ''
    },
    'language': {
        'en': 'English',
        'ar': 'Arabic',
        'ar-Latn': 'Arabic in Latin script',
        'el': 'Modern Greek',
        'grc': 'Ancient Greek',
        'tr': 'Turkish',
        'grc-Latn': 'Ancient Greek in Latin script'
    }
}

UNICODE_RANGES = {
    'basic_latin': (r'\u0020', r'\u007F'),
    'latin_1': (r'\u00A0', r'\u00FF'),
    'latin_extended_a': (r'\u0100', r'\u017F'),
    'latin_extended_b': (r'\u0180', r'\u024F'),
    'latin_extended_additional': (r'\u1E00', r'\u1EFF'),
    'combining_diacritical_marks': (r'\u0300', r'\u036F')
}
