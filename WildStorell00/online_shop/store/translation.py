from .models import Categoty, SubCategory, Product
from modeltranslation.translator import TranslationOptions,register

@register(Categoty)
class CategotyTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('sub_category_name',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'description')