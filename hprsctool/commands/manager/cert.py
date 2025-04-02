'''RSC certificate commands'''

import argparse
from ...comm.remote_system_controller import Rsc
from ...comm.operations import cert as cert_ops

def get_parameters(parser: argparse.ArgumentParser) -> None:
    '''Get the parameters for the certificate command'''
    subparsers = parser.add_subparsers(help="Certificate commands")
    subparsers.required = True
    get_subparser = subparsers.add_parser("get", help="Get the RSC certificate information")
    get_subparser.set_defaults(func=print_rsc_https_cert)
    upload_subparser = subparsers.add_parser("replace", help="Replace the HTTPS certificate")
    upload_subparser.add_argument("cert_file", help="Certificate file in PEM format",
                                  action="store")
    upload_subparser.add_argument("key_file", help="Private key file in PEM format", action="store")
    upload_subparser.set_defaults(func=upload_cert)

def print_rsc_https_cert(args: argparse.Namespace):
    '''Print the certificate information'''
    rsc: Rsc = args.rsc
    cert = cert_ops.get_certificate(rsc)
    print(cert)

def upload_cert(args: argparse.Namespace):
    '''Upload a certificate'''
    cert_ops.replace_certificate(args.rsc, args.cert_file, args.key_file)
    print("Certificate replaced")
