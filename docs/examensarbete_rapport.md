# Examensarbete – Min lokala vän

**Student:** Ninis Blomerus  
**Handledare:** William Enander  
**Utbildning:** Javautvecklare (YH00887) – EC Utbildning  
**Kurs:** Examensarbete, 20 YH-poäng  
**Datum:** Juni 2026

---

## Sammanfattning (Abstract)

Modern AI assistants such as ChatGPT and Microsoft Recall rely on cloud infrastructure, raising privacy concerns as sensitive screen data is transmitted to and stored on external servers. This thesis explores whether a fully local AI assistant can analyse screen activity and deliver contextual commentary without any data leaving the user's machine.

The project, named "Min lokala vän" (Local Friend), implements a desktop overlay application built with Python 3.11, PyQt6, and the Ollama framework for running vision language models (VLMs) locally. The system captures screenshots at regular intervals using the mss library, processes them entirely in RAM as base64-encoded data — never writing image files to disk — and sends them to a local VLM that generates short, personality-driven comments displayed in a speech bubble beside an animated avatar.

An iterative development methodology was employed: a rapid prototype validated technical feasibility, after which the system was rebuilt from scratch (greenfield) with a modular, signal-driven architecture separating UI, capture, AI services, and control logic.

The resulting application demonstrates that local VLMs can analyse screen content and respond within approximately 5–10 seconds on consumer hardware while maintaining strict data privacy. Key architectural decisions — RAM-only image handling, overlay self-hiding before capture, and a controller-mediated signal pipeline — proved effective in balancing privacy, usability, and performance. The project contributes a concrete reference implementation illustrating that privacy-first design need not preclude meaningful AI functionality.

**Keywords:** local AI, vision language model, privacy, screen analysis, desktop assistant

---

## Förkortningar och Begrepp

| Term/Förkortning | Förklaring |
|---|---|
| AI | Artificial Intelligence – Artificiell intelligens |
| API | Application Programming Interface – Gränssnitt för kommunikation mellan mjukvarusystem |
| base64 | Kodningsformat som representerar binärdata (t.ex. bilder) som ASCII-text |
| CLI | Command Line Interface – Kommandoradsgränssnitt |
| GGUF | GPT-Generated Unified Format – Filformat för kvantiserade AI-modeller |
| GUI | Graphical User Interface – Grafiskt användargränssnitt |
| Kvantisering | Teknik som reducerar AI-modellers precisionsformat (t.ex. från 32-bit till 4-bit) för att minska minnesåtgång |
| LLM | Large Language Model – Stor språkmodell, t.ex. GPT, Gemma |
| Mediator-mönster | Designmönster där en central komponent koordinerar kommunikation mellan objekt utan att de känner till varandra |
| mss | Multiple Screen Shots – Python-bibliotek för plattformsoberoende skärmdumpar |
| MVP | Minimum Viable Product – Minsta fungerande produkt |
| Ollama | Ramverk för att köra LLM/VLM-modeller lokalt via ett REST-API |
| Overlay | Transparent fönster som visas ovanpå andra program utan att störa interaktion med underliggande fönster |
| PIL/Pillow | Python Imaging Library – Bibliotek för bildbehandling i Python |
| PyQt6 | Python-bindning för Qt 6, ramverk för grafiska gränssnitt med signaldriven arkitektur |
| QThread | Trådklass i Qt som möjliggör parallell exekvering utan att frysa gränssnittet |
| RAM | Random Access Memory – Datorns arbetsminne; flyktig lagring som rensas vid avstängning |
| REST | Representational State Transfer – Arkitekturstil för webbaserade API:er |
| Signal-slot | Designmönster i Qt för löst kopplad, trådsäker kommunikation mellan objekt |
| TTS | Text-to-Speech – Omvandling av text till syntetiskt tal |
| Vision Transformer | Neural nätverksarkitektur som tillämpar transformermodellens uppmärksamhetsmekanism på bildsegment |
| VLM | Vision Language Model – Språkmodell med förmåga att analysera bilder och generera text baserat på visuellt innehåll |
| X11 | Fönsterhanteringssystem för Unix/Linux som tillåter extern skärmåtkomst |

---

## 1. Inledning

### 1.1 Bakgrund

AI-assistenter har under de senaste åren blivit en integrerad del av den digitala vardagen. Verktyg som ChatGPT, GitHub Copilot och diverse röstassistenter erbjuder kraftfull funktionalitet, men nästan samtliga bygger på molnbaserad infrastruktur där användardata skickas till externa servrar för bearbetning [1]. Detta skapar en grundläggande spänning mellan funktionalitet och integritet – en spänning som blir särskilt påtaglig när AI-system ges tillgång till visuellt skärminnehåll.

Ett tydligt exempel på denna problematik är Microsofts "Recall"-funktion, introducerad i Windows 11 under 2024. Recall tar kontinuerliga skärmdumpar av användarens aktivitet för att möjliggöra sökbar historik [2]. Funktionen möttes av omfattande kritik från säkerhetsforskare, som påpekade att lagring av detaljerade visuella avbildningar av användarens skärm utgör en betydande säkerhetsrisk. Säkerhetsforskaren Kevin Beaumont demonstrerade att den lagrade databasen kunde nås av obehöriga genom skadlig programvara, vilket i praktiken innebar att en angripare kunde rekonstruera allt användaren gjort på sin dator [3]. Den centrala sårbarheten är inte bara att data lagras, utan *hur* och *var* – persistent lagring av visuell data skapar en attack-yta som inte existerar om data aldrig lämnar arbetsminnet.

Parallellt med denna utveckling har lokala AI-modeller gjort betydande framsteg. Ramverk som Ollama [4] gör det möjligt att köra avancerade språk- och visionmodeller direkt på konsumenthårdvara, utan behov av internetuppkoppling eller molntjänster. Modeller som Qwen [5], Gemma [6] och LLaMA [7] erbjuder kapacitet som för några år sedan krävde serverparker – nu tillgänglig på en vanlig bärbar dator, tack vare tekniker som kvantisering som reducerar modellernas minneskrav utan proportionell förlust av kapacitet. Denna tekniska utveckling öppnar för en ny kategori av AI-verktyg: assistenter som kan analysera visuellt innehåll lokalt, utan att kompromissa med användarens integritet.

Det är i denna skärningspunkt – mellan behovet av intelligent skärmanalys och kravet på strikt dataintegritet – som detta examensarbete tar sin utgångspunkt.

### 1.2 Syfte

Syftet med detta examensarbete är att utforska och utveckla en mjukvaruarkitektur för en lokal AI-assistent som prioriterar användarens integritet. Genom att bygga applikationen stegvis undersöks hur mycket funktionalitet och personlighet ett system kan erbjuda utan att någon data lämnar datorn eller lagras permanent som rådata. Projektet syftar till att visa på ett fungerande alternativ till molnbaserade skärmanalysverktyg, och att dokumentera de arkitektoniska avvägningar som krävs när integritet behandlas som ett designkrav snarare än en efterkonstruktion.

### 1.3 Frågeställningar

1. **Hur kan en lokal VLM analysera och kommentera skärmaktivitet i realtid utan att data lämnar användarens dator?**
2. **Vilka arkitekturval krävs för att säkerställa att bilddata enbart hanteras i RAM och aldrig skrivs till disk?**
3. **Hur påverkas systemets responstid och resursanvändning av modellstorlek och bildupplösning vid lokal inferens?**
4. **Vilka avvägningar uppstår mellan integritet, funktionalitet och prestanda vid utveckling av lokala AI-assistenter?**

