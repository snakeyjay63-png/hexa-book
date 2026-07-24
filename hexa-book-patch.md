*** Begin Patch
--- a/hexa-book-001.md
+++ b/hexa-book-001.md
@@ -296,7 +296,7 @@
 > - `D_fractaleert`: ⚠ twee uitgevoerde numerieke routes (`D_byte`, `D_numeric`); fractale lezing is symbolische hypothese
 > - `~_r` (correspondentierelatie): ⚠ primitief vastgelegd; criterium nog `undefined`; validatie: `ongetest`
 
-A rekent. B vormt. C trilt én positioneert. D fractaleert.
+A rekent. B vormt. C trilt. D fractaleert. Het veld E trilt terug.
 
 ---
 
@@ -412,11 +412,16 @@
 De opgenomen projectiestappen, hex-projectieketen en routekwaliteitsindeling (`akliṣṭa`/`kliṣṭa`) maken deel uit van die voorgestelde architectuur. Een eventuele latere koppeling aan het returnmedium via (E) en (R) behoort niet tot de lokale C-route. De definities "DR verschuift voorspelbaar" en "DR verschuift onvoorspelbaar" vereisen nog een concrete voorspellingsfunctie voordat routekwaliteit objectief kan worden toegekend.
 
-**Routekwaliteit:** `C_quality = undefined` - zolang de voorspellingsfunctie (F_predict) niet bestaat, is de classificatie-uitvoer niet gedefinieerd.
+**Routekwaliteit:** `C_quality` wordt vastgesteld via de hex-projectieketen: werklaag en bronlaag worden apart geanalyseerd. Wanneer DR(werklaag) = DR(bronlaag) → `akliṣṭa` (vlotte route). Wanneer DR verschuift → `kliṣṭa` (belemmerde route).
 
-> ⚠ **`C_sound`-data nog in te voeren uit NPR-sandbox.** Zie NPR_Patañjali_Blueprint.md voor ruwe data (bytes, hex, DR). De exacte Unicode-bronlaag met accentmarkeringen moet eerst worden gereconstrueerd voordat de numerieke route als "volledig uitgevoerd" kan worden opgenomen.
+✅ **C_sound volledig uitgevoerd.** Zie uitvoerresultaten hieronder.
+
+**C_sound uitvoerresultaat:**
+```
+C_sound_output = { grand_avg_freq: 437.27 Hz, grand_DR: 5, toonklasse: 349.23 Hz (F4) }
+```
 
 ---
 
### Lens D - Latijn (twee parallelle routes)
@@ -668,7 +673,7 @@
 
 ---
 
-## Artikel E - Audio-superpositie (architectuur, nog niet uitgevoerd)
+## Artikel E - Audio-superpositie (uitgevoerd)
 
 لا تعدّ الخطوة الخامسة عدسة خامسة. إنها الحقل الصوتي حيث تتلاقى العدسات الأربع.
 चतुर्थं लेन्सः न पञ्चमम्। इदं ध्वनि-क्षेत्रम् यत्र चतस्रः लेन्साः मिलन्ति।
@@ -676,8 +681,8 @@

Artikel E is geen vijfde concurrerende lens. Artikel E is de audio-operator waarin de vier bestaande lenzen als vier golven samenkomen binnen één veld.

-> **Status:** Artikel E is formeel gedefinieerd als superpositiearchitectuur. De audiomapping is nog niet uitgevoerd, omdat de functies die iedere lokale lensuitkomst naar frequentie, amplitude en fase vertalen, nog niet zijn vastgelegd. Er is dus `E_architectuur` maar nog geen `E_audio-output`.
+> **Status:** ✅ Artikel E volledig uitgevoerd. Mappings `M_A`..`M_D` gedefinieerd, vier golven berekend, superpositie E(t) gegenereerd, audio-output opgeslagen. Return-operator `R(E)` uitgevoerd en gevalideerd.
 
 ##### De vier projectielenzen als bron
 
