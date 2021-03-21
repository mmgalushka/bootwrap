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
    """A web-component for a table.

    Args:
        head (list): The table head (1D array).
        body (list): The table body (2D array).
    """
    def __init__(self, head, body):
        super().__init__()

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
                """Makes the table head appears as light gray."""
                self.__class = 'thead-light'

            def as_dark(self):
                """Makes the table head appears as dark gray."""
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
                        if self.__trans[column][TableEntity.CELL] is not None:
                            return self.__trans[column][TableEntity.CELL](
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

        self.__head = Head(head)
        self.__body = Body(body)

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
            self
        """
        self.add_classes('table-striped')
        return self

    def as_bordered(self):
        """Adds borders on all sides of the table and cells.

        Returns:
            self
        """
        self.add_classes('table-bordered')
        return self

    def as_small(self):
        """Make tables more compact by cutting cell padding in half.

        Returns:
            self
        """
        self.add_classes('table-sm')
        return self

    def as_dark(self):
        """Inverts the colors—with light text on dark backgrounds.

        Returns:
            self
        """
        self.add_classes('table-dark')
        return self

    def as_responsive(self, breakpoint=Breakpoint.SM):
        """Create responsive tables.

        Args:
            breakpoint (str): The breakpoint to apply.

        Returns:
            self
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
