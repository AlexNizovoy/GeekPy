from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core import mail
from django.conf import settings
from django.http import HttpResponse

import mimetypes
from datetime import datetime
import tempfile
import xlrd, xlwt, xlutils


def send_out_data(data, filename, email_addr=None, subject=None, msg=None):
    # Try send dump to email
    try:
        validate_email(email_addr)
    except ValidationError:
        # return data as filestream
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        response = HttpResponse(data, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        subject = subject or ''
        msg = msg or ''
        email = mail.EmailMessage(subject=subject, body=msg, from_email=settings.EMAIL_FROM, to=[email_addr])
        email.attach(filename, data, content_type)
        email.send()
        return True


def dump_item_to_xls(cls, exclude_fields=('id',), query=None):
    """
    Dump items from Django Model to xls file
    :param cls: Django Model Class
    :param exclude_fields: List of excluded fields (by default - 'id' field)
    :param query: Specific query for filter records
    :return: Raw data of xls-file. May be saved, sent in e-mail etc.
    """

    if exclude_fields is None:
        exclude_fields = []
    tmp = tempfile.NamedTemporaryFile()
    wb = xlwt.Workbook()

    # Get name of Model: "<class 'product.models.Currency'>" -->
    # ["<class 'product", 'models', "Currency'>"] --> "Currency'>" --> "Currency"
    sheet = wb.add_sheet(str(cls).split('.')[-1][:-2])
    # Insert Title row
    fields = [i.name for i in cls._meta.fields if i.name not in exclude_fields]
    row = 0
    for col, value in enumerate(fields):
        sheet.write(row, col, value.capitalize())

    row += 1
    records = cls.objects.filter(**query) if query else cls.objects.all()
    for row_idx, record in enumerate(records):
        values = [record.__getattribute__(attr) for attr in fields]
        for col_idx, val in enumerate(values):
            sheet.write(row + row_idx, col_idx, val)

    wb.save(tmp)
    tmp.seek(0)
    data = tmp.file.read()
    tmp.close()
    return data


def update_item_from_xls(cls, filename, key_field):
    """
    Update objects in Django-model from xls-file
    :param cls: Model
    :param filename: filename of xls-file
    :param key_field: key field for objects (for update_or_create)
    :return: tuple -> (count_of_created_items, count_of_updated_items)
    """

    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_index(0)
    keys = [val.lower() for val in sheet.row_values(0)]
    updated, created = 0, 0

    for row in range(1, sheet.nrows):
        item = dict(zip(keys, sheet.row_values(row)))
        query_field = {key_field.lower(): item.get(key_field.lower())}
        obj, status = cls.objects.update_or_create(**query_field, defaults=item)
        if status:
            created += 1
        else:
            updated += 1

    return created, updated
