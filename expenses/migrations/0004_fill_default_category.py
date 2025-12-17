from django.db import migrations


def set_default_category(apps, schema_editor):
    Expense = apps.get_model('expenses', 'Expense')
    Expense.objects.filter(category__isnull=True).update(category='OTHER')


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0003_expense_created_at_expense_updated_at_and_more'),
    ]

    operations = [
        migrations.RunPython(set_default_category, reverse_code=migrations.RunPython.noop),
    ]
