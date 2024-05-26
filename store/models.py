from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save


from userauths.models import User, Profile
from vendor.models import Vendor
from shortuuid.django_fields import ShortUUIDField


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to="category", default="category.jpg", null=True, blank=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Category"
        ordering = ["title"]


class Product(models.Model):

    STATUS = (
        ("draft", "Draft"),
        ("disabled", "Disabled"),
        ("in_review", "In Review"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=100)
    image = models.FileField(upload_to="product", default="product.jpg", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(decimal_places=0, max_digits=20, default=0.00)
    old_price = models.DecimalField(decimal_places=0, max_digits=20, default=0.00)
    shipping_amount = models.DecimalField(decimal_places=0, max_digits=20, default=0.00)
    stock = models.PositiveIntegerField(default=1)
    in_stock = models.BooleanField(default=True)
    status = models.CharField(max_length=100, choices=STATUS, default="published")
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(default=0, null=True, blank=True)
    product_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrtuvwxyz")
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.name)
        
        super(Product, self).save(*args, **kwargs)

    def product_rating(self):
        product_rating = Review.objects.filter(product=self).aggregate(avg_rating=models.Avg("rating"))
        return product_rating['avg_rating']
    
    def save(self, *args, **kwargs):
        if self.rating:
            self.rating = self.product_rating()
        super(Product, self).save(*args, **kwargs)
    
    def rating_count(self):
        rating_count = Review.objects.filter(product=self).count()
        return rating_count
    
    def gallery(self):
        gallery = Gallery.objects.filter(gallery_product=self)
        return gallery
    
    def specification(self):
        specification = Specification.objects.filter(specification_product=self)
        return specification
    
    def size(self):
        size = Size.objects.filter(size_product=self)
        return size
    
    def color(self):
        color = Color.objects.filter(color_product=self)
        return color


class Gallery(models.Model):
    gallery_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField(upload_to="product", default="product.jpg")
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    gid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrtuvwxyz")

    def __str__(self):
        return self.gallery_product.title
    

class Specification(models.Model):
    specification_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return self.title
    
class Size(models.Model):
    size_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    price = models.DecimalField(decimal_places=0, max_digits=20, default=0.00)

    def __str__(self):
        return self.name
    

class Color(models.Model):
    color_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    color_code = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    cart_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    sub_total = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    shipping_amount = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    tax_fee = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    service_fee = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    total = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    country = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    cart_id = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cart_id} - {self.cart_product.title}"
    

class CartOrder(models.Model):

    PAYMENT_STATUS = (
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("cancelled", "Cancelled"),
    )

    ORDER_STATUS = (
        ("pending", "Pending"),
        ("fulfilled", "Fulfilled"),
        ("cancelled", "Cancelled"),
    )

    cart_order_vendor = models.ManyToManyField(Vendor, blank=True)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    sub_total = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    shipping_amount = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    tax_fee = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    service_fee = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    total = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS, default="pending")
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS, default="pending")
    initial_total = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    saved = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)

    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)

    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    oid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrtuvwxyz")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.oid
    

class CartOrderItem(models.Model):

    PAYMENT_STATUS = (
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("cancelled", "Cancelled"),
    )

    ORDER_STATUS = (
        ("pending", "Pending"),
        ("fulfilled", "Fulfilled"),
        ("cancelled", "Cancelled"),
    )

    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    item_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    item_product = models.ForeignKey(Product, on_delete=models.CASCADE)

    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    sub_total = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    shipping_amount = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    tax_fee = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    service_fee = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    total = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    country = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    initial_total = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)
    saved = models.DecimalField(default=0.00, max_digits=20, decimal_places=0)  

    oid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrtuvwxyz")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.oid
    

class ProductFaq(models.Model):
    user_faq = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product_faq = models.ForeignKey(Product, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    question = models.CharField(max_length=1000)
    answer = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "Product FAQs"

  
class Review(models.Model):

    RATING = (
        (1, "1 star"),
        (2, "2 star"),
        (3, "3 star"),
        (4, "4 star"),
        (5, "5 star"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    reply = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=None, choices=RATING)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title
    
    class Meta:
        verbose_name_plural = "Reviews and Ratings"

    def profile(self):
        return Profile.objects.get(user=self.user)
    

@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    if instance.product:
        instance.product.save()

class WhishList(models.Model):
    whishlist_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title
    

class Notification(models.Model):
    notification_user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(CartOrder, on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey(CartOrderItem, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.order:
            return self.order.oid
        else:
            return f"Notification: {self.pk}"
        

class Coupon(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    user_by = models.ManyToManyField(User, blank=True)
    code = models.CharField(max_length=1000)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
    

class Tax(models.Model):
    country  = models.CharField(max_length=100)
    rate = models.IntegerField(default=5, help_text="numbers added here are in percentage")
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.country
    
    class Meta:
        verbose_name_plural = "Taxes"
        ordering = ["country"]