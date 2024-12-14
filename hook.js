Java.perform(function () {
    var x2Class = Java.use("X2.a");

    function bytesToString(arr) {
        let str = "";
        arr = new Uint8Array(arr);
        for (let i in arr) {
            str += String.fromCharCode(arr[i]);
        }
        return str;
    }


    x2Class.a.overload("javax.crypto.spec.SecretKeySpec", "[B").implementation = function (key, plainText) {
        const result = this.a(key, plainText);
        console.log(`Plain text: ${bytesToString(plainText)}`);
        return result;
    };
});
