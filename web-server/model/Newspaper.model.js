const mongoose = require("mongoose")
const Schema = mongoose.Schema

const NewspaperSchema = new Schema({
    _id: {
        type: String,
        required: true,
    },
    _source:{
        url:{
            type: String,
        },
        title:{
            type: String,
        },
        summary:{
            type: String,
        },
        content:{
            type: String,
        },
        source:{
            type: String,
        },
        published_date:{
            type: String, 
        },
        images:{
            type: [{
                type: String
            }]
        },
        indexed_date:{
            type:String,
        },
        processor_ner_loc:{
            cities:[{
                type: String,
            }],
            provinces: [{
                type: String,
            }],
            nations: [{
                type: String,
            }]
        },
        processor_category_classify:{
            type: String
        },
        process_talent_info:{
            Salary: [{
                type: String,
            }],
            Environment:[{
                type: String
            }],
            Regime:[{
                type: String
            }]
        }
    },
    no_view:{
        type: Number
    }
})

module.exports = Newspaper = mongoose.model("newspaper",NewspaperSchema)