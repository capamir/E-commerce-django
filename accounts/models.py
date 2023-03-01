from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
import uuid

class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=255, unique=True)
	phone_number = models.CharField(max_length=11, unique=True)
	full_name = models.CharField(max_length=100)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	image = models.ImageField(null=True, blank=True, upload_to='products/', 
                            default="products/default.jpg")
	id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
	
	objects = UserManager()

	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELDS = ['email', 'full_name']

	def __str__(self):
		return self.email

	@property
	def is_staff(self):
		return self.is_admin


class OtpCode(models.Model): # one time password code
	phone_number = models.CharField(max_length=11, unique=True)
	code = models.PositiveSmallIntegerField()
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.phone_number} - {self.code} - {self.created}'
