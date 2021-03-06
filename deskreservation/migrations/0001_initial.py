# Generated by Django 3.1.1 on 2020-09-26 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('capacity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('employee_id', models.TextField()),
                ('area_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deskreservation.officearea')),
            ],
            options={
                'unique_together': {('date', 'employee_id')},
            },
        ),
    ]
