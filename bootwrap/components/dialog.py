"""
A dialog
"""

from .base import (
    WebComponent,
    AppearanceMixin
)
from .utils import inject

__all__ = [ 'Dialog' ]


class Dialog( WebComponent, AppearanceMixin):
    """A dialog.

    Args:
        title (str): The dialog title.
        message (str): The dialog message.
        actions (obj): The dialog actions (default=None).
    """
    def __init__(self, title, message, actions=None):
        super().__init__()
        self.__title = title
        self.__message = message
        self.__actions = actions

    def __str__(self):
        return f'''
            <div id="{self.identifier}" class="modal">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title text-{self._category}">
                                {self.__title}
                            </h5>
                            <button type="button" 
                                class="close"
                                data-dismiss="modal"
                                aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <p>
                                {self.__message}
                            </p>
                        </div>
                        <div class="modal-footer">
                            {inject(*self.__actions)}
                        </div>
                    </div>
                </div>
            </div>
        '''