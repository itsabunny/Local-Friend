# Projektplan för Examensarbete

**Ditt namn:** Ninis Blomerus\
**Din handledare:** William Enander

## 1. Projektöversikt
### 1.1 Projekttitel
Min lokala vän

### 1.2 Projekttyp
- [x] Utvecklingsprojekt (bygga en applikation/system)\
- [ ] Forskningsprojekt (undersöka och analysera ett ämne)\
- [ ] Hybridprojekt (kombinerar utveckling med forskning)

### 1.3 Sammanfattning
Projektet syftar till att utveckla en lokal AI-baserad assistent i form av ett digitalt husdjur som kontinuerligt analyserar användarens skärmaktivitet och genererar korta, kontextuella kommentarer. Till skillnad från många moderna AI-assistenter sker all bearbetning lokalt på användarens dator med hjälp av en vision language model (VLM), vilket innebär att ingen data skickas till externa servrar.

Systemet använder regelbundna skärmdumpar som analyseras i realtid, där endast tillfälliga bilddata används i minnet och ingen rådata lagras permanent. Fokus ligger på att kombinera funktionalitet och personlighet med strikt integritet. 

Assistenten ska även kunna växla till ett interaktivt läge där användaren via klick på avataren kan ställa en fråga i ett textfält, varpå systemet tar en ny skärmdump och skickar både frågan och bilden till den lokala AI-modellen.

Projektet genomförs iterativt, med en initial prototyp (MVP) som validerar den tekniska genomförbarheten. Därefter byggs systemet om från grunden med fokus på ren arkitektur, versionshantering och vidareutveckling mot en mer avancerad assistent med minnesfunktioner baserade på textuell data.

Projektet är relevant då det undersöker hur AI-assistenter kan utvecklas på ett sätt som bevarar användarens integritet, samtidigt som de erbjuder både proaktivt stöd genom kommentarer och reaktiv hjälp genom ett interaktivt frågeläge.

## 2. Bakgrund och Problemformulering
### 2.1 Bakgrund
AI-assistenter har blivit allt vanligare i form av exempelvis ChatGPT, GitHub Copilot och olika röstassistenter. De flesta av dessa system är beroende av molnbaserade lösningar där användardata skickas till externa servrar för bearbetning. Detta innebär potentiella integritetsrisker, särskilt när känslig information kan förekomma i användarens arbetsflöde.

Ett aktuellt exempel är funktioner som Microsofts “Recall” i Windows 11, där kontinuerliga skärmdumpar används för att möjliggöra historik och återblickar. Denna typ av funktionalitet har väckt diskussion kring säkerhet och integritet, då insamling och lagring av visuella data från användarens skärm kan innebära risk för dataläckage eller obehörig åtkomst.

Samtidigt har utvecklingen av lokala AI-modeller för språkgenerering (LLM:er), såsom Gemma, gjort det möjligt att köra avancerad AI direkt på användarens dator utan behov av externa tjänster. Detta skapar möjligheter att utveckla system som både är intelligenta och integritetsbevarande.

Detta projekt utgår från behovet av en AI-assistent som kan analysera användarens aktivitet utan att kompromissa med integriteten. Genom att endast bearbeta data lokalt och undvika lagring av rådata, såsom skärmdumpar, kan systemet minimera risken för att känslig information exponeras.

### 2.2 Problemformulering
Hur kan en lokal AI-assistent utformas för att analysera och kommentera användarens skärmaktivitet på ett användbart sätt, samtidigt som strikt integritet upprätthålls genom att ingen känslig data lagras eller lämnar användarens dator, och hur påverkas funktionalitet, användbarhet och prestanda när systemet utvecklas stegvis från ett enkelt 'digitalt husdjur' till en mer avancerad assistent?

### 2.3 Syfte och Mål

**Syfte:** Syftet med projektet är att utforska och utveckla en mjukvaruarkitektur för en lokal AI-assistent som prioriterar användarens integritet framför allt annat. Genom att bygga applikationen stegvis vill jag undersöka hur mycket nytta och personlighet (i form av ett digitalt husdjur) en AI kan bidra med utan att någon data lämnar datorn eller lagras permanent i form av rådata. Projektet syftar till att visa på ett säkert alternativ till molnbaserade och integritetskränkande skärmanalysverktyg.

