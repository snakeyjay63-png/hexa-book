# Artikel 5 — Quran-bronroute en lokale Basmala-Abjadroute

> Dit document is een technische routebijlage bij `hexa-book-001.md` en vervangt niet `Artikel 5 — dimensie 5 (de return wordt zichtbaar)`. De nummering `005` werkt als documentkoppeling, niet als hoofdstuknummer.

**Lokale status:** uitgevoerd en reproduceerbaar  
**Volledige boekreturn:** ongetest  
**Datum:** 2026-07-22  
**Auditrapport:** `quran_field/derived/basmala_abjad_audit.json`

> ⚠ NPR-fase-toewijzing (ρ_NPR-phase) is interpretatief (vikalpa) tenzij expliciet gemarkeerd als gevalideerd.

---

## Toelichting

> **5-2:** Return-rekenkunde is conceptueel zonder operationele verificatie — bewezen en conceptueel inhoud zijn gescheiden.  
> **5-3:** Lensrekenkunde-operator ("wissel lens") is beschreven maar niet formeel gedefinieerd — `status = heuristisch`.  
> **E-1 (C_sound):** De audio-operator `C_sound` is conceptueel gedefinieerd maar niet geïmplementeerd — `status_defined = conceptueel | status_executed = niet_geïmplementeerd`.

---

## Samenvatting

De Quran-route gebruikt de raw-data-laag van `quran_field` als vastgelegde bronrepresentatie. De repository wordt lokaal geïmporteerd, waarna de gebruikte Git-commit, het concrete bronbestand, de UTF-8-codering en de SHA-256-checksum worden geregistreerd.

De operationele pipeline is:

$$
\text{repository-import} \rightarrow \text{raw bronbestand} \rightarrow \text{ongewijzigde bronlaag} \rightarrow \text{afgeleide kopie} \rightarrow \text{selectie} \rightarrow \text{normalisatie} \rightarrow \text{Abjad} \rightarrow r_{\text{local}}
$$

Niet:

$$
\text{Quran} \rightarrow 3\text{–}6\text{–}9
$$

zonder tussenstappen.

---

## 1. Bronvastlegging

De repository `snakeyjay63-png/NPR_OS_sandbox` wordt lokaal geïmporteerd. De gebruikte commit wordt vastgelegd:

| Parameter | Waarde |
|---|---|
| repository | `snakeyjay63-png/NPR_OS_sandbox` |
| commit | `0e53e3d98df5107d612afe4b3a38ea627230267e` |
| source_directory | `quran_field` |
| working_tree_clean | ja |

Voor reproduceerbaarheid wordt niet alleen `main` gebruikt, omdat `main` later kan veranderen. De volledige commit-SHA is het referentiepunt.

---

## 2. Raw bronbestand

Het bronbestand is geïdentificeerd binnen `quran_field`:

| Parameter | Waarde |
|---|---|
| `Q_source_file` | `quran_field/v1/raw/quran_source.json` |
| formaat | JSON, array van verse-objecten |
| veldsoera-aya | `verse_key` (bijv. `"1:1"`) |
| veldtekst | `text_uthmani` |
| diakritiek | aanwezig (Uthmani-script) |
| Basmala-positie | verse_key `"1:1"` |
| teksteditie | Quran.com API (quran-uthmani edition) |

De map `quran_field/source/quran_uthmani.txt` bevat een HTML-downloadpagina van Tanzil (geen raw tekst). Het bestand `quran_field/source/quran_uthmani_simple.txt` bevat een geparste versie maar is niet de primaire bron. Het JSON-bestand in `v1/raw/` is binnen deze NPR-route het primaire en normatieve bronbestand.

---

## 3. Bronbestand-integriteit

SHA-256 checksum van het bronbestand:

| Parameter | Waarde |
|---|---|
| `source_sha256` | `3754c592dd15d7047d5b4339737ad3171c5c1d431a8c3e4c1eee7781c135d58c` |
| encoding | UTF-8 |
| encoding_valid | ja |

Formeel:

$$
Q_{\text{raw}} := \operatorname{bytes}(\texttt{quran\_field/v1/raw/quran\_source.json})
$$

$$
Q_{\text{decoded}} := \operatorname{decode}_{\text{UTF-8}}(Q_{\text{raw}})
$$

$$
Q_{\text{source}} := P_{\text{JSON}}(Q_{\text{decoded}})
$$

Volgorde:

$$
Q_{\text{raw}} \rightarrow Q_{\text{decoded}} \rightarrow Q_{\text{source}} \rightarrow S_{\text{Basmala}}
$$

---

## 4. Scheiding bronlaag en analyselaag

Het originele bestand wordt niet aangepast. Alle verwerking gebeurt op afgeleide kopieën:

$$
Q_{\text{work}} = \operatorname{copy}(Q_{\text{source}})
$$

