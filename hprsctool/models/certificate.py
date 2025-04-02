"""Certificate models"""

from typing import Any

# Sample certificate json:
#
# {
#   "@odata.type": "#Certificate.v1_6_0.Certificate",
#   "@odata.id": "/redfish/v1/Managers/1/NetworkProtocol/HTTPS/Certificates/1",
#   "Name": "HTTPS Certificate",
#   "Id": "1",
#   "CertificateString": "-----BEGIN CERTIFICATE-----\nMIIE7jCCAtagAwIBAgIUFTJFuqm8YDvFI7Aa/3SntW2LURwwDQYJKoZIhvcNAQEL\nBQAwGTEXMBUGA1UEAwwOcnNjLThDQzIzMjIyQzEwHhcNMjQwNTAyMTkyNTMxWhcN\nMzQwNDMwMTkyNTMxWjAqMQ8wDQYDVQQKDAZIUCBSU0MxFzAVBgNVBAMMDnJzYy04\nQ0MyMzIyMkMxMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAxI7kL9HJ\nv6/mLj/LJLdlEGO0KYZB9y0ylWMunxpB8I0IuKUaCn4GjFJtwic87dkRbj/zyo4c\nnR+EXmOuYfzJiSu5QAQW5ZK3lf6kk8nc4hRnrWEbTvW6/nQcYe4tM0IpO6M1kXOp\ng11ih70NXQItPD/FxVQYx1eSlo3ckgwx+Jw/6W+S1uAtnsV/csuqwSFGpQUOQ8+J\nS7E5TIZSFOx+V6KupVqzykcWoSJpf8G+g/1f/TdKrvAS6sxQrW7jiCCzrR1DP7Mt\nWMnDydzfL3UAyGJiUp0tIeigUQfZrS4Y8mrLtK4mHXEY56N9YI4ytEA4TnCO0cdc\nY0mSPXCx4LEXUpvucNEEwRx49oH0WTEOovUhcQ/dyd4/dRSfxWuaC67Zdt8mvPMR\nQ+hu49ehZR25gCemIQa+p2fJmNc/Sd7StLQOypwk15jeBZPBB/h/sUdO37Jm+Duh\niZLWDSYM/0fCmbvHSQLCYoFMY60uTIDUPiuCXSTj/QtyDxZpmZAjeNkeM2E1HTRw\n2hC8Ra5HPJXkRhHorQodyzP1P8E8lFBwBzN0aG6uoT8Iji6xVdFUPCBdZGN5NeC9\nyTtEnSqzNy8Av6SSp6f4e11iYr6SFgzarJaCk6QjTkX33ASBw9D27UaZmTYgbI5i\neTAHqBjo6eo4uGpBndWkR4gbqITPRr/1PC0CAwEAAaMdMBswGQYDVR0RBBIwEIIO\ncnNjLThDQzIzMjIyQzEwDQYJKoZIhvcNAQELBQADggIBAObZX+6It9cGNiVwt9tL\n+oS1q/uICPF1kTgRN5fQ+QMDzY68BROXcBZgoyMghAxZ3aklqqsMaK1INd6ICQLf\nGwxt0ckdbw32pVn/ABGza1mzufB3NG915wiJbEBOZm6oioDPjYj+3rVoUwq1HLz3\nrwvMaOKTro+yTMf3+yWGRKccgCsFk9aVTCGT1/jzuEKJnB6kpSfb91DfXeiwvl+U\nfWLNTy2Z6Q/eYWPVc9cGUaFX/pLDAulfPxxrW3xssjGJ2ILyRoByEO/MnxWRHvkQ\nrXgbp6jJinyJQhnzOYallDt3M638OfC3xcK01EsOe3KjmpBgwrtw889cF07MKDgy\nx7ihH/HZBVrLUjX5jF6cgAhd9d0fIvoluOWymbzkdZI6OEKvIuRdWN+rwIbV40SM\nViPpeygGMs0FM2VTxi8sfTvjbitZsOi713Qp4WrASbAbZ1jrtjNjj4LY/CprcguP\nogZJVCv+N7+stO4fkdJbXwbTZsrBPU5LCf3/zpE3ABntE68Vm7M6bJO/tKsbzNae\nme2jNprw4/n5x/Ky8YUOmLVo/la5c+VS+GuubCLclya3PkBAILf7VzjpDqyy1u3J\nFxCqEUxO8gS1h6Y/0IX5ewguT7ay2c9n5WOSMM7xpbKc0j3JgwgW+iO5AGH0qU3+\nihwwUXTPHfBvO7y12RloMNIY\n-----END CERTIFICATE-----",
#   "CertificateType": "PEM",
#   "CertificateUsageTypes": [
#     "Web"
#   ],
#   "Subject": {
#     "CommonName": "rsc-8CC23222C1",
#     "Organization": "HP RSC"
#   },
#   "Issuer": {
#     "CommonName": "rsc-8CC23222C1"
#   },
#   "SerialNumber": "15:32:45:ba:a9:bc:60:3b:c5:23:b0:1a:ff:74:a7:b5:6d:8b:51:1c",
#   "Signature": "e6:d9:5f:ee:88:b7:d7:06:36:25:70:b7:db:4b:fa:84:b5:ab:fb:88:08:f1:75:91:38:11:37:97:d0:f9:03:03:cd:8e:bc:05:13:97:70:16:60:a3:23:20:84:0c:59:dd:a9:25:aa:ab:0c:68:ad:48:35:de:88:09:02:df:1b:0c:6d:d1:c9:1d:6f:0d:f6:a5:59:ff:00:11:b3:6b:59:b3:b9:f0:77:34:6f:75:e7:08:89:6c:40:4e:66:6e:a8:8a:80:cf:8d:88:fe:de:b5:68:53:0a:b5:1c:bc:f7:af:0b:cc:68:e2:93:ae:8f:b2:4c:c7:f7:fb:25:86:44:a7:1c:80:2b:05:93:d6:95:4c:21:93:d7:f8:f3:b8:42:89:9c:1e:a4:a5:27:db:f7:50:df:5d:e8:b0:be:5f:94:7d:62:cd:4f:2d:99:e9:0f:de:61:63:d5:73:d7:06:51:a1:57:fe:92:c3:02:e9:5f:3f:1c:6b:5b:7c:6c:b2:31:89:d8:82:f2:46:80:72:10:ef:cc:9f:15:91:1e:f9:10:ad:78:1b:a7:a8:c9:8a:7c:89:42:19:f3:39:86:a5:94:3b:77:33:ad:fc:39:f0:b7:c5:c2:b4:d4:4b:0e:7b:72:a3:9a:90:60:c2:bb:70:f3:cf:5c:17:4e:cc:28:38:32:c7:b8:a1:1f:f1:d9:05:5a:cb:52:35:f9:8c:5e:9c:80:08:5d:f5:dd:1f:22:fa:25:b8:e5:b2:99:bc:e4:75:92:3a:38:42:af:22:e4:5d:58:df:ab:c0:86:d5:e3:44:8c:56:23:e9:7b:28:06:32:cd:05:33:65:53:c6:2f:2c:7d:3b:e3:6e:2b:59:b0:e8:bb:d7:74:29:e1:6a:c0:49:b0:1b:67:58:eb:b6:33:63:8f:82:d8:fc:2a:6b:72:0b:8f:a2:06:49:54:2b:fe:37:bf:ac:b4:ee:1f:91:d2:5b:5f:06:d3:66:ca:c1:3d:4e:4b:09:fd:ff:ce:91:37:00:19:ed:13:af:15:9b:b3:3a:6c:93:bf:b4:ab:1b:cc:d6:9e:99:ed:a3:36:9a:f0:e3:f9:f9:c7:f2:b2:f1:85:0e:98:b5:68:fe:56:b9:73:e5:52:f8:6b:ae:6c:22:dc:97:26:b7:3e:40:40:20:b7:fb:57:38:e9:0e:ac:b2:d6:ed:c9:17:10:aa:11:4c:4e:f2:04:b5:87:a6:3f:d0:85:f9:7b:08:2e:4f:b6:b2:d9:cf:67:e5:63:92:30:ce:f1:a5:b2:9c:d2:3d:c9:83:08:16:fa:23:b9:00:61:f4:a9:4d:fe:8a:1c:30:51:74:cf:1d:f0:6f:3b:bc:b5:d9:19:68:30:d2:18",
#   "SignatureAlgorithm": "SHA256-RSA",
#   "ValidNotAfter": "2034-04-30T19:25:31Z",
#   "ValidNotBefore": "2024-05-02T19:25:31Z",
#   "Fingerprint": "1a:14:c7:93:fc:f0:25:2d:a4:ca:95:1c:1b:78:64:7d:ee:5e:46:1c:f6:18:2f:a7:4c:bd:12:97:e0:0f:56:e6",
#   "FingerprintHashAlgorithm": "TPM_ALG_SHA256"
# }