**Specifika mål:**

- Mål 1 (MVP - Husdjuret): Utveckla en funktionell Python-applikation med en grafisk avatar som kan ta skärmdumpar till internminnet (RAM), analysera dem via en lokal AI-modell (t.ex. Gemma 4 via Ollama). Systemet ska både kunna leverera proaktiva kontextuella kommentarer och erbjuda ett interaktivt hjälpläge där användaren kan ställa frågor baserat på nuvarande skärminnehåll, allt utan att rådata lagras permanent på disk.
- Mål 2 (Säker Datalagring): Implementera en lokal databaslösning (t.ex. PostgreSQL eller SQLite) där systemet endast lagrar metadata och textbaserade tolkningar av vad som hänt, för att kunna erbjuda historik utan att lagra faktiska bilder.
- Mål 3 (Assistent-funktionalitet): Utveckla funktioner där assistenten kan använda den lagrade text-historiken för att hjälpa användaren att minnas aktiviteter eller föra en enkel "dagbok", allt under användarens totala kontroll.
- Mål 4 (Prestandautvärdering): Dokumentera och utvärdera systemets resursanvändning (CPU/GPU/RAM) vid kontinuerlig lokal analys för att hitta en optimal balans mellan responsivitet och funktionalitet.

### 2.4 Avgränsningar

För att hålla projektet inom en rimlig omfattning och säkerställa att fokus ligger på kärnproblematiken (integritet och lokal AI-analys), har följande avgränsningar gjorts:
- Ingen molninteraktion: Applikationen ska vara helt funktionell offline. Inga externa API-anrop (som t.ex. OpenAI eller Google Cloud) tillåts, för att garantera 100 % integritet.
- Begränsad interaktion: Projektet fokuserar på textbaserad output från assistenten via ett grafiskt gränssnitt. Röststyrning, taligenkänning (Speech-to-Text) och syntetiskt tal (Text-to-Speech) inkluderas inte i grundomfattningen.
- Enkel grafik: Avataren (husdjuret) kommer att vara en enkel grafisk representation eller en statisk/enkel animerad bild. Fokus ligger på den bakomliggande logiken och AI-analysen, inte på avancerad spelgrafik eller 3D-animering.
- Operativsystem: Applikationen utvecklas primärt för Linux (Debian/X11), Windows och macOS via mss. Wayland-baserade miljöer stöds inte i nuläget då de begränsar extern skärmdumpsåtkomst av säkerhetsskäl.
- Ingen aktiv systemstyrning: Assistenten kommer inte att kunna styra mus, tangentbord eller utföra systemhandlingar. Detta avgränsas på grund av projektets tidsram samt för att bibehålla en strikt säkerhetsprofil, då aktiv styrning kräver komplexa felsäkringsmekanismer som ligger utanför detta arbetes fokus.

## 3. Teknisk Specifikation (för utvecklingsprojekt)

### 3.1 Teknisk Stack

- **Frontend (GUI):** PyQt6 (Python) – används för att skapa ett transparent overlay-fönster med avatar och text
- **Backend:** Python 3.11+
- **AI-modell:** Ollama (lokal server) med vision language models (t.ex. Qwen3.5 2B)
- **Bildhantering:** Pillow (PIL) för konvertering och nedskalning av bilder
- **Skärmdump:** Övergång till biblioteket mss för att möjliggöra plattformsoberoende hantering (Linux/Windows/macOS) direkt i RAM, med spectacle som tillfällig lösning under utvecklingsfasen på Linux.
- **Asynkronitet:** QThread (PyQt6) för att separera UI och AI-bearbetning
- **Databas (planerad):** SQLite eller PostgreSQL för lagring av textbaserad historik
- **Versionshantering:** Git med Conventional Commits
- **Paketering:** PyInstaller (för att skapa körbar applikation)

### 3.2 Funktionella Krav

