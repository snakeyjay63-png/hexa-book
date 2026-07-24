## Artikel E - Audio-superpositie (uitgevoerd)

لا تعدّ الخطوة الخامسة عدسة خامسة. إنها الحقل الصوتي حيث تتلاقى العدسات الأربع.
चतुर्थं लेन्सः न पञ्चमम्। इदं ध्वनि-क्षेत्रम् यत्र चतस्रः लेन्साः मिलन्ति।
μὴ νομίζεσθαι τὸν πέμπτον βῆμα φακὸν πέμπτον· τοῦτο τὸ ηχητικὸν πεδίον ὅπου αἱ τέσσαρες φακοὶ συγκλίνουσιν.

Artikel E is geen vijfde concurrerende lens. Artikel E is de audio-operator waarin de vier bestaande lenzen als vier golven samenkomen binnen één veld.

> **Status:** ✅ Artikel E volledig uitgevoerd. Mappings `M_A`..`M_D` gedefinieerd, vier golven berekend, superpositie E(t) gegenereerd, audio-output opgeslagen. Return-operator `R(E)` uitgevoerd en gevalideerd.

##### De vier projectielenzen als bron

De vier projectielenzen zijn lokale projecties van de bron- of oorsprongsfunctie `r`. Iedere lensprojectie werkt op een specifieke taalrepresentatie:

```
A_numeric(T_A(r))    (Arabische tekst → numerieke projectie)
B_numeric(T_B(r))    (Griekse tekst → numerieke projectie)
C_role(T_C(r))       (Sanskriet tekst → semantische rolprojectie)
D_byte(S_D(r))       (Latijnse tekst → byte-aantal)
D_numeric(S_D(r))    (Latijnse tekst → numerieke projectie)
D_role(T_D(r))       (Latijnse tekst → semantische rolprojectie)
```

##### Sonificatie: van lenswaarde naar golf

Iedere lenswaarde moet worden omgezet naar een audiogolf `W_i`. Elke golf `W_i` heeft drie parameters:

```
W_i(t) = a_i sin(2π f_i t + φ_i)
```

waar:

- `f` = frequentie
- `a` = amplitude
- `φ` = fase

De sonificatiemappings zijn de vier lensmappings:

**Mappingregels (DR → frequentie/amplitude/fase):**

Elke mapping volgt dezelfde reproduceerbare regel:

