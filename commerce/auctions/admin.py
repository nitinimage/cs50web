from django.contrib import admin
from django.apps import apps

# Register your models here.

# class BookAdmin(admin.ModelAdmin):
#     list_display = ('name', 'author')
# # model registered with custom admin
# admin.site.register(Book, BookAdmin)


app = apps.get_app_config('auctions')

for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except:
        pass