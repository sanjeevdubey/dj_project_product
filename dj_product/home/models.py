from django.db import models, connection
from django.contrib.auth.models import User
import uuid
from django.db import connection
from django.db.models import Sum




# Create your models here.


class BaseModel(models.Model):
    uid        = models.UUIDField(default=uuid.uuid4,editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract =True

class ProductCategory(BaseModel):
    category_name =  models.CharField(max_length=100)
    
    def __str__(self):
        return '%s' % (self.category_name)       

class Product(BaseModel):
    category     = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,related_name="products")
    product_name = models.CharField(max_length=100)
    price        = models.IntegerField(default=100)
    image        = models.ImageField(upload_to="product")

    def __str__(self):
        return '%s' % (self.category) 

class Cart(BaseModel):
    user    = models.ForeignKey(User, null=True,blank=True ,on_delete=models.SET_NULL, related_name="carts")
    is_paid = models.BooleanField(default=False)
    payment_ref_id =  models.CharField(max_length=1000, default=0)

    def get_cart_total(self):
       # return "hello"
       querysetss = CartItems.objects.filter(cart = self).aggregate(Sum('product__price'))['product__price__sum']
       # print(querysetss.query)
       #print(querysetss)
       return querysetss


       #return CartItems.objects.filter(cart = self).aggregate(sum('price'))['product__price__sum']

class CartItems(BaseModel):
    cart    = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    


