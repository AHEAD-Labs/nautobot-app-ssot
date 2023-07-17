# Generated by Django 3.2.16 on 2023-06-13 09:15

from django.contrib.contenttypes.models import ContentType
from django.db import migrations, models
from django.db.migrations.recorder import MigrationRecorder

import django.db.models.deletion
import uuid


_APP_LABEL = "nautobot_ssot"
_OLD_APP_LABEL = "nautobot_plugin_ssot_servicenow"
_MODEL_NAME = "SSOTServiceNowConfig"


def _move_data(apps, schema_editor):
    old_migration = {
        "app": _OLD_APP_LABEL,
        "name": "0001_initial",
    }
    if not MigrationRecorder.Migration.objects.filter(**old_migration).exists():
        return

    new_model_name = _MODEL_NAME.lower()
    new_model = apps.get_model(_APP_LABEL, new_model_name)
    new_table_name = new_model._meta.db_table
    old_table_name = new_table_name.replace(f"{_APP_LABEL}_", f"{_OLD_APP_LABEL}_")

    with schema_editor.connection.cursor() as cursor:
        # Table names are from trusted source (this script)
        cursor.execute(f"INSERT INTO {new_table_name} SELECT * FROM {old_table_name};")  # nosec

    # Update the content type to point to the new model
    old_content_type = ContentType.objects.get(app_label=_OLD_APP_LABEL, model=_MODEL_NAME.lower())
    old_content_type.app_label = _APP_LABEL
    old_content_type.model = new_model_name
    old_content_type.save()

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE {old_table_name} CASCADE;")


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0053_relationship_required_on"),
        ("nautobot_ssot", "0005_django_json_encoder"),
    ]

    operations = [
        migrations.CreateModel(
            name=_MODEL_NAME,
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("servicenow_instance", models.CharField(blank=True, max_length=100)),
                (
                    "servicenow_secrets",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="extras.secretsgroup"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RunPython(_move_data),
    ]
