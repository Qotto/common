# coding: utf-8
# Copyright (c) Qotto, 2017

import logging
import pyrebase

from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

__all__ = ['Client', 'fire']

class Client:
    user: dict = None
    last_auth_date: datetime = None

    def __init__(self, email: str = settings.FIREBASE_EMAIL, password: str = settings.FIREBASE_PASSWORD) -> None:
        logger.info("Initializing Firebase client…")
        self.firebase = pyrebase.initialize_app({
            'apiKey': settings.FIREBASE_API_KEY,
            'authDomain': settings.FIREBASE_AUTH_DOMAIN,
            'databaseURL': settings.FIREBASE_DB_URL,
            'storageBucket': settings.FIREBASE_SORAGE_BUCKET,
        })
        self.email = email
        self.password = password
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        self._check_auth()

    def child(self, *args, **kwargs):
        return self.db.child(*args, **kwargs)

    @property
    def token(self) -> str:
        self._check_auth()
        return self.user['idToken']

    def _check_auth(self) -> None:
        if self.last_auth_date:
            last_token_duration = timezone.now() - self.last_auth_date
            if last_token_duration < timedelta(seconds=settings.FIREBASE_TOKEN_TIMEOUT):
                return
            else:
                logger.info("Refreshing Firebase auth token…")
                self.user = self.auth.refresh(self.user['refreshToken'])
        else:
            logger.info("Authenticating Firebase client…")
            self.user = self.auth.sign_in_with_email_and_password(self.email, self.password)
        self.last_auth_date = timezone.now()

fire = Client()
