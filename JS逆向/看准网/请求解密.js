const CryptoJS = require('crypto-js')

e = '{"query":"python","cityCode":1,"industryCodes":"","pageNum":1,"limit":15}'
t = '9z6EtIbELlhpuN3e'
key = 'G$$QawckGfaLB97r'
r = CryptoJS.AES.encrypt(e.toString(), CryptoJS.enc.Utf8.parse(key), {
    iv: CryptoJS.enc.Utf8.parse(t),
    mode: CryptoJS.mode.CBC,
    pad: CryptoJS.pad.Pkcs7
});

console.log(r.toString())