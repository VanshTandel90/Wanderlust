const User = require("../models/user");

module.exports.checkAuth = (req, res) => {
  if (!req.isAuthenticated()) {
    return res.status(401).json({ message: "Not authenticated" });
  }

  res.status(200).json(req.user);
};

module.exports.signup = async (req, res, next) => {
  try {
    let { username, email, password, location } = req.body;
    const newUser = new User({ email, username, location });
    const registeredUser = await User.register(newUser, password);
    req.login(registeredUser, (err) => {
      if (err) {
        return next(err);
      }
      return res.status(201).json(registeredUser);
    });
  } catch (e) {
    next(e);
  }
};

module.exports.login = async (req, res) => {
  res.status(200).json(req.user);
};

module.exports.logout = (req, res, next) => {
  req.logout((err) => {
    if (err) {
      return next(err);
    }
    res.status(200).json({ message: "Successfully logged out" });
  });
};