const Listing = require("../models/listing")

module.exports.index = async (req, res) => {
    try {
        const allListings = await Listing.find({})
        
        res.status(200).json(allListings)
    } catch (err) {
        res.status(500).json({ error: err.message })
    }
}

module.exports.category = async (req, res) => {
    try {
        const { category } = req.params;
        const allListings = await Listing.find({ category: { $in: [category] } });
        res.status(200).json(allListings);
    } catch (err) {
        res.status(500).json({ error: err.message })
    }
};

module.exports.searchDestination = async (req, res) => {
    try {
        const { destination } = req.body;
                
        if (!destination || typeof destination !== 'string') {
            return res.status(400).json({ 
                error: "Search destination is required and must be a string" 
            });
        }
        
        const regex = new RegExp(destination, 'i'); // case-insensitive search
        const allListings = await Listing.find({
            $or: [
                { location: regex },
                { country: regex },
                { title: regex }
            ]
        });
        if (allListings.length == 0) {
            return res.status(200).json([]);
        }
        res.status(200).json(allListings);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};


module.exports.renderNewForm = (req, res) => {
    res.status(200).json({ message: "GET form data endpoint" })
}


module.exports.showListing = async (req, res) => {
    try {
        let { id } = req.params
        const listing = await Listing.findById(id).populate({
            path: "reviews",
            populate: { path: "author" }
        }).populate("owner")
        
        if (!listing) {
            return res.status(404).json({ error: "Listing not found" })
        }
        
        res.status(200).json(listing)
    } catch (err) {
        res.status(500).json({ error: err.message })
    }
}

module.exports.createListing = async (req, res, next) => {
    try {
        let url = req.file.path
        let filename = req.file.filename
        
        const newListing = new Listing(req.body.listing)
        newListing.owner = req.user._id
        newListing.image = { url, filename }
        
        await newListing.save()
        res.status(201).json({ 
            message: "New Listing Created!",
            listing: newListing 
        })
    } catch (err) {
        res.status(400).json({ error: err.message })
    }
}

module.exports.renderEditForm = async (req, res) => {
    try {
        let { id } = req.params
        const listing = await Listing.findById(id)
        
        if (!listing) {
            return res.status(404).json({ error: "Listing not found" })
        }
        
        res.status(200).json(listing)
    } catch (err) {
        res.status(500).json({ error: err.message })
    }
}

module.exports.updateListing = async (req, res) => {
    try {
        let { id } = req.params;

        // Find the listing to be updated
        let listing = await Listing.findById(id);
        if (!listing) {
            return res.status(404).json({ error: "Listing you requested for does not exist" });
        }
        Object.assign(listing, req.body.listing);
        
        if (req.file) {
            let url = req.file.path;
            let filename = req.file.filename;
            listing.image = { url, filename };
        }
        
        await listing.save();
        
        res.status(200).json({
            message: "Listing Updated!",
            listing: listing
        });
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
}

module.exports.destroyListing = async (req, res) => {
    try {
        let { id } = req.params
        let deletedListing = await Listing.findByIdAndDelete(id)
        
        if (!deletedListing) {
            return res.status(404).json({ error: "Listing not found" })
        }
        
        res.status(200).json({
            message: "Listing Deleted!",
            listingId: id
        })
    } catch (err) {
        res.status(500).json({ error: err.message })
    }
}