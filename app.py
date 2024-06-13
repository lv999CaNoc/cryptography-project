import base64
from aes import AES
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/aes', methods=['POST'])
def aes_text():
    args = request.json

    if (args["inputType"]== "UTF8"):
        input = args["input"].encode('utf-8')
    else:
        input = base64.b64decode(args["input"])

    
    if (args["encrypt"]):
        response = encrypt(args["padding"],
            args["mode"],
            args["iv"],
            input,
            args["key"])
    else:
        response = decrypt(args["padding"],
            args["mode"],
            args["iv"],
            input,
            args["outputType"],
            args["key"])

     
    return jsonify(response)

def encrypt(padding, mode, iv, input, key):
    m_aes = AES(key.encode('utf-8'))
    if mode == "ECB":
        output = m_aes.encrypt_ecb(input, padding)
    elif mode == "CBC":
        output = m_aes.encrypt_cbc(input, iv, padding)
    elif mode == "CFB":
        output = m_aes.encrypt_cfb(input, iv)
    elif mode == "OFB":
        output = m_aes.encrypt_ofb(input, iv)
    elif mode == "CTR":
        output = m_aes.encrypt_ctr(input, iv)

    return {
        "output": base64.b64encode(output).decode('utf-8'),
        "outputType": "BASE64"
    }

def decrypt(padding, mode, iv, input, outputType, key):
    m_aes = AES(key.encode('utf-8'))
    if mode == "ECB":
        output = m_aes.decrypt_ecb(input, padding)
    elif mode == "CBC":
        output = m_aes.decrypt_cbc(input, iv, padding)
    elif mode == "CFB":
        output = m_aes.decrypt_cfb(input, iv)
    elif mode == "OFB":
        output = m_aes.decrypt_ofb(input, iv)
    elif mode == "CTR":
        output = m_aes.decrypt_ctr(input, iv)

    if outputType == "UTF8":
        output = output.decode("utf-8")
    else:
        output = base64.b64encode(output).decode('utf-8')

    return {
        "output": output,
        "outputType": outputType
    }

if __name__ == '__main__':
    app.run(port=1111, debug=True)
