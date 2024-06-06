from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class User:
    _id: int
    _email: str
    _password: str
    _full_name: str
    _is_admin: bool = False
    _is_active: bool = True
    _likes: Optional[list] = None
    _is_manager: bool = False

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def full_name(self):
        return self._full_name

    @property
    def is_admin(self):
        return self._is_admin
    
    @property
    def is_active(self):
        return self._is_active
    
    @property
    def likes(self):
        return self._likes
    
    @property
    def is_manager(self):
        return self._is_manager

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_likes_count(self):
        if self.likes:
            return len(self.likes)
        return 0