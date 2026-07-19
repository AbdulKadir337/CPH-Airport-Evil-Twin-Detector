import time
import os
import json
from datetime import datetime
from mockwifi import get_wifi_scan

CPH_OFFICIAL_BSSIDS = ["00:11:22:33:44:55", "00:11:22:33:44:66"]
LOG_FILE = "cph_security_v2.json"

# State Management: Holder styr på, hvilke hacker-MAC-adresser vi ALLEREDE har logget
loggede_trusler = set()

def log_incident(incident_type, ssid, bssid, security):
    """Logger kun hændelsen, hvis vi ikke har set dette BSSID i denne session før"""
    if bssid in loggede_trusler:
        return # Stop her, vi har allerede logget denne hacker én gang!
        
    loggede_trusler.add(bssid)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "facility": "CPH_AIRPORT_WIFI_MONITOR",
        "severity": "CRITICAL",
        "incident": incident_type,
        "details": {"target_ssid": ssid, "rogue_bssid": bssid, "observed_security": security}
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def SOC_dashboard(scanning_count, alerts_found):
    os.system('clear')
    print("=" * 70)
    print("      KØBENHAVNS LUFTHAVNE A/S - CYBER SECURITY OPERATIONS CENTER")
    print("=" * 70)
    print(f"Status: AKTIV OVERVÅGNING  |  Scanninger kørt: {scanning_count}  |  Unikke Trusler: {alerts_found}")
    print(f"Sidste tjek: {datetime.now().strftime('%H:%M:%S')}  |  Lokation: CPH-Kastrup (Simuleret)")
    print("-" * 70)

def analyser_wifi():
    scanning_count = 0
    
    while True:
        scanning_count += 1
        SOC_dashboard(scanning_count, len(loggede_trusler))
        
        scan_data = get_wifi_scan()
        linjer = scan_data.strip().split('\n')
        
        for linje in linjer[1:]:
            if "CPH Airport Free Wi-Fi" in linje:
                try:
                    ssid = "CPH Airport Free Wi-Fi"
                    resten = linje.replace("CPH Airport Free Wi-Fi", "").split()
                    
                    # Defensiv kodning: Tjek om vi faktisk har nok kolonner tilgængelige
                    if len(resten) < 2:
                        continue
                        
                    bssid = resten[0]
                    security = resten[1]
                    
                    # DETEKTION 1: Evil Twin via manglende kryptering
                    if security == "--":
                        print(f"\n\033[91m[!!!] KRITISK ALARM: UBESKYTTET EVIL TWIN DETEKTERET!")
                        print(f"-> Forventede WPA2/WPA3, men netværket er HELT ÅBENT.")
                        print(f"-> Rogue BSSID: {bssid}\033[0m")
                        log_incident("UNENCRYPTED_EVIL_TWIN", ssid, bssid, security)
                        
                    # DETEKTION 2: Evil Twin via BSSID Spoofing (Ikke på hvidlisten)
                    elif bssid not in CPH_OFFICIAL_BSSIDS:
                        print(f"\n\033[93m[!] ADVARSEL: UAUTORISERET BSSID DETEKTERET!")
                        print(f"-> Netværket bruger kryptering, men matcher ikke CPH hvidlisten.")
                        print(f"-> Suspekt BSSID: {bssid}\033[0m")
                        log_incident("UNAUTHORIZED_BSSID_SPOOFING", ssid, bssid, security)
                        
                except Exception as e:
                    # Defensiv kodning: Hvis noget uforudset sker under parsing, overlever programmet her
                    continue

        print("\n[*] Venter på næste Layer 2 scanning (5s)...")
        time.sleep(5)

if __name__ == "__main__":
    try:
        analyser_wifi()
    except KeyboardInterrupt:
        print("\n[-] Overvågning stoppet af operatør. Logger af.")
