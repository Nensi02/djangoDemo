from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Services

@receiver(post_save, sender=Services)
def service_post_save_handler(sender, instance, created, **kwargs):
    if created:
        print(f"A new book titled '{instance.name}' has been added to the library.")
    else:
        print(f"The book titled '{instance.name}' has been updated.")

@receiver(pre_delete, sender=Services)
def service_pre_delete_handler(sender, instance, **kwargs):
    print(f"A new book titled '{instance.name}' will delete from the storage.")

@receiver(post_delete, sender=Services)
def service_post_delete_handler(sender, instance, **kwargs):
    print(f"A new book titled '{instance.name}' deleted from the storage.")