var NewspaperModel = require("../model/Newspaper.model")
var MathUtils = require("../utils/Math")
var request = require("request");
var username = "elastic",
    password = "elasticbk",
    url = "http://localhost:9200/talent-cleaned-e2/_search",
    auth = "Basic " + new Buffer(username + ":" + password).toString("base64");


const create = async (item)=>{
    try {
        //fake no view
        var Newspaper = await NewspaperModel.create({ 
            _id: item._id,
            _source: item._source,
            no_view: MathUtils.getRandomInt(1000)
            }); 
        console.log("newspaper "+Newspaper._id +" created")
    } catch (error) {
        console.log( {message: error});
    }
}
exports.create = create
//////////////////////////////////////////////////////////
const callExternalApiUsingRequest = (callback, hits) => {
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
            },
            "size": hits
        })
    },
    (err, res, body) => {
        if (err) { 
            return callback(err);
        }
        return callback(body);
    });
}
exports.callExternalApiUsingRequest = callExternalApiUsingRequest
//////////////////////////////////////////////////////////
exports.getFreshNewspaperFromElastic = (req, res)=>{
    request.get({    
        url : url,
        headers : {
            // "Authorization" : auth,
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
        callExternalApiUsingRequest(
            function(response){
                var values = JSON.parse(response).hits.hits;
                for(let i=0; i< hits; i++){
                    create(values[i]).then(
                        console.log(".......creating.......")
                    ).catch((err)=>{
                        console.log(err)
                    })
                }
            }, hits
        )
    })
}