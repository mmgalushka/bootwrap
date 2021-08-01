"""
User database for demo-application.
"""

from enum import Enum
from datetime import datetime

from collections import namedtuple
from flask_login import UserMixin
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)


class TransactionTarget(str, Enum):
    ACCOUNT = 'account'
    PORTFOLIO = 'portfolio'


class TransactionAction(str, Enum):
    BUY = 'buy'
    SELL = 'sell'
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'


UserTransaction = namedtuple(
    'UserTransaction', ['timestamp', 'target', 'action', 'description']
)
"""The user transaction."""


LedgerRecord = namedtuple(
    'LedgerRecord', ['sid', 'nos', 'investment']
)
"""The ledger record."""


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
        self.__balance = 100.0
        self.__portfolio = {}
        self.__activity = []

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

    @property
    def balance(self):
        """The user balance."""
        return self.__balance

    @property
    def portfolio(self):
        """The user portfolio iterator."""
        return iter(self.__portfolio.values())

    def deposit(self, amount):
        """Deposits money to the user account.

        Args:
            amount (float): The deposit amount.
        """
        self.__balance += amount
        self.__activity.insert(
            0,
            UserTransaction(
                datetime.now(),
                TransactionTarget.ACCOUNT,
                TransactionAction.DEPOSIT,
                (
                    'You deposit $%.2f to your account, ' +
                    'your new balance is $%.2f'
                ) % (amount, self.__balance)
            )
        )

    def withdraw(self, amount):
        """Withdraws money from the user account.

        Args:
            amount (float): The withdraw amount.
        """
        self.__balance -= amount
        self.__activity.insert(
            0,
            UserTransaction(
                datetime.now(),
                TransactionTarget.ACCOUNT,
                TransactionAction.WITHDRAW,
                (
                    'You withdraw $%.2f from your account, ' +
                    'your new balance is $%.2f'
                ) % (amount, self.__balance)
            )
        )

    def buy(self, sid, company, nos, amount):
        """Buys a new shares.

        Args:
            sid (str): The share ID to buy.
            nos (int): The number of shares to buy.
            amount (float): The te total price for all shares.
        """
        if sid in self.__portfolio:
            record = self.__portfolio[sid]
            self.__portfolio[sid] = LedgerRecord(
                sid,
                record.nos + nos,
                record.investment + amount
            )
        else:
            self.__portfolio[sid] = LedgerRecord(
                sid,
                nos,
                amount
            )
        self.__activity.insert(
            0,
            UserTransaction(
                datetime.now(),
                TransactionTarget.PORTFOLIO,
                TransactionAction.BUY,
                (
                    'You bought %d share(s) of %s, ' +
                    'by spending in total $%.2f;'
                ) % (nos, company, amount)
            )
        )

    def sell(self, sid, company, nos, amount):
        """Sells a existing shares.

        Args:
            sid (str): The share ID to sell.
            nos (int): The number of shares to sell.
        """
        if sid in self.__portfolio:
            record = self.__portfolio[sid]
            self.__portfolio[sid] = LedgerRecord(
                sid,
                record.nos - nos,
                record.investment - nos * record.investment / record.nos
            )
            self.__activity.insert(
                0,
                UserTransaction(
                    datetime.now(),
                    TransactionTarget.PORTFOLIO,
                    TransactionAction.SELL,
                    (
                        'You sold %d share(s) of %s, ' +
                        'by getting in total $%.2f;'
                    ) % (nos, company, amount)
                )
            )

    def get_record(self, sid):
        return self.__portfolio[sid]

    def get_activity(self, filter=[]):
        """Returns user activity log.

        Args:
            filter (str): The log items to filter;

        Returns:
            log (list): The user activity log;
        """
        columns = ['Date/Time', 'Target', 'Action', 'Description']

        log = []
        for record in self.__activity:
            if record.action not in filter:
                log.append(
                    [
                        record.timestamp,
                        record.target,
                        record.action,
                        record.description
                    ]
                )
        return columns, log

    def __str__(self):
        return f'''
            User(
                id: {self.id},
                email: {self.email},
                name: {self.name},
                password: {self.password},
                balance:  {self.balance}
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
        raise InvalidEmailOrPasswordError

    def get_user_by_id(self, id):
        """Gets user by ID

        Args:
            id (int): The user ID.
        Returns:
            user (User): The retrieved user.
        """
        for user in self.__database.values():
            if user.id == id:
                return user
        raise UserNotFoundError


class UserError(Exception):
    """This error is thrown if problems with authenticating a user."""


class UserNotFoundError(UserError):
    """This error is thrown if user has not found."""


class UserAlreadyExistError(UserError):
    """This error is thrown if user already exist."""


class InvalidEmailOrPasswordError(UserError):
    """This error is thrown if email or password is invalid."""
