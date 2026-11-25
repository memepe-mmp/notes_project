from celery import shared_task
from .models import Note
from .services import notify_external_service


@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def notify_note_created(note_id):
    note = Note.objects.filter(pk=note_id).first()
    if note is None:
        return
    notify_external_service(note)