### 1.4 Avgränsningar

Projektet avgränsas enligt följande:

- **Ingen molninteraktion:** Applikationen är helt funktionell offline. Inga externa API-anrop tillåts under körning.
- **Ingen aktiv systemstyrning:** Assistenten styr inte mus, tangentbord eller utför systemhandlingar. Aktiv styrning kräver komplexa felsäkringsmekanismer som ligger utanför arbetets fokus och tidsram.
- **Enkel grafisk representation:** Avataren använder emoji-baserad grafik; avancerad 3D-animering eller spelgrafik inkluderas inte.
- **Operativsystem:** Primärt utvecklat för Linux (X11) och Windows via mss-bibliotekets plattformsoberoende kapacitet. Wayland-baserade miljöer stöds inte, då Waylands säkerhetsmodell medvetet begränsar extern skärmdumpsåtkomst – en designfilosofi som ironiskt nog delar detta projekts integritetsfokus men som förhindrar den typ av skärmåtkomst applikationen kräver.
- **Ingen persistent lagring:** Lokal lagring av textbaserad metadata (planerad i projektplanen) implementerades inte inom tidsramen och lämnas som framtida arbete.
- **Inget interaktivt frågeläge:** Funktionalitet där användaren ställer fria frågor till assistenten implementerades inte inom tidsramen.

### 1.5 Metodöversikt

Projektet använder en iterativ, agil utvecklingsmetod bestående av två huvudfaser: (1) en snabb prototyp (MVP) för att validera teknisk genomförbarhet och (2) en greenfield-ombyggnad där systemet utvecklas från grunden med fokus på ren arkitektur, modularitet och separation of concerns. Arbetet dokumenteras genom Conventional Commits-konventionen och kontinuerlig reflektion över designbeslut. Tre dokumenterade AI-assisterade konversationer användes som stöd under planering, organisation och kodgranskning.

---

## 2. Teoretisk Grund och Relaterat Arbete

### 2.1 Tekniska Koncept

#### Vision Language Models (VLM)

En Vision Language Model (VLM) är en typ av AI-modell som kombinerar bildförståelse med språkgenerering [8]. Till skillnad från rena textmodeller (LLM) kan en VLM ta emot en bild som indata och producera text som beskriver, analyserar eller kommenterar bildens innehåll. Tekniskt uppnås detta genom en tvåstegsprocess: först omvandlar en bildencoder – ofta baserad på en Vision Transformer (ViT) – bilden till en sekvens av vektorer som representerar bildens semantiska innehåll. Dessa vektorer matas sedan in i en språkmodell tillsammans med en textprompt, varpå modellen genererar ett textbaserat svar som tar hänsyn till både den visuella och textuella informationen [9].

Denna arkitektur innebär att VLM:er ärver egenskaper från båda komponenterna: bildencodern avgör hur väl modellen "ser" detaljer, medan språkmodellen avgör hur väl den kan formulera relevanta och sammanhängande svar. Modeller som Qwen 2.5 VL [5], LLaVA [9] och Moondream [10] representerar aktuella exempel på VLM:er som kan köras lokalt med relativt begränsade hårdvaruresurser.

En förutsättning för lokal körning av dessa modeller är *kvantisering* – en teknik som reducerar modellens numeriska precision (exempelvis från 32-bit flyttal till 4-bit heltal) för att minska minnesåtgången [17]. En modell med 2 miljarder parametrar kräver vid full precision (FP32) cirka 8 GB RAM, medan samma modell i 4-bitars kvantisering (Q4) ryms i ungefär 1,5–2 GB. Denna reduktion medför viss förlust av precision, men modern forskning visar att kvalitetssänkningen ofta är marginell för praktiska tillämpningar [17]. Kvantisering är således den tekniska möjliggöraren som gör lokal VLM-inferens realistisk på konsumenthårdvara.

#### Ollama och lokalt AI-inferensramverk

Ollama [4] är ett ramverk med öppen källkod som förenklar körning av LLM- och VLM-modeller lokalt. Det abstraherar bort komplexiteten i modellnedladdning, kvantisering och inferens bakom ett enkelt CLI- och API-gränssnitt. Ollama exponerar ett lokalt REST-API (standardport 11434) som applikationer kan kommunicera med via HTTP-anrop. Ramverket stöder ett brett ekosystem av modeller i GGUF-format, inklusive vision-kapabla varianter.

En central egenskap för detta projekts syfte är att hela inferensprocessen sker på användarens hårdvara – ingen data skickas till externa servrar. Ollamas Python-klientbibliotek (`ollama`) erbjuder ett programmatiskt gränssnitt som inkluderar stöd för bildinmatning via `images`-parametern i chat-anrop, vilket möjliggör direkt integration av base64-kodade bilder utan mellanlagring. Konfigurationsparametrar som `num_predict` (antal genererade tokens) och `temperature` (kreativitetsgrad) ger finkorning kontroll över modellens beteende [4].

#### Signaldriven arkitektur och mediator-mönstret i Qt

PyQt6 [11] bygger på Qts signal-slot-mekanism, ett designmönster för löst kopplad kommunikation mellan objekt. En signal emitteras av ett objekt när något händer (exempelvis att ny data finns tillgänglig), och en eller flera slots (mottagarfunktioner) exekveras som svar. Mekanismen är trådsäker i Qt: signaler som emitteras från en bakgrundstråd (QThread) levereras automatiskt till mottagarens tråd via Qts event loop, utan risk för race conditions [12]. Detta eliminerar behovet av explicit lås-hantering (mutexes) för kommunikation mellan trådar.

I kombination med mediator-mönstret – där en central komponent (controllern) koordinerar kommunikation mellan delsystem utan att dessa behöver känna till varandra – möjliggörs en arkitektur med hög kohesion och låg koppling [18]. Bakgrundsarbetare behöver inte känna till gränssnittets implementation, och gränssnittet behöver inte veta var data kommer ifrån. Denna separation av ansvar är avgörande för testbarhet och utökbarhet.

#### Skärmdumpar i RAM med mss

Biblioteket mss (Multiple Screen Shots) [13] erbjuder plattformsoberoende skärmdumpar i Python. Till skillnad från vissa alternativ – exempelvis subprocess-anrop till Spectacle på Linux, Javas `Robot`-klass, eller Pythons egna `ImageGrab` – arbetar mss direkt med operativsystemets grafik-API och returnerar pixeldata som raw bytes. Dessa kan konverteras direkt till en PIL-bild via `Image.frombytes()` utan mellanlagring på disk. Denna egenskap är avgörande för projektets integritetsmål, eftersom den eliminerar den vanligaste källan till oavsiktliga dataspår: temporära filer i filsystemet.

### 2.2 Befintlig Forskning och Lösningar

#### Molnbaserade skärmanalysverktyg

Microsoft Recall representerar den mest uppmärksammade molnbaserade lösningen för skärmanalys [2]. Systemet tar periodiska skärmdumpar, lagrar dem i en lokal databas (kopplad till Windows-kontot) och använder OCR samt AI för att göra innehållet sökbart. Kritiken har fokuserat på att den lagrade bildhistoriken utgör en säkerhetsrisk: om en angripare får åtkomst till databasen erhålls en komplett visuell logg över allt användaren gjort [3]. Problemet är inte enbart tekniskt utan även konceptuellt – persistent lagring av visuell data skapar en attackyta som skalerar med tiden.

