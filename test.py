'''
Description: Rolin's code edit
Author: Rolin-Code
Date: 2021-11-05 10:14:40
LastEditors: Rolin
Code-Function-What do you want to do: test
'''
import base64

res = base64.b64decode('bGRhcCBhdXRoIGVycm9y'.encode()).decode
print(res.decode())
