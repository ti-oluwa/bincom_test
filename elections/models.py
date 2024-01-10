from django.db import models



class Party(models.Model):
    """Model to represent political parties"""
    id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    partyid = models.CharField(max_length=50)
    partyname = models.CharField(max_length=50)

    class Meta:
        db_table = 'party'
        ordering = ['partyname']
        verbose_name = 'Party'
        verbose_name_plural = 'Parties'

    def __str__(self) -> str:
        return f"{self.partyname} ({self.partyid})"



class Agentname(models.Model):
    """Model to represent polling unit agents"""
    name_id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(null=True, default=None)
    phone = models.CharField(max_length=13)
    pollingunit_uniqueid = models.IntegerField()

    class Meta:
        db_table = 'agentname'
        ordering = ['firstname']
        verbose_name = 'Agent name'
        verbose_name_plural = 'Agent names'

    @property
    def fullname(self) -> str:
        return f'{self.firstname} {self.lastname}'
    

    def __str__(self) -> str:
        return self.fullname



