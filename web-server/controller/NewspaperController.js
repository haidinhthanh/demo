const NewspaperService = require("../services/NewspaperService")

exports.getAll = (req, res) => {
    return NewspaperService.getALl(req, res);
}
exports.deleteAll = (req, res)=>{
    return NewspaperService.deleteAll(req,res);
}
exports.getN0Posts = (req, res)=>{
    return NewspaperService.getN0Posts(req, res);
}
exports.getPopularPosts = (req, res)=>{
    return NewspaperService.getPopularPosts(req, res);
}
exports.getRecentPosts = (req, res)=>{
    return NewspaperService.getRecentPosts(req, res)
}

exports.getPostById = (req, res)=>{
    return NewspaperService.getPostById(req, res)
}