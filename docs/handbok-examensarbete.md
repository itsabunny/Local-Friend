# Examensarbete - Handbok för Programmeringsstuderande

## Innehållsförteckning

1. Introduktion
2. Kursmål och betygskriterier
3. Att välja projekt eller forskningsområde
4. Planering av ditt arbete
5. Genomförande och dokumentation
6. Checklista för rapporten
7. Formella krav
8. Stöd och hjälp under arbetets gång
9. Inlämning och redovisning

---

## 1. Introduktion

Denna handbok ger dig konkret vägledning för att genomföra ditt examensarbete inom programmering. Som programmerare har du unika möjligheter att kombinera teoretisk kunskap med praktisk implementation.

**Handboken hjälper dig att:**

- Välja mellan utvecklingsprojekt, forskningsstudier eller kombinationer
- Planera ditt arbete metodiskt
- Dokumentera både process och resultat professionellt
- Förstå de tekniska och akademiska kraven
- Förbereda en övertygande redovisning

**Typer av examensarbeten inom programmering:**

- **Utvecklingsprojekt:** Bygga applikationer, system eller verktyg
- **Forskningsstudier:** Undersöka teknologier, prestanda eller metoder
- **Hybridprojekt:** Kombinera utveckling med systematisk utvärdering

---

## 2. Kursmål och betygskriterier

Kursmål och betygskriterier är nedskrivna i kursplanen för kursen. Ladda ned kursplanen på Omniway.

---

## 3. Att välja projekt eller forskningsområde

### Val av ämne, område och omfattning

- Välj ett tydligt och fokuserat ämne i form av en frågeformulering
- Begränsa frågan till något specifikt
  - Nivå 1: "Hur snabbt är Python?"
  - Nivå 2: "Hur snabbt är Python för maskininlärning?"
  - Nivå 3: "Prestandajämförelse mellan Pythons NumPy och native C++ applikation för matrix-operationer"
- Tänk på tillgängliga resurser och tid
  - Skriv ned och mappa upp resurser
  - Planera för potentiella hinder
  - Utnyttja 'Inversion'-tankemodellen

**Inspiration och idéer:**

1. Prestandaanalys
   - Frågeställning: "Hur påverkar olika implementationer av dependency injection prestandan i ASP.NET?"
   - Problem att undersöka: minnesanvändning, uppstartstid, svarstider, garbage collection
2. Säkerhetsanalys
   - Frågeställning: "Vilka säkerhetsrisker introduceras vid användning av microservices jämfört med monolitisk arkitektur?"
   - Problem: Identifiera sårbarheter, analysera attack-möjligheter
3. Utvecklingsprocesser
   - Frågeställning: "Hur påverkar införandet av CI/CD-pipeline kodkvaliteten i större utvecklingsteam?"
   - Problem: Att mäta kodkvalitet, teameffektivitet, versionshanteringverktyg som GitHub och GitLab
4. Teknisk jämförelse
   - Frågeställning: "Vilka för- och nackdelar finns med GraphQL vs REST för moderna webbapplikationer?"
   - Problem: Analysera bandbreddsanvändning, utvecklingstid, underhållbarhet, dokumentation
5. Optimering
   - Frågeställning: "Hur kan man optimera state-management i React applikationer?"
   - Problem: Minnesanvändning, latency spikes, resursutnyttjande, sync vs async

### 3.1 Hitta din frågeställning

**För utvecklingsprojekt, fråga dig:**

- Vilka problem har jag eller andra stött på som skulle kunna lösas med kod?
- Finns det befintliga verktyg som är otillfredsställande eller kan förbättras?
- Vilken typ av applikation skulle jag vilja lära mig att bygga?

**För forskningsprojekt, fråga dig:**

- Vilka teknologier är jag nyfiken på att utforska djupare?
- Finns det prestanda-, säkerhets- eller användbarhetsaspekter jag vill undersöka?
- Vilka val mellan teknologier eller metoder känns oklara?

### 3.2 Inspirationskällor för programmerare

**Tekniska källor:**

