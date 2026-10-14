# -*- coding: utf-8 -*-
"""Content of al-Wird al-Latif, phone edition v1.0.

Markers: ⟦ ... ⟧ wrap words that change between morning and evening.
Qur'anic Arabic and the English/German Qur'an translations are filled in at
build time, verbatim, from the KFGQPC and QuranEnc data files.
Duʿā English translations are new translations made for this edition.
"""

S = lambda n: f"<sup>{n}</sup>"

SECTIONS = [
    ("s1", "Qurʾānic passages", "Sūrahs and verses recited at the start"),
    ("s2", "Seeking protection", "Placing oneself in Allah’s care"),
    ("s3", "Thanks and bearing witness", "Faith, contentment and trust"),
    ("s4", "Asking Allah", "Forgiveness, help and well-being"),
    ("s5", "Greeting the morning and evening", "Lines that change in the evening"),
    ("s6", "Glorifying Allah", "Praise, glorification and blessings on the Prophet ﷺ"),
]

ITEMS = []

def add(sec, ar, tr, en, *, heading=None, count=None, quran=None, bism=False, ev=None, ref=None):
    """quran: list of (sura, first, last) used for the Arabic + translations.
    ev: (arabic, translit, english) evening form, when the line changes."""
    ITEMS.append(dict(sec=sec, ar=ar, tr=tr, en=en, heading=heading, count=count,
                      quran=quran, bism=bism, ev=ev, ref=ref))

BISM_TR = "Bismillāh il-Raḥmān il-Raḥīm."

# ================================================================ 1. Qur'an
add("s1", None,
    f"{BISM_TR}<br>{S(1)}Qul Huwa Allāhu aḥad. {S(2)}Allāhu al-Ṣamad. {S(3)}Lam yalid wa lam yūlad. {S(4)}Wa lam yakun lahu kufuwan aḥad.",
    None, heading="Sūrat al-Ikhlāṣ (112)", count="3×", quran=[(112, 1, 4)], bism=True)

add("s1", None,
    f"{BISM_TR}<br>{S(1)}Qul aʿūdhu bi rabb il-falaq. {S(2)}Min sharri mā khalaq. {S(3)}Wa min sharri ghāsiqin idhā waqab. {S(4)}Wa min sharri il-naffāthāti fil-ʿuqad. {S(5)}Wa min sharri ḥāsidin idhā ḥasad.",
    None, heading="Sūrat al-Falaq (113)", count="3×", quran=[(113, 1, 5)], bism=True)

add("s1", None,
    f"{BISM_TR}<br>{S(1)}Qul aʿūdhu bi rabb il-nās. {S(2)}Malik il-nās. {S(3)}Ilāh il-nās. {S(4)}Min sharri al-waswās al-khannās, {S(5)}alladhī yuwaswisu fī ṣudūr il-nās, {S(6)}min al-jinnati wa al-nās.",
    None, heading="Sūrat al-Nās (114)", count="3×", quran=[(114, 1, 6)], bism=True)

add("s1", None,
    f"{S(97)}Rabbī aʿūdhu bika min hamazāt il-shayāṭīn, {S(98)}wa aʿūdhu bika Rabbī an yaḥḍurūn.",
    None, heading="Sūrat al-Muʾminūn 23:97–98", count="3×", quran=[(23, 97, 98)])

add("s1", None,
    f"{S(115)}Afaḥasibtum annamā khalaqnākum ʿabathan wa annakum ilaynā lā turjaʿūn. {S(116)}Fa taʿālā Allāh ul-Malik ul-Ḥaqq, lā ilāha illā Huwa Rabb ul-ʿArsh il-Karīm. {S(117)}Wa man yadʿu maʿ Allāhi ilāhan ākhara lā burhāna lahu bihi, fa-innamā ḥisābuhu ʿinda Rabbih, innahu lā yufliḥ ul-kāfirūn. {S(118)}Wa qul Rabb ighfir warḥam wa anta khayr ul-rāḥimīn.",
    None, heading="Sūrat al-Muʾminūn 23:115–118", quran=[(23, 115, 118)])

add("s1", None,
    f"{S(17)}Fa-subḥān Allāhi ḥīna tumsūna wa ḥīna tuṣbiḥūn. {S(18)}Wa lahu al-ḥamdu fi al-samāwāti wa al-arḍi wa ʿashiyyan wa ḥīna tuẓhirūn. {S(19)}Yukhrij ul-ḥayya min al-mayyiti wa yukhrij ul-mayyita min al-ḥayyi wa yuḥyī il-arḍa baʿda mawtihā, wa kadhālika tukhrajūn.",
    None, heading="Sūrat al-Rūm 30:17–19", quran=[(30, 17, 19)])

