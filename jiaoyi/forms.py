from django import forms
# from users.models import UserProfile
from jiaoyi.models import Category, Tag, Image
import re


class AddProductForm(forms.Form):
    # ad_type = forms.CharField(label='买卖类型', max_length=50)
    title = forms.CharField(label='商品名称', max_length=50,widget=forms.TextInput(attrs={'class': "form-control"}))
    price = forms.DecimalField(label='商品价格', max_digits=8, decimal_places=2,widget=forms.TextInput(attrs={'class': "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control textarea"}))
    excerpt = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class': "form-control"}))
    category = forms.CharField(label='分类', max_length=50,widget=forms.TextInput(attrs={'class': "form-control"}))
    image = forms.ImageField()

    # tags = forms.CharField(label='标签', max_length=50)

    def clean_category(self):
        category = self.cleaned_data.get('category')
        filter_result = Category.objects.filter(name__exact=category)
        if len(filter_result) > 0:
            category = Category.objects.get(name=category)
            return category
        else:
            category = Category.objects.create(name=category)
        return category

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('请输入正确的价格')
        return price
