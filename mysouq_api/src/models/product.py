from mongoengine import *
from datetime import datetime
from .cart import Cart



class Product(Document):
    name = StringField(max_length=200, required=True)
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow())
    carts = ListField(ReferenceField(Cart))
    price = FloatField()
    owner_id = StringField()
    is_favorite =BooleanField(default=False)
    
    # my_image =open('src/endpoints/123.jpg','rb')
    # Product.image_url.replace(my_image,filename='123.jpg')
    # image_url.save()

# class ArticleImage(EmbeddedDocument):
#     image = FileField()


# class Article(Document):
#     images = ListField(EmbeddedDocumentField(ArticleImage))


# art = Article()
# image_1 = ArticleImage()
# with open('al-ammed.jpg', 'rb') as image_file:
#     image_1.put(image_file, content_type='image/jpg')
#     art.images.append(image_1)