add("s1", "أَعُوذُ بِاللَّهِ السَّمِيعِ الْعَلِيمِ مِنَ الشَّيْطَانِ الرَّجِيمِ",
    "Aʿūdhu billāhi al-Samīʿ al-ʿAlīm min al-shayṭān al-rajīm.",
    "I seek refuge in Allah, the All-Hearing, the All-Knowing, from Satan, the outcast.",
    heading="Seeking refuge before al-Ḥashr", count="3×")

add("s1", None,
    f"{S(21)}Law anzalnā hādhā al-Qurʾāna ʿalā jabalin laraʾaytahu khāshiʿan mutaṣaddiʿan min khashyat Illāh, wa tilk al-amthālu naḍribuhā li-l-nāsi laʿallahum yatafakkarūn. {S(22)}Huwa Allāhu alladhī lā ilāha illā Huwa, ʿālim ul-ghaybi wa al-shahādati Huwa al-Raḥmān ul-Raḥīm. {S(23)}Huwa Allāhu alladhī lā ilāha illā Huwa al-Malik ul-Quddūs ul-Salām ul-Muʾmin ul-Muhaymin ul-ʿAzīz ul-Jabbār ul-Mutakabbir, subḥān Allāhi ʿammā yushrikūn. {S(24)}Huwa Allāh ul-Khāliq ul-Bāriʾ ul-Muṣawwir, lahu ul-asmāʾ ul-ḥusnā, yusabbiḥu lahu mā fī al-samāwāti wa al-arḍi wa Huwa al-ʿAzīz ul-Ḥakīm.",
    None, heading="Sūrat al-Ḥashr 59:21–24", quran=[(59, 21, 24)])

add("s1", None,
    f"{S(79)}Salāmun ʿalā Nūḥin fi al-ʿālamīn. {S(80)}Innā kadhālika najzi al-muḥsinīn. {S(81)}Innahu min ʿibādina al-muʾminīn.",
    None, heading="Sūrat al-Ṣāffāt 37:79–81", quran=[(37, 79, 81)])

# ================================================================ 2. Protection
add("s2", "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ",
    "Aʿūdhu bikalimāt Illāhi al-tāmmāti min sharri mā khalaq.",
    "I seek refuge in the perfect words of Allah from the evil of what He has created.", count="3×")

add("s2", "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ",
    "Bismillāh alladhī lā yaḍurru maʿ ismihi shayʾun fi al-arḍi wa lā fī al-samāʾi wa Huwa al-Samīʿ ul-ʿAlīm.",
    "In the name of Allah, with whose name nothing on earth or in the sky can cause harm, and He is the All-Hearing, the All-Knowing.", count="3×")

# ================================================================ 3. Thanks and witness
add("s3", "اللَّهُمَّ إِنِّي ⟦أَصْبَحْتُ⟧ مِنْكَ فِي نِعْمَةٍ وَعَافِيَةٍ وَسِتْرٍ، فَأَتْمِمْ نِعْمَتَكَ عَلَيَّ وَعَافِيَتَكَ وَسِتْرَكَ فِي الدُّنْيَا وَالْآخِرَةِ",
    "Allāhumma innī ⟦aṣbaḥtu⟧ minka fī niʿmatin wa ʿāfiyatin wa sitr, fa-atmim niʿmataka ʿalayya wa ʿāfiyataka wa sitraka fi al-dunyā wa al-ākhirah.",
    "O Allah, I have reached ⟦the morning⟧ in blessing, well-being and protection from You. So complete Your blessing, Your well-being and Your protection upon me, in this world and the next.",
    count="3×",
    ev=("اللَّهُمَّ إِنِّي ⟦أَمْسَيْتُ⟧ مِنْكَ فِي نِعْمَةٍ وَعَافِيَةٍ وَسِتْرٍ، فَأَتْمِمْ نِعْمَتَكَ عَلَيَّ وَعَافِيَتَكَ وَسِتْرَكَ فِي الدُّنْيَا وَالْآخِرَةِ",
        "Allāhumma innī ⟦amsaytu⟧ minka fī niʿmatin wa ʿāfiyatin wa sitr, fa-atmim niʿmataka ʿalayya wa ʿāfiyataka wa sitraka fi al-dunyā wa al-ākhirah.",
        "O Allah, I have reached ⟦the evening⟧ in blessing, well-being and protection from You. So complete Your blessing, Your well-being and Your protection upon me, in this world and the next."))

