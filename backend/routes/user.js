const express=require("express")
const router=express.Router()
const User=require("../models/user.js")
const wrapAsync = require("../utils/wrapAsync")
const passport=require("passport")
const { saveRedirectUrl } = require("../middleware.js")

const userController=require("../controllers/users.js")


router.get("/me", userController.checkAuth);

router.route("/signup")
    // .get(userController.renderSignupForm) // This is for EJS, not needed for React
    .post(wrapAsync(userController.signup));

router.route("/login")
    // .get(userController.renderLoginForm) // This is for EJS, not needed for React
    .post(
        saveRedirectUrl, 
        passport.authenticate("local", { failureMessage: true }), 
        userController.login
    );

router.get("/logout",userController.logout)

module.exports=router