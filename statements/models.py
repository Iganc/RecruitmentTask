from django.db import models


def report_turnover_by_year_month(period_begin, period_end):
    # TODO: TASK → make report using 1 database query without any math in python
    # example output
    return {
        "2009-11": {
            {
                "incomes": {
                    "PLN": 120
                },
                "expenses": {
                    "PLN": 100
                }
            }
        }
    }


class Account(models.Model):
    name = models.CharField(max_length=100)
    currency = models.CharField(max_length=3)
    # TODO: TASK → add field balance that will update automatically 
     
    def __str__(self):
        return f'{self.name}[{self.currency}]'


class Statement(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    date = models.DateField()
    # TODO: TASK → make sure that account and date is unique on database level

    def __str__(self):
        return f'{self.account} → {self.date}'
    

class StatementItem(models.Model):
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=3)
    title = models.CharField(max_length=100)
    # TODO:  TASK → add field comments (type text)
    

    def __str__(self):
        return f'[{self.statement}] {self.amount} {self.currency} → {self.title}'
