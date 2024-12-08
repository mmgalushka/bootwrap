"""
A toast (popping out message).
"""

from .base import WebComponent, ClassMixin, AppearanceMixin, OutlineMixin
from .anchor import Anchor
from .button import Button
from .text import Text
from .utils import attr, inject


class Toast(WebComponent, ClassMixin, AppearanceMixin, OutlineMixin):
    """A toast.

    Args:
        title (str|WebComponent): The item title.
        description (str|WebComponent): The item description.
        marker (str|WebComponent): The item marker.
        figure (str|WebComponent): The item figure.

    Example:
        from bootwrap import Panel, Toast, Button, Icon, Text, Javascript

        tst_example = Toast(
            title="Bootwrap",
            description="Hello, world! This is a toast message.",
            marker="11 mins ago",
            figure=Icon("fa-solid fa-info"),
        )
        btn_show_toast = Button("Show toast")

        action = Javascript(
            script='''
            $("#btn_show_toast").on("click",function(){
                $("#tst_example").toast("show");
            });
            ''',
            submap={
                "tst_example": tst_example,
                "btn_show_toast": btn_show_toast,
            }
        )

        output = Panel(
            tst_example,
            btn_show_toast,
            action
        )
    """

    def __init__(self, title=None, description=None, marker=None, figure=None, hide_delay=None):
        super().__init__()
        self._title =  title
        self._description = description
        self._marker = marker
        self._figure = figure
        self._hide_delay = hide_delay
        if self._hide_delay is not None:
            if self._hide_delay < 0:
                raise ValueError(
                    f"The toast delay must be grater or equal to 0, but got: {hide_delay}"
                )
        
    def __str__(self):
        self.add_classes("toast")

        if self._border:
            self.add_classes(f'border')
            if self._category:
                self.add_classes(f'border-{self._category}')
                self.add_classes(f'text-{self._category}')
        else:
            if self._category:
                self.add_classes(f'text-bg-{self._category}')

        if self._hide_delay is None:
            autohide = "true"
        else:
            if self._hide_delay == 0:
                autohide = "false"
                self._hide_delay = None
            else:
                autohide = "true"

        wc_title = self._title
        if wc_title:
            if isinstance(wc_title, str):
                wc_title = Text(wc_title)
            if isinstance(wc_title, Text):
                wc_title.as_strong()
            wc_title.add_classes("me-auto")

            wc_marker = self._marker
            if wc_marker:
                if isinstance(wc_marker, str):
                    wc_marker = Text(wc_marker)
                if isinstance(wc_marker, Text):
                    wc_marker.as_small()

            wc_figure = self._figure
            if wc_figure:
                wc_figure.add_classes("me-2")

            return f'''
                <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 10">
                    <div {attr("id", self.identifier)}
                        {attr('class', self.classes)}
                        role="alert"
                        aria-live="assertive"
                        aria-atomic="true"
                        {attr('data-bs-autohide', autohide)}
                        {attr('data-bs-delay', self._hide_delay)}>
                        <div class="toast-header">
                            {inject(self._figure)}
                            {inject(wc_title)}
                            {inject(wc_marker)}
                            <button type="button"
                                class="btn-close"
                                data-bs-dismiss="toast"
                                aria-label="Close">
                            </button>
                        </div>
                        <div class="toast-body">
                            {inject(self._description)}
                        </div>
                    </div>
                </div>
            '''
        else:
            self.add_classes("align-items-center")
            return f'''
                <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 10">
                    <div {attr("id", self.identifier)}
                        {attr('class', self.classes)}
                        role="alert"
                        aria-live="assertive"
                        aria-atomic="true"
                        {attr('data-bs-autohide', autohide)}
                        {attr('data-bs-delay', self._hide_delay)}>
                        <div class="d-flex">
                            <div class="toast-body">
                                {inject(self._description)}
                            </div>
                            <button type="button"
                                class="btn-close me-2 m-auto"
                                data-bs-dismiss="toast"
                                aria-label="Close">
                            </button>
                        </div>
                    </div>
                </div>
            '''