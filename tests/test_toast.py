"""
Test for bootwrap/components/text.py
"""

import pytest

from bootwrap import Toast, Icon
from .helper import HelperHTMLParser


@pytest.mark.toast
def test_toast_with_title():
    toast = Toast(
        title="sometitle",
        description="somedescr",
        marker="somemark",
        figure=Icon("fa-solid fa-info"),
    )
    actual = HelperHTMLParser.parse(str(toast))
    expected = HelperHTMLParser.parse(f'''
        <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 10">
            <div id="{toast.identifier}"
                class="toast"
                role="alert"
                aria-live="assertive"
                aria-atomic="true"
                data-bs-autohide="true"
                >
                <div class="toast-header">
                    <i id="..."
                        class="me-2 fa-solid fa-info">
                    </i>
                    <strong id="..." class="me-auto">sometitle</strong>
                    <small id="..." >somemark</small>
                    <button type="button"
                        class="btn-close"
                        data-bs-dismiss="toast"
                        aria-label="Close">
                    </button>
                </div>
                <div class="toast-body">
                    somedescr
                </div>
            </div>
        </div>
    ''')
    assert actual == expected


@pytest.mark.toast
def test_toast_without_title():
    toast = Toast(
        description="somedescr",
    )
    actual = HelperHTMLParser.parse(str(toast))
    expected = HelperHTMLParser.parse(f'''
        <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 10">
            <div id="{toast.identifier}"
                class="toast align-items-center"
                role="alert"
                aria-live="assertive"
                aria-atomic="true"
                data-bs-autohide="true"
                >
                <div class="d-flex">
                    <div class="toast-body">
                        somedescr
                    </div>
                    <button type="button"
                        class="btn-close me-2 m-auto"
                        data-bs-dismiss="toast"
                        aria-label="Close">
                    </button>
                </div>
            </div>
        </div>
    ''')
    assert actual == expected


@pytest.mark.toast
def test_toast_appearance():
    toast = Toast(
        description="somedescr",
    ).as_primary()
    actual = HelperHTMLParser.parse(str(toast))
    expected = HelperHTMLParser.parse(f'''
        <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 10">
            <div id="{toast.identifier}"
                class="toast text-bg-primary align-items-center"
                role="alert"
                aria-live="assertive"
                aria-atomic="true"
                data-bs-autohide="true"
                >
                <div class="d-flex">
                    <div class="toast-body">
                        somedescr
                    </div>
                    <button type="button"
                        class="btn-close me-2 m-auto"
                        data-bs-dismiss="toast"
                        aria-label="Close">
                    </button>
                </div>
            </div>
        </div>
    ''')
    assert actual == expected

@pytest.mark.toast
def test_toast_outline():
    toast = Toast(
        description="somedescr",
    ).as_primary().as_outline()
    actual = HelperHTMLParser.parse(str(toast))
    expected = HelperHTMLParser.parse(f'''
        <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 10">
            <div id="{toast.identifier}"
                class="toast border border-primary text-primary align-items-center"
                role="alert"
                aria-live="assertive"
                aria-atomic="true"
                data-bs-autohide="true"
                >
                <div class="d-flex">
                    <div class="toast-body">
                        somedescr
                    </div>
                    <button type="button"
                        class="btn-close me-2 m-auto"
                        data-bs-dismiss="toast"
                        aria-label="Close">
                    </button>
                </div>
            </div>
        </div>
    ''')
    assert actual == expected

@pytest.mark.toast
def test_toast_hide_delay():
    toast = Toast(
        description="somedescr",
        hide_delay=0,
    )
    actual = HelperHTMLParser.parse(str(toast))
    expected = HelperHTMLParser.parse(f'''
        <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 10">
            <div id="{toast.identifier}"
                class="toast align-items-center"
                role="alert"
                aria-live="assertive"
                aria-atomic="true"
                data-bs-autohide="false">
                >
                <div class="d-flex">
                    <div class="toast-body">
                        somedescr
                    </div>
                    <button type="button"
                        class="btn-close me-2 m-auto"
                        data-bs-dismiss="toast"
                        aria-label="Close">
                    </button>
                </div>
            </div>
        </div>
    ''')
    assert actual == expected

    toast = Toast(
        description="somedescr",
        hide_delay=1,
    )
    actual = HelperHTMLParser.parse(str(toast))
    expected = HelperHTMLParser.parse(f'''
        <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 10">
            <div id="{toast.identifier}"
                class="toast align-items-center"
                role="alert"
                aria-live="assertive"
                aria-atomic="true"
                data-bs-autohide="true"
                data-bs-delay=1>
                <div class="d-flex">
                    <div class="toast-body">
                        somedescr
                    </div>
                    <button type="button"
                        class="btn-close me-2 m-auto"
                        data-bs-dismiss="toast"
                        aria-label="Close">
                    </button>
                </div>
            </div>
        </div>
    ''')
    assert actual == expected

    with pytest.raises(ValueError):
        Toast(
            description="somedescr",
            hide_delay=-1,
        )
