from django.contrib import admin
from .models import Todo


# To customize field 'date' - to view it in form
class TodoAdmin(admin.ModelAdmin):
  readonly_fields = ('date_created',)


admin.site.register(Todo, TodoAdmin)
