"""
The web-application for showing the project documentation.
"""

from flask import Flask, Markup, redirect, url_for, request

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)

import bootwrap as bw

from .demo_user import USERS

demo_app = Flask(__name__, static_folder='.', static_url_path='')
demo_app.secret_key = 'super secret key'
demo_app.config['SESSION_TYPE'] = 'filesystem'

login_manager = LoginManager()
login_manager.init_app(demo_app)


@login_manager.user_loader
def load_user(user_id):
    return USERS.get_user_by_id(user_id)


class DemoPage(bw.Page):
    """A demo web-pages.

    Args:
        config (dict): The configuration for generating a documentation
            contant.
    """

    def __init__(self, content):
        super().__init__(
            favicon='favicon.ico',
            menu=bw.Menu(
                logo=bw.Image(
                    'logo.png',
                    width=32,
                    alt='PiggyShares Logo'
                ),
                brand=bw.Text('PiggyShares').as_strong().as_light(),
                anchors=[
                    bw.Anchor('Portfolio').link('/portfolio'),
                    bw.Anchor('Insights').link('/insights'),
                    bw.Anchor('Discovery').link('/discovery'),
                    bw.Anchor('Activity').link('/activity'),
                    bw.Anchor('Account').link('/account'),
                ],
                actions=[
                    bw.Button('Logout').
                    as_outline().
                    as_light().
                    link('/logout')
                ]
            ),
            container=content
        )


WC_BRAND = bw.Panel(
    bw.Image('logo.png', height=32, width=32),
    bw.Text('PiggyShares').as_heading(1)
).add_classes("d-flex justify-content-center")
FAVICON = 'favicon.ico'


@demo_app.route('/')
def index():
    if current_user.is_authenticated:
        return Markup(DemoPage(''))
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
    return Markup(bw.LoginPage(
        WC_BRAND,
        href_on_submit='/login',
        href_on_cancel='/',
        favicon=FAVICON,
        title="PiggyShares Login Form",
    ))


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
    return Markup(bw.SignupPage(
        WC_BRAND,
        href_on_submit='/signup',
        href_on_cancel='/',
        favicon=FAVICON,
        title="PiggyShares Sign-up Form",
    ))


@demo_app.route('/portfolio')
def portfolio():
    return Markup(DemoPage('portfolio'))


@demo_app.route('/insights')
def insights():
    return Markup(DemoPage('insights'))


@demo_app.route('/discovery')
def discovery():
    return Markup(DemoPage('discovery'))


@demo_app.route('/activity')
def activity():
    return Markup(DemoPage('activity'))


@demo_app.route('/account')
def account():
    return Markup(DemoPage('account'))