Andra molnbaserade AI-assistenter som ChatGPT och Google Gemini erbjuder bildanalys via molnbaserade API:er, men kräver att bilddata skickas till externa servrar. Även om dessa tjänster ofta har integritetspolicyer som begränsar dataanvändning, kvarstår det faktum att användarens skärminnehåll passerar tredjepartsinfrastruktur – en modell som kan vara otillåten i reglerade miljöer (exempelvis sjukvård eller juridik).

#### Lokala alternativ

Projekt som PrivateGPT [14] och GPT4All [15] demonstrerar att det är möjligt att köra avancerade språkmodeller helt lokalt. Dessa fokuserar dock primärt på textbaserad interaktion (dokumentanalys, chattar) snarare än visuell skärmanalys. En kombination av lokal VLM med realtids-skärmdumpsfunktionalitet – det vill säga det som detta examensarbete implementerar – är ett relativt outforskat område där få öppna implementationer existerar. Denna lucka i befintliga lösningar utgör projektets forsknings- och utvecklingsbidrag.

### 2.3 Teknisk Jämförelse

Valet av teknikstack krävde flera avvägningar. Tabellen nedan sammanfattar de alternativ som övervägdes under planeringsfasen och de faktorer som avgjorde valet:

| Komponent | Övervägda alternativ | Valt | Motivering |
|---|---|---|---|
| Programspråk | Java + Spring, Python | Python 3.11+ | Överlägset ekosystem för AI/ML; Ollamas officiella Python-klient finns; snabbare prototypning [16] |
| GUI-ramverk | JavaFX, Tkinter, PyQt6 | PyQt6 | Stöd för ramlösa, transparenta fönster med `WindowStaysOnTopHint`; trådsäker signaldriven arkitektur; mogen dokumentation [11] |
| Skärmdump | Java Robot, Spectacle (subprocess), mss | mss | Plattformsoberoende; returnerar pixeldata direkt i RAM utan temporär fil; prestanda [13] |
| AI-inferens | OpenAI API, lokal GGUF + llama.cpp, Ollama | Ollama | Enklaste integrationspunkt för lokala VLM; stöd för vision-modeller; hanterar kvantisering automatiskt [4] |
| VLM-modell | Gemma 3, Llama 3.2, Qwen 2.5, Moondream | Qwen 3.5 2B | Balans mellan storlek (2B parametrar) och vision-kapacitet; snabb responstid på konsumenthårdvara |

Det initiala valet i projektplanen att använda Java med Spring Boot och React övergavs före implementationsstarten, då Python erbjuder ett avsevärt mer moget ekosystem för AI-relaterad utveckling. Denna övergång illustrerar vikten av att utvärdera teknikval kritiskt innan utvecklingsarbetet påbörjas – en insikt som sannolikt sparade betydande utvecklingstid och som bekräftar värdet av att separera planeringsfas från implementationsfas.

---

## 3. Metod och Genomförande

### 3.1 Övergripande Arbetsgång

Utvecklingen följde en iterativ process uppdelad i tydliga faser. Centralt i ansatsen var strategin att först bygga en prototyp (MVP) för att validera tekniska antaganden, och sedan genomföra en greenfield-ombyggnad där hela systemet konstruerades från grunden med fokus på modulär arkitektur och separation of concerns.

Denna tvåstegsmodell motiverades av en insikt från prototypfasen: den initiala koden hade vuxit organiskt till en enda fil utan tydlig struktur – ett vanligt mönster vid snabb prototypning. Istället för att refaktorera prototypen, som hade tjänat sitt syfte som "proof of concept", arkiverades den (som `docs/prototype-v1/`) och en ny kodbas byggdes med förutbestämd mappstruktur. Beslutet att starta om snarare än att refaktorera innebar mer arbete på kort sikt, men resulterade i en kodbas som var enklare att underhålla, testa och utöka. Denna avvägning mellan kortsiktig effektivitet och långsiktig kodkvalitet är en central lärdom från projektet.

**Fas 1 – Infrastruktur och grundläggande UI (vecka 1)**

Projektstruktur skapades med en `src/local_friend/`-layout som separerar moduler efter ansvar: `ai/`, `capture/`, `services/`, `ui/`, `workers/` och `app/`. Denna uppdelning etablerades innan någon funktionell kod skrevs – ett medvetet beslut som styrde all efterföljande utveckling. PyQt6-baserat overlay-fönster implementerades med egenskaper som transparens (`WA_TranslucentBackground`), alltid-överst (`WindowStaysOnTopHint`) och Tool-flagga (för att undvika att overlayen syns i aktivitetsfältet). Skärmdumpsfunktionalitet via mss integrerades med direkt konvertering till PIL-bild i RAM. Central konfigurationsfil (`config.py`) skapades med alla justerbara parametrar samlade på ett ställe.

**Fas 2 – AI-pipeline och end-to-end-flöde (vecka 2)**

Dedikerad `OllamaClient` implementerades som kapslar in all kommunikation med den lokala Ollama-servern. Persona-system med separata systempromptar skapades i `prompts.py`. Bildkonvertering till base64 i RAM (via `io.BytesIO()` utan temporära filer) implementerades – en medveten refaktorering bort från prototypens diskanvändning. Signalkedjan Worker → UI kopplades ihop genom `pyqtSignal`, vilket gav ett komplett end-to-end-flöde: skärmdump → bildbehandling → AI-analys → pratbubbla.

**Fas 3 – Arkitektur-refinement och stabilisering (vecka 3)**

Self-capture-prevention-mekanismen implementerades efter upptäckten att assistenten analyserade sin egen avatar i skärmdumparna (se avsnitt 4.3). `AppController` introducerades som central kopplingskomponent enligt mediator-mönstret, vilket eliminerade direkta beroenden mellan Worker, UI och tjänster. Widgets extraherades till separata klasser (`SpeechBubble`, `StatusLabel`, `AvatarWidget`) för ökad modularitet. Persona-systemet utökades till 5 avatarer med unika promptar och emoji-tillstånd.

**Fas 4 – Utökad funktionalitet och polish (vecka 4)**

Avatarval via högerklicksmeny implementerades som kontextmeny i overlayen. Offline text-to-speech (TTS) via pyttsx3 lades till – en funktionalitet som låg utanför den ursprungliga avgränsningen men som visade sig vara tekniskt okomplicerat att integrera tack vare den modulära arkitekturen: TTS-tjänsten kopplades in genom att lägga till en signal-koppling i controllern, utan ändringar i Worker eller UI. TTS-toggle integrerades i menysystemet och hanteras genom controllern via overlay-signaler.

### 3.2 Verktyg och Tekniker

| Kategori | Verktyg | Användning |
|---|---|---|
| IDE | Visual Studio Code | All kodutveckling och terminalanvändning |
| Versionshantering | Git + GitHub | Kontinuerlig versionshantering med Conventional Commits-konventionen |
| AI-inferens | Ollama (lokal) | Körning av vision-modeller via lokalt REST-API |
| Testning | pytest | Enhets- och konfigurationstester |
| Bildhantering | Pillow (PIL) | Nedskalning, formatkonvertering, base64-kodning i RAM |
| Skärmdump | mss | Plattformsoberoende skärmfångst direkt till RAM |
| GUI | PyQt6 | Overlay-fönster, widgets, signaler, kontextmenyer |
| TTS | pyttsx3 | Offline text-till-tal med trådsäker körning |
| AI-stöd | ChatGPT (3 konversationer) | Planering, repo-organisation och kodgranskning |

