"""Defines vocabularies used in pleiades-batching tools."""

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
    },
    'time_periods': {
        'paleolithic-middle-east': 'ME [[-2600000,-18000]]',
        'copy_of_paleolithic-middle-east': 'Middle East [[-2600000,-18000]]',
        'stone-age-oman': 'Persian Gulf [[-125000,-3200]]',
        'mesolithic-levant': 'Epipaleolithic-Protoneolithic Levant, Kebaran-Natufian [[-18000,-9500]]',
        'mesolithic-middle-east': 'Epipaleolithic-Protoneolithic ME [[-18000,-9000]]',
        'copy_of_mesolithic-middle-east': 'Epipaleolithic-Protoneolithic ME [[-18000,-9000]]',
        'mesolithic-europe-13-000-8-000-bc': 'The cultural period lying between paleolithic and neolithic, as described at https://en.wikipedia.org/wiki/Mesolithic [[-13000,-8000]]',
        'natufian-levant': 'Levant [[-12500,-9500]]',
        'neolithic-eastern-med': 'The so-called "Neolithic" or "New Stone Age" period as defined in the Eastern portion of the Mediterranean basin, lasting roughly from 10,000 - 3,300 BC. See further: http://ancienthistory.about.com/od/artarchaeologyarchitect/g/neolithic.htm [[-10000, -3300]]',
        'pre-pottery-neolithic-middle-east': 'Aceramic Neolithic ME [[-9000,-6000]]',
        'neolithic-middle-east': 'ME [[-9000,-4500]]',
        'ubaid': 'The prehistoric Ubaid period of Mesopotamia, as defined by Wikipedia following Carter, Robert A. and Philip, Graham Beyond the Ubaid: Transformation and Integration in the Late Prehistoric Societies of the Middle East (Studies in Ancient Oriental Civilization, Number 63) The Oriental Institute of the University of Chicago (2010) ISBN 978-1-885923-66-0 p.2, at http://oi.uchicago.edu/research/pubs/catalog/saoc/saoc63.html [[-6500, -3800]]',
        'chalcolithic-mesopotamia': 'Copper Age Mesopotamia, Halaf-Ubaid-Early Uruk Mesopotamia [[-6200,-3750]]',
        'neolithic-egypt': 'The Neolithic period in Egypt, following the chronology of the UCLA Encyclopedia of Egyptology (compiled by Thomas Schneider): http://www.uee.ucla.edu/contributors/chronology.htm. [[-6000, -4500]]',
        'pottery-neolithic-middle-east': 'ME [[-6000,-4500]]',
        'ubaid-early-dynastic-ii-mesopotamia': 'Late Chalcolithic-ED II Mesopotamia, Ubaid-Uruk-Jemdet Nasr-ED Mesopotamia [[-5500,-2600]]',
        'neolithic-malta': 'The neolithic or so-called "New Stone Age" as expressed in remains of physical culture on the island of Malta, where it appears to have lasted from around 5,000 to 2,500 BC [[-5000, -2500]]',
        'chalcolithic-iran': 'Iran [[-5000,-2500]]',
        'predynastic-egypt': 'The predynastic period in Egypt, following the chronology of the UCLA Encyclopedia of Egyptology (compiled by Thomas Schneider): http://www.uee.ucla.edu/contributors/chronology.htm. [[-4500, -2950]]',
        '4th-millenium-bce': 'The fourth millenium BCE as defined at http://en.wikipedia.org/wiki/4th_millennium_BC [[-4000, -3000]]',
        'neolithic-british': 'The Neolithic period in the British Isles, after Wikipedia, Neolithic British Isles, http://en.wikipedia.org/wiki/Neolithic_British_Isles. [[-4000, -2500]]',
        'uruk-mesopotamia': 'Protoliterate Mesopotamia [[-4000,-2950]]',
        'old-nubian': 'A-Group/Old Nubian--Middle Nubian--OK [[-3800,-2300]]',
        'early-bronze-age-southern-levant': 'southern Levant [[-3300,-2000]]',
        'elamite-western-iran': 'Proto--Old--Middle--Neo-Elamite [[-3200,-540]]',
        'early-minoan': 'Early Minoan period on Crete, after Shelmerdine, The Cambridge Companion to the Aegean Bronze Age, Cambridge UP, 2008. PeriodO URI: http://n2t.net/ark:/99152/p0qp9rs8fgh. [[-3100,-2000]]',
        'early-helladic': 'The Early Helladic period in the Greek mainland, after Preziosi and Hitchcock, Aegean Art and Architecture, Oxford History of Art, 1998. [[-3000,-2000]]',
        '3rd-millennium-bc': 'The 3rd millennium BC spans the Early to Middle Bronze Age. As described at http://en.wikipedia.org/wiki/3rd_millennium_BC. [[-3000, -2000]]',
        'early-dynastic-egypt': 'The Early Dynastic period in Egypt, following the chronology of the UCLA Encyclopedia of Egyptology (compiled by Thomas Schneider): http://www.uee.ucla.edu/contributors/chronology.htm. [[-2950, -2670]]',
        'early-dynastic-mesopotamia': 'Mesopotamia [[-2950,-2350]]',
        'old-kingdom-egypt': 'The Old Kingdom period in Egypt, following the chronology of the UCLA Encyclopedia of Egyptology (compiled by Thomas Schneider): http://www.uee.ucla.edu/contributors/chronology.htm. [[-2670, -2168]]',
        'bronze-age-oman': 'Persian Gulf [[-2600,-1900]]',
        'bronze-age-britain': 'A long time period associated with Bronze Age Britain. [[-2500, -800]]',
        'bronze-age-malta': 'The Bronze age as represented in the remains of physical culture from the island of Malta. [[-2500, -700]]',
        'early-bronze-age-iran': 'Jiroft [[-2500,-2000]]',
        'early-middle-bronze-age-iran': 'Iran [[-2500,-1500]]',
        'akkadian-ur-iii-mesopotamia': 'Akkadian--Neo-Sumerian Mesopotamia [[-2335,-2000]]',
        'middle-nubian': 'C-Group--Kerma--Middle Nubian--Pan-Grave--MK [[-2300,-1600]]',
        'first-intermediate-period-egypt': 'The First Intermediate Period in Egypt, following the chronology of the UCLA Encyclopedia of Egyptology (compiled by Thomas Schneider): http://www.uee.ucla.edu/contributors/chronology.htm. [[-2168, -2010]]',
        'transition-early-middle-bronze-age-southern-levant': 'southern Levant [[-2100,-1900]]',
        'middle-kingdom-egypt': 'The Middle Kingdom period in Egypt, following the chronology of the UCLA Encyclopedia of Egyptology (compiled by Thomas Schneider): http://www.uee.ucla.edu/contributors/chronology.htm. [[-2010, -1640]]',
        '2nd-millenium-bce': 'The second millenium BCE as defined at http://en.wikipedia.org/wiki/2nd_millennium_BC [[-2000, -1000]]',
        'middle-helladic': 'The Middle Helladic period in the Greek mainland, after Preziosi and Hitchcock, Aegean Art and Architecture, Oxford History of Art, 1998. [[-2000, -1600]]',
        'early-bronze-age-anatolia': 'Karum Anatolia [[-2000,-1750]]',
        'old-babylonian-assyrian-mesopotamia': 'Mesopotamia [[-2000,-1600]]',
        'middle-bronze-age-iran': 'Iran [[-2000,-1500]]',
        'middle-bronze-age-southern-levant': 'southern Levant [[-2000,-1400]]',
        '2nd-millennium-bc-egypt': 'Egypt [[-2000,-1000]]',
        '2nd-millennium-bc-levant': 'MBA Levant-LBA Levant-Iron Age I Levant [not sure as these are all taken from southern Levant periodisation] [[-2000,-1000]]',
        'middle-bronze-early-iron-age-iran': 'Iran [[-2000,-650]]',
        'middleminoan': 'The Middle Minoan period on Crete, as defined in C. Shelmerdine, The Cambridge Companion to the Aegean Bronze Age (2008), p. 4, figure 1.1. [[-2000,-1600]]',
        'middle-bronze-age-anatolia': 'Anatolia [[-1750,-1450]]',
        'copy_of_middle-bronze-age-anatolia': 'Anatolia [[-1750,-1450]]',
        'old-hittite-anatolia': 'Old-Middle Kingdom Hittite [[-1650,-1450]]',
        'second-intermediate-period-egypt': 'The Second Intermediate period in Egypt, following the chronology of the UCLA Encyclopedia of Egyptology (compiled by Thomas Schneider): http://www.uee.ucla.edu/contributors/chronology.htm. [[-1640, -1548]]',
        'late-helladic': 'The Late Helladic period in the Greek mainland, after Preziosi and Hitchcock, Aegean Art and Architecture, Oxford History of Art, 1998. [[-1600, -1200]]',
        'later-2nd-millennium-bc-mesopotamia': 'Middle Assyrian/Middle Babylonian/Kassite Mesopotamia, LBA-Early Iron Age Mesopotamia, incl. Sea Peoples [[-1600,-1000]]',
        'late-nubian': 'NK-Kushite-Meroitic [[-1600,-350]]',
        'late-bronze-age-anatolia': 'Late Bronze Age Anatolia [[-1600,-1200]]',
        'late-minoan': 'The Late Minoan period on Crete, as defined in C. Shelmerdine, The Cambridge Companion to the Aegean Bronze Age (2008), p. 4. PeriodO URI: http://n2t.net/ark:/99152/p0qp9rssm67. [[-1600,-1080]]',
        'new-kingdom-egypt': 'The New Kingdom period in Egypt, following the chronology of the UCLA Encyclopedia of Egyptology (compiled by Thomas Schneider): http://www.uee.ucla.edu/contributors/chronology.htm. [[-1548, -1086]]',
        'late-bronze-age-iran': 'Iran [[-1500,-1000]]',
        'middle-hittite-anatolia': 'New Kingdom Hittite [[-1450,-1200]]',
        'late-bronze-age-southern-levant': 'southern Levant [[-1400,-1200]]',
        'egyptian-hittite-levant': 'Levant [[-1344,-1212]]',
        'early-iron-age-anatolia': 'incl. Mitanni [[-1200,-700]]',
        'neo-hittite-northern-levant': 'Syro-Hittite Northern Levant [[-1200,-700]]',
        '1200-bc-middle-east': 'ME, Greece [[-1200, -1199]]',
        'iron-age-southern-levant': '[[-1200,-550]]',
        'third-intermediate-period-egypt': 'The Third Intermediate period in Egypt, following the chronology of the UCLA Encyclopedia of Egyptology (compiled by Thomas Schneider): http://www.uee.ucla.edu/contributors/chronology.htm. [[-1086, -664]]',
        'early-iron-age-iran': 'Pre-Classical Antiquity [[-1000,-650]]',
        'iron-age-italy-latial-culture-i-1000-900-bc': 'Latial I is concentrated around Rome, the Alban Hills, and the Monti della Tolfa. [[-1000, -900]]',
        'early-geometric': 'The Early Geometric period in ancient Greece, from 900-850 before the birth of Christ. [[-900, -850]]',
        'urartian-eastern-anatolia': 'eastern Anatolia [[-900,-600]]',
        'castro-culture-iron-age-ca.-900-bc-100-bc': 'The Castro Culture is an archaeological term describing the material culture of Celtic peoples of the Iberian peninsula during the first millennium BC, as described at https://en.wikipedia.org/wiki/Castro_culture. [[-900,-100]]',
        'middle-geometric': 'The Middle Geometric period in ancient Greece, from 850-750 before the birth of Christ. [[-850, -750]]',
        'iron-age-britain': 'A long time period associated with Iron Age Britain. [[-800, 100]]',
        'archaic': 'The Archaic period in Greek and Roman history. For the purposes of Pleiades, this period is seen to begin in the year 750 and end in the year 550 before the birth of Christ. [[-750, -550]]',
        'neo-assyrian-babylonian-middle-east': 'ME [[-720,-540]]',
        'middle-late-iron-age-anatolia': 'Anatolia [[-700,-500]]',
        'late-period-egypt': 'The Late Period in Egypt, following the chronology of the UCLA Encyclopedia of Egyptology (compiled by Thomas Schneider): http://www.uee.ucla.edu/contributors/chronology.htm. [[-664, -332]]',
        'neo-babylonian-achaemenid-southern-levant': 'southern Levant [[-587,-330]]',
        'classical': 'The Classical period in Greek and Roman history. For the purposes of Pleiades, this period is said to begin in the year 550 and end in the year 330 before the birth of Christ. [[-550, -330]]',
        'achaemenid-middle-east': 'ME [[-540, -330]]',
        'achaemenid-roman-republic-middle-east': 'ME [[-540,-30]]',
        'achaemenid-roman-levant': 'Persian-Hellenistic-Roman Levant [[-540,324]]',
        'achaemenid-central-asia': 'Period as defined by Soren Stark [[-540, -330]]',
        'macedonian-egypt': 'The Macedonian period in Egypt, following the chronology of the UCLA Encyclopedia of Egyptology (compiled by Thomas Schneider): http://www.uee.ucla.edu/contributors/chronology.htm. [[-332, -304]]',
        'hellenistic-republican': 'The Hellenistic period in Greek history and the middle-to-late Republican period in Roman history. For the purposes of Pleiades, this period is said to begin in the year 330 and end in the year 30 before the birth of Christ. [[-330, -30]]',
        'hellenistic-middle-east': 'Macedonian--Seleucid/Ptolemaic/Attalid/Greco-Bactrian [[-330, -140]]',
        'hellenistic-parthian-middle-east': 'Seleucid-Early Roman-Arsacid Middle East [[-330,226]]',
        'hellenistic-roman-early-empire': 'Mediterranean [[-330,300]]',
        'hellenistic-central-asia': 'As defined by Soren Stark [[-330, -100]]',
        'ptolemaic-egypt': 'The Ptolemaic period in Egypt, following the chronology of the UCLA Encyclopedia of Egyptology (compiled by Thomas Schneider): http://www.uee.ucla.edu/contributors/chronology.htm. [[-304, -30]]',
        'ptolemaic-roman-egypt': 'Egypt [[-304,640]]',
        'parthian-middle-east': 'Arsacid ME [[-140,226]]',
        'roman-middle-east': 'ME [[-140, 640]]',
        'roman-early-byzantine-middle-east': 'ME [[-140,850]]',
        'kangju-yuezhi-kushan-central-asia': 'Period as defined by Soren Stark [[-100, 250]]',
        'roman-umayyad-levant': 'Roman-Byzantine-Caliphate-Umayyad Levant [[-37,1099]]',
        'roman': 'The Roman period (i.e., the early Roman Empire) in Greek and Roman history. For the purposes of Pleiades, this period is said to begin in the year 30 before the birth of Christ and to end in the year 300 after the birth of Christ. [[-30, 300]]',
        'roman-early-empire-parthian-middle-east': 'Early Roman/Parthian [[-30, 226]]',
        'roman-early-empire-late-antique': 'Mediterranean [[-30,640]]',
        'late-antiquity-in-central-asia': 'Period as defined by Soren Stark [[250, 550]]',
        'sassanian-middle-east': 'Sassanid [[262,700]]',
        'transition-roman-early-empire-late-antique': 'Mediterranean [[284, 337]]',
        'late-antique': 'The Late Antique period in Greek and Roman history. For the purposes of Pleiades, this period is said to begin in the year 300 and to end in the year 640 after the birth of Christ. [[300, 640]]',
        'late-antique-sasanian-middle-east': 'ME [[300, 640]]',
        'late-antique-late-byzantine': 'ME [[300, 1450]]',
        'proto-byzantine': 'Early Byzantine; includes Justinian I [[500, 650]]',
        'anglo-saxon': '[[550, 1066]]',
        'pre-islamic-early-middle-ages-central-asia': 'Period as defined by Soren Stark [[550, 750]]',
        'persian-medieval-caucasus': 'Persian--Arabic--Early Medieval--Middle Medieval--Turco-Mongol/Late Medieval Caucasus [[600,1500]]',
        'caliphate-umayyad-middle-east': 'Early Islamic, Rashidun-Umayyad [starts with death of Muhammed who only controlled Arabia] [[632,750]]',
        'caliphate-fatimid-southern-levant': 'Caliphate/Rashidun-Umayyad-Abassid-Fatimid southern Levant [[632,1150]]',
        'mediaeval-byzantine': 'The Mediaeval period in the West, or the period from the end of Late Antiquity (640) to the fall of Constantinople in the East (1453). [[640, 1453]]',
        'early-byzantine': 'Early Byzantine Period in areas where such designations are appropriate. [[650, 850]]',
        'ummayad': 'The period of the Umayyad Caliphate as defined by http://en.wikipedia.org/wiki/Umayyad_Caliphate [[661, 750]]',
        'abassid-middle-east': 'ME, northern Africa [[750, 940]]',
        'abbasid-period-central-asia': 'Period as defined by Soren Stark [[750, 875]]',
        'samanid-ghaznavid-iran': 'Iran [[819,1186]]',
        'middle-byzantine': 'Middle Byzantine period in areas where such designations are appropriate. [[850, 1200]]',
        'early-medieval-caucasus': 'Bagratid, Kingdom of Armenia/Kingdom of Georgia [[850,1200]]',
        'samanid-period-central-asia': 'Period as defined by Soren Stark [[875, 1000]]',
        'fatimid-middle-east': 'Western ME, northern Africa [[950,1150]]',
        'qarakhanid-period-central-asia': 'Period as defined by Soren Stark [[1000, 1200]]',
        'seljuq-middle-east': 'Great Seljuq Empire [[1037,1150]]',
        'seljuq-khwarezmian-middle-east': 'ME [[1037,1258]]',
        'khwarezmian-middle-east': 'Khwarezmid [[1077,1258]]',
        'rum-crusader-anatolia': 'Seljuk-Latin States/Francocracy [[1077, 1307]]',
        'crusader-byzantine-seljuq-middle-east': 'Latin/1st-4th Crusades--end of Middle Byzantine--Rum/Seljuq [[1081, 1204]]',
        'crusader-seljuq-ayyubid-levant': 'Latin [[1099,1291]]',
        'crusader-ottoman-levant': 'Crusader-Seljuq-Ayyubid-Mamluk-Ottoman Levant [[1099,1750]]',
        'ayyubid-middle-east': 'Western ME [[1171,1258]]',
        'late-byzantine': 'Late Byzantine Period in contexts where such designations are appropriate. [[1200, 1450]]',
        '13th-century-ad-eastern-mediterranean': 'Late Byzantine-Ayyubid-Mamluk Western Middle East [[1200,1300]]',
        'late-byzantine-ottoman-rise': 'Aegean, Balkan &amp; Anatolia [[1200,1453]]',
        'late-medieval-caucasus': 'Turco-Mongol, Seljuq-Georgian-Ilkhanate-Turkmen Caucasus [[1200,1500]]',
        'ilkhanate-middle-east': 'Ilkhanid, Hulagu, Early Mongol [[1258,1335]]',
        'mongol-middle-east': 'ME, Central Asia [[1258,1501]]',
        'mamluk-middle-east': 'Western ME [[1258,1516]]',
        'ottoman-rise': 'ends with the conquest of Constantinople [[1300, 1453]]',
        'timurid-middle-east': 'Eastern ME, Central Asia [[1370,1501]]',
        'early-ottoman-empire': 'ends with the siege of Vienna [[1453,1683]]',
        '1500-ad-middle-east': 'ME, Greece, Indus [[1500,1500]]',
        'perso-ottoman-russian-caucasus': 'Safavid-Qajar-Ottoman Empire-Russian Empire Caucasus [[1500,1918]]',
        'safavid-middle-east': 'Eastern ME, Central Asia [[1501,1725]]',
        'ottoman-empire': 'ME, Balkan, Northern Africa [[1513,1918]]',
        'late-ottoman-empire': 'ME, Balkan, Northern Africa [[1683,1918]]',
        'modern': 'Our present, modern era. [[1700, 2100]]',
        'khedivate-egypt': 'Muhammed Ali-Khedivate Egypt, Alawiyya Egypt, Anglo-Egyptian [[1800,1922]]',
        'colonial-modern-middle-east': 'Late Ottoman-Colonial-Mandate Modern Middle east [[1800,2000]]',
        'ottoman-decline-mandate-middle-east': 'ME [[1900,1950]]',
        'modern-middle-east': 'ME [[1918, 2000]]'
    }
}

UNICODE_RANGES = {
    'basic_latin': (r'\u0020', r'\u007F'),
    'latin_1': (r'\u00A0', r'\u00FF'),
    'latin_extended_a': (r'\u0100', r'\u017F'),
    'latin_extended_b': (r'\u0180', r'\u024F'),
    'latin_extended_additional': (r'\u1E00', r'\u1EFF'),
    'ipa_extensions': (r'\u0250', r'\u02AF'),
    'spacing_modifier_letters': (r'\u02B0', r'\u02FF'),
    'latin_extended_c': (r'\u2C60', r'\u2C7F'),
    'combining_diacritical_marks': (r'\u0300', r'\u036F')
}