- Systemet ska kunna ta skärmdumpar med jämna intervall
- Systemet ska analysera bilder med en lokal AI-modell (VLM)
- Systemet ska generera korta, kontextuella kommentarer baserat på skärminnehållet
- Systemet ska visa kommentarer i ett grafiskt overlay-fönster
- Overlay-fönstret ska vara transparent, alltid överst och dragbart
- Systemet ska vid klick på avataren pausa den automatiska cykeln och öppna ett interaktivt hjälpläge med ett textfält.
- Hjälpläget ska tillåta användaren att ställa en specifik fråga som skickas till den lokala AI-modellen tillsammans med en ny skärmdump.
- Systemet ska automatiskt återgå till det passiva, periodiska analysläget efter att ett svar har levererats i hjälpläget.
- Systemet ska kunna använda olika "personas" för variation i kommentarer
- Systemet ska inte lagra några skärmdumpar permanent
- Systemet ska i framtida versioner kunna lagra textbaserade tolkningar i en lokal databas

### 3.3 Icke-funktionella Krav

- **Prestanda:** Systemet ska ge respons inom cirka 5–8 sekunder vid användning av en mindre lokal modell (ca 2B parametrar)
- **Säkerhet/Integritet:** Ingen data får lämna användarens dator. Skärmdumpar ska bearbetas direkt i internminnet (RAM) och raderas omedelbart efter avslutad analys. Ingen bilddata ska lagras permanent på disk.
- **Användbarhet:** Applikationen ska vara icke-intrusiv och kunna köras i bakgrunden utan att störa användaren
- **Tillförlitlighet:** Systemet ska inte krascha vid misslyckad bildanalys eller modellfel
- **Portabilitet:** Systemet ska initialt fungera på Linux (Debian), med mål att bli plattformsoberoende
- **Användbarhet:** Övergången mellan automatiskt läge och hjälpläge ska vara sömlös, och det ska vara tydligt för användaren att systemet väntar på input.
- **Tillförlitlighet:** Systemet ska kunna hantera att användaren klickar på dess UI upprepade gånger, skickar tom fråga eller avbryter utan att krascha

## 4. Metod och Genomförande

### 4.1 Utvecklingsmetod

Projektet använder en iterativ och agil utvecklingsmetod. En initial prototyp har redan utvecklats för att undersöka tekniska utmaningar, såsom kommunikation med lokala AI-modeller och hantering av skärmdumpar.

Den slutliga implementationen kommer dock att utvecklas från grunden (greenfield) för att säkerställa en genomtänkt arkitektur, hög kodkvalitet och en tydlig versionshistorik. Arbetet delas upp i mindre iterationer där funktionalitet byggs stegvis och utvärderas kontinuerligt.

### 4.2 Arbetsprocess

_Beskriv steg-för-steg hur du planerar att genomföra projektet:_

1. Fas 1: Design av systemarkitektur och uppsättning av utvecklingsmiljö
2. Fas 2: Implementation av MVP (skärmdump → AI → kommentar i GUI)
3. Fas 3: Förbättring av integritet (eliminera disklagring, optimera dataflöde)
4. Fas 4: Implementation av minnesfunktioner (textbaserad historik)
5. Fas 5: Testning, optimering och dokumentation

### 4.3 Verktyg och Resurser

- **Utvecklingsverktyg:** VS Code, Git, GitHub
- **Testning:** Manuell testning samt enklare enhetstester
- **Projekthantering:** GitHub Issues / Projects
- **Externa resurser:** Ollama dokumentation, PyQt6 dokumentation, Pillow, samt online-resurser kring lokala AI-modeller

## 5. Tidsplan

### 5.1 Milstolpar

| Vecka | Milstolpe | Leverabler |
|------|----------|-----------|
| 1 | Projektstart och ny arkitektur (greenfield) | Projektsetup (Git, struktur), grundläggande PyQt6-overlay, fungerande skärmdump i RAM, enkel koppling till Ollama |
| 2 | MVP – Digitalt husdjur | Komplett flöde: skärmdump → AI-analys → kommentar i GUI, asynkronitet (QThread), persona-system, ingen permanent lagring av bilder, klick på avatar för hjälpläge med textfält och fråga + skärmdump till AI |
| 3 | Integritet och utökad funktionalitet | Eliminering av temporära filer, plattformsoberoende capture (mss), förbättrad prestanda, eventuell start på textbaserad historik |
| 4 | Testning, optimering och färdigställande | Prestandamätningar, stabilitetstestning, bugfixar, paketering (PyInstaller), färdig rapport och förberedelse av presentation |