### 3.3 Datainsamling och Analys

Utvecklingsprocessen dokumenterades genom flera komplementära kanaler:

- **Git-historik:** 40 commits med Conventional Commits-format (t.ex. `feat:`, `fix:`, `refactor:`, `chore:`), vilket ger spårbar koppling mellan beslut och implementation. Formatet ger inte bara teknisk spårbarhet utan fungerar även som kronologisk berättelse om projektets utveckling.
- **AI-assisterade konversationer:** Tre dokumenterade konversationer användes som stöd: konversation 1 för planering och projektplan, konversation 2 för repo-organisation och dokumentstruktur, och konversation 3 för kodgranskning och vidareutveckling. Dessa konversationer utgör en del av projektets dokumentation och visar på arbetsprocessen.
- **Kontinuerlig manuell testning:** Varje ny funktionalitet testades genom att köra applikationen, verifiera visuell output och kontrollera terminalutskrifter. Avsaknaden av automatiserade integrationstester kompenserades delvis genom denna iterativa verifiering.

### 3.4 Kvalitetssäkring

Kvalitetssäkring genomfördes på flera nivåer:

- **Arkitektonisk granskning:** I konversation 3 genomgicks hela kodbasen i en extern granskning som identifierade förbättringsområden. Dessa implementerades i fas 3: controller-mönster, widget-extrahering och self-capture-prevention. Granskningen fungerade som en form av informell kodgranskning ("code review").
- **Felhantering:** `OllamaClient` fångar alla undantag via en generell `except`-block och returnerar en felsträng (`"Error: ..."`) istället för att krascha applikationen. `ScreenCaptureError` är en projektspecifik undantagsklass som kapslar capture-relaterade fel för tydligare felhantering uppåt i anropskedjan.
- **Deduplicering:** `CommentaryService` jämför varje ny kommentar med den föregående och filtrerar bort identiska svar, vilket förhindrar att samma meddelande visas flera gånger i rad vid statiskt skärminnehåll.
- **Enhetstester:** `test_config.py` verifierar att konfigurationsvariabler har korrekta typer och rimliga värden. `test_prompts.py` validerar persona-systemets struktur.
- **Metodbegränsning:** Projektet saknar omfattande integrationstester och automatiserad verifiering av integritetsgarantierna (se avsnitt 5.3 för vidare diskussion).

---

## 4. Resultat

### 4.1 Huvudresultat

#### Den färdiga applikationen

Projektet resulterade i en funktionell desktop-applikation bestående av 12 Python-källfiler i en modulär struktur. Applikationen implementerar följande kärnfunktionalitet:

1. **Automatisk skärmanalys:** Var 10:e sekund (konfigurerbart via `CAPTURE_INTERVAL_SECONDS`) tar systemet en skärmdump, analyserar den med en lokal VLM och visar en kontextuell kommentar.
2. **Integritetsskydd:** All bilddata hanteras exklusivt i RAM via base64-kodning. Ingen skärmdump skrivs till disk vid något tillfälle i pipelinen.
3. **Personlighetsystem:** 5 avatarer (Smiley, Anka, Kanin, Apa, Uggla) med unika systempromptar som ger varierande kommentarsstil – från analytiska observationer (Uggla) till lekfulla kommentarer (Anka).
4. **Visuell overlay:** Transparent, ramlöst fönster som är alltid-överst och dragbart, med emoji-animerade tillstånd (idle, thinking, capturing, talking).
5. **Röstutmatning:** Offline TTS via pyttsx3 med trådsäker körning (daemon-tråd med `threading.Lock`) som kan slås av och på via högerklicksmeny.
6. **Self-capture-prevention:** Overlayen gömmer sig automatiskt före varje skärmdump och visar sig igen efteråt, för att undvika att AI:n analyserar sin egen avatar.

#### Arkitektur

Systemets slutliga arkitektur följer ett signal-drivet mediator-mönster där `AppController` fungerar som central koordinator:

```
┌───────────────┐       signals        ┌─────────────────┐
│ AssistantWorker│ ──────────────────▶  │  AppController   │
│   (QThread)   │  status_update       │   (mediator)     │
│               │  new_commentary      │                  │
│               │  request_hide/show   │                  │
└───────────────┘                      └────────┬────────┘
        ▲                                       │
        │ overlay_hidden                        │ signals
        │                                       ▼
┌───────────────┐                      ┌─────────────────┐
│   PetOverlay  │ ◀──────────────────  │   TTSService    │
│   (PyQt6 UI)  │  update_status       │   (pyttsx3)     │
│               │  update_speech       │                  │
└───────────────┘                      └─────────────────┘
```

Diagrammet visar att Worker aldrig kommunicerar direkt med UI:t – all kommunikation medieras genom signaler som controllern kopplar ihop. Detta innebär att man kan byta ut UI-lagret utan att ändra Worker, eller lägga till nya mottagare (t.ex. en logg-tjänst) genom att koppla ytterligare en slot till befintliga signaler.

Dataflödet genom systemet vid varje capture-cykel:

1. `AssistantWorker` signalerar `request_hide` → overlay gömmer sig och bekräftar med `overlay_hidden` efter en kort fördröjning (300 ms).
2. `capture_primary_screen()` (mss) fångar primär skärm → returnerar `PIL.Image` direkt i RAM via `Image.frombytes()`.
3. `request_show` signaleras → overlay visas igen.
4. `prepare_image_for_model()` skalar ner bilden till max 896 pixlars bredd med Lanczos-interpolering och konverterar till RGB.
5. `_pil_to_base64()` konverterar bilden till base64 via `io.BytesIO()` – ingen fil på disk.
6. `OllamaClient.get_vision_commentary()` skickar base64-data + systemprompt till Ollamas lokala API med parametrarna `num_predict=35` (maximal svarslängd) och `temperature=0.75` (kreativitetsgrad).
7. Svar dedupliceras mot föregående kommentar och emitteras via `new_commentary`-signalen.
8. `AppController` vidarebefordrar till UI (pratbubbla + avatar-state) och TTS.

#### Kodexempel: Controllerns signalkoppling

Följande utdrag ur `controller.py` visar hur mediator-mönstret realiseras – controllern kopplar ihop alla signaler utan att de individuella komponenterna känner till varandra:

```python
class AppController(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.overlay = PetOverlay()
        self.worker = AssistantWorker()
        self.tts = TTSService()
        self._connect_signals()

    def _connect_signals(self) -> None:
        # Worker → UI
        self.worker.status_update.connect(self.overlay.update_status)
        self.worker.new_commentary.connect(self.overlay.update_speech)
        # Worker → TTS (via controller)
        self.worker.new_commentary.connect(self._on_new_commentary)
        # Hide/show-synkronisering för capture
        self.worker.request_hide.connect(self.overlay.hide_for_capture)
        self.worker.request_show.connect(self.overlay.show)
        self.overlay.overlay_hidden.connect(self.worker.on_overlay_hidden)
        # Avatar → persona-koppling
        self.overlay.avatar_changed.connect(
            self.worker.commentary_service.set_avatar
        )
        # TTS toggle från overlay
        self.overlay.tts_toggled.connect(self.tts.set_enabled)
```

