"""RSC certificate commands"""

import argparse
from ...comm.remote_system_controller import Rsc
from ...comm.operations import trusted_cert as trusted_cert_ops

def get_parameters(parser: argparse.ArgumentParser) -> None:
    """Get the parameters for the certificate command"""
    subparsers = parser.add_subparsers(help="Trusted certificate commands")
    subparsers.required = True

    list_trusted = subparsers.add_parser("list", help="List trusted certificates")
    list_trusted.set_defaults(func=print_trusted_certs)

    delete_trusted = subparsers.add_parser(
        "delete", help="Delete a trusted certificate"
    )
    delete_trusted.add_argument("cert_id", help="Certificate ID", action="store")
    delete_trusted.set_defaults(func=delete_trusted_cert)

    add_trusted = subparsers.add_parser("add", help="Add a trusted certificate")
    add_trusted.add_argument(
        "cert_file", help="Certificate file in PEM format", action="store"
    )
    add_trusted.set_defaults(func=add_trusted_cert)


def add_trusted_cert(args: argparse.Namespace):
    """Add a trusted certificate"""
    rsc: Rsc = args.rsc
    trusted_cert_ops.add_trusted_certificate(rsc, args.cert_file)
    print("Trusted certificate added")


def print_trusted_certs(args: argparse.Namespace):
    """Print the trusted certificates"""
    rsc: Rsc = args.rsc
    certs = trusted_cert_ops.get_trusted_certificates(rsc)
    if len(certs) == 0:
        print("No trusted certificates installed.\n")
        return
    for cert in certs:
        print(cert)
        print()


def delete_trusted_cert(args: argparse.Namespace):
    """Delete a trusted certificate"""
    rsc: Rsc = args.rsc
    trusted_cert_ops.delete_trusted_certificate(rsc, args.cert_id)
    print("Trusted certificate deleted")
