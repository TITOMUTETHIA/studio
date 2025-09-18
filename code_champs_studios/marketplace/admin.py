from django.contrib import admin
from .models import User, Model3D, Order

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username","email","is_creator","stripe_account_id")

@admin.register(Model3D)
class Model3DAdmin(admin.ModelAdmin):
    list_display = ("title","creator","price","approved","created_at")
    list_filter = ("approved","created_at","license_type")
    search_fields = ("title","creator__username")
    actions = ["approve_models"]

    def approve_models(self, request, queryset):
        queryset.update(approved=True)
    approve_models.short_description = "Approve selected models"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","buyer","model","amount_cents","fulfilled","created_at")
