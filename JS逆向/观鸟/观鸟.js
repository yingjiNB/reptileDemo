const JSEncrypt = require('node-jsencrypt');
var crypto = require("crypto");
const CryptoJS = require('crypto-js')

function getUuid() {
    var s = [];
    var a = "0123456789abcdef";
    for (var i = 0; i < 32; i++) {
        s[i] = a.substr(Math.floor(Math.random() * 0x10), 1)
    }
    s[14] = "4";
    s[19] = a.substr((s[19] & 0x3) | 0x8, 1);
    s[8] = s[13] = s[18] = s[23];
    var b = s.join("");
    return b
}

function sort_ASCII(a) {
    var b = new Array();
    var c = 0;
    for (var i in a) {
        b[c] = i;
        c++
    }
    var d = b.sort();
    var e = {};
    for (var i in d) {
        e[d[i]] = a[d[i]]
    }
    return e
}

function url2json(a) {
    var b = /^[^\?]+\?([\w\W]+)$/
        , reg_para = /([^&=]+)=([\w\W]*?)(&|$|#)/g
        , arr_url = b.exec(a)
        , ret = {};
    if (arr_url && arr_url[1]) {
        var c = arr_url[1], result;
        while ((result = reg_para.exec(c)) != null) {
            ret[result[1]] = result[2]
        }
    }
    return ret
}

function dataTojson(a) {
    var b = [];
    var c = {};
    b = a.split('&');
    for (var i = 0; i < b.length; i++) {
        if (b[i].indexOf('=') != -1) {
            var d = b[i].split('=');
            if (d.length == 2) {
                c[d[0]] = d[1]
            } else {
                c[d[0]] = ""
            }
        } else {
            c[b[i]] = ''
        }
    }
    return c
}

const serialize = function (a) {
    var b = [];
    for (var p in a)
        if (a.hasOwnProperty(p) && a[p]) {
            b.push(encodeURIComponent(p) + '=' + encodeURIComponent(a[p]))
        }
    return b.join('&')
};
var paramPublicKey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCvxXa98E1uWXnBzXkS2yHUfnBM6n3PCwLdfIox03T91joBvjtoDqiQ5x3tTOfpHs3LtiqMMEafls6b0YWtgB1dse1W5m+FpeusVkCOkQxB4SZDH6tuerIknnmB/Hsq5wgEkIvO5Pff9biig6AyoAkdWpSek/1/B7zYIepYY0lxKQIDAQAB";
var encrypt = new JSEncrypt();
encrypt.setPublicKey(paramPublicKey);


BIRDREPORT_APIJS = {
    iv: "d93c0d5ec6352f20",
    key: "3583ec0257e2f4c8195eec7410ff1619",
    url: "www.birdreport.cn"
}


function get_headers(b) {
    var c = Date.parse(new Date());
    var d = getUuid();
    var e = JSON.stringify(sort_ASCII(dataTojson(b.data || '{}')));
    b = encrypt.encryptUnicodeLong(e);
    // var f = MD5(e + d + c);
    var f = crypto.createHash("md5").update(e + d + c).digest("hex")
    return {
        "headers": {
            "Timestamp": c + "",
            "Sign": f,
            "Requestid": d
        },
        "data": b
    }
}

function pro_decode(a) {
    var b = CryptoJS.enc.Utf8.parse(BIRDREPORT_APIJS.key);
    var c = CryptoJS.enc.Utf8.parse(BIRDREPORT_APIJS.iv);
    var d = CryptoJS.AES.decrypt(a, b, {
        iv: c,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return d.toString(CryptoJS.enc.Utf8)
}

// console.log(get_headers('page=1&limit=20&pointname=%E7%89%8C%E5%9D%8A%E5%85%AC%E5%9B%AD'))

// console.log(pro_decode('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'))