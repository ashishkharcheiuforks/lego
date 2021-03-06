# Generated by Django 2.0 on 2017-12-10 20:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("tests", "0002_auto_20170903_2224")]

    operations = [
        migrations.AlterField(
            model_name="testmodel",
            name="created_by",
            field=models.ForeignKey(
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="testmodel_created",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="testmodel",
            name="updated_by",
            field=models.ForeignKey(
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="testmodel_updated",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
