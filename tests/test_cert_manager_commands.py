"""Manager cert command tests"""

import argparse

from unittest.mock import MagicMock, patch

import pytest

from hprsctool.commands.manager.cert import print_rsc_https_cert
from hprsctool.commands.manager.cert import get_parameters, upload_cert


def test_get_parameters():
    parser = argparse.ArgumentParser()
    get_parameters(parser)
    args = parser.parse_args(["get"])
    assert args.func.__name__ == "print_rsc_https_cert"

    args = parser.parse_args(["replace", "cert.pem", "key.pem"])
    assert args.func.__name__ == "upload_cert"
    assert args.cert_file == "cert.pem"
    assert args.key_file == "key.pem"


def test_get_parameters_missing_subcommand():
    parser = argparse.ArgumentParser()
    get_parameters(parser)
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_print_rsc_https_cert():
    mock_rsc = MagicMock()
    mock_cert = "Mock Certificate"
    mock_args = argparse.Namespace(rsc=mock_rsc)

    with patch(
        "hprsctool.commands.manager.cert.cert_ops.get_certificate",
        return_value=mock_cert,
    ) as mock_get_cert:
        print_rsc_https_cert(mock_args)
        mock_get_cert.assert_called_once_with(mock_rsc)


def test_print_rsc_https_cert_no_certificate():
    mock_rsc = MagicMock()
    mock_args = argparse.Namespace(rsc=mock_rsc)

    with patch(
        "hprsctool.commands.manager.cert.cert_ops.get_certificate", return_value=None
    ) as mock_get_cert:
        print_rsc_https_cert(mock_args)
        mock_get_cert.assert_called_once_with(mock_rsc)
        mock_rsc.print.assert_not_called()

def test_upload_cert():
    mock_rsc = MagicMock()
    mock_args = argparse.Namespace(rsc=mock_rsc, cert_file="cert.pem", key_file="key.pem")

    with patch("hprsctool.commands.manager.cert.cert_ops.replace_certificate") as mock_replace_cert:
        upload_cert(mock_args)
        mock_replace_cert.assert_called_once_with(mock_rsc, "cert.pem", "key.pem")

def test_upload_cert_prints_message(capfd):
    mock_rsc = MagicMock()
    mock_args = argparse.Namespace(rsc=mock_rsc, cert_file="cert.pem", key_file="key.pem")

    with patch("hprsctool.commands.manager.cert.cert_ops.replace_certificate"):
        upload_cert(mock_args)
        out, _ = capfd.readouterr()
        assert "Certificate replaced" in out
