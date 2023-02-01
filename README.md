# MacOSLocalAuthentication
A python module for using Apple's MacOS Local Authentication framework to authenticate the user.

This module is an addition to [Lukas Kollmer's](https://github.com/lukaskollmer) [touch-id](https://github.com/lukaskollmer/python-touch-id/blob/master/setup.py) for MacOS. Alot of the code was taken from it so any support should go to him.

## Requirements
The module requires pyobjc to be installed. This can be done via this command.
```
pip install pyobj
```
If this fails, more information on installation can be found here:

[Advanced pyobj installation instructions.](https://pyobjc.readthedocs.io/en/latest/install.html)

## Install
```
pip install git+https://github.com/jacob2004hamilton/MacOSLocalAuthentication
```

## Usage

Import the package:
```
import MacOSLocalAuthentication
```

To authenticate a user with biometrics (if available) or password:
```
MacOSLocalAuthentication.authenticate()
```

To authenticate a user with only biometrics:
```
MacOSLocalAuthentication.authenticate(password=False)
```

To pass a message to the user:
```
MacOSLocalAuthentication.authenticate(reason="<insert reason here>")
```

To use apple watch features:
```
MacOSLocalAuthentication.authenticate(apple_watch=True)
# AND/OR
MacOSLocalAuthentication.authenticate(wrist_detection=True)
```

To check if biometrics is available for your device:
```
MacOSLocalAuthentication.biometrics_is_available()
```

Feel free to use this library and it's code however your may please.