Koden illustrerar ett centralt arkitekturbeslut: `_connect_signals()` är den enda platsen i hela applikationen där komponenterna kopplas samman. Om en ny tjänst ska läggas till (exempelvis loggning), behöver enbart denna metod utökas – ingen befintlig komponent behöver modifieras.

#### Kodexempel: RAM-baserad bildhantering

Följande utdrag visar den centrala funktionen som konverterar en PIL-bild till base64 utan att involvera filsystemet:

```python
def _pil_to_base64(image: Image.Image) -> str:
    """Konverterar PIL-bild till base64-sträng i RAM – ingen fil skrivs till disk."""
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")
```

Genom att använda `io.BytesIO()` som en in-memory buffer skapas aldrig en temporär fil. Bilddatan existerar enbart som Python-objekt i RAM under bearbetningstiden och frigörs automatiskt av Pythons garbage collector när referenserna upphör. Detta är en medveten designändring jämfört med prototypen, som skrev en temporär PNG-fil till disk – en till synes oskyldig operation som dock skapar ett recoverable dataspår i filsystemet.

#### Kodexempel: Self-capture-prevention

Mekanismen för att gömma overlayen före skärmdump illustrerar samspelet mellan QThread och Pythons `threading.Event`:

```python
# I AssistantWorker.run():
self._hidden_event.clear()
self.request_hide.emit()           # Signal till overlay (korsar trådgräns)
self._hidden_event.wait(timeout=1.0)  # Vänta på bekräftelse (blocking i worker-tråd)
image = capture_primary_screen()    # Fota utan overlay synlig
self.request_show.emit()           # Visa overlay igen
```

Utan denna mekanism inkluderas assistentens egen avatar i varje skärmdump, vilket leder till cirkulära och irrelevanta kommentarer (AI:n kommenterar sin egen emoji). Lösningen kombinerar Qts signalsystem (trådsäkert för korsning mellan QThread och huvudtråd) med Pythons `threading.Event` (för blocking-väntan i worker-tråden). Timeout på 1 sekund förhindrar att worker-tråden blockas permanent om overlayen inte svarar.

#### Kodexempel: Persona-driven AI-interaktion

Persona-systemet visar hur samma VLM-modell ger olika karaktär beroende på systemprompt:

```python
PERSONAS = {
    "Uggla": [
        "You're a wise, calm owl giving thoughtful observations.",
        "You're a clever owl who comments with quiet intelligence.",
    ],
    "Anka": [
        "You're a calm, slightly silly duck commenting on the screen.",
        "You're a friendly duck who gives laid-back, playful remarks.",
    ],
    # ... (ytterligare 3 avatarer)
}
```

Varje avatar har flera alternativa persona-texter som väljs slumpmässigt (`random.choice`), vilket ger ytterligare variation. Systemet demonstrerar att personlighet i AI-svar kan styras effektivt genom prompt-design utan modellträning eller fine-tuning.

### 4.2 Detaljerade Fynd

#### Modellval och vision-kapacitet

Under utvecklingen identifierades ett problem där AI-modellen returnerade tomma eller irrelevanta svar. Felsökningen avslöjade att orsaken var att den initialt testade modellkonfigurationen inte korrekt tolkade bilddata via Ollamas API. Insikten att skillnaden mellan en textmodell och en vision-modell inte alltid är uppenbar i Ollamas modellkatalog ledde till en systematisk verifiering: modellen måste explicit stödja `images`-parametern i chat-anropet. I den slutliga versionen används Qwen 3.5 2B med bekräftad vision-kapacitet.

Konfigurationen `think=False` i Ollama-anropet visade sig vara nödvändig för konsekvent beteende – utan denna parameter inkluderades ibland modellens interna resonemangssteg i det synliga svaret, vilket störde användarupplevelsen.

#### Inferensparametrar och deras effekt

Parametern `num_predict=35` begränsar svaret till maximalt 35 tokens, vilket tvingar modellen att formulera korta, koncisa kommentarer. Kombinerat med `temperature=0.75` (något över standardvärdet 0.7) skapas svar som varierar tillräckligt för att inte upplevas som repetitiva, men som behåller relevans för skärminnehållet. Dessa parametrar kalibrerades empiriskt under utvecklingen.

#### Conventional Commits som dokumentationsverktyg

Användningen av Conventional Commits (t.ex. `feat:`, `fix:`, `refactor:`, `chore:`) genom hela Git-historiken (40 commits) visade sig vara värdefullt inte bara för versionshantering utan även som utvecklingsdokumentation. Commit-meddelanden som `feat(ui): add avatar selection via context menu` eller `refactor(workers): implement hide-for-capture mechanism` dokumenterar inte bara *vad* som ändrades utan ger kontext om *varför*. Historiken kan verifieras direkt mot denna rapport.

### 4.3 Oväntade Resultat

**TTS som utökning utanför scope:** Text-to-speech-funktionalitet exkluderades uttryckligen i projektplanens avgränsningar ("Röststyrning, taligenkänning och syntetiskt tal inkluderas inte i grundomfattningen"). Trots detta implementerades offline-TTS (pyttsx3) i fas 4 då det visade sig vara tekniskt okomplicerat – den modulära arkitekturen möjliggjorde integration genom att lägga till en ny tjänst (`TTSService`) och en signal-koppling i controllern, utan ändringar i befintlig kod. Att en avgränsning medvetet utökades, med bibehållen kontroll och dokumentation, illustrerar den iterativa metodens flexibilitet: avgränsningar fungerar som riktlinjer, inte som orubbliga ramar, förutsatt att utökningar inte äventyrar kärnfunktionaliteten.

**Self-capture-problemet:** Att assistenten analyserade sin egen avatar i skärmdumparna var inte ett förutsett problem. Upptäckten illustrerar en utmaning som är specifik för applikationer som kombinerar visuell analys med GUI-overlay: systemet måste vara medvetet om sin egen visuella närvaro på skärmen. Lösningen (gömma overlay → fota → visa overlay) är konceptuellt enkel men kräver trådsäker synkronisering mellan UI-tråd och worker-tråd. Implementationen ledde till fördjupad förståelse för Qt:s signal-slot-mekanism i flertrådade sammanhang, och specifikt hur `threading.Event` kan kombineras med `pyqtSignal` för synkron koordinering mellan trådar.

---

## 5. Diskussion

### 5.1 Analys av Resultat

#### Uppfyllelse av syfte och frågeställningar

**Frågeställning 1 – Lokal skärmanalys utan dataläckage:** Systemet demonstrerar att det är fullt möjligt att analysera skärminnehåll med en lokal VLM utan att data lämnar datorn. Hela pipelinen – från skärmdump via mss till AI-kommentar via Ollama – exekveras lokalt, och all kommunikation sker mot `localhost:11434`. Frågeställningen besvaras positivt: en lokal VLM *kan* analysera och kommentera skärmaktivitet i realtid. Det bör dock noteras att "realtid" i detta sammanhang innebär en cykel på ungefär 5–10 sekunder, vilket är en avsevärd fördröjning jämfört med mänsklig perception men ändå tillräckligt för att kommentarer upplevs som kontextuellt relevanta.

