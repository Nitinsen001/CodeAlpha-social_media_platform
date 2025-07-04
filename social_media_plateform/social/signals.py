from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Follow, Like, Comment, Notification

@receiver(post_save, sender=Follow)
def notify_follow(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            to_user=instance.following,
            from_user=instance.follower,
            message=f"{instance.follower.username} followed you"
        )

@receiver(post_save, sender=Like)
def notify_like(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            to_user=instance.post.user,
            from_user=instance.user,
            message=f"{instance.user.username} liked your post"
        )

@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            to_user=instance.post.user,
            from_user=instance.user,
            message=f"{instance.user.username} commented on your post"
        )