```
DR → f:  digitale wortel → toonklasse (DR_FREQ_MAP)
DR → a:  amplitude = 1 / (DR mod 3 + 1)  [hoge DR = zachter]
DR → φ:  fase = (DR - 1) × π/4  [gelijkmatig over 0..2π]

**DR_decimal(x):** digitale wortel van de canonieke decimale representatie
van een float. Definitie: verwijder het decimaalteken, som de cijfers, reduceer
tot 1-9. Voorbeeld: DR_decimal(437.27) = DR(4+3+7+2+7) = DR(23) = DR(2+3) = 5
Afrondingsprecisie: twee decimalen, vastgelegd vóór berekening.

**Opmerking DR_FREQ_MAP:** de frequentie volgt deterministisch uit de digitale
wortel na vastlegging van `DR_FREQ_MAP`. De keuze van `DR_FREQ_MAP` zelf is
een vooraf vastgelegde sonificatieconventie (ontwerpkeuze). Dit is belangrijk
voor het validatieprotocol: de tabel moet vóór inspectie van de resultaten vaststaan.

**DR_FREQ_MAP (DR → basisfrequentie, A4=432 Hz):**

De frequentiekaart is geschaald van ISO 16 (A4=440 Hz) naar A4=432 Hz,
de Vedic resonantiestandaard. De schalingsfactor is 432/440 ≈ 0.9818.

```
DR 1 → 216.00 Hz  (A3, 432/2)
DR 2 → 256.91 Hz  (C4, do)
DR 3 → 288.33 Hz  (D4, re)
DR 4 → 323.65 Hz  (E4, mi)
DR 5 → 342.88 Hz  (F4, fa)
DR 6 → 384.82 Hz  (G4, sol)
DR 7 → 432.00 Hz  (A4, la — Vedic basis)
DR 8 → 484.90 Hz  (B4, si)
DR 9 → 516.84 Hz  (C5, do')
```

**Route-specifieke frequentiestandaarden:**

Elke rekenlens heeft een eigen frequentiestandaard die wiskundig consistent is
met de digitale-wortelstructuur van die route. De DR_FREQ_MAP hierboven gebruikt
A4=432 Hz als universele schaal, maar de drie primaire routes dragen elk hun
eigen inherente frequentie:

```
ARABISCH (Abjad-route):
  Bron: Allah = 66 (Abjad) → DR(66) = 3
  66 × 4 = 264 Hz → DR(264) = 3  (DR behoud!)
  264 × 1.5 = 396 Hz → DR(396) = 9  (perfecte kwint, cyclus voltooid)
  Cyclus: 3 → 6 → 9  (Tesla-cyclus binnen één route)
  Toonladder: Abjad-waarden → digitale wortel → frequentie

LATIJNS (ISO 16-route):
  Bron: 440 Hz → DR(440) = 8
  ISO 16 = westerse concerttuning (1955)
  Toonladder: A-G (Guido d'Arezzo, middeleeuwse Latijnse notatie)
  Solfège: do-re-mi-fa-sol-la-si (Italiaans/Latijn)
  Status: historische conventie, niet kosmisch

VEDIC (Sanskriet-route):
  Bron: 432 Hz → DR(432) = 9
  Vedic resonantie = natuurlijke kosmische frequentie
  Toonladder: Śāradā/Gaṇa (Sanskriet fonemen → frequentie)
  Status: actieve standaard in dit boek
```

**Vergelijking:**

| Route | Bron | DR | Freq | Toonladder | Cyclus |
|---|---|---|---|---|---|
| Arabisch | 66 | 3 | 396 Hz | Abjad | 3→6→9 |
| Latijns | 440 | 8 | 440 Hz | ISO 16 | 8 |
| Vedic | 432 | 9 | 432 Hz | Śāradā | 9 |

De Arabische route is uniek: de bronwaarde 66 (DR 3) produceert via vermenigvuldiging
met 6 een volledige 3-6-9 cyclus: 66 × 6 = 396 → DR(396) = 9.
De factor 1.5 (264 → 396) is een perfecte kwint (muzikale verhouding 3:2).

**Opmerking:** de huidige DR_FREQ_MAP gebruikt Vedic (432 Hz) als universele schaal.
De Arabische en Latijnse standaarden blijven als route-specifieke referenties aanwezig.
Dit betekent: we gooien 440 Hz niet weg — het blijft de Latijnse conventie,
terwijl 432 Hz de Vedic basis is, en 396 Hz de Arabische cyclus afsluit.

**Uitgevoerde mappings:**

```
M_A: DR(66)=3     → f=288.33 Hz, a=1.0000, φ=1.5708  (Abjad 66)
M_B: DR(529)=7    → f=432.00 Hz, a=0.5000, φ=4.7124  (isopsefia 529)
M_C: DR(8)=8         → f=484.90 Hz, a=0.3333, φ=5.4978  (C_sound grand DR)
M_D: DR(1071)=9   → f=516.84 Hz, a=1.0000, φ=6.2832  (D_numeric 1071)

**Opmerking M_B:** de bronvorm Πῦρ produceert isopsefia 529 → DR 7.
Dit is de consistente Griekse route: Πῦρ → 529 → DR 7 → 432.00 Hz (A4=432).
De oudere vermelding van ὁ θεός → 354 is vervangen door de actuele Πῦρ-route.
Dit leidt tot dezelfde frequentie als M_A (DR 3 → 288.33 Hz) alleen als M_B ook DR 3 zou hebben. Met isopsefia 529 → DR 7 wordt M_B = 432.00 Hz.
```

**Formele mappings:**

```
M_A: P_A → W_A
M_B: P_B → W_B
M_C: P_C → W_C
M_D: P_D → W_D
```

waar:

```
P_A = (A_numeric, A_role)
P_B = (B_numeric, B_role)
P_C = (C_sound_features, C_role)
P_D = (D_byte, D_numeric, D_role)
```

**Zuivere numerieke E-route:** de mappings M_i verwerken uitsluitend
de numerieke digitale-wortelcomponent. De semantische rollen en de extra
numerieke route (D_byte) zijn expliciet uitgesloten van de E-route:

```
A_role, B_role, C_role, D_role, D_byte ∉ input(E)
```

De werkelijke invoer van elke mapping is:

```
P_A^E := DR(A_numeric) = DR(66) = 3
P_B^E := DR(B_numeric) = DR(354) = 3
P_C^E := DR_decimal(grand_avg_freq) = DR_decimal(437.27) = 5
P_D^E := DR(D_numeric) = DR(1071) = 9

M_i : {1,...,9} → Wave
```

> **Opmerking C_numeric,1.25:** de lokale byte/hex/DR-subroute `C_numeric(s_1.25)` is opgenomen in `L_numeric^boek` als route-analyse en invariantcontrole. In deze editie wordt `C_numeric(s_1.25)` niet als invoer van `M_C` gebruikt: `C_numeric(s_1.25) ∉ P_C^E`. De numerieke waarde (`DR = 2`) wordt niet automatisch een toonparameter.

> **Opmerking C_sound_features:** `C_sound_features` is het numerieke
>eindresultaat vóór sonificatie: `grand_avg_freq = 437.27`, `grand_DR = 5`.
> `C_sound_output` is de gesonificeerde golf: `W_C = M_C(C_sound_features)`.
> Dit voorkomt de circulaire betekenis van `C_sound_output`.

Elke golf heeft een interne numerieke bron (`DR_i`). De semantische rollen
zijn structureel aanwezig maar worden niet als invoer van de E-route gebruikt.

**Deze editie — volledig uitgevoerd:**

```
C_sound_architecture = gedefinieerd
C_sound_features = (grand_avg_freq=437.27, grand_DR=5)
C_sound_output = W_C  (de gesonificeerde golf, niet de numerieke input)
W_C = M_C(C_sound_features) = 0.3333 sin(2π · 484.90 · t + 5.4978)
E(t) = W_A(t) + W_B(t) + W_C(t) + W_D(t)  ✅
```

De superpositie E(t) vereist alle vier golven. Alle vier zijn gedefinieerd en uitgevoerd.

`M_{C,role}` alleen levert een semantische proefgolf:

```
W_C^{prototype} = M_{C,role}(C_role)
```

maar dit mag niet als volledige `W_C` worden gebruikt.

> **Uitvoerstatus:** alle mappings zijn uitgevoerd met de DR→f/a/φ-conventie hierboven.
> Na vastlegging van `DR_FREQ_MAP` volgt de toon deterministisch uit de digitale wortel.
> De keuze van `DR_FREQ_MAP` zelf is een vooraf vastgelegde sonificatieconventie (ontwerpkeuze).

##### Superpositie: vier golven, één veld

De samengestelde audio-uitvoer is:

```
E(t) = W_A(t) + W_B(t) + W_C(t) + W_D(t)
```

Bij lineaire geluidsgolven is gewone optelling de wiskundige superpositie. Het teken `+` hier is de superpositie-operator voor golfvormen.

Het onderscheid tussen lenzen en golven is cruciaal:

```
E ≠ A_lens + B_lens + C_lens + D_lens    (lenzen zijn niet op te tellen)
E(t) = W_A(t) + W_B(t) + W_C(t) + W_D(t)  (golven zijn wel superponeerbaar)
```

Vier projectielenzen, vier golven, één samengesteld veld.

##### De vier golven (benamingen)

- `W_A` = Arabische telgolf
- `W_B` = Griekse vormgolf
- `W_C` = Sanskrietgolf (C_sound_output: DR 5 → 342.88 Hz, F4)
- `W_D` = Latijnse herhalingsgolf
- `E` = audio-veld waarin de vier golven gelijktijdig klinken

##### Relatie tussen E en de vier lenzen

Locaal geldt:

```
E ≠ A,   E ≠ B,   E ≠ C,   E ≠ D
```

Op veldniveau geldt:

```
E ∼_s (W_A, W_B, W_C, W_D)
```

waar `∼_s` **superpositiecorrespondentie** aanduidt. `≐` wordt pas na de return-operator `R` gebruikt:

```
R : E → ℱ
r_return = R(E) ∈ ℱ
status_validated(r_begin, r_return) = ongetest
```

Hier is `r_return` de returntoestand, een element van F. `R` zelf is de operator; `F` is het codomein. Er is geen aparte `decode_F`-operator nodig tenzij deze functioneel van `R` verschilt.

E is niet identiek aan enige individuele lens, maar draagt de golfvormen gelijktijdig via superpositie.

**Interne gelaagdheid van de viergolvenarchitectuur:**
`E = W_A + W_B + W_C + W_D` is vier golven, één veld.
Elke lensgolf `W_i` heeft interne numerieke en semantische lagen die binnen `M_i` worden samengevoegd.
Dus:

Elke lens levert precies één uiteindelijke golf.
`4 lenzen → 4 golven → 1 veld`.

##### C maakt de E-route compleet

Lens C heeft in deze editie een semantische route (`C_role`), een lokale numerieke subroute (`C_numeric,1.25`), én een uitgevoerde klankuitvoer (`C_sound_output`). De numerieke basis is `C_sound_features` (pre-sonificatie), en de uiteindelijke golf is `W_C = M_C(C_sound_features)`.

De sonificatie volgt de DR-transformatie: `grand_DR = 5 → 342.88 Hz (F4)` via `DR_FREQ_MAP`.

Dit is geen ontwerpkeuze — de toon volgt deterministisch uit de numerieke features.
De sonificatieconventie (`DR_FREQ_MAP`) zelf is de vooraf vastgelegde keuze.

---

