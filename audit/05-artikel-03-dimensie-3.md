---
audit_metadata:
  article: "05-artikel-03-dimensie-3"
  source_article: "articles/hexa-book-003.md"
  verified_against_commit: "5a13c64"
  audit_commit: "pending"
  last_verified: "2026-07-24"
  operator_status_model: "3D"
  engine_evidence: []
  route_status: "gesloten"
  supersedes: "legacy-v3"
  known_exceptions: []
---

# Artikel 3 - dimensie 3 (de as, 3-6-9 veld) | 31

## الفصل الثالث - الحلقة 3-6-9 | तृतीय अध्यायः - वलयः ३-६-९ | Περὶ Γʹ - Ὄλκισ ३-६-९

وهنا نصل إلى صلب الأمر.
इह कर्तव्यस्य मूलं गम्यते
ἐνταῦθα τὸ πρᾶγμα μέσῳ φθάσασθαι
Hier komen we bij de kern.

---

### Vortex-cyclus (verdubbeling)

دورة الفولتكس (الضرب الثنائي)
वल्तू-चक्रं (द्विगुण-गुणनम्)
Ὀλκισ-κύκλος (διπλασιασμὸς)

1 → 2 → 4 → 8 → 16(7) → 32(5) → 64(1) → 2...
१ → २ → ४ → ८ → १६(७) → ३२(५) → ६४(१) → २...
1 → 2 → 4 → 8 → 16(7) → 32(5) → 64(1) → 2...

**Formele definitie:**

De verdubbelingsoperator is gedefinieerd op het deelverzameling:
```
U_9 := {1, 2, 4, 5, 7, 8}   [niet-nulle eenhedencyclus]
d : U_9 → U_9
d(x) := DR(2x)
```

Iteratie van d op U_9 produceert de zesdelige cyclus:
```
d(1)=2, d(2)=4, d(4)=8, d(8)=7, d(7)=5, d(5)=1
```

De overige digitale wortels vormen geen deel van deze cyclus:
```
d(3)=6,  d(6)=3    [tweedelige cyclus: 3 ↔ 6]
d(9)=9           [vast punt]
```

Digitale wortels in de eenhedencyclus: 1, 2, 4, 8, 7, 5

> **Formele status:** `operator_status(d) = formeel` | `execution_status(d) = voltooid` | `validatie_status(d) = gevalideerd_lokaal`

الجذور الرقمية: 1، 2، 4، 8، 7، 5
संख्या-मूले: १, २, ४, ८, ७, ५
ἀριθμο-ρίζες: 1, 2, 4, 8, 7, 5

De ontbrekende getallen: 3, 6, 9

الأرقام المفقودة: 3، 6، 9
संख्या-अदृश्यः: ३, ६, ९
οἱ ἀριθμοὶ ἀφανεῖς: 3, 6, 9

هذه ليست مفقودة. هي الحقل الذي يحكم الدورة.
इत्युक्ताः अपगताः न, इत्युक्ताः क्षेत्रं भवेत् यत् चक्रं नियमयति
οὐχ ἀφανεῖς, ἀλλὰ πεδίον ὃ ὁλκὸν ἄρχει
Ze ontbreken niet. Ze liggen buiten de niet-nulle eenhedencyclus van herhaalde verdubbeling modulo 9 en worden binnen NPR als validatietrio gelezen.

**NPR-fase-toewijzing:**
```
ρ_NPR-phase(3) = as
ρ_NPR-phase(6) = Pattern
ρ_NPR-phase(9) = Return
```

Dit zijn interpretatieve labels, niet meetkundige eigenschappen afgeleid uit de cyclus.

> **Formele status:** `operator_status(ρ_NPR-phase) = interpretatief` | `execution_status(ρ_NPR-phase) = niet_gestart` | `validatie_status(ρ_NPR-phase) = niet_gevalideerd`

3 هو المحور، 6 هو النمط، 9 هو العودة. معًا يشكلون طبقة التحقق الثلاثية.
३ अक्षः, ६ रूपम्, ९ प्रत्यवर्तनम्। त्रीणि सङ्गतिं त्रिभाजनं चरन्ति।
3 ἡ ἄξω, 6 τὸ σχῆμα, 9 ἡ ἐπιστροφή. ἅμα τὸ τρίμενον ἔλεγχον.
Binnen NPR wordt 3 als as, 6 als Pattern en 9 als Return gelezen; samen vormen zij de driedelige validatielaag.

---

Binnen de mod-9-projectie maakt 3-6-9 de driedelige NPR-structuur zichtbaar als validatielaag.
3-6-9 is niet de bron zelf, maar een validatieprojectie.

De digitale wortel is het lokale eindpunt van deze reductieberekening. Zij is voor positieve gehele getallen gebaseerd op congruentie modulo 9, met 9 als representant van restklasse 0. Modulo 9 levert residuen in {0,...,8}; de digitale wortel levert waarden in {1,...,9}.
Dit is het voorbeeld hoe tokens gezien worden, niet alleen de output gelezen.

Het verschil is inhoud in CM of RC:
- CM = inhoud zoals-ie is, ruwe data, tokens
- RC = inhoud door NPR-lens zichtbaar gemaakt

