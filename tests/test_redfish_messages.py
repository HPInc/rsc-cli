"""Tests for the redfish_messages module."""

from hprsctool.comm.redfish_messages import get_error_message

def test_get_error_message_with_none():
    """Test get_error_message with None input."""
    assert get_error_message(None) is None


def test_get_error_message_with_no_error_key():
    """Test get_error_message when 'error' key is not present."""
    resp_json = {"key": "value"}
    assert get_error_message(resp_json) is None


def test_get_error_message_with_empty_extended_info():
    """Test get_error_message with empty '@Message.ExtendedInfo'."""
    resp_json = {"error": {"@Message.ExtendedInfo": []}}
    assert get_error_message(resp_json) is None


def test_get_error_message_with_message_and_args():
    """Test get_error_message with valid message and arguments."""
    resp_json = {
        "error": {
            "@Message.ExtendedInfo": [
                {"Message": "Error %1 occurred.", "MessageArgs": ["123"]}
            ]
        }
    }
    assert get_error_message(resp_json) == "Error 123 occurred."


def test_get_error_message_with_extended_info():
    """Test get_error_message with '@Message.ExtendedInfo' key present."""
    resp_json = {
        "@Message.ExtendedInfo": [
            {
                "MessageArgs": ["123"],
                "Message": "Error %1 occurred."
            }
        ]
    }
    assert get_error_message(resp_json) == "Error 123 occurred."
