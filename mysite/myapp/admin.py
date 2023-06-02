from django.contrib import admin

from .models import Product



# переименовать header в админ панели
admin.site.site_header = 'My Django APP'
# переименовать title в админ панели
admin.site.site_title = 'Title of Django'
# переименовать index_title в админ панели
admin.site.index_title = 'My admin'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    # поля которые можно изменять без перехода в объект
    list_editable = ('price', 'description')
    # строка поиска по полю name
    search_fields = ('name',)
    # изменения actions
    actions = ('make_zero',)

    def make_zero(self, request, queryset):
        queryset.update(price=0)



admin.site.register(Product, ProductAdmin)