**Frågeställning 2 – RAM-baserad bildhantering:** De arkitekturval som krävdes identifierades och implementerades konkret: `mss` returnerar pixeldata direkt i RAM, `io.BytesIO()` eliminerar behovet av temporära filer vid base64-konvertering, och Pythons garbage collector frigör bilddata automatiskt. Prototypens diskanvändning (temporär PNG-fil) eliminerades medvetet i greenfield-versionen. Frågeställningen besvaras genom den konkreta implementationen – men en komplett verifiering skulle kräva analys av eventuella swap-filer på OS-nivå och kontroll av Ollamas interna bufferthantering, vilket ligger utanför detta arbetes scope.

**Frågeställning 3 – Prestanda:** Systemet levererar kommentarer inom uppskattningsvis 5–10 sekunder vid användning av Qwen 3.5 2B på konsumenthårdvara. Bildens nedskalning till max 896 pixlar bredd bidrar till kortare inferenstid genom att reducera mängden data som bildencodern behöver bearbeta. Parametern `num_predict=35` begränsar den generativa fasen, vilket ytterligare reducerar svarstiden. En systematisk prestandamätning med exakta tider, RAM-förbrukning under inferens och jämförelse mellan modellstorlekar genomfördes dock inte, vilket utgör en begränsning (se avsnitt 5.3).

**Frågeställning 4 – Avvägningar integritet/funktionalitet/prestanda:** Projektets genomförande avslöjade en konkret trevägs-spänning som genomsyrar alla designbeslut:

- *Integritet ↔ Prestanda:* RAM-baserad bildhantering eliminerar disk-spår men innebär att bilddata måste hållas i arbetsminnet under hela bearbetningskedjan. Lokal inferens ger fullständig integritet men begränsar val av modellstorlek till vad hårdvaran klarar.
- *Integritet ↔ Funktionalitet:* Avsaknaden av persistent lagring (för att skydda integriteten) omöjliggör funktioner som historik och sökbar skärmlogg – precis de funktioner som gör Microsoft Recall användbart. Den strikta integritetsmodellen begränsar alltså vilka användarfunktioner som kan erbjudas.
- *Prestanda ↔ Funktionalitet:* Större modeller ger rikare och mer nyanserade kommentarer men kräver längre inferenstid och mer hårdvaruresurser. Valet av en 2B-parametermodell är en kompromiss: tillräcklig kapacitet för korta kommentarer, men begränsad förmåga till djupare analys.

Denna trevägs-avvägning skiljer sig fundamentalt från molnbaserade system, där prestanda och funktionalitet kan skalas genom att lägga till serverresurser – men till priset av integritet. I ett lokalt system är alla tre dimensioner bundna till samma hårdvara, vilket tvingar utvecklaren att göra medvetna prioriteringar. I detta projekt prioriterades integritet högst, prestanda näst högst, och funktionalitetsbredd lägst – ett val som resulterade i en smal men robust applikation.

#### Jämförelse med befintliga lösningar

Jämfört med Microsoft Recall erbjuder Local Friend en fundamentalt annorlunda integritetsmodell: ingen persistent lagring av bilder, ingen sökbar databas över skärmhistorik, och ingen koppling till molnkonton. Priset är begränsad funktionalitet – Recall erbjuder retroaktiv sökning i skärmhistorik, vilket Local Friend inte kan utan en databaskomponent. Denna jämförelse illustrerar att integritet och funktionalitet inte nödvändigtvis är binärt: genom att lagra enbart textmetadata (aldrig bilddata) lokalt – som föreslås under framtida arbete – kan viss historikfunktionalitet implementeras utan att kompromissa med den strikta bildintegriteten.

Jämfört med PrivateGPT och GPT4All, som fokuserar på textbaserad lokal AI, adderar Local Friend en visuell dimension genom VLM-integration och skärmdumpsfunktionalitet. Dessa projekt demonstrerar att det finns en växande användarbas och efterfrågan på lokala AI-alternativ, vilket validerar projektets relevans. Samtliga projekt delar utmaningen att lokala modeller presterar sämre än molnbaserade varianter – en begränsning som gradvis minskar i takt med att nya, effektivare modeller släpps.

### 5.2 Reflektion över Metod

#### Styrkor

**Prototyp → greenfield-strategin** visade sig effektiv på flera plan. Prototypen validerade att konceptet fungerade (skärmdump → VLM → kommentar) och avslöjade tekniska utmaningar (modellval, bildformat) som kunde adresseras systematiskt i greenfield-versionen. Att prototypen arkiverades som `docs/prototype-v1/` snarare än raderades gör det möjligt att spåra projektets evolution och demonstrera den faktiska inlärningsprocessen. Denna strategi kan generaliseras: för projekt med hög teknisk osäkerhet är en billig prototyp för validering följt av en planerad omstart ofta mer effektiv än att försöka refaktorera en organiskt vuxen kodbas.

**Conventional Commits** gav en professionell och spårbar utvecklingshistorik. Formatet tvingade fram medvetna commit-meddelanden som dokumenterar inte bara *vad* som ändrades utan *varför*, vilket ger en kronologisk berättelse om projektet som kan verifieras mot rapporten.

**Signal-driven arkitektur** med Qt:s signal-slot-mekanism visade sig vara en naturlig passform för applikationens behov. Den lösa kopplingen möjliggjorde att TTS-funktionalitet kunde läggas till i fas 4 utan ändringar i befintlig kod – en konkret bekräftelse av arkitekturens utökbarhet. Mediator-mönstret via `AppController` centraliserar alla kopplingar till en enda metod, vilket ger hög spårbarhet.

#### Svagheter och problem

**AI som utvecklingsverktyg – möjligheter och risker:** Användningen av AI-assisterade konversationer för planering och kodgranskning var effektivt men skapade en risk för okritiskt beroende. I konversation 3 uppstod en situation där AI-assistenten antog att ett problem berodde på fel modell, när orsaken var en annan – studenten behövde korrigera assistenten. Denna erfarenhet understryker en viktig insikt: AI-verktyg kräver samma kritiska granskning som alla andra informationskällor. De kan accelerera utvecklingsprocessen avsevärt, men förmågan att bedöma och ifrågasätta deras förslag är avgörande. I en bredare kontext speglar detta den generella utmaningen med AI-assisterad utveckling: ökad produktivitet måste balanseras mot risken att okritiskt acceptera felaktiga förslag.

**Begränsad testning:** Projektet innehåller grundläggande konfigurationstester men saknar omfattande enhetstester för affärslogiken och integrationstester. Att verifiera att "ingen data skrivs till disk" kräver systematisk kontroll (exempelvis övervakning av filsystemsanrop med strace eller liknande verktyg), vilket inte genomfördes formellt. Detta begränsar styrkan i integritetsgarantin.

### 5.3 Begränsningar och Kritisk Granskning

**Ofullständig prestandautvärdering:** Projektplanen specificerade prestandautvärdering som ett centralt mål. I den slutliga implementationen saknas systematiska mätningar av CPU/GPU/RAM-förbrukning och exakta responstider vid olika modellstorlekar. Detta är en tydlig avvikelse från planen och begränsar möjligheten att kvantifiera systemets kapacitet. Orsaken var en medveten prioritering: den tillgängliga tiden användes till att fördjupa arkitekturen och lägga till personlighetsrelaterade funktioner snarare än att genomföra formella benchmarks. I efterhand hade en enkel mätning (t.ex. tidsstämplar runt inferensanropet) kunnat ge värdefull kvantitativ data med minimal extra insats.

