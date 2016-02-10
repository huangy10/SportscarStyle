from django.dispatch import Signal

send_notification = Signal(providing_args=["message_type"])