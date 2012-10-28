#!/usr/bin/env python

import base64,hashlib

def lineToFingerprint(line):
    key = base64.b64decode(line.strip().partition('ssh-rsa ')[2].split(' ')[0])
    fp_plain = hashlib.md5(key).hexdigest()
    return ':'.join(a+b for a,b in zip(fp_plain[::2], fp_plain[1::2]))


if __name__ == '__main__':
    line = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8Tq7CNTq/YMfQhquicqPUWXrPDFXTTEpwry1MeBQOI5rIgUk4iHnOz8aXSdZrlrsIu57cCrHwwq3G2RXvWAQmg9YUEnaeukopyRpcZRRUXPzbwT+xipJfyyxXYwMbCwpS3occqlIYcFAMgu3O3UcttSA6Vc6LBbMDwKBrDBK2e4zMo2tMOw4dZ02fEZ6Vfs5W/G8BFXCuVTTz6TJnrGPo0MwE8eKdzBf6qFQpyOpEfzq1gSM2B51pd/s5/uZmVP2knGcP3/RfcWRO4hdkadGNHCUILBmwFaCICahzEEHDGqNi4i8g8Mgcty7kdoyASxkjf/Oyih4jzIUl8UROEj7B ibkim@ubuntu"
    print lineToFingerprint(line)

