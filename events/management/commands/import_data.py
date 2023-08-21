import csv
from django.core.management.base import BaseCommand
from accounts.models import Account, Contact
from sales.models import Salesperson
from events.models import Event


class Command(BaseCommand):
    help = 'Import data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('csv1_path', help='Path to CSV 1 file (Contacts)')
        parser.add_argument('csv2_path', help='Path to CSV 2 file (Accounts)')

    def handle(self, *args, **options):
        csv1_path = options['csv1_path']
        csv2_path = options['csv2_path']

        # Process and import CSV 2 (Accounts)
        with open(csv2_path, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                # Try to retrieve the existing Salesperson or create a new one
                try:
                    bdr_instance = Salesperson.objects.get(name=row['BDR LDAP'])
                except Salesperson.DoesNotExist:
                    bdr_instance = Salesperson.objects.create(name=row['BDR LDAP'])

                # Check if Account with Account_ID already exists
                try:
                    account_instance = Account.objects.get(account_id=row['ID'])
                    account_instance.bdr = bdr_instance
                    account_instance.country = row['Country']
                    account_instance.industry = row['Industry']
                    account_instance.save()
                except Account.DoesNotExist:
                    # Create Account instance if it doesn't exist
                    Account.objects.create(
                        account_id=row['ID'],
                        bdr=bdr_instance,
                        country=row['Country'],
                        industry=row['Industry'],
                    )

        # Process and import CSV 1 (Contacts)
        with open(csv1_path, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                # Retrieve or create related objects like Account
                account_instance, _ = Account.objects.get_or_create(account_id=row['Account_ID'])

                # Create Contact instance
                contact_instance, created = Contact.objects.get_or_create(
                    contact_id=row['Contact_ID'],
                    account=account_instance,
                    name=row['Name'],
                    seniority=row['Seniority'],
                    job_function=row['Job Function'],
                    email=row['Email'],
                    # ... other fields
                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
