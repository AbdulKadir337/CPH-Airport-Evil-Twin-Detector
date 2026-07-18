from mockwifi import get_wifi_scan

def analyser_wifi():
    print("[*] Scanner efter Rogue APs / Evil Twins i CPH...")
    scan_data = get_wifi_scan()
    linjer = scan_data.strip().split('\n')
    
    for linje in linjer[1:]:
        if "CPH Airport Free Wi-Fi" in linje:
            # Hvis linjen indeholder CPH netværket, ved vi præcis hvad SSID er
            ssid = "CPH Airport Free Wi-Fi"
            # Vi fjerner navnet fra linjen for nemt at finde BSSID og kryptering bagefter
            resten = linje.replace("CPH Airport Free Wi-Fi", "").split()
            if len(resten) >= 2:
                bssid = resten[0]
                security = resten[1]
                
                # ALARM LOGIK: Hvis netværket er ubeskyttet
                if security == "--":
                    print("\n[!!!] ALARM: EVIL TWIN DETEKTERET!")
                    print(f"-> Netværksnavn (SSID): {ssid}")
                    print(f"-> Hackerens MAC (BSSID): {bssid}")
                    print(f"-> Sikkerhedsstatus: {security} (UBESKYTTET NETVÆRK!)\n")

if __name__ == "__main__":
    analyser_wifi()
