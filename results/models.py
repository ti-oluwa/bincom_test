from django.db import models



class AnnouncedStateResults(models.Model):
    """Model to represent announced state election results"""
    result_id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    state_name = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        db_table = 'announced_state_results'
        ordering = ['-date_entered']
        verbose_name = 'Announced state results'
        verbose_name_plural = 'Announced state results'

    def __str__(self) -> str:
        return f'Results announced in {self.state_name} state for {self.party_abbreviation}'



class AnnouncedLgaResults(models.Model):
    """Model to represent announced local government election results"""
    result_id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    lga_name = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        db_table = 'announced_lga_results'
        ordering = ['-date_entered']
        verbose_name = 'Announced LGA results'
        verbose_name_plural = 'Announced LGA results'

    def __str__(self) -> str:
        return f'Results announced in {self.lga_name} LGA for {self.party_abbreviation}'



class AnnouncedWardResults(models.Model):
    """Model to represent announced ward election results"""
    result_id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    ward_name = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        db_table = 'announced_ward_results'
        ordering = ['-date_entered']
        verbose_name = 'Announced ward results'
        verbose_name_plural = 'Announced ward results'

    def __str__(self) -> str:
        return f'Results announced in {self.ward_name} ward for {self.party_abbreviation}'



class AnnouncedPuResults(models.Model):
    """Model to represent announced polling unit election results"""
    result_id = models.BigAutoField(primary_key=True, unique=True, editable=False)
    polling_unit_uniqueid = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        db_table = 'announced_pu_results'
        ordering = ['-date_entered']
        verbose_name = 'Announced polling unit results'
        verbose_name_plural = 'Announced polling unit results'

    def __str__(self) -> str:
        return f'Results announced in polling unit {self.polling_unit_uniqueid} for {self.party_abbreviation}'

