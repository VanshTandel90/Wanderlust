const mongoose=require("mongoose")
const Schema=mongoose.Schema
const passportLocalMongoose=require("passport-local-mongoose")

const userSchema=new Schema({
    email:{
        type:String,
        required:true
    },
    mobile: {
      type: String,
      required: true,
    },
    location: {
      type: String,
      required: true, 
    },
    buyers: [
      {
        listingId: { type: Schema.Types.ObjectId, ref: "Listing" },
        listingTitle: String,
        interestedUserId: { type: Schema.Types.ObjectId, ref: "User" },
        interestedUserName: String,
        interestedUserEmail: String,
        interestedUserLocation: String,
        interestedUserMobile: String,
      },
    ],
})

userSchema.plugin(passportLocalMongoose)

module.exports=mongoose.model("User",userSchema)