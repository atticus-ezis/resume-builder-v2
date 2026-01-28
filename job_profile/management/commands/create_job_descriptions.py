from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create job descriptions"

    def add_arguments(self, parser):
        parser.add_argument(
            "count", type=int, help="Number of job descriptions to create"
        )
        parser.add_argument(
            "user_id", type=int, help="User ID to create job descriptions for"
        )

    def handle(self, *args, **options):
        # Import here to avoid issues during command discovery
        from job_profile.tests.factories import JobDescriptionFactory

        User = get_user_model()
        count = options.get("count", 10)
        user = User.objects.get(id=options.get("user_id"))

        for _ in range(count):
            JobDescriptionFactory(user=user)

        self.stdout.write(self.style.SUCCESS(f"Created {count} job descriptions"))
