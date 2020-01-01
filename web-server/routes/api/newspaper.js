let router = require("express").Router()
const NewspaperController = require("../../controller/NewspaperController")

router.get("/getAll",NewspaperController.getAll)
router.get("/getNOPosts", NewspaperController.getN0Posts)
router.get("/deleteAll", NewspaperController.deleteAll)
router.get("/getPopularPosts/:no_post/:from", NewspaperController.getPopularPosts)
router.get("/getRecentPosts", NewspaperController.getRecentPosts)
router.get("/getPost/:id", NewspaperController.getPostById)
module.exports = router