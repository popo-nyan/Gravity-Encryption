import time
import json
import httpx
import base64
import secrets
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

T_SECRET = 26714187
KEY = "baisimeji9262019"
IV = "qrstuvwxyz123456"
PUBLIC_KEY = b"""-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA1RkoPhcnXkqpklU9uCtQocKqZrFOlYnUbRP1Zc1Xmjl+zHTKEkfRfhRU80/Zqr0FdO78dAkExMBGZ1+8MMkmtvYFskpFIWPXBdtcWxlx13L5d1+31T+GUg4X1xqn+jidzXwR4pMaYE68hKGHGcjDhBpM8JPxYSrjtvhPA3MWHo80SKIQzXqgShNPNPx1EcDRYTeYliGZg41AeNAqCbB6CEVsa4CV4ZrvBh6tY1DL95YOA6IwMazczg9zMFM5ntAwgaKTrOmKpsF1omcvuSnooD4EE367xfTuM9D5ADRT7FRWrtO5lvAsMXXftR1HIum0dmfPV9dWCVthd4EKFQ16A1NoUeBG8nQ5i+qZUcm76MqY/IaPAlRq/7j8ukpXg4vEBYzFZ/PDYQS/+rdQ3UxmnlO/w47ZrLLJV5qZOh/NriRhVWEZ3E941gbEjuh69dIV0iM3MvPFHwti5QG86NsobEIIM6O2VfScljrWUxnyLmfD8zroHIwxOJc4kZdO0HUbpwoqTq78vi/4LzkC/Hyh89VYYJ+XQSE1jCsi51R+lxRP18a5zX6NxmRYCCEyYDeyfel0MKkoTkcqasuyChIipmQ+cIHa1rR46Kaxeey2tEkHSPaR6pJwPd56S1KZvtjUvqrHdNuv/G9rLa32PRsVhUP6j+2fecmQfr6MwP9H4EcCAwEAAQ==
    -----END PUBLIC KEY-----"""


def zero_pad(plain_text, block_size):
    data_length = len(plain_text)
    padding_length = block_size - (data_length % block_size)
    padded_data = plain_text + (b"\x00" * padding_length)
    return padded_data


def encrypt(plain_data, key: str = "", encrypt_type: int = 1) -> str:
    if encrypt_type == 1:
        return base64.b64encode(
            AES.new(key=KEY.encode(), iv=IV.encode(), mode=AES.MODE_CBC).encrypt(
                pad(data_to_pad=plain_data.encode(), block_size=AES.block_size)
            )
        ).decode()
    elif encrypt_type == 2:
        return base64.b64encode(
            AES.new(key=key.encode(), iv=key.encode(), mode=AES.MODE_CBC).encrypt(
                zero_pad(json.dumps(plain_data).encode(), 16)
            )
        ).decode()


def decrypt(data: str, key: str) -> str:
    return (
        AES.new(key=key.encode(), iv=key.encode(), mode=AES.MODE_CBC)
        .decrypt(base64.b64decode(data))
        .decode()
    )


def generate_api_secret(timestamp: str) -> str:
    return "KOjDJSavxhqM1Z" + str(int(timestamp) % T_SECRET) + "Xa6fucp2t0nFYdACe2d+Xxm"


def calculate_sign(payload: dict) -> str:
    payload.pop("sign") if payload.get("sign") is not None else ""
    text = ""
    for key, value in sorted(zip(payload.keys(), payload.values())):
        text += key + "=" + value
    return hashlib.md5(text.encode()).hexdigest()


def rsa_encrypt(plain_text: str):
    public_key = serialization.load_pem_public_key(
        PUBLIC_KEY, backend=default_backend()
    )
    cipher_text = public_key.encrypt(
        base64.b64encode(plain_text.encode()), padding.PKCS1v15()
    )
    return base64.b64encode(cipher_text).decode()


def main():
    uwd = ""
    token = ""
    aes_key = secrets.token_hex(8)
    data = {
        "country": "US",
        "star_id": "0",
        "sys_lang": "en-US",
        "uwd": uwd,
        "app_version": "11.1.2",
        "is_raising_question": "0",
        "sim_country": "",
        "type": "0",
        "is_sync": "0",
        "pkg": "anonymous.sns.community.gravity",
        "languageV2": "en",
        "porn_image": "0",
        "app_version_code": "467",
        "zone": "0",
        "system_version": "14",
        "sdk_version": "34",
        "model": "Pixel_6a",
        "brand": "Google",
        "view_scope": "0",
        "product": "gravity",
        "user_country": "US",
        "idfa": "juOwtzKZsQHwMov+aUW9MQ==",
        "token": token,
        "referrer": "Organic",
        "operator_name": "Android",
        "device": "android",
        "desc": "Hello world!",
        "ts": str(int(time.time())),
    }

    api_secret = generate_api_secret(data["ts"])
    data["api_security"] = api_secret
    sign = calculate_sign(data)
    data["sign"] = sign
    data.pop("api_security")
    data["secret_key"] = aes_key

    response = httpx.post(
        "https://api.gravity.place/gravity/feed/uploadFeedEncrypt",
        content=base64.b64encode(
            json.dumps(
                {"data": encrypt(data, aes_key, 2), "key": rsa_encrypt(aes_key)}
            ).encode()
        ).decode(),
        headers={
            "Host": "api.gravity.place",
            "Content-Type": "application/raw; charset=utf-8",
            "User-Agent": "okhttp/3.12.13",
            "Accept-Encoding": "gzip, deflate, br",
        },
    )
    print(response.status_code, response.text)


main()