Invariant:

$$
\operatorname{SHA256}(Q_{\text{raw}}^{\text{before}}) = \operatorname{SHA256}(Q_{\text{raw}}^{\text{after}})
$$

*(Een geparseerd object heeft niet noodzakelijk een unieke byte-representatie; de hash geldt voor de raw-bron.)*

Dit ondersteunt het CM/RC-onderscheid:

$$
\text{CM} := Q_{\text{source}}
$$

$$
\text{RC}_i = O_i(N_i(S_i(\text{CM})))
$$

waarbij:

* $S_i$ = selectie;
* $N_i$ = normalisatie;
* $O_i$ = operator.

---

## 5. Selectie van de Basmala

De selectiefunctie is expliciet gedefinieerd:

$$
S_{\text{Basmala}} : \mathcal{Q} \rightarrow \Sigma^*
$$

$$
s_{\text{Basmala}} := S_{\text{Basmala}}(Q_{\text{source}};\ \texttt{verse\_key}=\texttt{"1:1"},\ \texttt{field}=\texttt{"text\_uthmani"})
$$

Resultaat:

| Parameter | Waarde |
|---|---|
| selector | `surah=1, ayah=1` |
| parser | `json.verses[].verse_key == '1:1'` |
| `source_text` | بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ |
| selection_status | uitgevoerd |

---

## 6. Abjad-normalisatie

De normalisatie wordt alleen op een afgeleide representatie toegepast:

$$
s_{\text{basis}} = N_{\text{Abjad}}(s_{\text{Basmala}})
$$

### Normalisatievolgorde

De regels worden in deze volgorde toegepast:

$$
N_{\text{Abjad}} = N_{\text{spaces}} \circ N_{\text{carriers}} \circ N_{\text{wasla}} \circ N_{\text{marks}}
$$

waarbij $N_{\text{marks}}$ de volgende tekenverzameling verwijdert:

$$
\mathcal{M}_{\text{remove}} = \mathcal{M}_{\text{harakat}} \cup \mathcal{M}_{\text{tatwil}} \cup \mathcal{M}_{\text{superscript-alif}}
$$

- $\mathcal{M}_{\text{harakat}}$: U+064B–U+0652
- $\mathcal{M}_{\text{tatwil}}$: U+0640
- $\mathcal{M}_{\text{superscript-alif}}$: U+0670

$$
N_{\text{marks}}(x) = \operatorname{remove}(x, \mathcal{M}_{\text{remove}})
$$

1. Unicode-invoer onveranderd lezen;
2. toegestane marks verwijderen;
3. alif waṣla mappen;
4. hamzadragers mappen;
5. spaties verwijderen;
6. resterende tekens valideren tegen de Abjadtabel.

### Normalisatieregels

| Regel | Actie | Unicode |
|---|---|---|
| Harakat verwijderen | ً ٌ ٍ َ ُ ِ ّ ْ | U+064B–U+0652 |
| Tatwīl verwijderen | ـ | U+0640 |
| SuperScript Alif | ٰ | U+0670 |
| Alif Wasla → Alif | ٱ → ا | U+0671 → U+0627 |
| Hamza carriers | أ→ا, إ→ا, ؤ→و, ئ→ي | U+0623, U+0625, U+0624, U+0626 |
| Spaties | negeren | U+0020 |
| Onbekende tekens | rapporteren, niet negeren | — |

**Kritieke opmerking:** U+064A (ي, YEH) is een letter met Abjad-waarde 10, geen diakriet. Eerdere versies van de normalisatie verwijderden ي per ongeluk, wat leidde tot een incorrect resultaat (776 in plaats van 786). Dit is gecorrigeerd.

### Genummerde tekst

| Positie | Karakter | U+Code | Status |
|---|---|---|---|
| 1 | ب | U+0628 | letter |
| 2 | ِ | U+0650 | kasra → strip |
| 3 | س | U+0633 | letter |
| 4 | ْ | U+0652 | sukun → strip |
| 5 | م | U+0645 | letter |
| 6 | ِ | U+0650 | kasra → strip |
| 7 | (spatie) | U+0020 | negeren |
| 8 | ٱ | U+0671 | alif wasla → ا |
| 9 | ل | U+0644 | letter |
| 10 | ل | U+0644 | letter |
| 11 | ّ | U+0651 | shadda → strip |
| 12 | َ | U+064E | fatha → strip |
| 13 | ه | U+0647 | letter |
| 14 | ِ | U+0650 | kasra → strip |

*(Overige tekens voor `الرحمن` en `الرحيم` volgen analoog.)*

Resultaat:

| Parameter | Waarde |
|---|---|
| `source_text` | بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ |
| `normalized_text` | بسماللهالرحمنالرحيم |
| normalizer | `abjad_basis_v1` |
| normalizer_ref | vastgelegd via commit `0e53e3d` |

