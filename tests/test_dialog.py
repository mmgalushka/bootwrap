"""
Test for bootwrap/components/image.py
"""

import pytest

from bootwrap import Dialog, Button
from .helper import HelperHTMLParser


@pytest.mark.dialog
def test_without_dialog():
    # When a dialog without action, means that specific action must be
    # incorporated into the dialog content.
    dialog = Dialog(
        'sometitle',
        Button('submit').submit()
    ).as_primary()
    actual = HelperHTMLParser.parse(str(dialog))
    expected = HelperHTMLParser.parse(f'''
        <div id="{dialog.identifier}" class="modal">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title text-primary">
                            sometitle
                        </h5>
                        <button type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close">
                            
                        </button>
                    </div>
                    <div class="modal-body">
                        <button id="..."
                            class="btn"
                            type="submit">
                            submit
                        </button>
                    </div>
                </div>
            </div>
        </div>
    ''')
    assert actual == expected


@pytest.mark.dialog
def test_with_dialog():
    dialog = Dialog(
        'sometitle',
        'somecontent',
        Button('Close').dismiss()
    ).as_primary()
    actual = HelperHTMLParser.parse(str(dialog))
    expected = HelperHTMLParser.parse(f'''
        <div id="{dialog.identifier}" class="modal">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title text-primary">
                            sometitle
                        </h5>
                        <button type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close">
                            
                        </button>
                    </div>
                    <div class="modal-body">
                        somecontent
                    </div>
                    <div class="modal-footer">
                        <button id="..."
                            class="btn"
                            type="button"
                            data-bs-dismiss="modal"
                            onclick="return false;">
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    ''')
    assert actual == expected
