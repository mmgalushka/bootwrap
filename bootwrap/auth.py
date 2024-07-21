from .page import Page

from .components import (
    Button,
    TextInput,
    Form,
    Text,
    Panel,
    Javascript
)

EMAIL_REGEX = '/^\\S+@\\S+\\.\\S+$/i'
PASSWORD_REGEX = '/^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\\s).{8,15}$/i'  # NOQA
PASSWORD_TIPS = (
    'Your password must be between 8 and 30 characters, contain at '
    'least one: an uppercase or lowercase letter (ex: A, B, etc.), '
    'a digit (ex: 0, 1, 2, 3, etc.) and a special character(ex: '
    '$, #, @, !,%,^,&,*).'
)

WC_EMAIL = TextInput(
    'Your email',
    'email',
    placeholder='you@email.com'
).for_email().add_classes('form-group')

WC_NAME = TextInput(
    'Your name',
    'name',
    placeholder='Your Name'
).add_classes('form-group')

WC_PASSWORD = TextInput(
    'Your password',
    'password',
    placeholder='********'
).for_password().add_classes('form-group')

WC_CONF_PASSWORD = TextInput(
    'Confirm your password',
    'password',
    placeholder='********'
).for_password().add_classes('form-group')


class KeyActionActivator(Javascript):
    def __init__(self, wc_to_activate):
        super().__init__(
            script='''
                $('#wc_email, #wc_password, #wc_conf_password').on('keyup', function() {
                    const email_pattern = email_regex;
                    var email_filled = false;
                    if ($('#wc_email').length){
                        email_filled = email_pattern.test(
                            $('#wc_email').val())
                    } else {
                        email_filled = true;
                    }

                    const password_pattern = password_regex;
                    var password_filled = false;
                    if ($('#wc_password').length){
                        password_filled = password_pattern.test(
                            $('#wc_password').val())
                    } else {
                        password_filled = true;
                    }

                    console.log(email_filled && password_filled)

                    if(email_filled && password_filled) {
                        if( $('#wc_conf_password').length ) {
                            if ($('#wc_password').val() == $('#wc_conf_password').val()) {
                                $('#wc_to_activate').removeAttr('disabled');
                            } else {
                                $('#wc_to_activate').attr('disabled', 'disabled');
                            }
                        } else {
                            $('#wc_to_activate').removeAttr('disabled');
                        }
                    } else {
                        $('#wc_to_activate').attr('disabled', 'disabled');
                    }
                });
            ''',  # NOQA
            submap={
                'email_regex': EMAIL_REGEX,
                'password_regex': PASSWORD_REGEX,
                'wc_email': WC_EMAIL,
                'wc_password': WC_PASSWORD,
                'wc_conf_password': WC_CONF_PASSWORD,
                'wc_to_activate': wc_to_activate
            })


class Auth(Page):
    """A sign-up page."""

    def __init__(
            self,
            wc_brand,
            wc_form,
            wc_to_activate,
            favicon=None,
            title=None,
    ):

        # Defines the control to show an alert message.
        # self._wc_alert = Alert(error).add_classes('mt-3').as_danger()

        # Defines the input user password.
        self._wc_password_hint = Text(
            'Your password must be between 8 and 30 characters, contain at '
            'least one: an uppercase or lowercase letter (ex: A, B, etc.), '
            'a digit (ex: 0, 1, 2, 3, etc.) and a special character(ex: '
            '$, #, @, !,%,^,&,*).'
        ).as_secondary().as_small().add_classes('form-group')

        super().__init__(
            favicon=favicon,
            title=title,
            container=Panel(
                wc_brand,
                wc_form,
                KeyActionActivator(wc_to_activate)
            ).add_classes('mx-auto bg-light border rounded auth').p(3)
        )


class Signup(Auth):
    """A sign-up page."""

    def __init__(
            self,
            wc_brand,
            href_on_submit='/signup',
            href_on_cancel='/',
            favicon=None,
            title=None,
    ):

        wc_form_title = Text('Registration Form').as_heading(
            3).as_primary().my(3)

        wc_sign_up = Button('Sign up').submit().as_primary().as_disabled().mt(
            3).me(2)
        wc_cancel = Button('Cancel').link(href_on_cancel).as_light().mt(3)

        # Defines the input user password.
        wc_password_hint = Text(
            'Your password must be between 8 and 30 characters, contain at '
            'least one: an uppercase or lowercase letter (ex: A, b, etc.), '
            'a digit (ex: 0, 1, 2, 3  etc.) and a special character(ex: '
            '$, #, @, !,%,^,&,*).'
        ).as_secondary().as_small().add_classes('form-group')

        wc_form = Form(
            wc_form_title,
            WC_EMAIL,
            WC_NAME,
            WC_PASSWORD,
            WC_CONF_PASSWORD,
            wc_password_hint,
            Panel(
                wc_sign_up, wc_cancel
            ).add_classes("d-flex justify-content-end")
        ).on_submit(href_on_submit)

        super().__init__(
            favicon=favicon,
            title=title,
            wc_brand=wc_brand,
            wc_form=wc_form,
            wc_to_activate=wc_sign_up
        )


class Login(Auth):
    """A sign-up page."""

    def __init__(
            self,
            wc_brand,
            href_on_submit='/signup',
            href_on_cancel='/',
            favicon=None,
            title=None,
    ):
        wc_form_title = Panel(
            Button('Sign up').link('/signup').
            as_primary().as_outline().add_classes('float-right'),
            Text('Sign In').as_heading(3).as_primary()
        ).my(3)

        wc_login = Button('Login').submit().\
            as_primary().as_disabled().me(2)
        wc_cancel = Button('Cancel').link(href_on_cancel).\
            as_light()

        wc_form = Form(
            wc_form_title,
            WC_EMAIL,
            WC_PASSWORD,
            Panel(
                wc_login, wc_cancel
            ).add_classes("d-flex justify-content-end")
        ).on_submit(href_on_submit)

        super().__init__(
            favicon=favicon,
            title=title,
            wc_brand=wc_brand,
            wc_form=wc_form,
            wc_to_activate=wc_login
        )