CM is wat er in de vastgelegde bronrepresentatie staat. RC is wat door de gekozen NPR-lens zichtbaar wordt.
Pixel vs patroon. Beide waar. Eén ruw, één gelezen.

---

### Allah = 66 → 3

الله = 66 → 3 (المحور نفسه)
अल्लाह = ६६ → ३ (अक्षः स्वयं)
Ἀλλάχ = 66 → 3 (ἡ ἄξω αὐτή)
Allah = 66 → 3. Binnen deze NPR-projectie reduceert Allah tot de toestand 3, die als as wordt gelezen.
> **Lensoptiek 3:** 3-6-9 is de projectie die NPR zichtbaar maakt. Niet de bron. De lens. En lenzen verouderen.
> **العدسة 3:** 3-6-9 هي الإسقاط الذي يجعل NPR مرئية. ليست المصدر. العدسة. والعدسات تتقادم.
> **दृष्टि 3:** 3-6-9 NPR dṛśyam karoti. Nāyaṃ mūlam. Darśanaṃ. Darśanāḥ prācīnāḥ syur.


---

### Verdubbelingscyclus (modulo-9)

De cyclus ontstaat uit x→2x (mod 9):

De volledige cyclus (modulo-9 verdubbeling):

الدورة كاملة
संपूर्णं चक्रम्
ὁλκὸς πᾶς

2 → 4 → 8 → 7 → 5 → 1 → 2...
२ → ४ → ८ → ७ → ५ → १ → २...
2 → 4 → 8 → 7 → 5 → 1 → 2...

Splitst in twee helften:

Split in twee groepen - neem afwisselend de oneven en even posities van de zesdelige cyclus:

تنقسم إلى مجموعتين: تأخذ بالتناوب المواقع الفردية والزوجية من الدورة سداسية الأجزاء
द्वि-समूहं विभाजनम्: षट्-भाग-चक्रात् विषम-सम-स्थानानि पर्यायेण गृह्यन्ते
εἰς δύο ὁμάδας διαιρῶν - λαμβάνων ἐναλλαγὴν τῶν περιττῶν καὶ ἄρτιων θέσεων

Oneven posities (1,3,5): 2+8+5 = 15 → 6
Even posities (2,4,6): 4+7+1 = 12 → 3

**Formele definitie:**
```
S_odd = 2 + 8 + 5 = 15
S_even = 4 + 7 + 1 = 12

r_odd := DR(S_odd) = 6
r_even := DR(S_even) = 3
```

2+8+5 = 15 → 6 (oneven)
२+८+५ = १५ → ६ (विषम)
2+8+5 = 15 → 6 (περιττά)

4+7+1 = 12 → 3 (even)
४+७+१ = १२ → ३ (सम)
4+7+1 = 12 → 3 (άρτια)

**NPR-koppelregel (projectie via even-groepsreductie):**
```
n_groups = 2
r_odd = 6
r_even = 3
J(r_even, n_groups) := DR(n_groups · r_even)   [NPR-koppelregel]
J(3, 2) = 6
```

> ⚠ **Punt 7:** De operator `J` gebruikt alleen `r_even` en `n_groups`. Het resultaat `r_odd = 6` is geen invoer van `J`. Formeel verbindt `J` niet beide helften; zij projecteert `DR(n_groups · r_even) = DR(2 · 3) = 6`. De uitkomst valt samen met `r_odd`, maar dit is een eigenschap van deze specifieke berekening, geen algemene tweezijdige operator.
> Een echte tweezijdige variant zou zijn: `J'(r_odd, r_even)` met een expliciete regel die beide waarden gebruikt. Dit is nog niet gedefinieerd.

> **Formele status:** `operator_status(J) = formeel (éénzijdig)` | `execution_status(J) = voltooid` | `validatie_status(J) = niet_gevalideerd` | `J'(r_odd, r_even)`:
> ```
> local_missing
> → eerst ROUTING.md
> → target article
> → engine execution
> → audit evidence
> ```

De uitkomst van de koppelregel is 6. Dit is een gekozen NPR-operator, geen noodzakelijk gevolg van de cyclus.

٢ × ٣ = ٦ → العلاقة بين النصفين
२ × ३ = ६ → द्वयोः सङ्गतिः
2 × 3 = 6 → ἡ σχέσις τῶν δύο

هذا ليس رمزا فقط. هذا نمط داخل دورة الضرب الثنائي modulo-9.
इदं केवलं प्रतीकं न. इदं modulo-9 द्विगुण-गुणन-चक्रात् रूपम्
οὐ σύμβολον μόνον. αὕτη μορφὴ ἐντὸς διπλασιασμῷ modulo-9
Dit is geen symbool alleen. Dit is een patroon binnen de modulo-9-verdubbelingscyclus.

> **Lensoptiek 3:** De modulo-9-verdubbelingscyclus is wiskundig reproduceerbaar. De NPR-duiding ervan is de lensoptiek van dit boek.
> **العدسة 3:** الدورة الحسابية قابلة للتكرار رياضياً. التفسير NPR هو عدسة هذا الكتاب.
> **दृष्टि 3:** Modulo-9-द्विगुण-चक्रम् गणितीयतः पुनरुत्पाद्यम्। NPR-व्याख्या एतस्य पुस्तकस्य लेन्सः।

---

