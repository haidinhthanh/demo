let express = require('express')
let bodyParser = require('body-parser');
let mongoose = require('mongoose');
let cors = require("cors")
let apiRoutes = require("./routes/api/api-routes")
let newspaperApi = require("./routes/api/newspaper")

let newspaperUtils = require("./utils/NewspaperUtils")

let app = express();
var port = process.env.PORT || 80;
// body parser
app.use(cors())
app.use(bodyParser.urlencoded({
   extended: false
}));
app.use(bodyParser.json());

// connect mongodb
mongoose.connect('mongodb://localhost/resthub', { useNewUrlParser: true});
var db = mongoose.connection;

if(!db)
    console.log("Error connecting db")
else
    console.log("Db connected successfully")

//api
app.use('/api', apiRoutes)
app.use('/api/newspaper', newspaperApi)
////
app.get('/', (req, res) => res.send('Hello World with Express'));

var CronJob = require('cron').CronJob;
var job = new CronJob('00 22 21 * * *', function(req, res) {
    console.log("chay luc 23h 30 .........")
    console.log("chay luc 23h 30 .........")
    console.log("chay luc 23h 30 .........")
    newspaperUtils.getFreshNewspaperFromElastic(req, res)
  }, 
  true,
  'Asia/Ho_Chi_Minh' 
);
job.start()

var server = app.listen(port, () => console.log(`Server up and running on port ${port} !`));
server.timeout = 2000;
