---
audit_metadata:
  article: "06-artikel-04-dimensie-4"
  source_article: "articles/hexa-book-004.md"
  verified_against_commit: "5a13c64"
  audit_commit: "pending"
  last_verified: "2026-07-24"
  operator_status_model: "3D"
  engine_evidence: []
  route_status: "gesloten"
  supersedes: "legacy-v3"
  known_exceptions: []
---

# Artikel 4 - dimensie 4 (expansie) | 22

## الفصل الرابع - ماندلبروت: 0.0.0.0 جزيرة الصفر | चतुर्थ अध्यायः - मन्देलब्रोतः | Περὶ Δʹ - Μαντελμπρότ

هناك شكل هندسي يظهر نفس النمط: مجموعة ماندلبروت.
तदृशं ज्यामितीयं रूपं दृश्यते: मन्देलब्रोत-समुदायः
εἷς γεωμετρικὸς τύπος τὸ αὐτὸ σχῆμα φαίνει: Μαντελμπρότ-σύνολον
Er is een geometrische vorm die hetzelfde patroon toont: de Mandelbrot-set.

القاعدة بسيطة: z(n+1) = z(n)2 + c
नियमः सरलम्: z(n+1) = z(n)2 + c
ὁ κανὼν ἁπλοῦς: z(n+1) = z(n)2 + c
De regel: z(n+1) = z(n)2 + c

**Formele definitie:**
```
z_0 = 0
M = { c ∈ C : (z_n)_{n≥0} blijft begrensd }
```

waar `(z_n)` de iteratie van `z_{n+1} = z_n2 + c` met startwaarde `z_0 = 0`.

```
c ∈ M   ⟺   (z_n) blijft begrensd
c ∉ M   ⟺   |z_n| → ∞
```

**NPR-projectie:**
```
ρ_Mandelbrot-lens: C → P_NPR
ρ_Mandelbrot-lens(c) = leegte    indien c ∉ M
```

waar `(c ∉ M)` de voorwaarde is dat de baan divergeert (`|z_n| → ∞`).
Punten buiten M zijn geen wiskundige leegte - het zijn waarden van `c` waarvoor de baan divergeert.
"Leegte" is een symbolische projectie binnen NPR, geen wiskundige definitie.

> **Formele status:** `operator_status(ρ_Mandelbrot-lens) = interpretatief` | `execution_status(ρ_Mandelbrot-lens) = niet_gestart` | `validatie_status(ρ_Mandelbrot-lens) = niet_gevalideerd`

كل نقطة في المستوى المركب هي قيمة لـ c.
यत्किञ्चित् बिन्दु जटिल-तलं c-संख्या भवेत्
ἕκαστη πλῆθος ἐν τῷ φανταστικῷ πεδίῳ τιμή τῷ c
Elk punt in het complexe vlak is een c-waarde.

تطبق القاعدة مرارا. هل تبقى القيمة محدودة؟ أم تهرب إلى اللانهاية؟
नियमः पुनः पुनः प्रयुज्यते. संख्या सीमया तिष्ठति वा अनन्ते भगवति
ὁ κανὼν πολλάκις ἐφάπτεται. ἡ τιμὴ πεπερασμένη μένει; ἢ εἰς τὸ ἄπειρον φεύγει;
Herhaal. Blijft het begrensd? Of vlucht het naar oneindig?

في القيمة c = 0. هنا لا شيء يهرب. هنا الاستقرار المطلق.
तत्र c = 0. इह किञ्चित् न भगवति. इह परमं स्थिरम्
ἐνταῦθα c = 0. οὐδὲν ἐνταῦθα φεύγει. οὐσία ἀκίνητος
Voor `c = 0` met `z_0 = 0` geldt: `z_n = 0` voor alle `n`. Absolute stabiliteit.

```
ρ_HEXA(0_C) = 0.0.0.0        (HEXA-representatie)
ρ_cartografisch(0_C) = (0°,0°)  (Null Island, cartografisch)
```

Binnen NPR wordt dit punt als bronpunt aangemerkt:
```
ρ_Mandelbrot-role(0_C) = bronpunt
```
Dit is een NPR-roltoewijzing, geen eigenschap van de Mandelbrot-definitie.

*(Onderscheid met: `ρ_NPR-source(0) = ongedifferentieerd bronveld` - twee verschillende projecties, verschillende contexten.)*

