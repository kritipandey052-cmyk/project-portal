import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update the default admin user"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_ADMIN_USERNAME", "admin")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD", "Admin@12345")
        email = os.environ.get(
            "DJANGO_ADMIN_EMAIL",
            "admin@example.com"
        )

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Admin user "{username}" created successfully.'
                )
            )
        else:
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.set_password(password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Admin user "{username}" updated successfully.'
                )
            )