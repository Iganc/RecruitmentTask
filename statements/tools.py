import csv

from django.core.exceptions import ValidationError
from statements.models import Account, Statement, StatementItem
from django.db import transaction

def statement_import(file_handler):
    idx = 0
    # TODO: TASK → in case of errors database must not change
    # TODO: TASK → optimize database queries during import
    accounts_cache = {a.name: a for a in Account.objects.all()}
    statements_cache = {} 
    statement_items_to_create = []
    with transaction.atomic():
        for row in csv.DictReader(file_handler):
            account_name = row['account']
            currency = row['currency']
            date = row['date']
            amount = row['amount']

            account = accounts_cache.get(account_name)
            if not account:
                account = Account(name=account_name, currency=currency)
                accounts_cache[account_name] = account
            if account.currency != row['currency']:
                raise ValidationError('Invalid currency currency ')

            key = (account_name, date)
            statement = statements_cache.get(key)
            if not statement:
                statement = Statement(account=account, date=date)
                statements_cache[key] = statement

            statement_items_to_create.append(
                StatementItem(statement=statement, amount=amount, currency=currency)
            )
            idx += 1

        Account.objects.bulk_create(
            [a for a in accounts_cache.values() if a.pk is None], batch_size=1000
        )
        Statement.objects.bulk_create(
            [s for s in statements_cache.values() if s.pk is None], batch_size=1000
        )
        StatementItem.objects.bulk_create(statement_items_to_create, batch_size=1000)

        return idx

