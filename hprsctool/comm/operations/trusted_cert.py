"""RSC certificate commands"""

from typing import List
from pathlib import Path
from ...models import certificate
from ...comm.remote_system_controller import Rsc


def add_trusted_certificate(rsc: Rsc, cert_file_path: str):
    """Add a trusted certificate"""
    if not cert_file_path or cert_file_path == "":
        raise ValueError("No certificate file provided.")

    cert_path = Path(cert_file_path)
    if not cert_path.exists() or cert_path.is_dir():
        raise FileNotFoundError(f"Certificate file not found: {cert_file_path}")

    with open(cert_path, "r", encoding="utf-8") as cert_file:
        cert_data = cert_file.read()
    body = {"CertificateString": cert_data, "CertificateType": "PEM"}
    rsc.perform_redfish_post("/redfish/v1/Managers/1/TrustedCertificates", body)


def get_trusted_certificates(rsc: Rsc) -> List[certificate.Certificate]:
    """Get the trusted certificates"""
    response = rsc.perform_redfish_get(
        "/redfish/v1/CertificateService/CertificateLocations"
    ).dict

    result = []

    if "Links" not in response:
        return result
    if "Certificates" not in response["Links"]:
        return result

    for cert in response["Links"]["Certificates"]:
        if "TrustedCertificates" in cert["@odata.id"]:
            result.append(
                certificate.Certificate(rsc.perform_redfish_get(cert["@odata.id"]).dict)
            )
    return result


def delete_trusted_certificate(rsc: Rsc, cert_id: str):
    """Delete a trusted certificate"""
    rsc.perform_redfish_delete(f"/redfish/v1/Managers/1/TrustedCertificates/{cert_id}")
