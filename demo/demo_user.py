"""
User database for demo-application.
"""

from flask_login import UserMixin
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)


class User(UserMixin):
    """A user profile.

    Args:
        uid (int): The user identifier.
        email (str): The user email.
        name (str): The user name.
        password (str): The user password.
    """

    def __init__(self, uid, email, name, password):
        super().__init__()
        self.__uid = uid
        self.__email = email
        self.__name = name
        self.__password = password

    @property
    def id(self):
        """The user identifier."""
        return self.__uid

    @property
    def email(self):
        """The user email."""
        return self.__email

    @property
    def name(self):
        """The user name."""
        return self.__name

    @property
    def password(self):
        """The user password."""
        return self.__password

    def __str__(self):
        return f'''
            User(
                id: {self.id},
                email: {self.email},
                name: {self.name},
                password: {self.password}
            )
        '''


class UserManager:
    """A manager for application users."""

    def __init__(self):
        self.__database = {}

    def add_user(self, email, name, password):
        """Adds a new user.

        Args:
            email (str): The user email.
            name (str): The user name.
            password (str): The user password.

        Returns:
            user (User): The created user.
        """
        if email in self.__database:
            raise UserAlreadyExistError
        user = User(
            str(len(self.__database)),
            email,
            name,
            generate_password_hash(password)
        )
        self.__database[email] = user

        print('Added a new user: ', user)
        return user

    def get_user(self, email, password):
        """Gets a existing user using email and password.

        Args:
            email (str): The user email.
            password (str): The user password.

        Returns:
            user (User): The retrieved user.
        """
        if email not in self.__database:
            raise UserNotFoundError
        user = self.__database[email]
        if check_password_hash(user.password, password):
            return user

        print('Retrieved the existing user: ', user)
        return InvalidEmailOrPasswordError

    def get_user_by_id(self, id):
        """Gets user by ID

        Args:
            id (int): The user ID.
        Returns:
            user (User): The retrieved user.
        """
        # for user in self.__database.values():
        #     if user.id == id:
        #         return user
        # raise UserNotFoundError
        return User(
            '0', 'a@b.com', 'Nick', 'asdf'
        )


class UserError(Exception):
    """This error is thrown if problems with authenticating a user."""


class UserNotFoundError(UserError):
    """This error is thrown if user has not found."""


class UserAlreadyExistError(UserError):
    """This error is thrown if user already exist."""


class InvalidEmailOrPasswordError(UserError):
    """This error is thrown if email or password is invalid."""


USERS = UserManager()
