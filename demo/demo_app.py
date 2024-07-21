"""
The web-application for showing the project documentation.
"""

from flask import Flask, redirect, url_for, request
from markupsafe import Markup

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user
)

import bootwrap as bw

from .demo_user import TransactionAction, UserManager, UserAlreadyExistError
from .demo_stock import StockMarket
from .demo_components import (
    BuyDialog,
    SellDialog,
    ShareCard,
    ShareItem,
    UserAccountCard,
    DepositDialog,
    WithdrawDialog,
    ActivityTable
)

demo_app = Flask(__name__, static_folder='.', static_url_path='')
demo_app.secret_key = 'super secret key'
demo_app.config['SESSION_TYPE'] = 'filesystem'

login_manager = LoginManager()
login_manager.init_app(demo_app)

USERS = UserManager()
STOCKS = StockMarket()




def initialize():
    # "The Wolf of Wall Street is a 2013 American epic biographical black
    # comedy crime film directed by Martin Scorsese and written by Terence
    # Winter, based on the 2007 memoir of the same name by Jordan Belfort."
    # ---------------------------------------------------------------------
    #                                                             Wikipedia

    # For software demonstration purposes we need to create an account, so
    # anybody can log in and play with it. Why not make a mock of Jordan
    # Belfort's account. If he managed to get rich, then why not you? :)
    try:
        user = USERS.add_user(
            'j.belfort@notexist.com', 'Jordan Belfort', 'HardWork@2021'
        )
        # Transaction 1
        user.deposit(25000)
        # Transaction 2
        user.withdraw(560.0)
        user.buy('GOOGL', 'Alphabet Inc.', 2,  560.0)
        # Transaction 3
        user.withdraw(7090.0)
        user.buy('TSLA', 'Tesla Inc.', 10,  7090.0)
        # Transaction 4
        user.withdraw(1250)
        # Transaction 5
        user.withdraw(125)
        user.buy('AMZN', 'Amazon Inc.', 5, 125.0)
        # Transaction 6
        user.sell('AMZN', 'Amazon Inc.', 2, 625.0)
        user.deposit(625.0)
        # Transaction 7
        user.withdraw(590.0)
        user.buy('AAPL', 'Apple Inc.', 25,  590.0)
        # Transaction 8
        user.withdraw(16090.0)
        user.buy('NVDA', 'Nvidia Corporation.', 15,  16090.0)
        # Transaction 9
        user.sell('AAPL', 'Apple Inc.', 15,  18340.0)
        user.deposit(18340.0)
        # Transaction 10
        user.withdraw(16990.0)
    except UserAlreadyExistError:
        pass

    print('Stock market is open...')


demo_app.before_request_funcs = [(None, initialize())]

@login_manager.user_loader
def load_user(user_id):
    return USERS.get_user_by_id(user_id)


class DemoPage(bw.Page):
    """A demo web-pages.

    Args:
        config (dict): The configuration for generating a documentation
            contant.
    """

    def __init__(self, title, *wc):
        super().__init__(
            favicon='favicon.ico',
            menu=bw.Menu(
                logo=bw.Image(
                    'logo.png',
                    width=32,
                    alt='PiggyBank Logo'
                ),
                brand=bw.Text('PiggyBank').as_strong().as_light(),
                anchors=[
                    bw.Anchor('Portfolio').link('/portfolio'),
                    bw.Anchor('Discovery').link('/discovery'),
                    bw.Anchor('Account').link('/account'),
                    bw.Anchor('Activity').link('/activity')
                ],
                actions=[
                    bw.Button('Logout').
                    as_outline().
                    as_light().
                    link('/logout')
                ]
            ),
            container=bw.Panel(bw.Text(title).as_heading(1), *wc)
        )


WC_BRAND = bw.Panel(
    bw.Image('logo.png', height=48, width=48),
    bw.Text('PiggyBank').as_heading(1)
).add_classes("d-flex justify-content-center")
FAVICON = 'favicon.ico'


