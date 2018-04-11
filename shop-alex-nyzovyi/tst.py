import tempfile
import xlrd, xlwt, xlutils
from product.models import Currency as cls

#
# exclude_fields=('id',)
# wb = xlwt.Workbook()
# # Get name of Model: "<class 'product.models.Currency'>" -->
# # ["<class 'product", 'models', "Currency'>"] --> "Currency'>" --> "Currency"
# sheet = wb.add_sheet(str(cls).split('.')[-1][:-2])
# # Insert Title row
# fields = [i.name for i in cls._meta.fields if i.name not in exclude_fields]
# row = 0
# for col, value in enumerate(fields):
#     sheet.write(row, col, value.capitalize())
#
# row += 1
# for row_idx, currency in enumerate(cls.objects.all()):
#     values = [currency.__getattribute__(attr) for attr in fields]
#     for col_idx, val in enumerate(values):
#         sheet.write(row + row_idx, col_idx, val)
#
#
# wb.save('1.xls')

key_field = 'code'
wb = xlrd.open_workbook('1.xls')
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