_WIT_AR = "أُشْهِدُكَ، وَأُشْهِدُ حَمَلَةَ عَرْشِكَ وَمَلَائِكَتَكَ وَجَمِيعَ خَلْقِكَ، أَنَّكَ أَنْتَ اللَّهُ لَا إِلَٰهَ إِلَّا أَنْتَ وَحْدَكَ لَا شَرِيكَ لَكَ، وَأَنَّ سَيِّدَنَا مُحَمَّدًا عَبْدُكَ وَرَسُولُكَ"
_WIT_TR = "ushhiduk, wa ushhidu ḥamalata ʿarshik wa malāʾikataka wa jamīʿa khalqik, annaka anta Allāhu lā ilāha illā anta waḥdaka lā sharīka lak, wa anna Sayyidanā Muḥammadan ʿabduka wa rasūluk."
_WIT_EN = "calling You to witness, and calling to witness the bearers of Your Throne, Your angels and all Your creation, that You are Allah: there is no god but You, alone, without partner, and that our master Muhammad is Your servant and Your messenger."
add("s3", f"اللَّهُمَّ إِنِّي ⟦أَصْبَحْتُ⟧ {_WIT_AR}",
    f"Allāhumma innī ⟦aṣbaḥtu⟧ {_WIT_TR}",
    f"O Allah, I have reached ⟦the morning⟧ {_WIT_EN}",
    count="4×",
    ev=(f"اللَّهُمَّ إِنِّي ⟦أَمْسَيْتُ⟧ {_WIT_AR}",
        f"Allāhumma innī ⟦amsaytu⟧ {_WIT_TR}",
        f"O Allah, I have reached ⟦the evening⟧ {_WIT_EN}"))

add("s3", "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ، حَمْدًا يُوَافِي نِعَمَهُ وَيُكَافِئُ مَزِيدَهُ",
    "Al-ḥamdu lillāhi Rabb il-ʿālamīn, ḥamdan yuwāfī niʿamahu wa yukāfiʾu mazīdah.",
    "All praise is for Allah, Lord of the worlds — praise that matches His blessings and is equal to His ever-growing favour.", count="3×")

add("s3", "آمَنْتُ بِاللَّهِ الْعَظِيمِ، وَكَفَرْتُ بِالْجِبْتِ وَالطَّاغُوتِ، وَاسْتَمْسَكْتُ بِالْعُرْوَةِ الْوُثْقَىٰ لَا انْفِصَامَ لَهَا وَاللَّهُ سَمِيعٌ عَلِيمٌ",
    "Āmantu billāh il-ʿAẓīm, wa kafartu bil-jibti wa al-ṭāghūt, wastamsaktu bil-ʿurwat il-wuthqā, lan-fiṣāma lahā wa Allāhu Samīʿun ʿAlīm.",
    "I believe in Allah, the Magnificent, and I reject all idols and false gods. I hold on to the firmest handhold, which never breaks. And Allah is All-Hearing, All-Knowing.", count="3×")

add("s3", "رَضِيتُ بِاللَّهِ رَبًّا، وَبِالْإِسْلَامِ دِينًا، وَبِسَيِّدِنَا مُحَمَّدٍ صَلَّى اللَّهُ عَلَيْهِ وَآلِهِ وَسَلَّمَ نَبِيًّا وَرَسُولًا",
    "Raḍītu billāhi Rabbā, wa bil-Islāmi dīnā, wa bi-Sayyidinā Muḥammadin ṣallā Allāhu ʿalayhi wa ālihi wa sallama nabiyyan wa rasūlā.",
    "I am pleased with Allah as my Lord, with Islam as my religion, and with our master Muhammad — may Allah bless him and his family and grant them peace — as my Prophet and Messenger.", count="3×")

add("s3", None,
    "Ḥasbī Allāhu lā ilāha illā Huwa ʿalayhi tawakkaltu wa Huwa Rabb ul-ʿarsh il-ʿaẓīm.",
    "Allah is enough for me; there is no god but Him. In Him I put my trust, and He is the Lord of the Mighty Throne.",
    count="7×", ref="From Qurʾān 9:129", quran="9:129-part")

add("s3", "اللَّهُمَّ صَلِّ عَلَىٰ سَيِّدِنَا مُحَمَّدٍ وَآلِهِ وَصَحْبِهِ وَسَلِّمْ",
    "Allāhumma ṣalli ʿalā Sayyidinā Muḥammadin wa ālihi wa ṣaḥbihi wa sallim.",
    "O Allah, send blessings and peace upon our master Muhammad, his family and his companions.", count="10×")

