from django.db import models


class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    name = models.CharField(max_length=100, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return f'{self.name}, {self.price}, {self.image}, {self.release_date}, {self.lte_exists}, {self.slug}'

