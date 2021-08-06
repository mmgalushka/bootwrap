"""
Test for bootwrap/auth.py
"""

import pytest

from bootwrap import SignupPage, LoginPage, Text
from .helper import HelperHTMLParser


@pytest.mark.page
def test_signup_page():
    page = SignupPage(
        wc_brand=Text('SomeBrand'),
        title='Signup Page',
        favicon='somename.ico'
    )
    print(str(page))
    actual = HelperHTMLParser.parse(page.__html__())
    expected = HelperHTMLParser.parse(f''' 
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8"/>
                <meta name="viewport"
                    content="width=device-width, initial-scale=1,
                    shrink-to-fit=no"/>
                
                <link rel="stylesheet" type="text/css" href="..."/>
                <link rel="stylesheet" type="text/css" href="..."/>
                <link rel="stylesheet" type="text/css" href="..."/>
                <link rel="icon" type="image/x-icon" href="somename.ico"/>

                <script src="..." type="application/javascript"></script>
                <script src="..." type="application/javascript"></script>
                <script src="..." type="application/javascript"></script>
                <script src="..." type="application/javascript"></script>
                <script src="..." type="application/javascript"></script>
        
                <title>Signup Page</title>
            </head>
            <body>
                <div class="container-fluid">
                    <div id="..."
                        class="mx-auto bg-light border rounded auth p-3">
                        <span id="..." >SomeBrand</span>
                        
                        <form id="..."
                            action="/signup"
                            method="POST"
                            enctype="multipart/form-data">
                
                            <h3 id="..." class="text-primary my-3">Registration Form</h3>
        
                            <div class="form-group row">...</div>
                            <div class="form-group row">...</div>
                            <div class="form-group row">...</div>
                            <div class="form-group row">...</div>

                            <span id="..." class="text-secondary form-group">
                                <small>...</small>
                            </span>

                            <div id="..." class="d-flex justify-content-end">
                                ...
                            </div>
                        </form>
                        <script type="application/javascript">...</script>
                    </div>
                </div>
            </body>
            <script>...</script>
            <style>...</style>
        </html>
    ''')  # NOQA
    assert actual == expected


@pytest.mark.page
def test_login_page():
    page = LoginPage(
        wc_brand=Text('SomeBrand'),
        title='Login Page',
        favicon='somename.ico'
    )
    actual = HelperHTMLParser.parse(page.__html__())
    expected = HelperHTMLParser.parse(f''' 
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8"/>
                <meta name="viewport"
                    content="width=device-width, initial-scale=1,
                    shrink-to-fit=no"/>
                
                <link rel="stylesheet" type="text/css" href="..."/>
                <link rel="stylesheet" type="text/css" href="..."/>
                <link rel="stylesheet" type="text/css" href="..."/>
                <link rel="icon" type="image/x-icon" href="somename.ico"/>

                <script src="..." type="application/javascript"></script>
                <script src="..." type="application/javascript"></script>
                <script src="..." type="application/javascript"></script>
                <script src="..." type="application/javascript"></script>
                <script src="..." type="application/javascript"></script>
        
                <title>Login Page</title>
            </head>
            <body>
                <div class="container-fluid">
                    <div id="..."
                        class="mx-auto bg-light border rounded auth p-3">
                        <span id="..." >SomeBrand</span>
                        
                        <form id="..."
                            action="/signup"
                            method="POST"
                            enctype="multipart/form-data">
                
                            <div id="..." class="my-3">
                                <a id="..."
                                    class="float-right btn btn-outline-primary"
                                    href="/signup"
                                    role="button">
                                    Sign up
                                </a>
                                <h3 id="..." class="text-primary">Sign In</h3>
                            </div>
        
                            <div class="form-group row">...</div>
                            <div class="form-group row">...</div>
                            <div id="..." class="d-flex justify-content-end">
                                ...
                            </div>
                        </form>
                        <script type="application/javascript">...</script>
                    </div>
                </div>
            </body>
            <script>...</script>
            <style>...</style>
        </html>
    ''')  # NOQA
    assert actual == expected