Dit zijn NPR-projecties, geen wiskundige Mandelbrot-afleidingen.

> **Formele status:**
> `operator_status(ρ_HEXA) = interpretatief` | `operator_status(ρ_cartografisch) = interpretatief` | `operator_status(ρ_Mandelbrot-role) = interpretatief` | `operator_status(ρ_NPR-source) = interpretatief`

هذا هو رمز 0.0.0.0 في هذه العدسة. جزيرة الصفر.
इदं ०.०.०.० इत्यस्य लेन्स-प्रतीकम्। शून्य-द्वीपः
αὐτὸ εἶναι τὸ σύμβολον 0.0.0.0 ἐν τῇ φακῇ. νῆσος μηδέν
Binnen de HEXA-lens wordt dit bronpunt gerepresenteerd als 0.0.0.0 en cartografisch als Null Island.

النقطة التي منها يبدأ كل شيء ولا يعود إليها شيء - لأنها لا تتحرك.
तस्माद् बिन्दोः सर्वं आरभ्यते, तत्र किञ्चित् न प्रतिगच्छति - किं न चरति
ἐκ τῆς πλοκάμου ταύτης πάντα ἄρχειται, οὐδὲν εἰς αὐτὴν ἐπιστρέφει - ὅτι οὐκ ἔκινετο
Het bronpunt zelf beweegt niet. De projecties vertrekken ervan en worden in de return opnieuw op dezelfde bron betrokken.

0 ≠ 1
शून्यं ≠ एकम्
μηδὲν ≠ εἷς
Lokaal: de nul verschilt van de één.

0 ≐_lens 1
शून्यं ≐_lens एकम्
μηδὲν ≐_lens εἷς
Lensaxioma: de route sluit bij dezelfde bron.

الصفر الذي يحتوي على كل الأرقام.
शून्यं सर्वाः संख्याः भवन्ति
τὸ μηδὲν ὃ πάντα τὰς ἀριθμοὺς ἔχει
De nul die alle getallen bevat. Dit is een lensaxioma, geen gevolg van de Mandelbrot-definitie.
```
ρ_NPR-source(0) = ongedifferentieerd bronveld
```

*(0_C = complex Mandelbrot-nulpunt; 0_NPR = abstracte NPR-brontoestand. Twee verschillende projecties:
`ρ_Mandelbrot-role(0_C) = bronpunt` en `ρ_NPR-source(0) = ongedifferentieerd bronveld`.)*

هذا بالضبط ما تفعله الأبجد: تحول حرفا إلى رقم. رقم إلى جذر. جذر إلى نمط. نمط إلى عدسة.
इदं यत् अबाज् कृते: अक्षरम् संख्याम्, संख्याम् मूलम्, मूलम् रूपम्, रूपम् लेन्सम्
αὐτὸ ὃ ὁ ἀρτζ ποιεῖ: γράμμα εἰς ἀριθμόν, ἀριθμὸν εἰς ρίζαν, ρίζαν εἰς σχῆμα, σχῆμα εἰς lens
Precies wat Abjad doet: letter → getal → digitale wortel → NPR-patroonpositie.

De route is:
```
x → A_value(x) → DR(A_value(x))
```
Daarna volgt interpretatie via ρ_NPR onder de gekozen lens.
De lens is de operator waaronder dit gebeurt, niet noodzakelijk het uitvoerresultaat.

النتيجة واحدة: من نقطة واحدة، يظهر العالم.
एकं परिणामम्: एकात् बिन्दोः संसारः प्रकटः
ἀποτέλεσμα ἓν: ἐκ μιᾶς πλοκάμου, ὁ κόσμος φαίνεται
Één resultaat: uit één punt verschijnt de wereld.


> **Lensoptiek 4:** Expansie vermenigvuldigt lenzen. Meer lenzen, meer perspectieven, meer ruis. Wat verdwenen lijkt, draait op een andere frequentie - dit is symbolisch, tenzij later een concrete sonificatie- of meetoperator wordt toegepast.
> **العدسة 4:** التوسع يضاعف العدسات. عدسات أكثر، منظورات أكثر، ضوضاء أكثر. ما يبدو مختفياً يعمل على تردد مختلف.
> **दृष्टि 4:** Prasaṃkhyam darśanāḥ bahu. Bahudarśanam, bahuṃ rasi. Yaḥ apātaḥ anyasmin svare pravartate.


---

