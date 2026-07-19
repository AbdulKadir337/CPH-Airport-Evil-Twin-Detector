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

## 📊 Eksempel på SIEM JSON-Log
Hver unik alarm gemmes i en ren JSON-linje med tidsstempel, trusselsniveau og hackerens rå data:
`{"timestamp": "2026-07-19T01:00:20", "facility": "CPH_MONITOR", "severity": "CRITICAL", "incident": "UNENCRYPTED_EVIL_TWIN", "details": {"target_ssid": "CPH Airport Free Wi-Fi", "rogue_bssid": "AA:BB:CC:DD:EE:FF", "observed_security": "--"}}`
