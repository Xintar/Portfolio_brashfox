"""
Message Service - Business logic for contact messages
"""
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction

from brashfox_app.models import Message
from brashfox_app.api.utils.validators import validate_message_length


class MessageService:
    """
    Handles contact form message business logic:
    - Message validation
    - Email notifications
    - Spam prevention
    """
    
    @staticmethod
    def create_message(validated_data):
        """
        Create a contact message and optionally send notification.
        
        Args:
            validated_data: Dictionary with message data (name, email, subject, message)
            
        Returns:
            Message instance
        """
        # Validate using centralized validator
        validate_message_length(validated_data['message'])
        
        with transaction.atomic():
            message = Message.objects.create(**validated_data)
            
            # Send email notification to admin (if configured)
            MessageService.send_admin_notification(message)
        
        return message
    
    @staticmethod
    def send_admin_notification(message):
        """
        Send email notification to admin about new contact message.
        
        Args:
            message: Message instance
        """
        if not hasattr(settings, 'ADMINS') or not settings.ADMINS:
            return
        
        try:
            admin_emails = [email for name, email in settings.ADMINS]
            
            send_mail(
                subject=f'New Contact Message: {message.subject}',
                message=f"""
New contact form submission:

From: {message.name} <{message.email}>
Subject: {message.subject}

Message:
{message.message}

---
Sent: {message.created}
                """.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=admin_emails,
                fail_silently=True,
            )
        except Exception:
            # Don't fail message creation if email fails
            pass
    
    @staticmethod
    def mark_as_read(message):
        """
        Mark a message as read (if we add that field in the future).
        
        Args:
            message: Message instance
            
        Returns:
            Updated message
        """
        # Placeholder for future functionality
        return message
