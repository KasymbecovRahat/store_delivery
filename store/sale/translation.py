from .models import *
from modeltranslation.translator import TranslationOptions,register


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'product_description', )


@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('store_name', 'store_description')


@register(Rating)
class RatingTranslationOptions(TranslationOptions):
    fields = ('author', 'comment')