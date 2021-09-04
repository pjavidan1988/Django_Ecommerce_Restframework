from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Avg, Count
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django_jalali.db import models as jmodels


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE,verbose_name='دسته والد')
    title = models.CharField(max_length=50, verbose_name='عنوان')
    keywords = models.CharField(max_length=255, verbose_name='کلید واژه')
    description = models.TextField(max_length=255, verbose_name='توضیحات')
    image = models.ImageField(blank=True, upload_to='images/Category/%Y/%m/%d', verbose_name='تصویر')
    status = models.CharField(max_length=10, choices=STATUS, verbose_name='وضعیت')
    slug = models.SlugField(null=False, unique=True, verbose_name='نامک')
    create_at = jmodels.jDateField(auto_now_add=True)
    update_at = jmodels.jDateField(auto_now=True, verbose_name='به روز شده در')

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return f'/{self.slug}/'

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته بندی')
    title = models.CharField(max_length=150, verbose_name='عنوان')
    keywords = models.CharField(max_length=255, verbose_name='کلید واژه ها')
    brand_name = models.CharField(max_length=255, verbose_name='نام برند')
    model_name = models.CharField(max_length=255, verbose_name='نام مدل')
    short_description = RichTextUploadingField(verbose_name='توضیحات کوتاه')
    description = RichTextUploadingField(verbose_name='توضیحات')
    image = models.ImageField(upload_to='images/Product/%Y/%m/%d/', null=False, verbose_name='تصویر')
    slider_image = models.ImageField(upload_to='images/Slider/%Y/%m/%d/', null=False, verbose_name='تصویر اسلایدر')
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='قیمت')
    amount = models.PositiveIntegerField(default=0, verbose_name='مقدار')
    minAmount = models.PositiveIntegerField(default=3, verbose_name='کمترین مقدار')
    detail = RichTextUploadingField(verbose_name='جزئیات')
    transportation = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='حمل و نقل')
    slug = models.SlugField(null=False, unique=True, verbose_name='نامک')
    status = models.CharField(max_length=10, choices=STATUS, verbose_name='وضعیت')
    create_at = jmodels.jDateField(auto_now_add=True)
    update_at = jmodels.jDateField(auto_now=True, verbose_name='به روز شده در')

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    image_tag.short_description = 'تصویر'

    def get_absolute_url(self):
        return f'/{self.slug}/'


    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    title = models.CharField(max_length=50, blank=True, verbose_name='عنوان')
    image = models.ImageField(blank=True, upload_to='images/Product/%Y/%m/%d/', verbose_name='تصویر')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'
