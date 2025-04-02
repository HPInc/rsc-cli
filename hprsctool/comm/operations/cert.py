'''RSC certificate commands'''

from ...comm.remote_system_controller import Rsc
from ...models import certificate

def get_certificate(rsc: Rsc) -> certificate.Certificate:
    """Get the certificate information"""
    return certificate.Certificate(
        rsc.perform_redfish_get(
            "/redfish/v1/Managers/1/NetworkProtocol/HTTPS/Certificates/1"
        ).dict
    )

def replace_certificate(rsc: Rsc, cert_file_path: str, key_file_path: str):
    """Upload a certificate"""
    with open(cert_file_path, "r", encoding="utf-8") as cert_file:
        cert_data = cert_file.read()
    with open(key_file_path, "r", encoding="utf-8") as key_file:
        key_data = key_file.read()
    body = {
        "CertificateUri": {
            "@odata.id": "/redfish/v1/Managers/1/NetworkProtocol/HTTPS/Certificates/1"
        },
        "CertificateString": cert_data + key_data,
        "CertificateType": "PEM",
    }
    rsc.perform_redfish_post(
        "/redfish/v1/CertificateService/Actions/CertificateService.ReplaceCertificate",
        body,
    )
