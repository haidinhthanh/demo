var request = require("request");
var username = "elastic",
    password = "elasticbk",
    url = "http://54.68.196.78:9200",
    auth = "Basic " + new Buffer(username + ":" + password).toString("base64");
Request.get(
    {
        url : url,
        headers : {
            "Authorization" : auth,
            "Content-Type": 'application/json',
        }
    },
    function (error, response, body) {
        if(error) {
            return console.dir(error);
        }
        console.dir(JSON.parse(body));       
    }
);
