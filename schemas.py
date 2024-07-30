from marshmallow import Schema, fields

class PlainUserschema(Schema):

    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    user_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    desc = fields.Str()
    city = fields.Str()
    gender = fields.Str()
    phone_number = fields.Str()
    status  = fields.Int(dump_only=True)
    country = fields.Str(dump_only=True)
    region = fields.Str(dump_only=True)
    profile_pic = fields.Str(dump_only=True)
    
class PlainReviewSchema(Schema):

    id = fields.Int(dump_only=True)
    brandname = fields.Str(required=True)
    product = fields.Str(required=True)
    review = fields.Str(required=True)
    type = fields.Str(required=True)
    file = fields.Raw(type='file')
    rating = fields.Int()
    tag_users = fields.List(fields.Integer())

class PlainFileSchema(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.Str()

class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    category_name = fields.Str(required=True)

class ReviewSchema(PlainReviewSchema):
     user_id = fields.Int(load_only=True)
     status = fields.Str(required=True)
     message = fields.Str(required=True) 
     user = fields.Nested(PlainUserschema(), dump_only = True)
     category = fields.Nested(PlainCategorySchema(), dump_only = True)
     likes = fields.List(fields.Nested(PlainUserschema()), dump_only = True)
     files = fields.List(fields.Nested(PlainFileSchema()), dump_only = True)
     tag_user = fields.List(fields.Nested(PlainUserschema()), dump_only = True)

class Userschema(PlainUserschema):
    reviews = fields.List(fields.Nested(PlainReviewSchema()), dump_only=True)
    #followers = fields.List(fields.Nested(PlainUserschema()), dump_only=True)
    like = fields.List(fields.Nested(PlainReviewSchema()), dump_only=True)
    taged = fields.List(fields.Nested(PlainReviewSchema()), dump_only=True)

class FileSchema(PlainFileSchema):
    review_id = fields.Int(load_only=True)
    review = fields.Nested(ReviewSchema(), dump_only = True)

# class CategorySchema(PlainCategorySchema):
#     pass
    #review_id = fields.Int(dump_only=True)
    #review = fields.Nested(ReviewSchema(), dump_only = True)


class UserUpdateSchema(Schema):

    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    user_name = fields.Str(required=True)
    #email = fields.Email(required=True)
    #password = fields.Str(required=True, load_only=True)
    desc = fields.Str()
    city = fields.Str()
    gender = fields.Str()
    phone_number = fields.Str()
    profile_pic = fields.Raw(type='file')
    
class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    id = fields.Int(dump_only = True)
    access_token = fields.Str(dump_only=True)
    refresh_token = fields.Str(dump_only=True)

class FilterSchema(Schema):
    search = fields.Str(required=True)
    category = fields.Int()
    brandname = fields.Str()
    type = fields.Str()
    

class UserFilterSchema(Schema):
    search = fields.Str(required=True)

class FileformSchema(Schema):
    #file = fields.Raw(type='file')
    name = fields.Str()
    title = fields.Str()


class SupporterSchema(Schema):
     user_id = fields.Int(required=True)
     suppoter_id = fields.Int(required=True)


class LikeAndReviewSchema(Schema):
     message = fields.Str()
     user = fields.Nested(Userschema)
     review = fields.Nested(ReviewSchema)

class ReviewLikeSchema(Schema):
     user_id = fields.Int(required=True)
     review_id = fields.Int(required=True)

class NotificationSchema(Schema):
    user_id = fields.Int(required=True)
    title = fields.Str(required=True)
    notification = fields.Str(required=True)
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class MessageSchema(Schema):
    to_user = fields.Int(required=True)
    from_user = fields.Int(required=True)
    message= fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)


class ChangePasswordSchema(Schema):
    user_id = fields.Int(required=True)
    password = fields.Str(required=True, load_only=True)
    new_password = fields.Str(required=True, load_only=True)
    id = fields.Int(dump_only = True)

class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True)
    new_password = fields.Str()
    otp = fields.Str()

class AppVersionSchema(Schema):
    id = fields.Int(required=True)
    version = fields.Str()
    status = fields.Str(required=True)
    name= fields.Str()



