from product.models import Category


def menu_context(request):
    return {'menu_categories': Category.objects.all()}
