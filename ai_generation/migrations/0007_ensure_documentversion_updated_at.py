# Migration to ensure updated_at exists (fixes DBs where 0005 was applied but column missing)

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "ai_generation",
            "0006_remove_documentversion_unique_version_document_per_document_and_more",
        ),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE ai_generation_documentversion
            ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW();
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
