from django.db import models

class Asset(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Decommissioned', 'Decommissioned'),
        ('Maintenance', 'Maintenance'),
    ]
    
    DMR_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Scanned', 'Scanned'),
        ('Failed', 'Failed'),
    ]

    asset_id = models.CharField(max_length=20, unique=True, editable=False, help_text="Auto-generated Asset ID (e.g., AST-0001)")
    serial_number = models.CharField(max_length=100)
    asset_tag = models.CharField(max_length=100, blank=True, null=True)
    model_id = models.CharField(max_length=100)
    model_category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    ci_name = models.CharField(max_length=100, blank=True, null=True, help_text="Configuration Item Name")
    ip_address = models.GenericIPAddressField(blank=True, null=True, protocol='both')

    mac_address = models.CharField(max_length=17, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    dmr_status = models.CharField(max_length=20, choices=DMR_STATUS_CHOICES, default='Pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset_id} - {self.ci_name or self.serial_number}"

    class Meta:
        ordering = ['-created_at']
