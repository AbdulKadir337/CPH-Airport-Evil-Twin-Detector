def get_wifi_scan():
    mock_output = (
        "SSID              BSSID              SECURITY  CHAN\n"
        "CPH Airport Free Wi-Fi    00:11:22:33:44:55  WPA2      1   \n"
        "CPH Airport Free Wi-Fi    AA:BB:CC:DD:EE:FF  --        6   \n"
        "SAS_Lounge        12:34:56:78:9A:BC  WPA3      11  \n"
        "Falsk_Netvaerk    FE:ED:FA:CE:11:22  --        36  "
    )
    return mock_output