# ================================================================ 4. Asking Allah
add("s4", "اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فُجَاءَةِ الْخَيْرِ، وَأَعُوذُ بِكَ مِنْ فُجَاءَةِ الشَّرِّ",
    "Allāhumma innī asʾaluka min fujāʾat il-khayr, wa aʿūdhu bika min fujāʾat il-sharr.",
    "O Allah, I ask You for good that comes suddenly, and I seek refuge in You from evil that comes suddenly.")

add("s4", "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَٰهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَىٰ عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ وَأَبُوءُ بِذَنْبِي، فَاغْفِرْ لِي فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ",
    "Allāhumma anta Rabbī lā ilāha illā ant, khalaqtanī wa anā ʿabduk, wa anā ʿalā ʿahdika wa waʿdika mā astaṭaʿt, aʿūdhu bika min sharri mā ṣanaʿt, abūʾu laka bi-niʿmatika ʿalayya wa abūʾu bi-dhanbī, faghfir lī, fa-innahu lā yaghfir ul-dhunūba illā ant.",
    "O Allah, You are my Lord; there is no god but You. You created me and I am Your servant. I keep my promise and pledge to You as best I can. I seek refuge in You from the evil of what I have done. I admit Your blessings upon me, and I admit my sins — so forgive me, for no one forgives sins except You.")

add("s4", "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَٰهَ إِلَّا أَنْتَ، عَلَيْكَ تَوَكَّلْتُ وَأَنْتَ رَبُّ الْعَرْشِ الْعَظِيمِ",
    "Allāhumma anta Rabbī lā ilāha illā ant, ʿalayka tawakkaltu wa anta Rabb ul-ʿarsh il-ʿaẓīm.",
    "O Allah, You are my Lord; there is no god but You. In You I put my trust, and You are the Lord of the Mighty Throne.")

add("s4", "مَا شَاءَ اللَّهُ كَانَ، وَمَا لَمْ يَشَأْ لَمْ يَكُنْ، وَلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ",
    "Mā shāʾ Allāhu kān, wa mā lam yashaʾ lam yakun, wa lā ḥawla wa lā quwwata illā billāh il-ʿAliyy il-ʿAẓīm.",
    "Whatever Allah wills happens, and whatever He does not will does not happen. There is no power and no strength except through Allah, the Most High, the Magnificent.")

add("s4", "أَعْلَمُ أَنَّ اللَّهَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ، وَأَنَّ اللَّهَ قَدْ أَحَاطَ بِكُلِّ شَيْءٍ عِلْمًا",
    "Aʿlamu anna Allāha ʿalā kulli shayʾin qadīr wa anna Allāha qad aḥāṭa bi-kulli shayʾin ʿilmā.",
    "I know that Allah has power over all things, and that Allah’s knowledge surrounds all things.")

add("s4", "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنْ شَرِّ نَفْسِي، وَمِنْ شَرِّ كُلِّ دَابَّةٍ أَنْتَ آخِذٌ بِنَاصِيَتِهَا، إِنَّ رَبِّي عَلَىٰ صِرَاطٍ مُسْتَقِيمٍ",
    "Allāhumma innī aʿūdhu bika min sharri nafsī, wa min sharri kulli dābbatin anta ākhidhun bi-nāṣiyatihā, inna Rabbī ʿalā ṣirāṭin mustaqīm.",
    "O Allah, I seek refuge in You from the evil of my own self, and from the evil of every living creature, each of which You hold by its forelock. Truly, my Lord is on a straight path.")

add("s4", "يَا حَيُّ يَا قَيُّومُ، بِرَحْمَتِكَ أَسْتَغِيثُ، وَمِنْ عَذَابِكَ أَسْتَجِيرُ، أَصْلِحْ لِي شَأْنِي كُلَّهُ، وَلَا تَكِلْنِي إِلَىٰ نَفْسِي وَلَا إِلَىٰ أَحَدٍ مِنْ خَلْقِكَ طَرْفَةَ عَيْنٍ",
    "Yā Ḥayyu yā Qayyūm, bi-raḥmatika astaghīth, wa min ʿadhābika astajīr, aṣliḥ lī shaʾnī kullah, wa lā takilnī ilā nafsī wa lā ilā aḥadin min khalqika ṭarfata ʿayn.",
    "O Ever-Living, O Self-Sustaining! By Your mercy I call for help, and from Your punishment I seek protection. Set right all my affairs, and do not leave me to myself, or to any of Your creation, even for the blink of an eye.")

