"""
A dialog
"""

from .base import WebComponent, AppearanceMixin
from .utils import inject


class Dialog(WebComponent, AppearanceMixin):
    """A dialog.

    Args:
        title (str): The dialog title.
        content (str|WebComponent): The content inside a dialog window to show.
        *actions (list): The dialog actions.

    Example:
        from bootwrap import Dialog, Button

        dialog = Dialog(
            'Greeting',
            'Hello World!',
            Button('Bye').dismiss()
        )
        button = Button('Say Hello').toggle(dialog)

    Demo:
        from bootwrap import Panel, Dialog, Button

        dialog = Dialog(
            'Greeting',
            'Hello World!',
            Button('Bye').dismiss()
        )
        button = Button('Say Hello').toggle(dialog)

        output = Panel(dialog, button)
    """
    def __init__(self, title, content, *actions):
        super().__init__()
        self.__title = title
        self.__content = content
        self.__actions = actions

    def __str__(self):
        modal_footer = None
        if len(self.__actions) > 0:
            modal_footer = f'''
                <div class="modal-footer">
                    {inject(*self.__actions)}
                </div>
            '''

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
                            {inject(self.__content)}
                        </div>
                        {inject(modal_footer)}
                    </div>
                </div>
            </div>
        '''
