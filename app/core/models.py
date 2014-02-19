from random import randint

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

# from protecton_score import make_user_score_metrics


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """Create and save a new user"""
        if not phone_number:
            raise ValueError("User must have a phone_number")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password):
        """Create and save a new superuser"""
        user = self.create_user(phone_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that support using phone number instead of username"""

    EDUCATION_CHOICES = [
        ("Associate degree", "Associate degree"),
        ("Bachelor's degree", "Bachelor's degree"),
        ("Master's degree", "Master's degree"),
        ("Doctoral degree", "Doctoral degree"),
    ]
    EMPLOYMENT_CHOICES = [
        ("Employed", "Employed"),
        ("Unemployed", "Unemployed"),
        ("Contractor", "Contractor"),
        ("Student", "Student"),
    ]
    COVERAGE_CHOICES = [("Yes", "Yes"), ("No", "No"), ("Don't know", "Don't know")]
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. \
            Up to 15 digits allowed.",
    )

    # PERSONAL INFO
    phone_number = models.CharField(_("phone number"), max_length=17, unique=True)
    email = models.EmailField(_("email address"), blank=True)
    name = models.CharField(max_length=255)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    age = models.PositiveSmallIntegerField(
        _("age"),
        validators=[MinValueValidator(18), MaxValueValidator(150)],
        blank=True,
        null=True,
    )
    zipcode = models.CharField(
        _("zipcode"), max_length=5, validators=[MinLengthValidator(5)], blank=True
    )
    income = models.DecimalField(
        _("income"), max_digits=10, decimal_places=2, blank=True, null=True
    )
    savings = models.DecimalField(
        _("savings"), max_digits=10, decimal_places=2, blank=True, null=True
    )
    debt = models.DecimalField(
        _("debt"), max_digits=10, decimal_places=2, blank=True, null=True
    )
    education = models.CharField(
        _("education"), max_length=50, choices=EDUCATION_CHOICES, blank=True
    )
    employment = models.CharField(
        _("employment"), max_length=50, choices=EMPLOYMENT_CHOICES, blank=True
    )

    # SCORES
    score = models.ForeignKey("Score", on_delete=models.CASCADE, blank=True, null=True)

    # STUFF
    own_vehicle = models.BooleanField(default=False)
    own_pet = models.BooleanField(default=False)
    own_rent_house = models.BooleanField(default=False)

    # COVERAGES
    have_health_cover = models.CharField(
        _("health"), max_length=50, choices=COVERAGE_CHOICES, blank=True
    )
    have_vision_cover = models.CharField(
        _("vision"), max_length=50, choices=COVERAGE_CHOICES, blank=True
    )
    have_dental_cover = models.CharField(
        _("dental"), max_length=50, choices=COVERAGE_CHOICES, blank=True
    )
    have_life_cover = models.CharField(
        _("life"), max_length=50, choices=COVERAGE_CHOICES, blank=True
    )
    have_longtermdisability_cover = models.CharField(
        _("long term disability"), max_length=50, choices=COVERAGE_CHOICES, blank=True
    )
    have_shorttermdisability_cover = models.CharField(
        _("short term disability"), max_length=50, choices=COVERAGE_CHOICES, blank=True
    )
    have_accident_cover = models.CharField(
        _("accident"), max_length=50, choices=COVERAGE_CHOICES, blank=True
    )
    have_criticalillness_cover = models.CharField(
        _("critical illness"), max_length=50, choices=COVERAGE_CHOICES, blank=True
    )
    have_auto_cover = models.CharField(
        _("auto"), max_length=50, choices=COVERAGE_CHOICES, blank=True
    )
    have_homeowner_cover = models.CharField(
        _("homeowner"), max_length=50, choices=COVERAGE_CHOICES, blank=True
    )
    have_renters_cover = models.CharField(
        _("renters"), max_length=50, choices=COVERAGE_CHOICES, blank=True
    )
    have_pet_cover = models.CharField(
        _("pet"), max_length=50, choices=COVERAGE_CHOICES, blank=True
    )

    date_joined = models.DateTimeField(_("registered"), auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        """Returns the firstname plus the last_name, and a space in between."""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def calculate_score(self):
        """Initializes dummy score object for now."""

        # TODO: Call make_user_score_metrics(user, products) to get score metrics

        overall_score = randint(0, 100)
        return Score(
            score_overall=overall_score,
            score_medical=randint(0, 100),
            score_income=randint(0, 100),
            score_stuff=randint(0, 100),
            score_liability=randint(0, 100),
            score_digital=randint(0, 100),
            content_overall="Your overall score of {} shows you're doing good.".format(overall_score),
            content_medical="You are underprotected in your medical category.",
            content_income="We also think you're overprotected in your income category.",
            content_stuff="",
            content_liability="",
            content_digital="",
        )


class Tag(models.Model):
    """Tags to be used for products"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Coverage(models.Model):
    """Coverage model to be used for products"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product object"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField("Tag")
    coverages = models.ManyToManyField("Coverage")

    def __str__(self):
        return self.title


class Score(models.Model):
    """Score object"""

    MIN_SCORE = 0
    MAX_SCORE = 100
    score_overall = models.PositiveSmallIntegerField(
        _("overall score"),
        validators=[MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)],
        blank=True,
        null=True,
    )
    score_medical = models.PositiveSmallIntegerField(
        _("medical score"),
        validators=[MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)],
        blank=True,
        null=True,
    )
    score_income = models.PositiveSmallIntegerField(
        _("income score"),
        validators=[MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)],
        blank=True,
        null=True,
    )
    score_stuff = models.PositiveSmallIntegerField(
        _("stuff you own score"),
        validators=[MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)],
        blank=True,
        null=True,
    )
    score_liability = models.PositiveSmallIntegerField(
        _("liabilities score"),
        validators=[MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)],
        blank=True,
        null=True,
    )
    score_digital = models.PositiveSmallIntegerField(
        _("digital score"),
        validators=[MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)],
        blank=True,
        null=True,
    )
    content_overall = models.TextField(blank=True)
    content_medical = models.TextField(blank=True)
    content_income = models.TextField(blank=True)
    content_stuff = models.TextField(blank=True)
    content_liability = models.TextField(blank=True)
    content_digital = models.TextField(blank=True)

    def __str__(self):
        return str(self.score_overall)