Planeringen är flexibel och kan justeras beroende på tekniska utmaningar, där fokus alltid ligger på att säkerställa en fungerande MVP tidigt i processen.


### 5.2 Tidsallokering

- **Timmar per vecka:** ca 40–45 timmar
- **Total beräknad arbetstid:** ca 160–180 timmar

## 6. Riskanalys

| Risk | Sannolikhet | Påverkan | Åtgärd |
|------|-------------|----------|--------|
| AI-modellen är för långsam | Medel | Hög | Använd mindre modeller och nedskalade bilder |
| Problem med skärmdump på olika system | Hög | Medel | Byta till plattformsoberoende bibliotek (mss) |
| Integritetsproblem (t.ex. data sparas felaktigt) | Låg | Kritisk | Säkerställa RAM-baserad hantering och granska implementation |
| Tidsbrist | Medel | Medel | Prioritera MVP och kärnfunktionalitet |

## 7. Utvärdering och Testning

### 7.1 Testplan

Testningen av systemet kommer att ske kontinuerligt under utvecklingen och fokuserar på både teknisk funktionalitet och användarupplevelse.

#### Enhetstestning
Individuella komponenter testas separat, exempelvis:
- Bildhantering (nedskalning och konvertering till korrekt format)
- Kommunikation med Ollama (att rätt svar returneras)
- Logik för att filtrera bort upprepade kommentarer

#### Integrationstestning
Systemets delar testas tillsammans för att säkerställa att hela flödet fungerar:
- Skärmdump → bildbearbetning → AI-analys → visning i GUI
- Test av asynkronitet (att UI inte fryser under AI-bearbetning)
- Test av att overlay döljs korrekt innan skärmdump
- Testa att klick på avataren pausar automatiska skärmdumpar
- Testa att textfält visas och att användaren kan skriva och skicka en fråga
- Testa att “Skicka” triggar en ny skärmdump och att både fråga + bild skickas till modellen
- Testa att systemet återgår till automatiskt läge efter svar
- Edge cases: tom fråga, väldigt lång fråga, dubbelklick, spam-klick, avbryt/stäng hjälpläge

#### Systemtestning
Applikationen körs under längre perioder för att observera:
- Stabilitet över tid
- Minnesanvändning (RAM)
- Eventuella krascher eller fel vid upprepade körningar

#### Prestandatestning
Mätning av:
- Tid från skärmdump till visad kommentar
- Skillnader mellan olika modeller (t.ex. mindre vs större VLM)
- Påverkan av bildstorlek på responstid

#### Integritetstestning
- Verifiera att ingen data skickas till externa servrar (endast localhost används)
- Säkerställa att skärmdumpar inte lagras permanent på disk
- Kontrollera eventuella temporära filer och eliminera dessa i slutversionen

#### Användartestning (informell)
En annan användare utöver mig själv testar systemet för att utvärdera:
- Om kommentarerna upplevs relevanta
- Om systemet känns störande eller hjälpsamt
- Om användargränssnittet är tydligt och lätt att använda

### 7.2 Framgångskriterier

- Systemet kan analysera skärmen och generera relevanta kommentarer lokalt
- Ingen data skickas till externa servrar
- Systemet fungerar stabilt under längre användning
- Responsen sker inom acceptabel tid (≤ 8 sekunder)
- Användaren upplever att systemet tillför någon form av nytta eller personlighet

## 8. Referenser och Källor

- Ollama Documentation: https://ollama.com
- PyQt6 Documentation: https://doc.qt.io/qtforpython-6/
- Pillow (PIL) Documentation: https://pillow.readthedocs.io/
- Microsoft Recall (Windows 11) – säkerhetsdiskussioner kring lokal skärminspelning
- Artiklar och resurser om lokala LLM/VLM-modeller ([Gemma](https://unsloth.ai/docs/models/gemma-4), [Qwen](https://qwen.ai))
