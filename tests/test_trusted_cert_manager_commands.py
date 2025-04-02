"""Tests for the trusted_cert_manager_commands module."""

from unittest.mock import patch, MagicMock
import pytest
from hprsctool.commands.manager.trusted_cert import (
    print_trusted_certs,
    add_trusted_cert,
    delete_trusted_cert,
)


@pytest.fixture(name="mock_rsc")
def fixture_mock_rsc():
    return MagicMock()


@pytest.fixture(name="mock_args")
def fixture_mock_args(mock_rsc):
    args = MagicMock()
    args.rsc = mock_rsc
    return args


@pytest.fixture(name="mock_args_with_cert")
def fixture_mock_args_with_cert(mock_rsc):
    mock_args = MagicMock()
    mock_args.rsc = mock_rsc
    mock_args.cert_file = "path/to/cert"
    return mock_args


def test_print_trusted_certs_no_certs(mock_args):
    with patch(
        "hprsctool.comm.operations.trusted_cert.get_trusted_certificates",
        return_value=[],
    ):
        with patch("builtins.print") as mock_print:
            print_trusted_certs(mock_args)
            mock_print.assert_called_once_with("No trusted certificates installed.\n")

def test_add_trusted_cert(mock_args_with_cert):
    with patch(
        "hprsctool.comm.operations.trusted_cert.add_trusted_certificate"
    ) as mock_add_cert:
        add_trusted_cert(mock_args_with_cert)
        mock_add_cert.assert_called_once_with(
            mock_args_with_cert.rsc, mock_args_with_cert.cert_file
        )


def test_add_trusted_cert_no_cert(mock_args):
    mock_args.cert_file = None
    with pytest.raises(ValueError):
        add_trusted_cert(mock_args)


@pytest.fixture(name="mock_args_with_cert_id")
def fixture_mock_args_with_cert_id(mock_rsc):
    args = MagicMock()
    args.rsc = mock_rsc
    args.cert_id = "test-cert-id"
    return args


def test_delete_trusted_cert(mock_args_with_cert_id):
    with patch(
        "hprsctool.comm.operations.trusted_cert.delete_trusted_certificate"
    ) as mock_delete_cert:
        delete_trusted_cert(mock_args_with_cert_id)
        mock_delete_cert.assert_called_once_with(
            mock_args_with_cert_id.rsc, mock_args_with_cert_id.cert_id
        )
