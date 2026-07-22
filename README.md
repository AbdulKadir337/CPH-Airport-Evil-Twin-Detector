# CPH Airport - Rogue AP & Evil Twin Detector

Dette projekt er bygget forud for mit 3. semester på IT-teknologuddannelsen. Målet er at overvåge Layer 2 trådløse beacons i luften og slå alarm, hvis en hacker opsætter et falsk, ubeskyttet netværk, der efterligner lufthavnens officielle "CPH Airport Free Wi-Fi".

Da min VMware Ubuntu-VM ikke har direkte adgang til computerens interne Wi-Fi-kort, har jeg bygget en komplet Simulation Engine (`mockwifi.py`), der spytter præcis samme data ud som `nmcli device wifi list`. Det gør, at hele systemet kan testes uden ekstra hardware.

## 🛠️ Projekthistorik (Mine versioner)
Projektet er opdelt i tre filer for at vise min udvikling i koden:

*   **`detecterv1.py`**: Den første rå prototype. Den splitter tekst-outputtet fra scanningen, isolerer SSID, BSSID (MAC) og sikkerhedskolonnen, og spytter en alarm ud, hvis netværket er ubeskyttet (`--`).
*   **`cph_soc_monitor.py`**: Her pakkede jeg logikken ind i et uendeligt loop, lavede et rent SOC-dashboard på skærmen og tilføjede JSON-logning. Den gemmer alarmer i et format, der kan læses direkte ind i et SIEM-system (f.eks. Splunk).
*   **`cph_soc_monitor_v2.py` (Det færdige produkt)**: Min optimerede version, hvor jeg fiksede to store problemer:
    1. **Støjreduktion (State Management)**: I v1 kørte loggen i ring og spammerede logfilen hvert 5. sekund. I v2 bruger jeg et Python `set` til at huske hackerens MAC-adresse. Den advarer på skærmen live, men logger kun hackeren ÉN gang.
    2. **Defensiv kodning**: Tilføjet `try/except` og datavalidering, så scriptet ikke crasher, hvis det modtager korrupte eller uventede netværkspakker i luften.
 

## 🖥️ Live SOC Dashboard & Logs (Screenshots)

Her er systemet i aktion under en simuleret scanning. Læg mærke til, hvordan v2 holder styr på de unikke trusler og stopper log-spamming:

### 1. Det aktive SOC Dashboard i terminalen
<img width="607" height="221" alt="detecterv1" src="https://github.com/user-attachments/assets/f875092f-3672-4a9f-8363-11155b5c0dfe" />

### 2. cph_soc_monitor.py - Dashboard til v1 (pumper dublerede alarmer ud)
<img width="797" height="270" alt="cph_soc_monitorv1" src="https://github.com/user-attachments/assets/419d13fb-f4e7-4401-9078-52668147b8f9" />

### 3. cph_soc_monitor_v2.py - Dashboard til v2 (isolerer unikke trusler og fjerner støj)
<img width="809" height="290" alt="cph_soc_monitorv2" src="https://github.com/user-attachments/assets/1daabaef-45ac-4e7f-9879-d364420a546f" />



## 📊 Eksempel på SIEM JSON-Log
Hver unik alarm gemmes i en ren JSON-linje med tidsstempel, trusselsniveau og hackerens rå data:
`{"timestamp": "2026-07-19T01:00:20", "facility": "CPH_MONITOR", "severity": "CRITICAL", "incident": "UNENCRYPTED_EVIL_TWIN", "details": {"target_ssid": "CPH Airport Free Wi-Fi", "rogue_bssid": "AA:BB:CC:DD:EE:FF", "observed_security": "--"}}`



🎯 Formål og anvendelse

Dette projekt er lavet som et praktisk læringsværktøj til mit studie som IT-teknolog.

Det viser:
- Hvordan ubeskyttede netværk kan misbruges
- Hvordan man opdager simple rogue APs
- Hvordan man bygger et SOC-lignende dashboard i terminalen
- Hvordan man gemmer hændelser i et simpelt JSON-format
- Hvordan man arbejder med Python, loops, state management og defensiv kodning

Projektet er ikke et professionelt sikkerhedsprodukt, men et studieprojekt der viser min interesse for netværkssikkerhed og praktisk Python-automatisering.



📁 Projektstruktur

CPH-Airport-Evil-Twin-Detector/
│
├── detecterv1.py
├── cph_soc_monitor.py
├── cph_soc_monitor_v2.py
├── mockwifi.py
└── README.md



🔧 Fremtidige forbedringer

Hvis jeg vælger at arbejde videre på projektet, kunne jeg tilføje:

- Whitelist/blacklist af MAC-adresser
- Bedre håndtering af nmcli output
- Farvekoder i dashboardet
- En simpel web-visning af alarmer
- Mulighed for at gemme logs i en separat fil pr. scanning



👤 Om mig

Jeg studerer IT-teknolog og arbejder med Python, Linux, netværk og små sikkerhedsprojekter.
Dette projekt er lavet for at vise min tilgang til praktisk problemløsning og min interesse for IT-sikkerhed.

