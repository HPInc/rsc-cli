'''RSC certificate commands'''

from ...comm.remote_system_controller import Rsc
from ...models import certificate
from .collection import get_default_uri

def get_certificate(rsc: Rsc) -> certificate.Certificate:
    """Get the certificate information"""
    manager_uri = get_default_uri(rsc, "/redfish/v1/Managers")
    return certificate.Certificate(
        rsc.perform_redfish_get(
            f"{manager_uri}/NetworkProtocol/HTTPS/Certificates/1"
        ).dict
    )

def replace_certificate(rsc: Rsc, cert_file_path: str, key_file_path: str):
    """Upload a certificate"""
    with open(cert_file_path, "r", encoding="utf-8") as cert_file:
        cert_data = cert_file.read()
    with open(key_file_path, "r", encoding="utf-8") as key_file:
        key_data = key_file.read()
    manager_uri = get_default_uri(rsc, "/redfish/v1/Managers")
    body = {
        "CertificateUri": {
            "@odata.id": f"{manager_uri}/NetworkProtocol/HTTPS/Certificates/1"
        },
        "CertificateString": cert_data + key_data,
        "CertificateType": "PEM",
    }
    rsc.perform_redfish_post(
        "/redfish/v1/CertificateService/Actions/CertificateService.ReplaceCertificate",
        body,
    )
