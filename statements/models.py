from django.db import models
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Case, When, F, FloatField

def report_turnover_by_year_month(period_begin, period_end):
    # TODO: TASK → make report using 1 database query without any math in python
    items = (
        StatementItem.objects
        .filter(statement__date__gte=period_begin, statement__date__lte=period_end)
        .annotate(month=TruncMonth('statement__date'))
        .values('month', 'currency')
        .annotate(
            incomes=Sum(Case(
                When(amount__gt=0, then=F('amount')),
                default=0,
                output_field=FloatField()
            )),
            expenses=Sum(Case(
                When(amount__lt=0, then=-F('amount')),
                default=0,
                output_field=FloatField()
            )),
        )
        .order_by('month')
    )
    MainDict = {}
    for item in items:
        date = f"{item['month'].year}-{item['month'].month:02d}"
        currency=str(item['currency'])
        incomes=item['incomes']
        expenses=item['expenses']
        if date not in MainDict:
            MainDict[date] = {"incomes": {}, "expenses": {}}
        MainDict[date]["incomes"][currency] = incomes
        MainDict[date]["expenses"][currency] = expenses

    return MainDict


class Account(models.Model):
    name = models.CharField(max_length=100)
    currency = models.CharField(max_length=3)
    # TODO: TASK → add field balance that will update automatically 
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    def __str__(self):
        return f'{self.name}[{self.currency}]'


class Statement(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    date = models.DateField()
    # TODO: TASK → make sure that account and date is unique on database level
    class Meta:
        unique_together = ('account', 'date')
    def __str__(self):
        return f'{self.account} → {self.date}'
    

class StatementItem(models.Model):
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=3)
    title = models.CharField(max_length=100)
    # TODO:  TASK → add field comments (type text)
    comments = models.TextField(default="")

    def __str__(self):
        return f'[{self.statement}] {self.amount} {self.currency} → {self.title}'

@receiver(post_save, sender=StatementItem)
@receiver(post_delete, sender=StatementItem)
def update_account_balance(sender, instance, **kwargs):
    account = instance.statement.account
    total = StatementItem.objects.filter(statement__account=account).aggregate(
        balance=Sum('amount')
    )['balance'] or 0
    account.balance = total
    account.save(update_fields=['balance'])