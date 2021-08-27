import io
from django.core.files.base import ContentFile
from faker import Faker
import csv
from celery_tasks.celery import app
from challenge.models import DataSet, TYPE_DEFAULT_ARGS


@app.task
def task_generate_file(ds_id):

    data_set = DataSet.objects.get(id=ds_id)
    fields = data_set.data_schema.fields.all().order_by('order').values('column_name', 'type')
    fake = Faker('en_US')
    writer_file = io.StringIO()
    writer = csv.DictWriter(writer_file, fieldnames=[field['column_name'] for field in fields])
    writer.writeheader()
    for i in range(data_set.count):
        row = {
            field['column_name']: getattr(fake, field['type'])(
                **TYPE_DEFAULT_ARGS.get(field['type'], {})
            ) for field in fields
        }

        writer.writerow(row)

    csv_file = ContentFile(writer_file.getvalue().encode('utf-8'))
    data_set.csv_file.save(f'{data_set.data_schema.name}.csv', csv_file)
