from cryptography import x509
from cryptography.hazmat.backends import default_backend

# Zertifikat im DER-Format laden
with open(r"C:\Users\jonas\OneDrive\Dokumente\BBS-Brinkstraße\VIT (C. Wichmann)\OPC-UA\Zertifikate\uaexpert.der", "rb") as cert_file:
    cert_data = cert_file.read()

# Zertifikat parsen
cert = x509.load_der_x509_certificate(cert_data, default_backend())

# Alternative Namen (URN) extrahieren
try:
    alt_names = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
    for name in alt_names.value:
        if isinstance(name, x509.UniformResourceIdentifier):
            print("URN:", name.value)
except Exception as e:
    print("Fehler beim Auslesen der URN:", e)