# Generated by Django 5.0.4 on 2024-04-27 05:40

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models, connection


course_insert_trigger = "course/sql/insert_trigger.sql"
drop_trigger = "DROP FUNCTION IF EXISTS course_before_insert_update_trigger"


def create_trigger(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute(open(course_insert_trigger).read())


def remove_trigger(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute(drop_trigger)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "title",
                    models.CharField(
                        blank=True, db_index=True, max_length=255, null=True
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("duration", models.DurationField(blank=True, null=True)),
                (
                    "price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        default=Decimal("0.00"),
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "instructor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="instructed_course",
                        to="user.user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Course",
                "verbose_name_plural": "Courses",
                "db_table": "course",
            },
        ),
        migrations.RunPython(create_trigger, remove_trigger),
    ]