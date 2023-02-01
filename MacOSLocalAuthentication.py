"""
The main bulk of this code is from lukaskollmer on GitHub.
This simply allows the user to access the other functions on the Apple Authentication framework.

ORIGINAL SOURCE:
https://github.com/lukaskollmer/python-touch-id/blob/master/touchid.py

This addition also requires pyobjc to be installed.

NOTE: I could not find a solution to only allow a password input as this does not seem to be a policy in the LA framework.
"""

import sys
import ctypes
from LocalAuthentication import *

kTouchIdPolicy = LAPolicyDeviceOwnerAuthenticationWithBiometrics

c = ctypes.cdll.LoadLibrary(None)

PY3 = sys.version_info[0] >= 3
if PY3:
    DISPATCH_TIME_FOREVER = sys.maxsize
else:
    DISPATCH_TIME_FOREVER = sys.maxint

dispatch_semaphore_create = c.dispatch_semaphore_create
dispatch_semaphore_create.restype = ctypes.c_void_p
dispatch_semaphore_create.argtypes = [ctypes.c_int]

dispatch_semaphore_wait = c.dispatch_semaphore_wait
dispatch_semaphore_wait.restype = ctypes.c_long
dispatch_semaphore_wait.argtypes = [ctypes.c_void_p, ctypes.c_uint64]

dispatch_semaphore_signal = c.dispatch_semaphore_signal
dispatch_semaphore_signal.restype = ctypes.c_long
dispatch_semaphore_signal.argtypes = [ctypes.c_void_p]

def biometrics_is_available():
    context = LAContext.new()
    return context.canEvaluatePolicy_error_(kTouchIdPolicy, None)[0]

def authenticate(reason="authenticate the user", biometrics=True, password=True, apple_watch=False, wrist_detection=False):
    """
    Authentication function that returns a boolean value based on whether authentication was successful.
    Parameters:
        reason: message to be displayed to the user when authentication is requested.
        biometrics: option to use face-id or touch-id, will raise an error if not available.
        password: option to allow the user to input their password instead of biometrics. 
        apple_watch: option to enter code on apple watch as authentication.
        wrist_detection: option to use wrist detection (apple watch) for authentication.
    """

    context = LAContext.new()

    # sorting through LAPolicies
    if biometrics:
        if not biometrics_is_available():
            raise NotImplementedError("Your device does not have biometric authentication methods.")
        if biometrics and not password and not apple_watch:
            kTouchIdPolicy = LAPolicyDeviceOwnerAuthenticationWithBiometrics
        if biometrics and password:
            kTouchIdPolicy =  LAPolicyDeviceOwnerAuthentication
        if not biometrics and not password and apple_watch:
            kTouchIdPolicy = LAPolicydeviceOwnerAuthenticationWithWatch
        if biometrics and not password and apple_watch:
            kTouchIdPolicy = LAPolicydeviceOwnerAuthenticationWithBiometricsOrWatch

    can_evaluate = context.canEvaluatePolicy_error_(kTouchIdPolicy, None)[0]
    if not can_evaluate:
        raise Exception("Authentication failed.")

    sema = dispatch_semaphore_create(0)

    # we can't reassign objects from another scope, but we can modify them
    res = {'success': False, 'error': None}

    def cb(_success, _error):
        res['success'] = _success
        if _error:
            res['error'] = _error.localizedDescription()
        dispatch_semaphore_signal(sema)

    context.evaluatePolicy_localizedReason_reply_(kTouchIdPolicy, reason, cb)
    dispatch_semaphore_wait(sema, DISPATCH_TIME_FOREVER)

    if res['error']:
        raise Exception(res['error'])

    return res['success']
