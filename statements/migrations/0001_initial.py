import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('currency', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='statements.account')),
            ],
        ),
        migrations.CreateModel(
            name='StatementItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('currency', models.CharField(max_length=3)),
                ('title', models.CharField(max_length=100)),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statements.statement')),
            ],
        ),
    ]