@demo_app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('portfolio'))
    else:
        return redirect(url_for('login'))


@demo_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_user(
            USERS.get_user(
                request.form.get('email'),
                request.form.get('password')
            )
        )
        return redirect(url_for('index'))

    # request.method == 'GET'
    return Markup(
        bw.LoginPage(
            WC_BRAND,
            href_on_submit='/login',
            href_on_cancel='/',
            favicon=FAVICON,
            title="PiggyBank Login Form",
        ).background(
            image='url("background.jpg")',
            repeat='no-repeat',
            position='center',
            size='cover'
        )
    )


@demo_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@demo_app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        USERS.add_user(
            request.form.get('email'),
            request.form.get('name'),
            request.form.get('password')
        )
        return redirect(url_for('login'))

    # request.method == 'GET'
    return Markup(
        bw.SignupPage(
            WC_BRAND,
            href_on_submit='/signup',
            href_on_cancel='/',
            favicon=FAVICON,
            title="PiggyBank Sign-up Form",
        ).background(
            image='url("background.jpg")',
            position='center',
            repeat='no-repeat',
            size='cover'
        )
    )


@demo_app.route('/portfolio', methods=['GET'])
@demo_app.route('/portfolio/<action>/<sid>', methods=['POST'])
def portfolio(action=None, sid=None):
    if request.method == 'POST':
        nos = int(request.form.get('nos'))
        share = STOCKS.get_stock(sid)
        company = share.company
        amount = nos * share.price
        if action == 'buy':
            current_user.withdraw(amount)
            current_user.buy(sid, company, nos, amount)
        if action == 'sell':
            current_user.sell(sid, company, nos, amount)
            current_user.deposit(amount)
        return redirect(url_for('portfolio'))

    # request.method == 'GET'
    STOCKS.update()

    wc_dialogs = []
    wc_items = []
    for record in current_user.portfolio:
        share = STOCKS.get_stock(record.sid)

        wc_sell_dialog = SellDialog(share, current_user)
        wc_item = ShareItem(share, current_user, wc_sell_dialog)

        wc_dialogs.append(wc_sell_dialog)
        wc_items.append(wc_item)

    return Markup(
        DemoPage(
            'My Portfolio', bw.List(*wc_items), *wc_dialogs,
            bw.Text('Portfolio Transactions').as_heading(4).mt(4),
            ActivityTable(
                current_user,
                [TransactionAction.DEPOSIT, TransactionAction.WITHDRAW]
            )
        )
    )


@ demo_app.route('/discovery')
def discovery():
    STOCKS.update()

    wc_dialogs = []
    wc_cards = []
    for share in STOCKS.get_stocks():
        wc_buy_dialog = BuyDialog(share, current_user)
        wc_card = ShareCard(share, current_user, wc_buy_dialog)

        wc_dialogs.append(wc_buy_dialog)
        wc_cards.append(wc_card)

    return Markup(
        DemoPage(
            'Available Shares', bw.Deck(*wc_cards), *wc_dialogs
        )
    )


@ demo_app.route('/account', methods=['GET'])
@ demo_app.route('/account/<action>', methods=['POST'])
def account(action=None):
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        if action == 'deposit':
            current_user.deposit(amount)
        if action == 'withdraw':
            current_user.withdraw(amount)
        return redirect(url_for('account'))

    # request.method == 'GET'
    wc_deposit_dialog = DepositDialog(current_user)
    wc_withdraw_dialog = WithdrawDialog(current_user)
    return Markup(
        DemoPage(
            'My Account',
            UserAccountCard(current_user, wc_deposit_dialog,
                            wc_withdraw_dialog),
            bw.Text('Account Transactions').as_heading(4).mt(4),
            ActivityTable(
                current_user,
                [TransactionAction.BUY, TransactionAction.SELL],

            ),
            wc_deposit_dialog,
            wc_withdraw_dialog
        )
    )


@ demo_app.route('/activity')
def activity():
    return Markup(
        DemoPage(
            'My Activity', ActivityTable(current_user)
        )
    )