**Ej implementerade mål från projektplanen:** Av fyra specificerade mål uppnåddes Mål 1 (MVP) fullständigt, medan Mål 2 (lokal databas för textmetadata), Mål 3 (assistent-/historikfunktionalitet) och Mål 4 (prestandautvärdering) inte implementerades. Det interaktiva frågeläget, specificerat i de funktionella kraven, genomfördes inte heller. Transparens kring dessa avvikelser är viktig: den tillgängliga tiden användes till att fördjupa arkitekturen (controller-mönster, widget-extrahering) och lägga till personlighetsrelaterade funktioner (avatarer, persona-system, TTS) snarare än bredden av funktionalitet som beskrevs i planen. Arkitekturens kvalitet prioriterades framför funktionalitetsbredd – ett val som bedömdes gynna projektets långsiktiga värde men som innebar att planen inte uppfylldes i sin helhet.

**Avsaknad av formell integritetstestning:** Påståendet att "ingen data lämnar datorn" stöds av kodanalys (alla Ollama-anrop går mot localhost, bilddata hanteras via `io.BytesIO()`, ingen `open()`-anrop med skrivläge förekommer i bildpipelinen) men verifierades inte genom systematisk nätverksövervakning eller filsystemsmonitoring. En komplett verifiering borde även inkludera Ollamas interna hantering av mottagen bilddata – ramverket kan teoretiskt använda temporär disklagring som inte syns i applikationskoden.

**Plattformstestning:** Applikationen utvecklades och testades primärt på en enskild Linux-installation med X11. Trots att mss är plattformsoberoende genomfördes ingen systematisk testning på Windows eller macOS, och Wayland-miljöer stöds inte.

### 5.4 Bredare Perspektiv

Projektet adresserar en aktuell och växande samhällsfråga: avvägningen mellan AI-funktionalitet och dataintegritet. I takt med att AI-assistenter integreras djupare i arbetsflöden och operativsystem – exemplifierat av Microsoft Recall, Apple Intelligence och Google Gemini – ökar behovet av alternativ som ger användaren full kontroll över sin data.

Den tekniska utvecklingen inom lokala AI-modeller, med allt mer kapabla modeller som kan köras på konsumenthårdvara tack vare förbättrad kvantisering och optimerade inferensramverk, gör denna typ av lösning alltmer realistisk. Projektet visar att det redan idag är tekniskt genomförbart att bygga en visuell AI-assistent som är 100 % lokal, om man accepterar de begränsningar som följer av lokal inferens.

Resultaten har relevans för utvecklare och organisationer som hanterar känslig information – exempelvis inom sjukvård, juridik eller myndighetsarbete – där molnbaserade AI-verktyg kan vara otillåtna på grund av regulatoriska krav som GDPR eller branschspecifika dataskyddsbestämmelser. Arkitekturen och designmönstren som dokumenteras i detta projekt kan tjäna som utgångspunkt för sådana tillämpningar.

Avvägningen integritet–prestanda–funktionalitet som identifierades i detta projekt är inte unik för skärmanalys; den återkommer i alla lokala AI-tillämpningar, från dokumentanalys till röstassistenter. Insikten att denna avvägning kräver medvetna, dokumenterade designbeslut – snarare än att behandla integritet som en efterkonstruktion – kan generaliseras till en designprincip för integritetskänslig mjukvaruutveckling.

---

## 6. Slutsatser

### 6.1 Huvudslutsatser

Examensarbetet demonstrerar att det är tekniskt genomförbart att bygga en lokal AI-assistent som analyserar skärmaktivitet i realtid med bibehållen strikt integritet. Följande konkreta slutsatser kan dras:

1. **Lokal VLM-baserad skärmanalys fungerar:** Med Ollama och en 2B-parametermodell kan skärminnehåll analyseras och kommenteras med relevanta, kontextuella svar inom 5–10 sekunder på konsumenthårdvara. Responstiden är tillräcklig för passiv kommentering men otillräcklig för interaktiva användningsfall.

2. **RAM-exklusiv bildhantering är möjlig och praktisk:** Genom kombinationen av mss (direkta pixeldata), Pillow (in-memory bearbetning) och `io.BytesIO()` (base64-konvertering utan fil) kan hela bildpipelinen köras utan att data berör filsystemet. Denna kedja eliminerar den vanligaste källan till oavsiktliga dataspår.

3. **Arkitektoniska val har direkt koppling till integritetsmål:** Separationen av ansvar (capture, AI, UI, controller) gör det möjligt att verifiera varje steg i datapipelinen oberoende. Den signal-drivna arkitekturen med mediator-mönster säkerställer att bilddata flödar genom definierade kanaler utan sidoeffekter, och att nya komponenter kan läggas till utan att befintliga modifieras.

4. **Trevägs-avvägningen integritet–prestanda–funktionalitet är reell och kräver medvetna designbeslut:** Lokal inferens eliminerar integritetsrisken helt men innebär längre svarstider, begränsningar i modellstorlek och funktionalitetsbredd jämfört med molnalternativ. Denna avvägning kan inte lösas tekniskt – den kräver strategiska prioriteringar som bör dokumenteras och kommuniceras.

5. **Iterativ utveckling med prototyp → greenfield är en effektiv strategi vid hög teknisk osäkerhet:** Prototypen validerade tekniska antaganden medan greenfield-ombyggnaden möjliggjorde en genomtänkt arkitektur utan ackumulerad teknisk skuld. Arkivering av prototypen möjliggör spårbarhet av projektets evolution.

### 6.2 Bidrag och Betydelse

Projektet bidrar med en konkret, fungerande referensimplementation av en lokal visuell AI-assistent med dokumenterad arkitektur. Designbesluten – RAM-baserad bildhantering, signal-driven mediatorarkitektur, self-capture-prevention – adresserar utmaningar som är generella för applikationer som kombinerar visuell AI med integritetskrav, och kan återanvändas i liknande projekt.

Ur ett utbildningsperspektiv demonstrerar arbetet förmågan att självständigt genomföra ett mjukvaruprojekt från idé till fungerande produkt, inklusive kritiska tekniska val, arkitekturdesign, iterativ utveckling med versionshantering, och ärlig reflektion över avvikelser mellan plan och utfall.

### 6.3 Framtida Arbete

Följande områden identifieras som naturliga vidareutvecklingar:

- **Interaktivt frågeläge:** Implementera klick-baserad interaktion där användaren kan ställa frågor om aktuellt skärminnehåll – en funktionalitet specificerad i projektplanen som inte hann implementeras men som den befintliga arkitekturen stöder genom tillägg av en ny signal och textinmatnings-widget.
- **Lokal textdatabas:** SQLite-baserad lagring av enbart textmetadata (aldrig bilddata), vilket möjliggör historik- och dagboksfunktionalitet utan att kompromissa med bildintegriteten. Denna utökning skulle adressera delar av gapet mellan Local Friends integritetsmodell och Recalls funktionalitet.
- **Systematisk prestandautvärdering:** Mätningar av CPU/GPU/RAM-förbrukning och responstider vid olika modellstorlekar (2B, 7B, 13B) och bildupplösningar, samt jämförelse mellan VLM-modeller (Qwen, LLaVA, Moondream). Automatiserade tidsstämplar i capture-loopen skulle möjliggöra kontinuerlig datainsamling.
- **Paketering och distribution:** Distribution via PyInstaller eller liknande verktyg för att eliminera behovet av manuell Python-installation och göra applikationen tillgänglig för icke-tekniska användare.
- **Plattformstestning:** Systematisk verifiering på Windows och macOS, samt undersökning av eventuellt Wayland-stöd via alternativa capture-metoder (exempelvis PipeWire-baserade gränssnitt).
- **Förstärkt integritetstestning:** Automatiserade tester som verifierar frånvaron av diskskrivning (via filsystemsmonitoring) och nätverkstrafik (via socket-övervakning) under körning.

