# Dokumentation (Examensarbete)

Den här mappen innehåller material kopplat till examensarbetet **"Min lokala vän"**:
projektplan, instruktioner från skolan, exempelrapport samt en arkiverad prototyp (MVP).

> Tips: Den “riktiga” implementationen som hör till examensarbetet ska ligga i repo:t i övrigt.
> Allt i `docs/` är stödmaterial och historik.

## Innehåll

### Skolmaterial
- `instruktioner-examensarbete.md`  
  Instruktioner för upplägg, inlämning och redovisning.

- `handbok-examensarbete.md`  
  Handbok med tips kring planering, rapportstruktur, SOLO-taxonomi m.m.

- `Examensarbete exempel.pdf`  
  Exempel på examensrapport (referens för struktur/stil).

### Projektplan
- `Projektplan-Ninis_Blomerus.md`  
  Godkänd projektplan med problemformulering, mål, avgränsningar, teknisk stack, tidsplan och riskanalys.

### Prototyp / MVP (historik)
- `prototype-v1/LocalDesktopPet-main.zip`  
  Arkiverad prototyp från innan greenfield-ombyggnaden.
  Syftet är att kunna jämföra “första MVP:n” med den nya arkitekturen och dokumentera lärdomar.

  Notering: Zip-arkivet innehåller i nuläget:
  - `script.py`
  - `README.md`
  - `.gitignore`

## Varför prototypen ligger som zip
- För att tydligt markera att det är en “frysning”/historik och inte den kod som vidareutvecklas.
- För att minska risken att blanda prototypkod med den nya implementationen.

## Hur jag öppnar prototypen lokalt

### Linux/macOS
```sh
cd docs/prototype-v1
unzip LocalDesktopPet-main.zip -d LocalDesktopPet-main
