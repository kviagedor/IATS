from django.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Employee(models.Model):
    STATUS = [
        ('Active', 'Active'),
        ('Resigned', 'Resigned'),
        ('Supended', 'Suspended'),
        ('Terminated', 'Terminated'),
        ('Retired', 'Retired'),
    ]
    
    employee_id = models.CharField(max_length=100, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    reports_to = models.CharField(max_length=100, null=False, blank=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE )
    status = models.CharField(max_length=100, choices=STATUS)
    hire_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class ITAsset(models.Model):
    ASSET_TYPES = [
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
        ('Headset', 'Headset'),
        ('Printer', 'Printer'),
        ('Server', 'Server'),
        ('Networking', 'Networking'),
        ('Other', 'Other'),
    ]

    STATE = [
        ('In stock', 'In stock'),
        ('In transit', 'In transit'),
        ('In use', 'In use'),
        ('In maintenance', 'In maintenance'),
        ('Retired', 'Retired'),
        ('Missing', 'Missing'),
        ('Duplicate', 'Duplicate'),
    ]

    asset_tag = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=ASSET_TYPES)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(max_length=100, choices=STATE)
    deployed_date = models.DateField(null=True, blank=True)
    request_no = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.serial_number} {self.model} - {self.assigned_to}"