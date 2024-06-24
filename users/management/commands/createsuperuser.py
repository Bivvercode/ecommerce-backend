import getpass
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Update a superuser with first name and last name.'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str,
                            help='The username of the superuser.', default='')
        parser.add_argument('--email', type=str,
                            help='The email of the superuser.', default='')
        parser.add_argument('--password', type=str,
                            help='The password of the superuser.', default='')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if not username:
            username = input("Username: ").strip()
        if not email:
            email = input("Email: ").strip()
        if not password:
            while True:
                password = getpass.getpass("Password: ").strip()
                password_confirmation = getpass.getpass(
                    "Confirm Password: "
                ).strip()
                if password == password_confirmation:
                    break
                self.stdout.write(self.style.ERROR(
                    "Passwords do not match. Please try again."
                ))

        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()

        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            self.stdout.write(self.style.SUCCESS(
                f"Superuser '{username}' was successfully created."
            ))
        except Exception as exc:
            raise CommandError(
                f"An error occurred while creating "
                f"superuser '{username}': {exc}"
            ) from exc
