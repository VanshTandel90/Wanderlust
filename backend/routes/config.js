const express = require("express");
const router = express.Router();

router.get("/config", (req, res) => {
  res.status(200).json({
    mapboxToken: process.env.MAP_API_TOKEN,
    openCageToken: process.env.OPENCAGE_API_TOKEN,
  });
});

module.exports = router; 