add("s4", "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْهَمِّ وَالْحَزَنِ، وَأَعُوذُ بِكَ مِنَ الْعَجْزِ وَالْكَسَلِ، وَأَعُوذُ بِكَ مِنَ الْجُبْنِ وَالْبُخْلِ، وَأَعُوذُ بِكَ مِنْ غَلَبَةِ الدَّيْنِ وَقَهْرِ الرِّجَالِ",
    "Allāhumma innī aʿūdhu bika min al-hammi wa al-ḥazan, wa aʿūdhu bika min al-ʿajzi wa al-kasal, wa aʿūdhu bika min al-jubni wa al-bukhl, wa aʿūdhu bika min ghalabat il-dayni wa qahr il-rijāl.",
    "O Allah, I seek refuge in You from worry and sadness; I seek refuge in You from helplessness and laziness; I seek refuge in You from cowardice and stinginess; and I seek refuge in You from being overwhelmed by debt and overpowered by people.")

add("s4", "اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَافِيَةَ فِي الدُّنْيَا وَالْآخِرَةِ",
    "Allāhumma innī asʾaluk al-ʿāfiyah fī al-dunyā wa al-ākhirah.",
    "O Allah, I ask You for well-being in this world and the next.")

add("s4", "اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَفْوَ وَالْعَافِيَةَ وَالْمُعَافَاةَ الدَّائِمَةَ فِي دِينِي وَدُنْيَايَ وَأَهْلِي وَمَالِي",
    "Allāhumma innī asʾaluk al-ʿafwa wa al-ʿāfiyah wa al-muʿāfāt al-dāʾimah fī dīnī wa dunyāya wa ahlī wa mālī.",
    "O Allah, I ask You for pardon, well-being and lasting safety in my religion, my worldly life, my family and my wealth.")

add("s4", "اللَّهُمَّ اسْتُرْ عَوْرَاتِي وَآمِنْ رَوْعَاتِي",
    "Allāhumma ustur ʿawrātī wa āmin rawʿātī.",
    "O Allah, cover my faults and calm my fears.")

add("s4", "اللَّهُمَّ احْفَظْنِي مِنْ بَيْنِ يَدَيَّ وَمِنْ خَلْفِي، وَعَنْ يَمِينِي وَعَنْ شِمَالِي وَمِنْ فَوْقِي، وَأَعُوذُ بِعَظَمَتِكَ أَنْ أُغْتَالَ مِنْ تَحْتِي",
    "Allāhumma iḥfaẓnī min bayna yadayya wa min khalfī, wa ʿan yamīnī wa ʿan shimālī wa min fawqī, wa aʿūdhu bi-ʿaẓamatika an ughtāla min taḥtī.",
    "O Allah, protect me from in front of me and from behind me, from my right and from my left, and from above me; and I seek refuge in Your greatness from being struck unawares from below me.")

add("s4", "اللَّهُمَّ أَنْتَ خَلَقْتَنِي وَأَنْتَ تَهْدِينِي وَأَنْتَ تُطْعِمُنِي وَأَنْتَ تَسْقِينِي وَأَنْتَ تُمِيتُنِي وَأَنْتَ تُحْيِينِي، وَأَنْتَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ",
    "Allāhumma anta khalaqtanī wa anta tahdīnī wa anta tuṭʿimunī wa anta tasqīnī wa anta tumītunī wa anta tuḥyīnī, wa anta ʿalā kulli shayʾin qadīr.",
    "O Allah, You created me and You guide me; You feed me and You give me drink; You cause me to die and You give me life; and You have power over all things.")

# ================================================================ 5. Morning / evening
_FIT_AR = "عَلَىٰ فِطْرَةِ الْإِسْلَامِ، وَعَلَىٰ كَلِمَةِ الْإِخْلَاصِ، وَعَلَىٰ دِينِ نَبِيِّنَا مُحَمَّدٍ صَلَّى اللَّهُ عَلَيْهِ وَآلِهِ وَسَلَّمَ، وَعَلَىٰ مِلَّةِ أَبِينَا إِبْرَاهِيمَ حَنِيفًا مُسْلِمًا وَمَا كَانَ مِنَ الْمُشْرِكِينَ"
_FIT_TR = "ʿalā fiṭrat il-Islām wa ʿalā kalimat il-ikhlāṣ wa ʿalā dīni nabiyyinā Muḥammadin ṣallā Allāhu ʿalayhi wa ālihi wa sallam, wa ʿalā millati abīnā Ibrāhīma ḥanīfan musliman wa mā kāna min al-mushrikīn."
_FIT_EN = "upon the natural way of Islam, upon the word of sincere faith, upon the religion of our Prophet Muhammad — may Allah bless him and his family and grant them peace — and upon the way of our father Ibrāhīm, who was upright, a Muslim, and not one of those who worship others besides Allah."
add("s5", f"⟦أَصْبَحْنَا⟧ {_FIT_AR}", f"⟦Aṣbaḥnā⟧ {_FIT_TR}", f"We have reached ⟦the morning⟧ {_FIT_EN}",
    ev=(f"⟦أَمْسَيْنَا⟧ {_FIT_AR}", f"⟦Amsaynā⟧ {_FIT_TR}", f"We have reached ⟦the evening⟧ {_FIT_EN}"))

