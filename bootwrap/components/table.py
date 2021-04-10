"""
A table.
"""

from enum import Enum

from .base import WebComponent, ClassMixin, Breakpoint
from .utils import inject, attr


class TableEntity(Enum):
    """The body entity to enumerator."""
    VALUE = 'value'
    """The cell value"""
    CELL = 'cell'
    """The cell class"""
    ROW = 'row'
    """The row class"""


class Table(WebComponent, ClassMixin):
    """A web component for a table.

    Args:
        head (list): The table head (1D array).
        body (list): The table body (2D array).

    Example:
        from bootwrap import Table

        Table(
            ["Column 1", "Column 2", "Column 3"],
            [
                ["Value 11", "Value 12", "Value 13"],
                ["Value 21", "Value 22", "Value 23"],
                ["Value 31", "Value 32", "Value 33"],
            ]
        )

    Demo:
        from bootwrap import Table

        output = Table(
            ["Column 1", "Column 2", "Column 3"],
            [
                ["Value 11", "Value 12", "Value 13"],
                ["Value 21", "Value 22", "Value 23"],
                ["Value 31", "Value 32", "Value 33"],
            ]
        )
    """
    def __init__(self, head, body):
        super().__init__()
        self.__head = Table.Head(head)
        self.__body = Table.Body(body)

    class Head(WebComponent):
        """The table head."""
        def __init__(self, head):
            if head is None:
                self.__head = []
            else:
                if not isinstance(head, list):
                    raise TypeError(
                        'Parameter "head" must be 1D <list>,'
                        f' but got {type({head})};'
                    )
                self.__head = head
            self.__class = None

        def __len__(self):
            return len(self.__head)

        def as_light(self):
            """Makes the table head appears as light gray.

            Example:
                from bootwrap import Table

                table = Table(
                    ["Column 1", "Column 2", "Column 3"],
                    [
                        ["Value 11", "Value 12", "Value 13"],
                        ["Value 21", "Value 22", "Value 23"],
                        ["Value 31", "Value 32", "Value 33"],
                    ]
                )
                table.head.as_light()

            Demo:
                from bootwrap import Table

                table = Table(
                    ["Column 1", "Column 2", "Column 3"],
                    [
                        ["Value 11", "Value 12", "Value 13"],
                        ["Value 21", "Value 22", "Value 23"],
                        ["Value 31", "Value 32", "Value 33"],
                    ]
                )
                table.head.as_light()

                output = table
            """
            self.__class = 'thead-light'

        def as_dark(self):
            """Makes the table head appears as dark gray.

            Example:
                from bootwrap import Table

                table = Table(
                    ["Column 1", "Column 2", "Column 3"],
                    [
                        ["Value 11", "Value 12", "Value 13"],
                        ["Value 21", "Value 22", "Value 23"],
                        ["Value 31", "Value 32", "Value 33"],
                    ]
                )
                table.head.as_dark()

            Demo:
                from bootwrap import Table

                table = Table(
                    ["Column 1", "Column 2", "Column 3"],
                    [
                        ["Value 11", "Value 12", "Value 13"],
                        ["Value 21", "Value 22", "Value 23"],
                        ["Value 31", "Value 32", "Value 33"],
                    ]
                )
                table.head.as_dark()

                output = table
            """
            self.__class = 'thead-dark'

        def __str__(self):
            if len(self) == 0:
                return ''
            else:
                columns = []
                for name in self.__head:
                    columns.append(f'''
                        <th scope="col">{name}</th>
                    ''')
                return f'''
                    <thead {attr('class', self.__class)}>
                        <tr>
                            {inject(*columns)}
                        </tr>
                    </thead>
                '''

    class Body(WebComponent):
        """The table body."""
        def __init__(self, body):
            if body is None:
                self.__body = []
            else:
                if not isinstance(body, list):
                    raise TypeError(
                        'Parameter "body" must be 2D <list>,'
                        f' but got {type({body})};'
                    )
                self.__body = body
            self.__trans = {}

        def __len__(self):
            return len(self.__body)

        def transform(self, index, entity, fn):
            """Defines a function to transform a cell value

            Args:
                index (int): The column index to which transformation
                    is applied;
                entity (Entity): The entity to which transformation
                    is applied;
                fn (func): The function to use for transformation.

            Example:
                from bootwrap import Table, TableEntity, Text

                table = Table(
                    ["Column 1", "Column 2", "Column 3"],
                    [
                        ["val1", "int", "this is a description for val1;"],
                        ["val2", "str", "this is a description for val2;"],
                        ["val3", "bool", "this is a description for val3;"],
                    ]
                )

                table.body.transform(
                    0,
                    TableEntity.CELL,
                    lambda v: "font-weight-bold" if v.startswith("val") else ""
                )

                table.body.transform(
                    0,
                    TableEntity.ROW,
                    lambda v: "bg-warning" if v == "val2" else ""
                )

                table.body.transform(
                    1,
                    TableEntity.VALUE,
                    lambda v: f"<code>{v}</code>"

            Demo:
                from bootwrap import Table, TableEntity, Text

                table = Table(
                    ["Column 1", "Column 2", "Column 3"],
                    [
                        ["val1", "int", "this is a description for val1;"],
                        ["val2", "str", "this is a description for val2;"],
                        ["val3", "bool", "this is a description for val3;"],
                    ]
                )

                table.body.transform(
                    0,
                    TableEntity.CELL,
                    lambda v: "font-weight-bold" if v.startswith("val") else ""
                )

                table.body.transform(
                    0,
                    TableEntity.ROW,
                    lambda v: "bg-warning" if v == "val2" else ""
                )

                table.body.transform(
                    1,
                    TableEntity.VALUE,
                    lambda v: f"<code>{v}</code>"
                )

                output = table
            """
            if index not in self.__trans:
                self.__trans[index] = {
                    TableEntity.VALUE: None,
                    TableEntity.CELL: None,
                    TableEntity.ROW: None
                }
            if self.__trans[index][entity] is None:
                self.__trans[index][entity] = fn
            else:
                raise ValueError(
                    f'The transformation for {entity} in column {index} '
                    'already defined;'
                )

        def __str__(self):
            def get_cell_value(column, value):
                if column in self.__trans:
                    if self.__trans[column][TableEntity.VALUE] is not None:
                        return self.__trans[column][TableEntity.VALUE](
                            value
                        )
                return value

            def get_cell_classes(column, value):
                if column in self.__trans:
                    if self.__trans[column][TableEntity.CELL] is not None:
                        return self.__trans[column][TableEntity.CELL](
                            value
                        )
                return ''

            def get_row_classes(column, value):
                if column in self.__trans:
                    if self.__trans[column][TableEntity.ROW] is not None:
                        return self.__trans[column][TableEntity.ROW](
                            value
                        )
                return ''

            if len(self) == 0:
                return ''
            else:
                records = []
                for row in self.__body:
                    row_classes = []
                    record = []
                    for column, value in enumerate(row):
                        cell_value = get_cell_value(column, value)
                        cell_classes = get_cell_classes(column, value)
                        row_classes.append(
                            get_row_classes(column, value)
                        )

                        if len(record) == 0:
                            record.append(f'''
                                <td scope="row"
                                    {attr("class", cell_classes)}>
                                    {cell_value}
                                </td>
                            ''')
                        else:
                            record.append(f'''
                                <td {attr("class", cell_classes)}>
                                    {cell_value}
                                </td>
                            ''')
                    records.append(f'''
                        <tr {attr("class", " ".join(row_classes))}>
                            {"".join(record)}
                        </tr>
                    ''')

                return f'''
                    <tbody>
                        {inject(*records)}
                    </tbody>
                '''

    @property
    def head(self):
        """The table head."""
        return self.__head

    @property
    def body(self):
        """The table body."""
        return self.__body

    def as_striped(self):
        """Adds zebra-striping to any table row within the table body.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Table

            Table(
                ["Column 1", "Column 2", "Column 3"],
                [
                    ["Value 11", "Value 12", "Value 13"],
                    ["Value 21", "Value 22", "Value 23"],
                    ["Value 31", "Value 32", "Value 33"],
                ]
            ).as_striped()

        Demo:
            from bootwrap import Table

            output = Table(
                ["Column 1", "Column 2", "Column 3"],
                [
                    ["Value 11", "Value 12", "Value 13"],
                    ["Value 21", "Value 22", "Value 23"],
                    ["Value 31", "Value 32", "Value 33"],
                ]
            ).as_striped()
        """
        self.add_classes('table-striped')
        return self

    def as_bordered(self):
        """Adds borders on all sides of the table and cells.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Table

            Table(
                ["Column 1", "Column 2", "Column 3"],
                [
                    ["Value 11", "Value 12", "Value 13"],
                    ["Value 21", "Value 22", "Value 23"],
                    ["Value 31", "Value 32", "Value 33"],
                ]
            ).as_bordered()

        Demo:
            from bootwrap import Table

            output = Table(
                ["Column 1", "Column 2", "Column 3"],
                [
                    ["Value 11", "Value 12", "Value 13"],
                    ["Value 21", "Value 22", "Value 23"],
                    ["Value 31", "Value 32", "Value 33"],
                ]
            ).as_bordered()
        """
        self.add_classes('table-bordered')
        return self

    def as_small(self):
        """Make tables more compact by cutting cell padding in half.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Table

            Table(
                ["Column 1", "Column 2", "Column 3"],
                [
                    ["Value 11", "Value 12", "Value 13"],
                    ["Value 21", "Value 22", "Value 23"],
                    ["Value 31", "Value 32", "Value 33"],
                ]
            ).as_small()

        Demo:
            from bootwrap import Table

            output = Table(
                ["Column 1", "Column 2", "Column 3"],
                [
                    ["Value 11", "Value 12", "Value 13"],
                    ["Value 21", "Value 22", "Value 23"],
                    ["Value 31", "Value 32", "Value 33"],
                ]
            ).as_small()
        """
        self.add_classes('table-sm')
        return self

    def as_dark(self):
        """Inverts the colors—with light text on dark backgrounds.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Table

            Table(
                ["Column 1", "Column 2", "Column 3"],
                [
                    ["Value 11", "Value 12", "Value 13"],
                    ["Value 21", "Value 22", "Value 23"],
                    ["Value 31", "Value 32", "Value 33"],
                ]
            ).as_dark()

        Demo:
            from bootwrap import Table

            output = Table(
                ["Column 1", "Column 2", "Column 3"],
                [
                    ["Value 11", "Value 12", "Value 13"],
                    ["Value 21", "Value 22", "Value 23"],
                    ["Value 31", "Value 32", "Value 33"],
                ]
            ).as_dark()
        """
        self.add_classes('table-dark')
        return self

    def as_responsive(self, breakpoint=Breakpoint.SM):
        """Create responsive tables.

        Args:
            breakpoint (str): The breakpoint to apply.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Table

            Table(
                ["Column 1", "Column 2", "Column 3"],
                [
                    ["Value 11", "Value 12", "Value 13"],
                    ["Value 21", "Value 22", "Value 23"],
                    ["Value 31", "Value 32", "Value 33"],
                ]
            ).as_responsive()

        Demo:
            from bootwrap import Table

            output = Table(
                ["Column 1", "Column 2", "Column 3"],
                [
                    ["Value 11", "Value 12", "Value 13"],
                    ["Value 21", "Value 22", "Value 23"],
                    ["Value 31", "Value 32", "Value 33"],
                ]
            ).as_responsive()
        """
        self.add_classes(f'table-responsive-{breakpoint}')
        return self

    def __str__(self):
        classes = 'table'
        if self.classes:
            classes += f' {self.classes}'

        return f'''
            <table id="{self.identifier}"
                {attr('class', classes)}>
                {self.__head} {self.__body}
            </table>
        '''
