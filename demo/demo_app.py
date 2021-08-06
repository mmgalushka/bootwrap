"""
The web-application for showing the project documentation.
"""

from flask import Flask, Markup, redirect, url_for, request

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user
)

import bootwrap as bw

from .demo_user import TransactionAction, UserManager
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


@demo_app.before_first_request
def initialize():
    if not STOCKS.is_alive():
        # STOCKS.start()
        pass

    USERS.add_user('j.belfort@notexist.com', 'Jordan Belfort', 'HardWork@2021')
    user = USERS.get_user_by_id('0')
    user.deposit(25000)
    user.buy('GOOGL', 'Alphabet Inc.', 2,  1285.0)
    user.withdraw(1200)
    user.buy('AMZN',  'Amazon Inc.', 4, 125.0)
    user.sell('AMZN',  'Amazon Inc.', 1, 45.0)

    print('Stock market is open...')


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
