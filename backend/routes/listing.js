const express=require("express")
const router=express.Router()
const wrapAsync=require("../utils/wrapAsync.js")
const Listing=require("../models/listing.js")
const {isLoggedIn, isOwner, validateListing}=require("../middleware.js")

const listingController=require("../controllers/listings.js")
const multer=require("multer")
const {storage}=require("../cloudConfig.js")
const upload=multer({storage})

// Add this import at the top of the file
const axios = require('axios');



router.route("/")
    // index route
    .get(wrapAsync(listingController.index))
    //create route
    .post(isLoggedIn , upload.single('listing[image]') , validateListing , wrapAsync(listingController.createListing )) 


// new route
router.get("/new", isLoggedIn ,listingController.renderNewForm)

//category
router.get("/categories/:category",wrapAsync(listingController.category))

router.post("/search",wrapAsync(listingController.searchDestination))

router.route("/:id")
    // show route
    .get(wrapAsync(listingController.showListing ))
    // update route
    .put(isLoggedIn , isOwner , upload.single('listing[image]') , validateListing, wrapAsync(listingController.updateListing))
    //delete route
    .delete(isLoggedIn , isOwner , wrapAsync(listingController.destroyListing))

// edit route
router.get("/:id/edit",isLoggedIn , isOwner , wrapAsync(listingController.renderEditForm))

// New route to predict price
router.post("/predict-price", wrapAsync(async (req, res) => {
    try {
        const { location, country } = req.body;
        // Forward the request to the Python microservice
        const pythonResponse = await axios.post('http://localhost:8001/predict-price', {
            location,
            country
        });
        res.status(200).json(pythonResponse.data);
    } catch (err) {
        console.error("Error calling Python service:", err.response?.data || err.message);
        res.status(err.response?.status || 500).json({ 
            error: err.response?.data?.error || "Failed to get price prediction from Python service."
        });
    }
}));

module.exports=router