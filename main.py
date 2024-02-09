import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

KEY = "baisimeji9262019"
IV = "qrstuvwxyz123456"


def encrypt(plain_text: str) -> str:
    return base64.b64encode(AES.new(key=KEY.encode(), iv=IV.encode(), mode=AES.MODE_CBC).encrypt(pad(data_to_pad=plain_text.encode(), block_size=AES.block_size))).decode()


def decrypt(cipher_text: str) -> str:
    return AES.new(key=KEY.encode(), iv=IV.encode(), mode=AES.MODE_CBC).decrypt(base64.b64decode(cipher_text.encode())).decode()


print(encrypt("20FF6747-36C8-4DDC-A2EC-1DDC23C8A88F"))
print(encrypt("65b6be33-4f47-4a12-a51d-802caf718422"))
print(encrypt("12064743925"))
print(encrypt("hoge@example.net"))
print(decrypt("eTw17q4kUr/RU51LIXenRw=="))
print(decrypt("g5NUW1JrtR9uuU6+tYTfqs4OlybKuxK8HkOsWNLIPYs="))
print(encrypt("gravity@@@hoge@example.net@@@1706611279@@@passport2020"))
