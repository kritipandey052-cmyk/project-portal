from django.db import models

class MaterialIssue(models.Model):
    date = models.DateField()
    person = models.CharField(max_length=200)
    material_category = models.CharField(max_length=200, blank=True)
    material_description = models.CharField(max_length=200)
    material_size = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    issued_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    site_name = models.CharField(max_length=200, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.person} - {self.material_description} ({self.material_size})"

class MaterialConsumption(models.Model):
    date = models.DateField()
    person = models.CharField(max_length=200)
    site_name = models.CharField(max_length=200, blank=True)
    material_description = models.CharField(max_length=200)
    material_size = models.CharField(max_length=100, blank=True)
    issued_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    installed_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    remaining_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.person} - {self.material_description} consumed"

class DPR(models.Model):
    date = models.DateField()
    person = models.CharField(max_length=200)
    rfc_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ng_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tf_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gi_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.person} DPR {self.date}"

class Expense(models.Model):
    date = models.DateField()
    person = models.CharField(max_length=200)
    category = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=300, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    site_name = models.CharField(max_length=200, blank=True)
    reference = models.CharField(max_length=200, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.person} expense {self.amount}"
