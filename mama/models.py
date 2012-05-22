from datetime import datetime, timedelta

from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.signals import class_prepared, pre_save
from django.dispatch import receiver
from preferences.models import Preferences
from userprofile.models import AbstractProfileBase
from mama.forms import RegistrationForm


class Link(models.Model):
    title = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        help_text="A short descriptive title. Leave blank to use target's title.",
    )
    source = models.ForeignKey(
        'jmbo.ModelBase',
        related_name="link_target_set"
    )
    target = models.ForeignKey(
        'jmbo.ModelBase',
        related_name="link_source_set"
    )

    def __unicode__(self):
        return self.title

class NavigationLink(models.Model):
    title = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        help_text="A short descriptive title. Leave blank to use target's title.",
    )
    source = models.ForeignKey(
        'jmbo.ModelBase',
        related_name="navigation_link_target_set"
    )
    target = models.ForeignKey(
        'jmbo.ModelBase',
        related_name="navigation_link_source_set"
    )

    def __unicode__(self):
        return self.title


class SitePreferences(Preferences):
    __module__ = 'preferences.models'
    pregnancy_helpline_number = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )
    baby_helpline_number = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )
    hivaids_helpline_number = models.CharField(
        "HIV/Aids helpline number",
        max_length=64,
        blank=True,
        null=True
    )
    about = RichTextField(
        blank=True,
        null=True
    )
    terms = RichTextField(
        blank=True,
        null=True
    )
    contact_email_recipients = models.ManyToManyField(
        'auth.User',
        blank=True,
        null=True,
        help_text='Select users who will recieve emails sent via the contact form.'
    )

    class Meta:
        verbose_name_plural = "Site preferences"


class UserProfile(AbstractProfileBase):
    registration_form = RegistrationForm
    mobile_number = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )
    weeks_pregnant_signup = models.IntegerField(
        choices=((i, 'Week%s %s' % ('s' if i > 1 else '', i)) for i in range(1,43)),
        blank=True,
        null=True,

    )
    computed_delivery_date = models.DateField(
        blank=True,
        null=True,
    )
    last_reset_date = models.DateField(
        blank=True,
        null=True,
        help_text='Last date on which user tried to reset her password.',
    )
    reset_count = models.IntegerField(
        blank=True,
        null=True,
        help_text='Number of times user has tried to reset her password on the last reset date.',
    )


@receiver(class_prepared)
def add_field(sender, **kwargs):
    """
    Monkey patch color field to Category model.
    """
    if sender.__name__ == 'Category':
        color_field = models.CharField(
            choices=(
                ("yorange", "Light Orange"),
                ("dorange", "Dark Orange"),
                ("maroon", "Maroon"),
                ("purple", "Purple"),
            ),
            max_length=64,
            blank=True,
            null=True,
            default='yorange',
            help_text="Color categorized content is styled with."
        )
        color_field.contribute_to_class(sender, "color")


@receiver(pre_save, sender=UserProfile)
def compute_delivery_date(sender, instance, **kwargs):
    if instance.weeks_pregnant_signup:
        weeks_left = 42 - int(instance.weeks_pregnant_signup)
        instance.computed_delivery_date = datetime.now() + timedelta(days=7 * weeks_left)