add("s5", "اللَّهُمَّ بِكَ ⟦أَصْبَحْنَا⟧ وَبِكَ ⟦أَمْسَيْنَا⟧ وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَعَلَيْكَ نَتَوَكَّلُ وَإِلَيْكَ ⟦النُّشُورُ⟧",
    "Allāhumma bika ⟦aṣbaḥnā⟧ wa bika ⟦amsaynā⟧ wa bika naḥyā wa bika namūt wa ʿalayka natawakkal wa ilayk ⟦al-nushūr⟧.",
    "O Allah, by You we reach ⟦the morning⟧ and by You we reach ⟦the evening⟧; by You we live and by You we die; in You we put our trust, and to You is ⟦the rising again⟧.",
    ev=("اللَّهُمَّ بِكَ ⟦أَمْسَيْنَا⟧ وَبِكَ ⟦أَصْبَحْنَا⟧ وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَعَلَيْكَ نَتَوَكَّلُ وَإِلَيْكَ ⟦الْمَصِيرُ⟧",
        "Allāhumma bika ⟦amsaynā⟧ wa bika ⟦aṣbaḥnā⟧ wa bika naḥyā wa bika namūt wa ʿalayka natawakkal wa ilayk ⟦al-maṣīr⟧.",
        "O Allah, by You we reach ⟦the evening⟧ and by You we reach ⟦the morning⟧; by You we live and by You we die; in You we put our trust, and to You is ⟦the final return⟧."))

add("s5", "⟦أَصْبَحْنَا⟧ ⟦وَأَصْبَحَ⟧ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
    "⟦Aṣbaḥnā⟧ ⟦wa aṣbaḥa⟧ al-mulku lillāh, wa al-ḥamdu lillāhi Rabb il-ʿālamīn.",
    "We have reached ⟦the morning⟧, and all the kingdom has reached ⟦the morning⟧ belonging to Allah. All praise is for Allah, Lord of the worlds.",
    ev=("⟦أَمْسَيْنَا⟧ ⟦وَأَمْسَى⟧ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
        "⟦Amsaynā⟧ ⟦wa amsā⟧ al-mulku lillāh, wa al-ḥamdu lillāhi Rabb il-ʿālamīn.",
        "We have reached ⟦the evening⟧, and all the kingdom has reached ⟦the evening⟧ belonging to Allah. All praise is for Allah, Lord of the worlds."))

add("s5", "اللَّهُمَّ إِنِّي أَسْأَلُكَ خَيْرَ ⟦هَٰذَا الْيَوْمِ⟧، ⟦فَتْحَهُ⟧ ⟦وَنَصْرَهُ⟧ ⟦وَنُورَهُ⟧ ⟦وَبَرَكَتَهُ⟧ ⟦وَهُدَاهُ⟧",
    "Allāhumma innī asʾaluka khayra ⟦hādhā al-yawm⟧, ⟦fatḥahu⟧ ⟦wa naṣrahu⟧ ⟦wa nūrahu⟧ ⟦wa barakatahu⟧ ⟦wa hudāh⟧.",
    "O Allah, I ask You for the good of ⟦this day⟧: its openings, its victory, its light, its blessing and its guidance.",
    ev=("اللَّهُمَّ إِنِّي أَسْأَلُكَ خَيْرَ ⟦هَٰذِهِ اللَّيْلَةِ⟧، ⟦فَتْحَهَا⟧ ⟦وَنَصْرَهَا⟧ ⟦وَنُورَهَا⟧ ⟦وَبَرَكَتَهَا⟧ ⟦وَهُدَاهَا⟧",
        "Allāhumma innī asʾaluka khayra ⟦hādhihi al-laylah⟧, ⟦fatḥahā⟧ ⟦wa naṣrahā⟧ ⟦wa nūrahā⟧ ⟦wa barakatahā⟧ ⟦wa hudāhā⟧.",
        "O Allah, I ask You for the good of ⟦this night⟧: its openings, its victory, its light, its blessing and its guidance."))