---

## 7. Abjad-berekening

De Abjad-waardetabel (28 letters):

| Letter | Waarde | Letter | Waarde | Letter | Waarde |
|---|---|---|---|---|---|
| ا | 1 | ك | 20 | ق | 100 |
| ب | 2 | ل | 30 | ر | 200 |
| ج | 3 | م | 40 | ش | 300 |
| د | 4 | ن | 50 | ت | 400 |
| ه | 5 | س | 60 | ث | 500 |
| و | 6 | ع | 70 | خ | 600 |
| ز | 7 | ف | 80 | ذ | 700 |
| ح | 8 | ص | 90 | ض | 800 |
| ط | 9 | | | ظ | 900 |
| ي | 10 | | | غ | 1000 |

### Woord-voor-woord

$$
\text{بسم} = 2 + 60 + 40 = 102
$$

$$
\text{الله} = 1 + 30 + 30 + 5 = 66
$$

$$
\text{الرحمن} = 1 + 30 + 200 + 8 + 40 + 50 = 329
$$

$$
\text{الرحيم} = 1 + 30 + 200 + 8 + 10 + 40 = 289
$$

$$
A_{\text{Abjad}}(s_{\text{basis}}) = 102 + 66 + 329 + 289 = 786
$$

unknown_characters_after_normalization: []

*(Harakat en spaties zijn bekende normalisatietekens en zijn per regel verwijderd.)*

---

## 8. Digitale wortel

De digitale wortel is een aparte operator:

$$
DR(n) = 
\begin{cases}
0, & n = 0 \\
1 + ((n-1) \bmod 9), & n > 0
\end{cases}
$$

$$
DR(786) = 1 + ((786-1) \bmod 9) = 1 + (785 \bmod 9) = 1 + 2 = 3
$$

Lokaal eindpunt:

$$
r_{\text{local},A,\text{Basmala}} = 3
$$

Dit lokale eindpunt is niet de volledige boekreturn:

$$
r_{\text{return}} = \operatorname{undefined}
$$

$$
\operatorname{status}_{\text{validated}}(r_{\text{begin}}, r_{\text{return}}) = \text{ongetest}
$$

De toestanden (6) en (9) worden niet door deze specifieke Abjad-berekening geproduceerd. Zij behoren tot het algemene NPR-validatietrio en worden via afzonderlijk gedefinieerde routes behandeld.

---

## 9. Operationele status

| Parameter | Waarde |
|---|---|
| `status_repo_import` | uitgevoerd |
| `status_source_file_identified` | uitgevoerd |
| `status_source_integrity` | gecontroleerd |
| `status_source_encoding` | geldig |
| `status_selection(Basmala)` | uitgevoerd |
| `status_normalization(abjad_basis_v1)` | uitgevoerd |
| `status_unknown_characters_after_normalization` | [] |
| `status_local(A_Abjad, Basmala)` | uitgevoerd |
| `status_reproducible(A_Abjad, Basmala)` | ja |
| `status_validated(r_begin, r_return)` | ongetest |

---

## 10. Drie niveaus van uitvoering

Artikel 5 onderscheidt drie niveaus:

### Niveau 1 — bronroute

$$
\text{GitHub} \rightarrow \text{lokale checkout} \rightarrow \texttt{quran\_field} \rightarrow Q_{\text{source}}
$$

Status: **uitgevoerd** (bestand, commit, hash bekend).

### Niveau 2 — lokale Basmala-Abjadroute

$$
Q_{\text{source}} \rightarrow S_{\text{Basmala}} \rightarrow N_{\text{Abjad}} \rightarrow A_{\text{Abjad}} \rightarrow 786 \rightarrow DR \rightarrow 3
$$

Status: **lokaal uitgevoerd**.

### Niveau 3 — corpusbrede NPR-route

$$
Q_{\text{source}} \rightarrow Q_{\text{corpus-analysis}} \rightarrow \text{3–6–9-structuur}
$$

Status: **ongetest**. Een beschikbare bronmap alleen bewijst nog geen corpuspatroon. Deze route geldt als uitgevoerd alleen als ook de volledige corpusselectie, normalisatie, operator, aggregatieregel en uitvoer reproduceerbaar zijn vastgelegd.

---

## Bijlage A — Auditrapport (JSON)

Het volledige auditrapport is beschikbaar als:

```
quran_field/derived/basmala_abjad_audit.json
```

## Bijlage B — Uitvoerscript

De volledige pipeline is geïmplementeerd als:

```
quran_field/scripts/audit_basmala_abjad.py
```

Uitvoering:

```bash
cd NPR_OS_sandbox
python3 quran_field/scripts/audit_basmala_abjad.py
```

---

*Einde Artikel 5.*
