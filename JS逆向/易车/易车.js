var crypto = require("crypto");

function my_md5(e) {
    return crypto.createHash("md5").update(e).digest("hex");
}

console.log(my_md5('123456'))

function get_headers(params) {
    headers = {}
    headers["x-timestamp"] = (new Date).getTime() + "";
    o = "19DDD1FBDFF065D3A4DA777D2D7A81EC";
    n = "cid=" + 508 + "&param=" + JSON.stringify(params) + o + headers["x-timestamp"]
    headers["x-sign"] = my_md5(n);
    headers["x-platform"] = "pc";
    headers["x-city-id"] = "2401";
    headers["x-ip-address"] = "101.87.131.240";
    headers["x-user-guid"] = "e79cb639-097c-41fc-b867-1e0d788b0c78";
    return headers
}
params = {cityId: '2401', serialId: '7219'}
console.log(get_headers(params))