const mongoose=require("mongoose")
const Schema=mongoose.Schema
const passportLocalMongoose=require("passport-local-mongoose")

// username , hashing salting of password passport passport-local-mongoose j define kari dei ...

const userSchema=new Schema({
    email:{
        type:String,
        required:true
    },
})

userSchema.plugin(passportLocalMongoose)

module.exports=mongoose.model("User",userSchema)