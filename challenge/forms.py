from django import forms
from challenge.models import SchemaField, DataSchema
from django.forms.models import inlineformset_factory


class SchemaFieldForm(forms.ModelForm):

    class Meta:
        model = SchemaField
        exclude = ()


SchemaFieldFormSet = inlineformset_factory(DataSchema, SchemaField, form=SchemaFieldForm, extra=1)