---

## 7. Referenser

[1] OpenAI, "ChatGPT – Optimizing Language Models for Dialogue." [Online]. Available: https://openai.com/blog/chatgpt. [Accessed: 2 Jun. 2026].

[2] Microsoft, "Retrace your steps with Recall." [Online]. Available: https://support.microsoft.com/en-us/windows/retrace-your-steps-with-recall. [Accessed: 2 Jun. 2026].

[3] K. Beaumont, "Stealing everything you've ever typed or viewed on your own Windows PC is now possible with two lines of code," DoublePulsar Blog, Jun. 2024. [Online]. Available: https://doublepulsar.com/recall-stealing-everything-youve-ever-typed-or-viewed-on-your-own-windows-pc-is-now-possible-da3e12e9465e. [Accessed: 2 Jun. 2026].

[4] Ollama, "Ollama – Get up and running with large language models locally." [Online]. Available: https://ollama.com. [Accessed: 2 Jun. 2026].

[5] Qwen Team, "Qwen2.5-VL: To See the World More Clearly." [Online]. Available: https://qwen.ai. [Accessed: 2 Jun. 2026].

[6] Google DeepMind, "Gemma: Open Models Based on Gemini Research and Technology." [Online]. Available: https://ai.google.dev/gemma. [Accessed: 2 Jun. 2026].

[7] Meta AI, "Llama: Open Foundation and Fine-Tuned Chat Models." [Online]. Available: https://llama.meta.com. [Accessed: 2 Jun. 2026].

[8] J. Li, D. Li, S. Savarese, and S. Hoi, "BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models," in Proc. ICML, 2023.

[9] H. Liu, C. Li, Q. Wu, and Y. J. Lee, "Visual Instruction Tuning," in Proc. NeurIPS, 2023.

[10] Vikhyat Korrapati, "Moondream – Tiny Vision Language Model." [Online]. Available: https://moondream.ai. [Accessed: 2 Jun. 2026].

[11] The Qt Company, "Qt for Python Documentation." [Online]. Available: https://doc.qt.io/qtforpython-6/. [Accessed: 2 Jun. 2026].

[12] The Qt Company, "Signals & Slots." [Online]. Available: https://doc.qt.io/qt-6/signalsandslots.html. [Accessed: 2 Jun. 2026].

[13] mss contributors, "python-mss: An ultra fast cross-platform multiple screenshots module." [Online]. Available: https://python-mss.readthedocs.io/. [Accessed: 2 Jun. 2026].

[14] Zylon, "PrivateGPT – Interact with your documents using the power of GPT, 100% privately." [Online]. Available: https://privategpt.dev. [Accessed: 2 Jun. 2026].

[15] Nomic AI, "GPT4All – Run Large Language Models Locally." [Online]. Available: https://gpt4all.io. [Accessed: 2 Jun. 2026].

[16] Python Software Foundation, "Python Documentation." [Online]. Available: https://docs.python.org/3/. [Accessed: 2 Jun. 2026].

[17] T. Dettmers, M. Lewis, Y. Belkada, and L. Zettlemoyer, "GPT3.int8(): 8-bit Matrix Multiplication for Transformers at Scale," in Proc. NeurIPS, 2022.

[18] E. Gamma, R. Helm, R. Johnson, and J. Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*. Reading, MA: Addison-Wesley, 1994.

---

## Bilagor

### Bilaga A: Källkod och Repository

Fullständig källkod finns tillgänglig på GitHub:  
**https://github.com/itsabunny/Local-Friend**

Projektstruktur:

```
Local-Friend/
├── src/local_friend/
│   ├── main.py                      # Entry point: startar QApplication + AppController
│   ├── config.py                    # Central konfiguration (modell, intervall, marginaler)
│   ├── app/
│   │   └── controller.py            # AppController (mediator – kopplar signaler)
│   ├── ui/
│   │   ├── overlay.py               # PetOverlay (ramlöst, translucent, dragbart fönster)
│   │   └── widgets.py               # SpeechBubble, StatusLabel, AvatarWidget + AVATARS-map
│   ├── workers/
│   │   └── assistant_worker.py      # QThread: capture-loop med hide/show-synkronisering
│   ├── capture/
│   │   └── screen_capture.py        # mss-baserad skärmdump → PIL.Image i RAM
│   ├── services/
│   │   ├── commentary_service.py    # Bildförberedelse + base64 i RAM + deduplicering
│   │   └── tts_service.py           # Offline TTS (pyttsx3) i daemon-tråd
│   └── ai/
│       ├── ollama_client.py         # Vision-anrop mot lokal Ollama-server
│       └── prompts.py               # 5 persona-system kopplade till avatarer
├── tests/
│   ├── test_config.py               # Verifiering av konfigurationstyper och värden
│   └── test_prompts.py              # Validering av persona-struktur
└── docs/
    ├── prototype-v1/                # Arkiverad MVP-prototyp (proof of concept)
    ├── Projektplan-Ninis_Blomerus.md
    └── (skolmaterial)
```

### Bilaga B: Installationsguide

**Förutsättningar:**
- Python 3.11+
- Ollama installerat och igång med en vision-kapabel modell
- X11-baserad skärmmiljö (Linux) eller Windows

**Steg:**

```bash
# 1. Klona repot
git clone https://github.com/itsabunny/Local-Friend.git
cd Local-Friend

# 2. Skapa virtuell miljö
python -m venv venv
source venv/bin/activate  # Linux/macOS
# .\venv\Scripts\Activate.ps1  # Windows

# 3. Installera beroenden
pip install PyQt6 Pillow mss ollama pyttsx3

# 4. Starta Ollama med vision-modell
ollama pull qwen3.5:2b  # eller annan vision-kapabel modell

# 5. Kör applikationen
PYTHONPATH=src python -m local_friend.main
```

### Bilaga C: Projektplan

Se `docs/Projektplan-Ninis_Blomerus.md` i GitHub-repot för den fullständiga, godkända projektplanen.

### Bilaga D: Git-historik (urval av milstolpar)

| Datum | Commit-typ | Beskrivning |
|---|---|---|
| 2026-05-05 | docs | Repo skapat, skolmaterial tillagt |
| 2026-05-11 | feat | Greenfield-start: projektstruktur, config, PyQt6-overlay, mss-capture |
| 2026-05-12 | feat | OllamaClient för vision, persona-prompts, RAM/base64 |
| 2026-05-17 | feat | Komplett end-to-end-flöde med signaler |
| 2026-05-24 | fix/chore | Stabilisering, think=False, capture-intervall |
| 2026-05-30 | refactor | Hide overlay during capture, AppController, widget-extrahering |
| 2026-05-31 | feat | Avatarval via högerklicksmeny |
| 2026-06-02 | feat | Offline TTS, TTS-toggle, persona-avatar-koppling |
