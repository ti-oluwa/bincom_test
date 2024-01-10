from django.db import models


class States(models.Model):
    """Model to represent state electoral divisions"""
    state_id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    state_name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'states'
        ordering = ['state_name']
        verbose_name = 'States'
        verbose_name_plural = 'States'

    def __str__(self) -> str:
        return self.state_name



class LGA(models.Model):
    """Model to represent local government electoral divisions"""
    uniqueid = models.BigAutoField(primary_key=True, unique=True, editable=False)
    lga_id = models.CharField(max_length=50, unique=True)
    lga_name = models.CharField(max_length=50)
    state_id = models.CharField(max_length=50)
    lga_description = models.TextField(blank=True)
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        db_table = 'lga'
        ordering = ['lga_id']
        verbose_name = 'LGA'
        verbose_name_plural = 'LGAs'

    def __str__(self) -> str:
        return f"({self.lga_id}) {self.lga_name}"


class Ward(models.Model):
    """Model to represent ward electoral divisions"""
    uniqueid = models.BigAutoField(primary_key=True, unique=True, editable=False)
    ward_id = models.CharField(max_length=50, unique=True)
    ward_name = models.CharField(max_length=50)
    lga_id = models.CharField(max_length=50)
    ward_description = models.CharField(max_length=50, blank=True)
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        db_table = 'ward'
        ordering = ['ward_id']
        verbose_name = 'Ward'
        verbose_name_plural = 'Wards'

    def __str__(self) -> str:
        return f"({self.ward_id}) {self.ward_name}"



class PollingUnit(models.Model):
    """Model to represent polling units"""
    uniqueid = models.BigAutoField(primary_key=True, unique=True, editable=False)
    polling_unit_id = models.CharField(max_length=50, unique=True)
    ward_id = models.CharField(max_length=50)
    lga_id = models.CharField(max_length=50, blank=True)
    uniquewardid = models.CharField(max_length=50, null=True, default=None)
    polling_unit_number = models.CharField(max_length=50, null=True, default=None)
    polling_unit_name = models.CharField(max_length=50, null=True, default=None)
    polling_unit_description = models.TextField(blank=True)
    lat = models.CharField(max_length=255, null=True, default=None)
    long = models.CharField(max_length=255, null=True, default=None)
    entered_by_user = models.CharField(max_length=50, null=True, default=None)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=255, null=True, default=None)

    class Meta:
        db_table = 'polling_unit'
        ordering = ['polling_unit_id']
        verbose_name = 'Polling unit'
        verbose_name_plural = 'Polling units'

    def __str__(self) -> str:
        return f"({self.polling_unit_id}) {self.polling_unit_name}"


# Set settings.USE_TZ = False to avoid errors from DateTimeFields

