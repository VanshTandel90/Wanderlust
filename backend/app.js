if (process.env.NODE_ENV != "production") {
  require("dotenv").config();
}

const express = require("express");
const app = express();
const mongoose = require("mongoose");
const path = require("path");
const methodOverride = require("method-override");
const ExpressError = require("./utils/ExpressError.js");
const session = require("express-session");
const flash = require("connect-flash");
const passport = require("passport");
const LocalStrategy = require("passport-local");
const User = require("./models/user.js");
const cors = require("cors");

const listingRouter = require("./routes/listing.js");
const reviewRouter = require("./routes/review.js");
const userRouter = require("./routes/user.js");
const configRouter = require("./routes/config.js");

const MONGO_URL = "mongodb://127.0.0.1:27017/wanderlust";

main().then(() => {
  console.log("connected to DB");
});

async function main() {
  await mongoose.connect(MONGO_URL);
}

// Middleware
app.use(
  cors({
    origin: "http://localhost:5173", // React app will run on this port
    methods: ["GET", "POST", "PUT", "DELETE"],
    credentials: true,
  })
);
app.use(express.json()); // Parse JSON bodies

app.use(express.urlencoded({ extended: true }));
app.use(methodOverride("_method"));

const sessionOptions = {
  secret: "mysupersecret",
  resave: false,
  saveUninitialized: true,
  cookie: {
    expires: Date.now() + 7 * 24 * 60 * 60 * 1000,
    maxAge: 7 * 24 * 60 * 60 * 1000,
    httpOnly: true,
  },
};

app.use(session(sessionOptions));
app.use(flash());

app.use(passport.initialize());
app.use(passport.session());
passport.use(new LocalStrategy(User.authenticate()));

passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());

app.use((req, res, next) => {
  res.locals.success = req.flash("success");
  res.locals.error = req.flash("error");
  res.locals.currUser = req.user;
  next();
});

// API Routes
app.get("/", (req, res) => {
  res.json({ message: "Welcome to RentEasy API" });
});

app.use("/api/listings", listingRouter);
app.use("/api/listings/:id/reviews", reviewRouter);
app.use("/api", userRouter);
app.use("/api", configRouter);

// Error handling
app.all("*", (req, res, next) => {
  next(new ExpressError(404, "API endpoint not found"));
});

app.use((err, req, res, next) => {
  let { statusCode = 500, message = "Something went wrong" } = err;
  res.status(statusCode).json({
    error: {
      statusCode,
      message,
    },
  });
});

// const PORT = process.env.PORT || 8080
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`API server running on http://localhost:${PORT}`);
});
