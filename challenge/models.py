from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

FULL_NAME = 'name'
EMAIL = 'email'
PHONE_NUMBER = 'phone_number'
TEXT = 'sentences'
ADDRESS = 'address'
DATE = 'date'
JOB = 'job'
COMPANY = 'company'
DOMAIN_NAME = 'domain_name'
INTEGER = 'random_int'

TYPE_CHOICES = (
    (FULL_NAME, "Full name!"),
    (JOB, "Job"),
    (EMAIL, "Email"),
    (DOMAIN_NAME, "Domain name"),
    (PHONE_NUMBER, "Phone number"),
    (COMPANY, "Company name"),
    (TEXT, "Text!"),
    (INTEGER, "Integer!"),
    (ADDRESS, "Address"),
    (DATE, "Date"),
)

TYPE_DEFAULT_ARGS = {
    INTEGER: {'min': 1, 'max': 60},
    TEXT: {'nb': 3},
    DATE: {'pattern': "%d-%m-%Y"},
}


class DataSchema(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_modified = models.DateField(auto_now_add=True)


class SchemaField(models.Model):
    data_schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE, related_name='fields')
    column_name = models.CharField(max_length=128)
    type = models.CharField(choices=TYPE_CHOICES, max_length=128)
    order = models.PositiveIntegerField()


class DataSet(models.Model):
    data_schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE)
    csv_file = models.FileField(null=True, blank=True)
    count = models.PositiveIntegerField()
    date_created = models.DateField(auto_now_add=True)