add("s5", "اللَّهُمَّ إِنِّي أَسْأَلُكَ خَيْرَ ⟦هَٰذَا الْيَوْمِ⟧ وَخَيْرَ مَا ⟦فِيهِ⟧، وَخَيْرَ مَا ⟦قَبْلَهُ⟧ وَخَيْرَ مَا ⟦بَعْدَهُ⟧، وَأَعُوذُ بِكَ مِنْ شَرِّ ⟦هَٰذَا الْيَوْمِ⟧ وَشَرِّ مَا ⟦فِيهِ⟧، وَشَرِّ مَا ⟦قَبْلَهُ⟧ وَشَرِّ مَا ⟦بَعْدَهُ⟧",
    "Allāhumma innī asʾaluka khayra ⟦hādhā al-yawmi⟧ wa khayra mā ⟦fīh⟧, wa khayra mā ⟦qablahu⟧ wa khayra mā ⟦baʿdah⟧, wa aʿūdhu bika min sharri ⟦hādhā al-yawmi⟧ wa sharri mā ⟦fīh⟧, wa sharri mā ⟦qablahu⟧ wa sharri mā ⟦baʿdah⟧.",
    "O Allah, I ask You for the good of ⟦this day⟧ and the good of what is in it, the good of what came before it and the good of what comes after it; and I seek refuge in You from the evil of ⟦this day⟧ and the evil of what is in it, the evil of what came before it and the evil of what comes after it.",
    ev=("اللَّهُمَّ إِنِّي أَسْأَلُكَ خَيْرَ ⟦هَٰذِهِ اللَّيْلَةِ⟧ وَخَيْرَ مَا ⟦فِيهَا⟧، وَخَيْرَ مَا ⟦قَبْلَهَا⟧ وَخَيْرَ مَا ⟦بَعْدَهَا⟧، وَأَعُوذُ بِكَ مِنْ شَرِّ ⟦هَٰذِهِ اللَّيْلَةِ⟧ وَشَرِّ مَا ⟦فِيهَا⟧، وَشَرِّ مَا ⟦قَبْلَهَا⟧ وَشَرِّ مَا ⟦بَعْدَهَا⟧",
        "Allāhumma innī asʾaluka khayra ⟦hādhihi al-laylati⟧ wa khayra mā ⟦fīhā⟧, wa khayra mā ⟦qablahā⟧ wa khayra mā ⟦baʿdahā⟧, wa aʿūdhu bika min sharri ⟦hādhihi al-laylati⟧ wa sharri mā ⟦fīhā⟧, wa sharri mā ⟦qablahā⟧ wa sharri mā ⟦baʿdahā⟧.",
        "O Allah, I ask You for the good of ⟦this night⟧ and the good of what is in it, the good of what came before it and the good of what comes after it; and I seek refuge in You from the evil of ⟦this night⟧ and the evil of what is in it, the evil of what came before it and the evil of what comes after it."))

_MA_AR = "بِي مِنْ نِعْمَةٍ أَوْ بِأَحَدٍ مِنْ خَلْقِكَ، فَمِنْكَ وَحْدَكَ لَا شَرِيكَ لَكَ، فَلَكَ الْحَمْدُ وَلَكَ الشُّكْرُ عَلَىٰ ذَٰلِكَ"
_MA_TR = "bī min niʿmatin aw bi-aḥadin min khalqik, fa-minka waḥdaka lā sharīka lak, fa-laka al-ḥamdu wa laka al-shukru ʿalā dhālik."
add("s5", f"اللَّهُمَّ مَا ⟦أَصْبَحَ⟧ {_MA_AR}", f"Allāhumma mā ⟦aṣbaḥa⟧ {_MA_TR}",
    "O Allah, whatever blessing has come to me or to any of Your creation ⟦this morning⟧ is from You alone, without partner. So all praise and all thanks are Yours for it.",
    ev=(f"اللَّهُمَّ مَا ⟦أَمْسَى⟧ {_MA_AR}", f"Allāhumma mā ⟦amsā⟧ {_MA_TR}",
        "O Allah, whatever blessing has come to me or to any of Your creation ⟦this evening⟧ is from You alone, without partner. So all praise and all thanks are Yours for it."))

