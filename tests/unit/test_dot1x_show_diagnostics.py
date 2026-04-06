"""Unit tests for dot1x_show_diagnostics module parser."""

from dot1x_show_diagnostics import _parse_diagnostics

SINGLE_OUTPUT = """
eth1/0/1 dot1x diagnostic information are following:
EntersConnecting                      : 20
EAP-LogoffsWhileConnecting            : 0
EntersAuthenticating                  : 0
SuccessesWhileAuthenticating          : 0
TimeoutsWhileAuthenticating           : 0
FailsWhileAuthenticating              : 0
ReauthsWhileAuthenticating            : 0
EAP-StartsWhileAuthenticating         : 0
EAP-LogoffsWhileAuthenticating        : 0
ReauthsWhileAuthenticated             : 0
EAP-StartsWhileAuthenticated          : 0
EAP-LogoffsWhileAuthenticated         : 0
BackendResponses                      : 0
BackendAccessChallenges               : 0
BackendOtherRequestsToSupplicant      : 0
BackendNonNakResponsesFromSupplicant : 0
BackendAuthSuccesses                  : 0
BackendAuthFails                      : 0
"""

MULTI_OUTPUT = """
eth1/0/1 dot1x diagnostic information are following:
EntersConnecting                      : 20
EAP-LogoffsWhileConnecting            : 0
EntersAuthenticating                  : 3
SuccessesWhileAuthenticating          : 2
TimeoutsWhileAuthenticating           : 1
FailsWhileAuthenticating              : 0
ReauthsWhileAuthenticating            : 0
EAP-StartsWhileAuthenticating         : 0
EAP-LogoffsWhileAuthenticating        : 0
ReauthsWhileAuthenticated             : 0
EAP-StartsWhileAuthenticated          : 0
EAP-LogoffsWhileAuthenticated         : 0
BackendResponses                      : 10
BackendAccessChallenges               : 3
BackendOtherRequestsToSupplicant      : 0
BackendNonNakResponsesFromSupplicant : 2
BackendAuthSuccesses                  : 2
BackendAuthFails                      : 1

eth1/0/2 dot1x diagnostic information are following:
EntersConnecting                      : 5
EAP-LogoffsWhileConnecting            : 1
EntersAuthenticating                  : 0
SuccessesWhileAuthenticating          : 0
TimeoutsWhileAuthenticating           : 0
FailsWhileAuthenticating              : 0
ReauthsWhileAuthenticating            : 0
EAP-StartsWhileAuthenticating         : 0
EAP-LogoffsWhileAuthenticating        : 0
ReauthsWhileAuthenticated             : 0
EAP-StartsWhileAuthenticated          : 0
EAP-LogoffsWhileAuthenticated         : 0
BackendResponses                      : 0
BackendAccessChallenges               : 0
BackendOtherRequestsToSupplicant      : 0
BackendNonNakResponsesFromSupplicant : 0
BackendAuthSuccesses                  : 0
BackendAuthFails                      : 0
"""


def test_parse_single_interface():
    results = _parse_diagnostics(SINGLE_OUTPUT)
    assert len(results) == 1
    r = results[0]
    assert r["interface"] == "eth1/0/1"
    assert r["enters_connecting"] == 20
    assert r["eap_logoffs_while_connecting"] == 0
    assert r["backend_auth_successes"] == 0
    assert r["backend_auth_fails"] == 0


def test_parse_multi_interface():
    results = _parse_diagnostics(MULTI_OUTPUT)
    assert len(results) == 2

    r1 = results[0]
    assert r1["interface"] == "eth1/0/1"
    assert r1["enters_connecting"] == 20
    assert r1["enters_authenticating"] == 3
    assert r1["successes_while_authenticating"] == 2
    assert r1["backend_responses"] == 10
    assert r1["backend_auth_successes"] == 2
    assert r1["backend_auth_fails"] == 1

    r2 = results[1]
    assert r2["interface"] == "eth1/0/2"
    assert r2["enters_connecting"] == 5
    assert r2["eap_logoffs_while_connecting"] == 1
    assert r2["backend_responses"] == 0


def test_parse_empty():
    results = _parse_diagnostics("")
    assert results == []