- [GitHub Trending](https://github.com/trending) - populära projekt och teknologier
- [Stack Overflow Developer Survey](https://survey.stackoverflow.co/) - trender inom utveckling
- [Developer.mozilla.org](https://developer.mozilla.org/) - webbteknik och standards
- [Smashing Magazine](https://www.smashingmagazine.com/) - frontend och UX
- [Martin Fowler's Blog](https://martinfowler.com/) - mjukvaruarkitektur
- Tech-poddar och YouTube-kanaler inom ditt intresseområde

**Branschspecifika källor:**

- [Computer Sweden](https://computersweden.se/) - svensk IT-bransch
- [Breakit](https://breakit.se/) - startup och tech-företag

**Akademiska källor:**

- [IEEE Xplore](https://ieeexplore.ieee.org/) - teknisk forskning
- [ACM Digital Library](https://dl.acm.org/) - datavetenskap
- [arXiv.org](https://arxiv.org/list/cs.SE/recent) - mjukvaruteknik

### 3.3 Validera din idé

**Kontrollera att ditt ämne är:**

- **Genomförbart:** Kan du realistiskt slutföra det på given tid?
- **Relevant:** Är det kopplat till din utbildning och framtida yrkesroll?
- **Avgränsat:** Är omfattningen rimlig för ett examensarbete?
- **Intressant:** Kommer du att orka arbeta med det i flera veckor?

---

## 4. Planering av ditt arbete

### 4.1 Utvecklingsprojekt - Metodval

**Agile/Scrum-inspirerad approach:**

- Dela upp funktionalitet i "sprints" (1-2 veckor)
- Prioritera core-funktionalitet först (MVP)
- Planera för iterationer och förbättringar

**Teknisk planering:**

- Välj tech stack tidigt (frontend, backend, databas)
- Sätt upp utvecklingsmiljö och verktyg först
- Planera för testning från början
- Överväg deployment-strategi

### 4.2 Forskningsprojekt - Metodval

**Litteraturstudier:**

- Använd Google Scholar, IEEE Xplore, ACM Digital Library
- Sök på engelska tekniska termer
- Fokusera på peer-reviewed källor
- Spara och organisera källor från början

**Experimentella studier:**

- Definiera vad du ska mäta (prestanda, minneskonsumption, etc.)
- Välj mätverktyg och metoder
- Planera för reproducerbara experiment
- Överväg statistisk signifikans

**Jämförande studier:**

- Välj teknologier/ramverk att jämföra
- Definiera tydliga jämförelsekriterier
- Utveckla enhetliga testmiljöer
- Dokumentera skillnader i implementation

### 4.3 Riskhantering för programmerare

**Vanliga risker och åtgärder:**

| Risk                                | Förebyggande åtgärd                 |
| ----------------------------------- | ----------------------------------- |
| API:er slutar fungera               | Identifiera backup-alternativ       |
| Teknisk komplexitet högre än väntat | Ha enklare fallback-lösning         |
| Integrationsproblem                 | Testa integrationer tidigt          |
| Prestanda inte tillräcklig          | Definiera minimikrav från start     |
| Tidsbrist                           | Prioritera kärnfunktionalitet (MVP) |

---

## 5. Genomförande och dokumentation

### 5.1 Utvecklingsprojekt - Best practices

**Kodorganisation:**

- Använd versionskontroll (Git) från dag 1
- Skriv tydliga commit-meddelanden
- Dokumentera komplexa delar i koden
- Följ etablerade kodstandarder

**Dokumentation under utveckling:**

- Dagbok över viktiga beslut och problem
- Skärmdumpar av olika utvecklingsstadier
- Anteckningar om prestandaproblem och lösningar
- Lista över använda resurser och tutorials

**Testing:**

- Skriv åtminstone grundläggande enhetstester
- Testa i olika miljöer/webbläsare
- Dokumentera kända buggar och begränsningar
- Övervag basic säkerhetsaspekter

### 5.2 Forskningsprojekt - Best practices

**Datainsamling:**

- Använd strukturerade dokument (spreadsheets) för data
- Spara rådata separat från analyser
- Dokumentera metodologi för varje mätning
- Säkerhetskopiera data regelbundet

**Litteraturhantering:**

- Använd referensverktyg (Zotero, Mendeley)
- Anteckna reflektion om varje källa
- Kategorisera källor efter tema
- Sammanfatta nyckelfynd löpande

### 5.3 Skrivprocess

**Börja skriva tidigt:**

- Använd den medföljande rapportmallen
- Skriv metodkapitlet medan du gör arbetet
- Dokumentera resultat omedelbart
- Spara analyser och reflektion till sist

**Teknisk skrivning:**

- Förklara tekniska begrepp för läsare som inte är experter
- Använd konkreta exempel och kodutdrag
- Inkludera relevanta diagram och skärmdumpar
- Referera till dokumentation och standards

**Språk och grammatik:**

1. Var effektiv och undvik non-words som: så, nå, väl
   - Ord skall ha betydelse och vara effektiva
   - Förkorta meningar om det går, men dölj inte viktiga detaljer
   - Oeffektivt: Nå, han är väl inte så snabb?
   - Effektivt: Är han långsam?
2. Undvik subjektiva ord och ord med variation i definition
   - Exempel: liten, stor, vanlig, ganska, relativt, mycket, små, väl, dåligt, bra
3. Undvik att påverka läsarens uppfattning, speciellt vid resultat och slutsatser
   - Påverkar uppfattning: "Prestandan ökade jätte mycket"
   - Fakta: "Prestandan ökade med 10%"
4. Föredra nummer, antal och procent före ord och meningar

**Vanliga misstag:**

- För personligt och subjektivt
- Otydlig avgränsning
- Bristfällig metodbeskrivning
- Otillräcklig källhänvisning

**SOLO taxonomy:**

Structure of Observed Learning Outcomes (SOLO) är ett sätt att utvärdera och strukturera akademiskt arbete. Det kan användas för att strukturera rapporter.

1. Pre-structural
   - Ingen förståelse
   - Missar poängen
   - Irrelevant information

2. Uni-structural
   - En relevant aspekt
   - Grundläggande terminologi
   - Identifierar enkla koncept

3. Multi-structural
   - Flera relevanta aspekter
   - Beskriver, listar upp och kombinerar

4. Relational
   - Kopplar samman flera aspekter
   - Förklarar orsak och verkan
   - Jämför och analyserar
   - Applicerar teori
   - Exempel: `I Java samverkar trådar och synkronisering för att hantera concurrency i program. När flera trådar delar på en resurs, som en ArrayList, kan synchronized-nyckelordet användas för att låsa objektet. Detta förhindrar att andra trådar ändrar på datan samtidigt och skapar race conditions. Men överdriven användning av synchronized kan leda till deadlocks och försämrad prestanda eftersom trådarna måste vänta på varandra. Därför måste man balansera säkerhet och effektivitet.`

5. Extended Abstract
   - Generaliserar
   - Teoretiserar och bildar nya idéer
   - Reflekterar
   - Exempel: `Concurrency i Java illustrerar en fundamental utmaning inom mjukvaruutveckling: balansen mellan säkerhet och prestanda. Trådhantering och synkronisering är bara ett exempel på detta mönster. Vi ser samma avvägning i andra aspekter av systemdesign, som valet mellan 'strong' och 'svaga' referenser för minneshantering, eller mellan 'eager' och 'lazy' loading. För att hantera dessa kompromisser kan vi tillämpa designprinciper som 'separation of concerns' genom att isolera problem till specifika komponenter. Vi kan också abstrahera logiken till högre nivåer genom att använda concurrent collections eller async programmering.`

---

## 6. Checklista för programmeringsrapporter

### Allmän struktur

- [ ] Alla avsnitt från mallen är inkluderade
- [ ] Röd tråd från problem till slutsats
- [ ] Tekniska termer förklarade
- [ ] Figurer och kod-exempel kommenterade

### Tekniskt innehåll

- [ ] Arkitektur/design beskrivet med diagram
- [ ] Tekniska val motiverade och jämförda
- [ ] Kod-exempel relevanta och förklarade
- [ ] Testresultat dokumenterade
- [ ] Säkerhet och prestanda diskuterade

### För utvecklingsprojekt

- [ ] Installation/setup-instruktioner
- [ ] Funktionalitet demonstrerad med skärmdumpar
- [ ] Källkod tillgänglig (GitHub/bilaga)
- [ ] API-dokumentation (om relevant)

### För forskningsprojekt

- [ ] Sökstrategi och urvalskriterier beskrivna
- [ ] Experimentuppställning reproducerbar
- [ ] Resultat presenterade objektivt
- [ ] Begränsningar i metoden diskuterade

### Källhantering

- [ ] Alla tekniska påståenden refererade
- [ ] Senaste versioner av dokumentation använda
- [ ] Mix av akademiska och tekniska källor
- [ ] Korrekta URL:er och åtkomstdatum

---

## 7. Formella krav

### Struktur och innehåll

_[Använd den reviderade rapportmallen som beskrivits tidigare]_

### Språk och stil

- **Teknisk precision:** Använd korrekta tekniska termer konsekvent
- **Balanserad ton:** Akademisk men inte onödigt komplex
- **Längd:** 2500-8000 ord (flexibelt beroende på projekttyp)
- **Kodsegment:** Använd markdown formatering, kommentera väl

### Tekniska bilagor

**För utvecklingsprojekt:**

- Källkod (viktiga delar eller länk till repository)
- Installation/deployment-guide
- API-dokumentation
- Testprotokoll

**För forskningsprojekt:**

- Rådata från experiment
- Detaljerade mätresultat
- Sökstrategi och källförteckning
- Analysverktyg och scripts

---

## 8. Stöd och hjälp

### Uppstart och planering

- Diskutera idéer med kursansvarig innan du bestämmer dig
- Få feedback på projektplan innan du börjar
- Delta i gruppsdiskussioner om ämnesval

### Teknisk hjälp

**Utvecklingsproblem:**

- Stack Overflow och GitHub Issues
- Officiell dokumentation
- Discord/Slack-communities inom ditt område
- Handledaren för övergripande vägledning

**Forskningshjälp:**

- Bibliotekarier för litteratursökning
- Statistikstöd för dataanalys
- Handledaren för metodvägledning

### Löpande handledning

- Boka tid tidigt och regelbundet
- Kom förberedd med konkreta frågor
- Dela kod/text i förväg för feedback
- Dokumentera råd och uppföljning

---

## 9. Inlämning och redovisning

### Inlämning

- **Format:** .md (markdown fil) via Omniway
- **Deadline:** Se kursschema - inga undantag
- **Kompletteringsmaterial:** Länka till GitHub eller bifoga kod

### Redovisning (10 - 20 minuter)

Redovisningen måste göras med slides (valfritt program).

**Presentation-struktur:**

_Detta är ett förslag, du får ändra strukturen så länge innehållet finns med._

1. **Problem och syfte**
   - Vad ville du lösa/undersöka?
   - Varför är det viktigt?

2. **Teknisk approach**
   - Vilka teknologier/metoder använde du?
   - Visa arkitektur/design
   - Förklara viktiga designbeslut

3. **Resultat och demo**
   - **Utvecklingsprojekt:** Live-demo av funktionalitet
   - **Forskningsprojekt:** Viktigaste fynd och data
   - **Hybridprojekt:** Kombination av demo och resultat

4. **Reflektion och lärdomar**
   - Vad fungerade bra/mindre bra?
   - Vad skulle du gjort annorlunda?
   - Vad rekommenderar du till andra?

5. **Diskussion:** (om aktuellt)
   - Ta upp intressanta och/eller viktiga frågor

6. **Frågor från lärare och publiken** (räknas inte med i tidsgränsen)
   - Svara på eventuella frågor från lärare och publik

### Presentation-tips för programmerare

- **Ha backup:** Live-demos kan gå fel - ha skärmdumpar/video
- **Förklara koden:** Visa kod men fokusera på logik, inte syntax
- **Kvantifiera resultat:** Konkreta siffror är övertygande
- **Var ärlig:** Erkänn begränsningar och problem

### Bedömning

Handledaren utvärderar baserat på:

- Teknisk komplexitet och kvalitet
- Problemlösningsförmåga
- Dokumentation och rapportskrivning
- Muntlig presentation
- Självreflektion och kritiskt tänkande

---

**Lycka till med ditt examensarbete!**

_Vid frågor, kontakta din handledare eller kursansvarig._
