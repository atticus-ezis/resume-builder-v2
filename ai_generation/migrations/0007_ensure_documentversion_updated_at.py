# Migration to ensure updated_at exists (fixes DBs where 0005 was applied but column missing)

from django.db import migrations


def ensure_updated_at_column(apps, schema_editor):
    """Add updated_at only if missing; use SQL valid for current backend."""
    conn = schema_editor.connection
    with conn.cursor() as cursor:
        if conn.vendor == "sqlite":
            cursor.execute("PRAGMA table_info(ai_generation_documentversion)")
            columns = [row[1] for row in cursor.fetchall()]
            if "updated_at" in columns:
                return
            cursor.execute(
                "ALTER TABLE ai_generation_documentversion "
                "ADD COLUMN updated_at datetime NOT NULL DEFAULT current_timestamp"
            )
        else:
            # PostgreSQL
            cursor.execute(
                """
                ALTER TABLE ai_generation_documentversion
                ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                """
            )


class Migration(migrations.Migration):
    dependencies = [
        (
            "ai_generation",
            "0006_remove_documentversion_unique_version_document_per_document_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(ensure_updated_at_column, migrations.RunPython.noop),
    ]