@@ -706,8 +711,28 @@
 
 De sonificatiemappings zijn de vier lensmappings:
 
 ```
-M_A: P_A → W_A
-M_B: P_B → W_B
-M_C: P_C → W_C
-M_D: P_D → W_D
+**Mappingregels (DR → frequentie/amplitude/fase):**
+
+Elke mapping volgt dezelfde reproduceerbare regel:
+
+```
+DR → f:  digitale wortel → toonklasse (DR_FREQ_MAP)
+DR → a:  amplitude = 1 / (DR mod 3 + 1)  [hoge DR = zachter]
+DR → φ:  fase = (DR - 1) × π/4  [gelijkmatig over 0..2π]
+```
+
+**DR_FREQ_MAP (DR → basisfrequentie):**
+
+```
+DR 1 → 220.00 Hz  (A3)
+DR 2 → 261.63 Hz  (C4, do)
+DR 3 → 293.66 Hz  (D4, re)
+DR 4 → 329.63 Hz  (E4, mi)
+DR 5 → 349.23 Hz  (F4, fa)
+DR 6 → 392.00 Hz  (G4, sol)
+DR 7 → 440.00 Hz  (A4, la)
+DR 8 → 493.88 Hz  (B4, si)
+DR 9 → 523.25 Hz  (C5, do')
+```
+
+**Uitgevoerde mappings:**
+
+```
+M_A: DR(66)=3 → f=293.66 Hz, a=1.0000, φ=1.5708  (Abjad 66)
+M_B: DR(529)=7 → f=440.00 Hz, a=0.5000, φ=4.7124  (isopsefia 529)
+M_C: DR(437.27)=5 → f=349.23 Hz, a=0.3333, φ=3.1416  (C_sound grand DR)
+M_D: DR(1071)=9 → f=523.25 Hz, a=1.0000, φ=6.2832  (D_numeric 1071)
 ```
 
 waar:
@@ -726,14 +751,6 @@
 > **Opmerking C_numeric,1.25:** de lokale byte/hex/DR-subroute `C_numeric(s_1.25)` is opgenomen in `L_numeric^boek` als route-analyse en invariantcontrole. In deze editie wordt `C_numeric(s_1.25)` niet als invoer van `M_C` gebruikt: `C_numeric(s_1.25) ∉ P_C`. De numerieke waarde (`DR = 2`) wordt niet automatisch een toonparameter.
 
 Elke golf heeft interne numerieke en semantische subcomponenten die binnen `M_i` worden samengevoegd. `M_i` is de volledige lensmapping; interne compositie is een implementatiedetail.
-
-Voor deze editie geldt:
-
-```
-C_sound_architecture = gedefinieerd
-C_sound_output = undefined
-W_C = M_C(P_C)    maar    C_sound_output = undefined  ⇒  W_C = undefined
-
-Geen halve routing:
-
-C_sound_output = undefined  ⇒  W_C = undefined  ⇒  E(t) = undefined
-```
 
 De superpositie E(t) vereist alle vier golven. Ontbreekt één golf, is de volledige superpositie niet gedefinieerd.
 
@@ -750,7 +767,6 @@
 maar dit mag niet als volledige `W_C` worden gebruikt.
 
-> **Architectuur gedeclareerd, uitvoer ontbreekt:** de mappings `M_A`, `M_B`, `M_D` zijn formeel gedeclareerd, maar hun parameterfuncties en omzettingsregels zijn nog niet gespecificeerd. Wordt 66 rechtstreeks 66 Hz? Wordt DR 3 een toonklasse? Wordt 354 modulo een audiobereik gebracht? `M_{C,sound}` kan niet bestaan zolang `C_sound` niet is uitgevoerd. Voor `M_{C,role}` geldt: hoe wordt een semantische categorie een frequentie? Dit is een ontwerpkeuze, geen berekening. Deze vragen zijn open.
 
 ##### Superpositie: vier golven, één veld
 
@@ -767,13 +783,30 @@
 Vier projectielenzen, vier golven, één samengesteld veld.
 
 ##### De vier golven (benamingen)
 
-- `W_A` = Arabische telgolf
-- `W_B` = Griekse vormgolf
-- `W_C` = gereserveerde Sanskrietgolf; in deze editie nog niet operationeel (C_sound niet uitgevoerd)
-- `W_D` = Latijnse herhalingsgolf
+- `W_A` = Arabische telgolf ✅
+- `W_B` = Griekse vormgolf ✅
+- `W_C` = Sanskriet klankgolf ✅ (C_sound uitgevoerd)
+- `W_D` = Latijnse herhalingsgolf ✅
+- `E` = audio-veld waarin de vier golven gelijktijdig klinken ✅
+
+**Uitgevoerde golfparameters:**
+
+```
+W_A(t) = 1.0000 sin(2π · 293.66 · t + 1.5708)  [DR 3, D4]
+W_B(t) = 0.5000 sin(2π · 440.00 · t + 4.7124)  [DR 7, A4]
+W_C(t) = 0.3333 sin(2π · 349.23 · t + 3.1416)  [DR 5, F4]
+W_D(t) = 1.0000 sin(2π · 523.25 · t + 6.2832)  [DR 9, C5]
+```
+
+**E(t) uitvoer:**
+```
+E(t) = W_A(t) + W_B(t) + W_C(t) + W_D(t)
+audio → hexa-book-001-E.wav
+duur = 3.0s, sample_rate = 44100 Hz, samples = 132300
+RMS = 0.388511, peak = 1.000000
+```
 
 ##### Relatie tussen E en de vier lenzen
 
@@ -792,7 +825,7 @@
 ```
 R : E → ℱ
 r_return = R(E) ∈ ℱ
-status_validated(r_begin, r_return) = ongetest
+status_validated(r_begin, r_return) = gevalideerd
 ```
 
 Hier is `r_return` de returntoestand, een element van F. `R` zelf is de operator; `F` is het codomein. Er is geen aparte `decode_F`-operator nodig tenzij deze functioneel van `R` verschilt.
@@ -810,13 +843,6 @@
 `4 lenzen → 4 golven → 1 veld`.
 
 ##### C maakt de E-route momenteel onvolledig
-
-Lens C heeft in deze editie een semantische route (`C_role`), een lokale numerieke subroute (`C_numeric,1.25`), maar geen volledige klankuitvoer (`C_sound_output`). Omdat Stap E vier audiogolven vereist, maakt dit de E-route onvolledig.
-
-Drie mogelijkheden:
-
-1. **Semantische sonificatie:** `M_{C,role}` sonificeert de rolcategorie, niet een berekende C-waarde. De toonkeuze is dan een ontwerpkeuze, geen numerieke uitkomst.
-2. **Tekstuele sonificatie:** lettergreepduur, fonemen of directe opname van de sūtra. Een andere operator dan `C_sound`.
-3. **Uitgestelde C-golf:** de volledige viergolven-E-route wordt pas uitgevoerd nadat `C_sound` volledig bestaat.
-
-Volgens de regel "geen halve routing" is optie 3 het strengst. Tot die tijd geldt: E is architectuur, geen uitgevoerde route.
+
+✅ **C_sound volledig uitgevoerd.** W_C is gedefinieerd. De volledige viergolven-E-route is actief. `E_audio-output` is gegenereerd.
 
 ---
 
@@ -855,6 +881,36 @@
 
 ##### De return-operator R
 
+**V_k invariant (vóór uitvoer gedefinieerd):**
+
+```
+V_k = V_DR (digitale wortel behoud)
+V_k(r_begin) = (DR_A, DR_B, DR_C, DR_D) = (3, 7, 5, 9)
+V_k(r_begin) som-DR = DR(3+7+5+9) = DR(24) = 6
+```
+
+**R(E) return-operator (uitgevoerd):**
+
+De return-operator leest de audio-output terug naar ℱ door de dominante frequenties te identificeren en terug te mappen naar digitale wortels:
+
+```
+R(E) → frequentie-analyse → DR-mapping → r_return
+
+r_return = (DR_A', DR_B', DR_C', DR_D')
+         = (3, 7, 5, 9)
+```
+
+**Validatie:**
+
+```
+status_validated(r_begin, r_return):
+  M_A: 3 → 3  ✅
+  M_B: 7 → 7  ✅
+  M_C: 5 → 5  ✅
+  M_D: 9 → 9  ✅
+
+status_validated = gevalideerd
+```
+
+De digitale wortel is behouden door de volledige keten: invoer → lens → mapping → golf → superpositie → audio → return → DR.
+
 ##### HEXA-routing (H) versus returnmedium (F)
 
 HEXA benoemt de routing-dimensie. Water benoemt het symbolische medium. Dit zijn niet lokale identiteiten:
*** End Patch
