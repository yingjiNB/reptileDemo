var crypto = require("crypto");
CryptoJS = require('crypto-js')


h = function (t) {
    var data = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {}
        , e = 'a75846eb4ac490420ac63db46d2a03bf'
        , n = e + f(data) + f(t) + e;
    return n = d(n),
        n = v(n)
}

f = function (t) {
    var e = "";
    return Object.keys(t).sort().forEach((function (n) {
            e += n + ("object" === typeof t[n] ? JSON.stringify(t[n], (function (t, e) {
                    return "number" == typeof e && (e = String(e)),
                        e
                }
            )).replace(/\//g, "\\/") : t[n])
        }
    )),
        e
}

function r(e) {
    return r = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (e) {
            return typeof e
        }
        : function (e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
        }
        ,
        r(e)
}

d = function (data) {
    return crypto.createHash("md5").update(data).digest("hex").toString();
}
v = function (data) {
    return CryptoJS.AES.encrypt(data, l.key, {
        iv: l.iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    }).toString()
}
l = {
    key: CryptoJS.enc.Utf8.parse("fX@VyCQVvpdj8RCa"),
    iv: CryptoJS.enc.Utf8.parse(function (t) {
        for (var e = "", i = 0; i < t.length - 1; i += 2) {
            var n = parseInt(t[i] + "" + t[i + 1], 16);
            e += String.fromCharCode(n)
        }
        return e
    }("00000000000000000000000000000000"))
}


function fn(P) {
    let date = parseInt((new Date).getTime() / 1e3)

    var U = {
        "App-Ver": "",
        "Os-Ver": "",
        "Device-Ver": "",
        Imei: "",
        "Access-Token": "",
        Timestemp: date+"",
        NonceStr: "".concat(date).concat("bmkcg"),
        "App-Id": "4ac490420ac63db4",
        "Device-Os": "web"
    };
    U['Signature'] = h(U, P, 'a75846eb4ac490420ac63db46d2a03bf')

    return U
}
console.log(fn)