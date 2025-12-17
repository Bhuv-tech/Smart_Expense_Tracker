from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0004_fill_default_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('FOOD', 'FOOD'), ('TRAVEL', 'TRAVEL'), ('RENT', 'RENT'), ('SHOPPING', 'SHOPPING'), ('BILLS', 'BILLS'), ('OTHER', 'OTHER')], max_length=20),
        ),
    ]
