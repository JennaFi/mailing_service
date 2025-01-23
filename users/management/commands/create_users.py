from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        User = get_user_model()

        try:
            group = Group.objects.get(name='Manager')
        except ObjectDoesNotExist:
            group = Group.objects.create(name='Manager')
            cancel_mailing_permission = Permission.objects.get(
                codename='can_cancel_mailing'
            )
            block_user_permission = Permission.objects.get(codename='can_block_user')
            group.permissions.add(cancel_mailing_permission, block_user_permission)
            group.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Group {group.name} successfully created and has permissions to: "{cancel_mailing_permission}",'
                    f' "{block_user_permission}"'
                )
            )

        try:
            user = User.objects.get(email='manager1@manager.org').delete()

        except ObjectDoesNotExist:
            pass

        user = User.objects.create(
            email='manager1@manager.org',
        )
        user.set_password('12345qwerty')
        user.groups.add(group)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Manager {user.email} created successfully. Group: {group.name}"
            )
        )
        try:
            user = User.objects.get(email='test1@test1.org').delete()

        except ObjectDoesNotExist:
            pass

        user = User.objects.create(
            email='test1@test1.org',
        )
        user.set_password('12345ty')
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"User {user.email} created successfully."
            )
        )

        try:
            user = User.objects.get(email='test2@test2.org').delete()

        except ObjectDoesNotExist:
            pass

        user = User.objects.create(
            email='test2@test2.org',
        )
        user.set_password('123456ty')
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"User {user.email} created successfully."
            )
        )
