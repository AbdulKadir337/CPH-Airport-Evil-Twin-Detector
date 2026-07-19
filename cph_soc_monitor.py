import time
import os
import json
from datetime import datetime
from mockwifi import get_wifi_scan

# ENTERPRISE WHITELIST: De officielle MAC-adresser (BSSIDs) for lufthavnens Wi-Fi
CPH_OFFICIAL_BSSIDS = ["00:11:22:33:44:55", "00:11:22:33:44:66"]
LOG_FILE = "cph_security_v1.json"

def log_incident(incident_type, ssid, bssid, security):
    """Genererer professionelle JSON logs til SIEM-systemer"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "facility": "CPH_AIRPORT_WIFI_MONITOR",
        "severity": "CRITICAL",
        "incident": incident_type,
        "details": {
            "target_ssid": ssid,
            "rogue_bssid": bssid,
            "observed_security": security
        }
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def SOC_dashboard(scanning_count, alerts_found):
    """Opretter en professionel overvågningsskærm i terminalen"""
    os.system('clear')
    print("=" * 70)
    print("      KØBENHAVNS LUFTHAVNE A/S - CYBER SECURITY OPERATIONS CENTER")
    print("=" * 70)
    print(f"Status: AKTIV OVERVÅGNING  |  Scanninger kørt: {scanning_count}  |  Alarmer: {alerts_found}")
    print(f"Sidste tjek: {datetime.now().strftime('%H:%M:%S')}  |  Lokation: CPH-Kastrup (Simuleret)")
    print("-" * 70)

def analyser_wifi():
    scanning_count = 0
    alerts_found = 0
    
    while True:
        scanning_count += 1
        SOC_dashboard(scanning_count, alerts_found)
        
        scan_data = get_wifi_scan()
        linjer = scan_data.strip().split('\n')
        
        for linje in linjer[1:]:
            if "CPH Airport Free Wi-Fi" in linje:
                ssid = "CPH Airport Free Wi-Fi"
                resten = linje.replace("CPH Airport Free Wi-Fi", "").split()
                if len(resten) >= 2:
                    bssid = resten[0]
                    security = resten[1]
                    
                    # DETEKTION 1: Evil Twin via manglende kryptering
                    if security == "--":
                        alerts_found += 1
                        print(f"\n\033[91m[!!!] KRITISK ALARM: UBESKYTTET EVIL TWIN DETEKTERET!")
                        print(f"-> Forventede WPA2/WPA3, men netværket er HELT ÅBENT.")
                        print(f"-> Rogue BSSID: {bssid}\033[0m\n")
                        log_incident("UNENCRYPTED_EVIL_TWIN", ssid, bssid, security)
                        
                    # DETEKTION 2: Evil Twin via BSSID Spoofing (Ikke på hvidlisten)
                    elif bssid not in CPH_OFFICIAL_BSSIDS:
                        alerts_found += 1
                        print(f"\n\033[93m[!] ADVARSEL: UAUTORISERET BSSID DETEKTERET!")
                        print(f"-> Netværket bruger kryptering, men MAC-adressen matcher ikke CPH hvidlisten.")
                        print(f"-> Suspekt BSSID: {bssid}\033[0m\n")
                        log_incident("UNAUTHORIZED_BSSID_SPOOFING", ssid, bssid, security)

        print("[*] Venter på næste Layer 2 scanning (5s)...")
        time.sleep(5)

if __name__ == "__main__":
    try:
        analyser_wifi()
    except KeyboardInterrupt:
        print("\n[-] Overvågning stoppet af operatør. Logger af.")
