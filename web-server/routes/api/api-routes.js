let router = require('express').Router();
const NewspaperUtils = require("../../utils/NewspaperUtils")
var request = require("request");
var username = "elastic",
    password = "elasticbk",
    url = "http://localhost:9200/talent-cleaned-e2/_search",
    auth = "Basic " + new Buffer(username + ":" + password).toString("base64");


router.get('/', function (req, res) {
    res.json({
        status: 'API Its Working',
        message: 'Welcome to RESTHub crafted with love!'
    });
});

router.get('/gete',function (req, res){
    request.get({    
        url : url,
        headers : {
            "Authorization" : auth,
            "Content-Type": 'application/json',
        },
        body:JSON.stringify({
            "query": {
                "range" : {
                    "indexed_date" : {
                        "gte" : "now-1d/d",
                        "lte" :  "now/d"
                    }
                }
            }
        })
    }, function(error, response, body){
        if(error){
            res.json({
                status: 'Error',
                message: 'Error!'
            })
        }
        var hits = JSON.parse(body).hits.total.value
        NewspaperUtils.callExternalApiUsingRequest(
            function(response){
                var values = JSON.parse(response).hits.hits;
                for(let i=0; i< 2; i++){
                    NewspaperUtils.create(values[i]).then(
                        console.log("success")
                    ).catch((err)=>{
                        console.log(err)
                    })
                }
                res.end()
            }, hits
        )
    })
})


module.exports = router;
