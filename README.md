# Gravity
Gravityでは、ほぼすべてのリクエストにuwd（ユーザーID）やidfa（広告識別子）というパラメータが含まれており、これを用いてユーザーを検証しています。  
また、アカウントのログインや作成時には、pnum（電話番号）やaddress（メールアドレス）に暗号化されたデータを送信しています。

バージョン10.7.0からは、主要なエンドポイントの末尾に**Encrypt**が追加され、ペイロード自体が暗号化されるようになりました。  
さらに、使用される共通鍵もRSAの公開鍵で暗号化されるようになっています。  
具体的な実装については、[upload_feed.py](https://github.com/popo-nyan/Gravity-Encryption/blob/master/upload_feed.py)を参照してください。

# 連絡先
- Matrix: @kounomiya:hackliberty.org
- Discord: popo.nyan

# スクリーンショット
メールアドレスでログイン
![](2023-02-09-12-05-21.png)

電話番号でログイン
![](2023-02-09-12-12-51.png)
