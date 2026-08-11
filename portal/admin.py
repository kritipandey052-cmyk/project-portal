from django.contrib import admin
from .models import MaterialIssue, MaterialConsumption, DPR, Expense

@admin.register(MaterialIssue)
class MaterialIssueAdmin(admin.ModelAdmin):
    list_display = ('date', 'person', 'material_description', 'material_size', 'issued_quantity', 'site_name')
    search_fields = ('person', 'material_description', 'site_name')

@admin.register(MaterialConsumption)
class MaterialConsumptionAdmin(admin.ModelAdmin):
    list_display = ('date', 'person', 'material_description', 'material_size', 'issued_quantity', 'installed_quantity', 'remaining_quantity')
    search_fields = ('person', 'material_description', 'site_name')

@admin.register(DPR)
class DPRAdmin(admin.ModelAdmin):
    list_display = ('date', 'person', 'rfc_quantity', 'ng_quantity', 'tf_quantity', 'gi_quantity')
    search_fields = ('person',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'person', 'category', 'amount', 'site_name')
    search_fields = ('person', 'category', 'site_name')
