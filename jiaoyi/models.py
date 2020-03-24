from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    # ad_type = (
    #     ('buy', "买"),
    #     ('sale', "卖"),
    # )
    title = models.CharField(verbose_name='标题',max_length=70, blank=True)
    price = models.DecimalField(verbose_name='价格', max_digits=8, decimal_places=2, blank=True)
    description = models.TextField(verbose_name='描述',blank=True)
    created_time = models.DateTimeField(verbose_name='创建时间',default=timezone.now)
    modified_time = models.DateTimeField(verbose_name='修改时间')
    excerpt = models.CharField(verbose_name='摘要',max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE, blank=True)
    # tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0, editable=False)

    def get_absolute_url(self):
        return reverse('jiaoyi:pro_detail', args=[str(self.id)])

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title


class Image(models.Model):
    imgpath = models.ImageField("图片", upload_to="mypictures", blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # def get_absolute_url(self):
    #     return reverse('jiaoyi:pic_detail', args=[str(self.id)])
