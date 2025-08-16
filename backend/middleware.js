const Listing = require("./models/listing")
const Review = require("./models/review.js")
const ExpressError = require("./utils/ExpressError.js")
const {listingSchema, reviewSchema} = require("./schema.js")

module.exports.isLoggedIn = (req, res, next) => {
    if (!req.isAuthenticated()) {
        return res.status(401).json({ error: "You must be logged in to do that!" });
    }
    next();
}

module.exports.saveRedirectUrl = (req, res, next) => {
    if (req.session && req.session.redirectUrl) {
        res.locals.redirectUrl = req.session.redirectUrl;
    }
    next();
}

module.exports.isOwner = async (req, res, next) => {
    try {
        let { id } = req.params;
        let listing = await Listing.findById(id);
        
        if (!listing) {
            return res.status(404).json({ error: "Listing not found" });
        }
        
        if (!listing.owner.equals(req.user._id)) {
            return res.status(403).json({ error: "You don't have permission to do that!" });
        }
        
        next();
    } catch (err) {
        return res.status(500).json({ error: err.message });
    }
}

module.exports.validateListing = (req, res, next) => {
    try {
        let {error} = listingSchema.validate(req.body);
        if (error) {
            let errMsg = error.details.map((el) => el.message).join(",");
            return res.status(400).json({ error: errMsg });
        } else {
            next();
        }
    } catch (err) {
        return res.status(500).json({ error: "Error validating listing" });
    }
}

module.exports.validateReview = (req, res, next) => {
    try {
        let {error} = reviewSchema.validate(req.body);
        if (error) {
            let errMsg = error.details.map((el) => el.message).join(",");
            return res.status(400).json({ error: errMsg });
        } else {
            next();
        }
    } catch (err) {
        return res.status(500).json({ error: "Error validating review" });
    }
}

module.exports.isReviewAuthor = async (req, res, next) => {
    try {
        let { id, reviewId } = req.params;
        let review = await Review.findById(reviewId);
        
        if (!review) {
            return res.status(404).json({ error: "Review not found" });
        }
        
        if (!review.author.equals(req.user._id)) {
            return res.status(403).json({ error: "You don't have permission to do that!" });
        }
        
        next();
    } catch (err) {
        return res.status(500).json({ error: err.message });
    }
}