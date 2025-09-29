import csv

from django.core.exceptions import ValidationError
from statements.models import Account, Statement, StatementItem

def statement_import(file_handler):
    idx = 0
    # TODO: TASK → in case of errors database must not change
    # TODO: TASK → optimize database queries during import
    for row in csv.DictReader(file_handler):
        account = Account.objects.get_or_create(
            name=row['account'],
            defaults={'currency': row['currency']}
        )[0]
        if account.currency != row['currency']:
            raise ValidationError('Invalid currency currency ')

        statement = Statement.objects.get_or_create(
            account=account,
            date=row['date']
        )[0]
        StatementItem.objects.create(
            statement=statement,
            amount=row['amount'],
            currency=row['currency'],
        )
        idx += 1
    return idx

