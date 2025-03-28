from time import sleep
from opcua import Client
from cryptography import x509
from cryptography.hazmat.backends import default_backend

# Pfade zu Zertifikat und privatem Schlüssel
certificate_path = r"c:\Users\jonas\OneDrive\Dokumente\BBS-Brinkstraße\VIT (C. Wichmann)\OPC-UA\Zertifikate\uaexpert.der"
private_key_path = r"c:\Users\jonas\OneDrive\Dokumente\BBS-Brinkstraße\VIT (C. Wichmann)\OPC-UA\Zertifikate\uaexpert_key.pem"
 
# Erzeuge Client-Objekt
client = Client("opc.tcp://192.168.24.105:4840")

client.set_security_string(f"Basic256Sha256,SignAndEncrypt,{certificate_path},{private_key_path}")


client.application_uri = "urn:Surface_Lueke:UnifiedAutomation:UaExpert"
# setze Benutzername und Passwort
client.set_user('OPC')
client.set_password('OPC')

try:
    client.connect()

    # greife auf Elemente im Baum zu
    Root = client.get_root_node()
    Objects = client.get_objects_node()


    device_set = Objects.get_child(["2:DeviceSet"])
    codesys_control = device_set.get_child(["4:CODESYS Control for Raspberry Pi 64 SL"])
    resources = codesys_control.get_child(["3:Resources"])
    application = resources.get_child(["4:Application"])
    programs = application.get_child(["3:Programs"])
    plc_prg = programs.get_child(["4:PLC_PRG"])

    # erzeuge Objekte für Knoten aus dem Baum über OPC UA Notation
    ausgang = client.get_node('ns=4;s=|var|CODESYS Control for Raspberry Pi 64 SL.Application.PLC_PRG.ausgang')
    eingang1 = client.get_node('ns=4;s=|var|CODESYS Control for Raspberry Pi 64 SL.Application.PLC_PRG.eingang1')
    eingang2 = client.get_node('ns=4;s=|var|CODESYS Control for Raspberry Pi 64 SL.Application.PLC_PRG.eingang2')


    # OPC-Variablen besitzen vier Attribute: Datentyp, Wert, Status, Zeitstempel
    data = ausgang.get_data_value()
    print('************ Variable: Ausgang ************')
    print('Datentyp:    ', data.Value.VariantType)
    print('Wert:        ', data.Value.Value)
    print('Status:      ', data.StatusCode)
    print('Zeitstempel: ', data.SourceTimestamp)
    print('*******************************************')

    # Variable ausgang auslesen
    print('Wert der Variable "ausgang": ', ausgang.get_value())

    # Variablen eingang1 und eingang2 schreiben
    print('Setzen beider Eingänge auf True!')
    eingang1.set_value(True)
    eingang2.set_value(True)
    sleep(1.0)

    # Variable ausgang auslesen
    print('Wert der Variable "ausgang": ', ausgang.get_value())

    # Variablen eingang1 und eingang2 schreiben
    print('Setzen eines Eingangs auf False!')
    eingang1.set_value(False)
    sleep(1.0)

    # Variable ausgang auslesen
    print('Wert der Variable "ausgang": ', ausgang.get_value())

finally:
    client.disconnect()