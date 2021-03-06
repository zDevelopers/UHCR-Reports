# Generated by Django 2.2.4 on 2019-08-31 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("hawk_gui", "0003_minecraft_version_is_nullable")]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="generator_link",
            field=models.URLField(
                blank=True, editable=False, null=True, verbose_name="Generator link"
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="generator_name",
            field=models.CharField(
                blank=True,
                db_index=True,
                editable=False,
                max_length=128,
                null=True,
                verbose_name="Generator",
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="minecraft_version",
            field=models.CharField(
                blank=True,
                db_index=True,
                editable=False,
                max_length=64,
                null=True,
                verbose_name="Minecraft version",
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="published_by",
            field=models.GenericIPAddressField(
                blank=True, editable=False, null=True, verbose_name="Published by"
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="uuid",
            field=models.UUIDField(editable=False, verbose_name="UUID"),
        ),
        migrations.AlterField(
            model_name="report",
            name="views_count",
            field=models.IntegerField(
                default=0, editable=False, verbose_name="Views count"
            ),
        ),
    ]
