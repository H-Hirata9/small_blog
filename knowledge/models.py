import uuid

from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from taggit.managers import TaggableManager


def post_file_dir(instance, filename):
    # file will be uploaded to MEDIA_ROOT/post_<id>/<filename>
    return f'post_{instance.post.id}/{filename}'



class MyUserManager(BaseUserManager):
    def create_user(self, email, employee_id, password=None):
        """
        Creates and saves a User with the given email, employee_id and password.
        """
        if not email or not employee_id :
            raise ValueError('Users must have an email address and an employee_id')

        user = self.model(
            email=self.normalize_email(email),
            employee_id=employee_id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, employee_id, password=None):
        """
        Creates and saves a superuser with the given email,
        employee id and password.
        """
        user = self.create_user(
            email,
            password=password,
            employee_id=employee_id,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create your models here.

class MyUser(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name=_('E-mail address'),
        max_length=255,
        unique=True,
        validators=[EmailValidator(
        )]
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employee_id = models.CharField(max_length=7)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('employee_id',)


    def __str__(self):
        return f"{self.email}"


class DepartmentCode(models.Model):

    department_code = models.CharField(
        _('department code'),
        max_length=3,
        unique=True,
        validators=[RegexValidator(regex=r'\d{3}')]
    )
    name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='dpt_code_updated_by', on_delete=models.CASCADE)


    REQUIRED_FIELDS = ('department_code',)

    def __str__(self):
        return f"{self.department_code}:{self.name}"

    class Meta:
        verbose_name_plural = "DepartmentCodes"


class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='user_profile',
                                on_delete=models.CASCADE,)
    department = models.ManyToManyField("DepartmentCode", through="Belongs",
                                        through_fields=("profile", "department"))

    free_text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Belongs(models.Model):

    department = models.ForeignKey(DepartmentCode, related_name='belongs_dpt_code',on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, related_name='user_belongs', on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.department}:{self.profile.user}"

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["profile", "is_primary"],
                name="const_prime_dpt",
                condition=models.Q(is_primary=True)
            ),
            models.UniqueConstraint(
                fields=["profile", "department"],
                name="const_dpt",
            ),
        )
        verbose_name_plural = "Belongs"


class Article(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='article_author', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    initial_published_at  = models.DateTimeField(null=True, blank=True)
    last_published_at = models.DateTimeField(null=True, blank=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_likes',  blank=True)
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_bookmarks',  blank=True)
    tags = TaggableManager()


    REQUIRED_FIELDS = ('author', 'title', 'text',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.is_published:
            if self.initial_published_at is None:
                self.initial_published_at = now
            self.last_published_at = now
        else:
            self.published_at = None
        super().save(*args, **kwargs)


    class Meta:
        verbose_name_plural = "Articles"



class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='article_images')
    image = models.ImageField(upload_to=post_file_dir)

    class Meta:
        verbose_name_plural = "ArticleImages"


class ArticleAttachedFile(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='article_attached_files')
    files = models.FileField(upload_to=post_file_dir)

    class Meta:
        verbose_name_plural = "ArticleAttachedFiles"

class Comment(models.Model):
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='commenter', on_delete=models.CASCADE)
    text = models.TextField()
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    ancestor = models.ForeignKey('self', related_name='descendants',
                                 on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL,  blank=True)


    REQUIRED_FIELDS = ('commenter', 'article', 'text', )

    def __str__(self):
        if len(self.text) > 10:
            text = self.text[:11]
        else:
            text = self.text
        return f"{self.article}:{self.commenter}:{text}"

    def save(self, *args, **kwargs):
        if self.ancestor:
            self.article = self.ancestor.article
        super().save(*args, **kwargs)


    class Meta:
        verbose_name_plural = "Comments"