# Sample certificate in version 23.02 json:
# {
#   "@odata.type": "#Certificate.v1_1_0.Certificate",
#   "@odata.id": "/redfish/v1/Managers/1/TrustedCertificates/fe5c994e-a62a-46ac-8ba0-5d424661d748",
#   "Name": "Trusted Certificate",
#   "Id": "fe5c994e-a62a-46ac-8ba0-5d424661d748",
#   "CertificateString": "-----BEGIN CERTIFICATE-----\nMIIFLzCCAxegAwIBAgIUH2wDZDaJPf9DrPRvjIndE64nyUEwDQYJKoZIhvcNAQEL\nBQAwJzELMAkGA1UECgwCSFAxGDAWBgNVBAMMD0lBbVRoZUF1dGhvcml0eTAeFw0y\nMzExMTAxNjUyNDlaFw0yNjA4MzAxNjUyNDlaMCcxCzAJBgNVBAoMAkhQMRgwFgYD\nVQQDDA9JQW1UaGVBdXRob3JpdHkwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIK\nAoICAQC2rigg5eM1tK3SQAWIgvvT6GDdPLneaZqgGIMckDA/irVCePf+rpakF1bE\nmhqXMa4c+1YFDRjGWdTCUtBOuuQxOKxQofzHiQLoy12VEMs7PFtOexAfUNWLmVmn\nDHIE49K9xwNEejtc6LvpCyUbJXOVxX7xeU1wqBh9w4lUkCABvzLN89OORDKVY0tm\nFXhJodls98Yo2yXBVFX4ieFrWJCQ/gqr3d/B9bQ+kYQ+9GTc3/9UfX4wVrP2l8Zc\nYmj3DDAKMea8R013XuczYFKgNxD5eP3c5gUgcGUwB5AeYhTiY/1etGfzOwcvuKhN\nc2/RF+KQ6JxLmfHUtskU1jgZxO8hxRyEOQdatFcjl1BE1Xf/Ngs4sN3FXmOljvBj\ng/Cp5WS/UJh2ZUwSiLgonOhmN2N5oJ4nZ1G7sQ/waytpSlawtojewaYnMf5W7wph\n5EObQZCQXfW+QSGMnMgWQvTY4/93kLv1aBbIKGXOvjE8TC7YOYgqm9k7OTb78Qcp\nud2XB7n+gm9EeugOn9N8xYUSvxmCEVpknBsGu+ZQ5TNT1nda+9UUCTraG0Pg/k1D\ncTUjA+juSDNa5vmBrjBcXNF35JH/UT9LS4dN2BIorNa1cBhh6e/FwOI921ENXKOX\nxFBdSsiGgLxRvnycvl2dJITyEtxjCPWzSdozCJMbCtOWwbp8zQIDAQABo1MwUTAd\nBgNVHQ4EFgQU1RUwFf05yVh5oXeUYAsRVMVkU6gwHwYDVR0jBBgwFoAU1RUwFf05\nyVh5oXeUYAsRVMVkU6gwDwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0BAQsFAAOC\nAgEAk6VO6/bxflnul8vumBX02PiKIdhebwmU894nZI9v1VodR9cxFFcjy4E5Ii5C\nBURaIePmdkWGzH0hTZcMbs0gDGTNYdGNbejrXX2hwFr6+dyJE7LTN9eFe3WayE7z\nfqhdjAxTo0FfKfaCibGfRKzvQx1LB/FPkeAv1y4DLqG4WijNdaW0e9RTJ0hdOh6c\n+JzNquPrjl4Fc9Fr9EFnieBVihPBkyvENcWBW4IZekj5r5pqXnBPwkLJ6yFhtJfs\nhcHNxBHZVGRP7/+tkv8ePPK1OgKeVGNpTxr2u/IDLBt/AiyCZ/4whwK+MOfqLPzP\nBptvxQuIhTnqlLrDQn4dgemodA2knFORkWUdnk34ZhhND8px/1CcJSKysNaIyBmJ\nLkAFfYdVI2A9j7+hihyX1puSlhDSVlj+scBapUzYKHTsV5I5l7LWFNnuV2xSew0S\ntOlwvRNbXmNZRqsVHJFo2ErxSvvj6MvXefSUH5zx96ZBy4XPTiwK0EJtcrO4bhcH\nEF7MxZZudboPcl6JbF/mhKCj4MRrBTTdsfsu5gaTXjvkv5Qcw5pTlpqNSbpSbp3U\ne+f6imZXi1ltyPH8PebdPAR6SDVkpeSGvca9+RLI3FbthJhMJiLsdAIutDNDit+Z\n78+clCnqITL95v2Ug24AdIUnQoWlEuDQ5Lkab8KiqRzUmuI=\n-----END CERTIFICATE-----\n",
#   "CertificateType": "PEM",
#   "CertificateUsageType": "Web",
#   "Subject": {
#     "City": "",
#     "CommonName": "IAmTheAuthority",
#     "Country": "",
#     "Organization": "HP",
#     "OrganizationalUnit": "",
#     "State": ""
#   }
# }


class Certificate:
    """Certificate model"""

    def __init__(self, data: Any) -> None:
        if data is None:
            raise ValueError("data is required")
        self.data = data

    @property
    def certificate(self) -> str:
        """Get the certificate"""
        return self.data.get("CertificateString", "N/A")

    @property
    def certificate_type(self) -> str:
        """Get the certificate type"""
        return self.data.get("CertificateType", "N/A")

    @property
    def certificate_expiration(self) -> str:
        """Get the certificate expiration"""
        return self.data.get("ValidNotAfter", "N/A")

    @property
    def certificate_id(self) -> str:
        """Get the certificate ID"""
        return self.data.get("Id", "N/A")

    @property
    def certificate_fingerprint(self) -> str:
        """Get the certificate fingerprint"""
        return self.data.get("Fingerprint", "N/A")

    def __str__(self) -> str:
        """Print the certificate"""
        return (
            f"ID: {self.certificate_id}\n"
            f"Certificate:\n{self.certificate}\n"
            f"Type: {self.certificate_type}\n"
            f"Expiration: {self.certificate_expiration}\n"
            f"Fingerprint: {self.certificate_fingerprint}"
        )
