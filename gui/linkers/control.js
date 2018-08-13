function call_control () {
    var python = require("python-shell");
    var path = require("path");

    var control = document.getElementById("control");

    var options = {
        scriptPath : path.join(__dirname, '/../engine/'),
        pythonPath : "/home/jota/.virtualenvs/pyelectron/bin/python"
    }

    var serial = new python("ledSerial.py", options)
    serial.end(function (err, code, message) {
        
    });
}