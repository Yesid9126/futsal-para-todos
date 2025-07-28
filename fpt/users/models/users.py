# Django
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Models
from fpt.utils.models import FptBaseModel


class User(FptBaseModel, AbstractUser):
    """User model.

    Extend from Django abstract user, change the username field to email
    and add some extra info
    """

    email = models.EmailField(
        "email address",
        unique=True,
        error_messages={
            "unique": "A user with that email already exist",
        },
    )
    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="phone number must be entered in the format +99999999999",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, unique=True
    )

    photo = models.ImageField(
        "profile picture",
        upload_to="users/photos/",
        blank=True,
        null=True,
    )
    birthdate = models.DateField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    is_client = models.BooleanField(
        "client",
        default=True,
    )
    is_verified = models.BooleanField(
        "verified",
        default=False,
        help_text="set to true when address email have verified",
    )
    discount_used = models.BooleanField(
        "Ya uso el descuento de registro?",
        default=False,
    )


class FutsalModel(models.Model):
    """Training base model.
    TrainingModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """

    created = models.DateTimeField(
        "created at",
        auto_now_add=True,
        help_text="Date time on which the object was created.",
    )
    modified = models.DateTimeField(
        "modified at",
        auto_now=True,
        help_text="Date time on which the object was last modified.",
    )

    class Meta:
        """Meta option."""

        abstract = True
        get_latest_by = "created"
        ordering = ["-created", "-modified"]


class UserAddress(FptBaseModel):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_address",
    )
    country = models.ForeignKey(
        "orders.Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_addresses",
    )
    department = models.ForeignKey(
        "orders.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_addresses",
    )
    address = models.CharField(max_length=500, blank=True, null=True)
    neighborhood = models.CharField(max_length=500, blank=True, null=True)
    additional_information = models.CharField(max_length=500, blank=True, null=True)
    secondary_contact = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"User address {self.address}"


class CodePromotion(FptBaseModel):
    """code promotion"""

    name = models.CharField(max_length=100)
    date_init = models.DateField()
    date_end = models.DateField()

    def __str__(self):
        return f"Code promotion {self.name}"

    class Meta:
        """Meta option."""

        verbose_name = "Código promocional"
        verbose_name_plural = "Codigos promocionales"


class UserPromotionCode(FptBaseModel):
    """User promotion code"""

    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="user_code"
    )
    promotion_code = models.ForeignKey(
        CodePromotion, on_delete=models.CASCADE, related_name="user_code"
    )
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"User code for {self.user.first_name} - code {self.promotion_code.name}"

    class Meta:
        """Meta option."""

        verbose_name = "Código de usuario"
        verbose_name_plural = "Codigos de usuario"