# ================================================================ 6. Glorification
_ADAD_EN = "as many times as the number of His creation, as much as pleases Him, as heavy as His Throne, and as much as the ink of His words."
add("s6", "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ عَدَدَ خَلْقِهِ وَرِضَاءَ نَفْسِهِ وَزِنَةَ عَرْشِهِ وَمِدَادَ كَلِمَاتِهِ",
    "Subḥān Allāhi wa bi-ḥamdihi ʿadada khalqihi wa riḍāʾ nafsihi wa zinata ʿarshihi wa midāda kalimātih.",
    f"Glory be to Allah and praise be to Him — {_ADAD_EN}", count="3×")

add("s6", "سُبْحَانَ اللَّهِ الْعَظِيمِ وَبِحَمْدِهِ عَدَدَ خَلْقِهِ وَرِضَاءَ نَفْسِهِ وَزِنَةَ عَرْشِهِ وَمِدَادَ كَلِمَاتِهِ",
    "Subḥān Allāhi al-ʿAẓīmi wa bi-ḥamdihi ʿadada khalqihi wa riḍāʾ nafsihi wa zinata ʿarshihi wa midāda kalimātih.",
    f"Glory be to Allah, the Magnificent, and praise be to Him — {_ADAD_EN}", count="3×")

def _four(ar_phrase, tr_phrase, en_phrase):
    ar = "، ".join(f"{ar_phrase} عَدَدَ {x}" for x in ["مَا خَلَقَ فِي السَّمَاءِ", "مَا خَلَقَ فِي الْأَرْضِ", "مَا بَيْنَ ذَٰلِكَ", "مَا هُوَ خَالِقٌ"])
    tr = ", ".join(f"{tr_phrase} ʿadada {x}" for x in ["mā khalaqa fī al-samāʾ", "mā khalaqa fī al-arḍ", "mā bayna dhālik", "mā Huwa khāliq"])
    tr = tr[0].upper() + tr[1:] + "."
    en = "; ".join(f"“{en_phrase}” {x}" for x in ["as many times as all He has created in the sky", "as many times as all He has created on the earth", "as many times as all that is between them", "as many times as all He will yet create"]) + "."
    return ar, tr, en

for a, t, e in [
    ("سُبْحَانَ اللَّهِ", "subḥān Allāhi", "Glory be to Allah"),
    ("الْحَمْدُ لِلَّهِ", "al-ḥamdu lillāhi", "All praise is for Allah"),
    ("لَا إِلَٰهَ إِلَّا اللَّهُ", "lā ilāha illā Allāh", "There is no god but Allah"),
    ("اللَّهُ أَكْبَرُ", "Allāhu akbar", "Allah is the Greatest"),
    ("لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ الْعَلِيِّ الْعَظِيمِ", "lā ḥawla wa lā quwwata illā billāh il-ʿAliyy il-ʿAẓīm", "There is no power and no strength except through Allah, the Most High, the Magnificent"),
]:
    add("s6", *_four(a, t, e))

add("s6", "لَا إِلَٰهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، يُحْيِي وَيُمِيتُ وَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ، عَدَدَ كُلِّ ذَرَّةٍ أَلْفَ مَرَّةٍ",
    "Lā ilāha illā Allāhu waḥdahu lā sharīka lah, lahu ul-mulku wa lahu ul-ḥamdu, yuḥyī wa yumīt wa Huwa ʿalā kulli shayʾin qadīr, ʿadada kulli dharratin alfa marrah.",
    "There is no god but Allah, alone, without partner. His is the kingdom and His is the praise. He gives life and causes death, and He has power over all things — as many times as every atom, a thousand times over.", count="3×")

add("s6", "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَىٰ سَيِّدِنَا مُحَمَّدٍ مِفْتَاحِ بَابِ رَحْمَةِ اللَّهِ، عَدَدَ مَا فِي عِلْمِ اللَّهِ، صَلَاةً وَسَلَامًا دَائِمَيْنِ بِدَوَامِ مُلْكِ اللَّهِ، وَعَلَىٰ آلِهِ وَصَحْبِهِ عَدَدَ كُلِّ ذَرَّةٍ أَلْفَ مَرَّةٍ",
    "Allāhumma ṣalli wa sallim ʿalā Sayyidinā Muḥammadin miftāḥi bāb raḥmat Illāh, ʿadada mā fī ʿilm Illāh, ṣalātan wa salāman dāʾimayni bi-dawāmi mulk Illāh, wa ʿalā ālihi wa ṣaḥbihi ʿadada kulli dharratin alfa marrah.",
    "O Allah, send blessings and peace upon our master Muhammad, the key to the door of Allah’s mercy — as many times as all that is in Allah’s knowledge — blessings and peace that last as long as Allah’s kingdom lasts; and upon his family and companions, as many times as every atom, a thousand times over.", count="3×")
