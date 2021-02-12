"""
A table.
"""

from .base import (
    WebComponent,
    ClassMixin
)
from .utils import inject, attr

__all__ = [ 'Table' ]


class Table(WebComponent, ClassMixin):
    """A web-component for a table.

    Args:
        head (list): The table head (1D array).
        body (list): The table body (2D array).
    """
    def __init__(self, head, body):
        super().__init__()
        if head is None:
            raise TypeError(
                f'Parameter "head" must be defined, but got None;'
            )
        else:
            if not isinstance(head, list):
                raise TypeError(
                    'Parameter "head" must be 1D <list>,'
                    f' but got {type({head})};'
                )
        self.__head = head

        if body is None:
            raise TypeError(
                f'Parameter "body" must be defined, but got None;'
            )
        else:
            if not isinstance(body, list):
                raise TypeError(
                    'Parameter "body" must be 2D <list>,'
                    f' but got {type({body})};'
                )
        self.__body = body

    def __str__(self):
        columns = []
        for name in self.__head:
            columns.append(f'''
                <th scope="col">{name}</th>
            ''')
        thead = f'''
            <thead>
                <tr>
                    {inject(*columns)}
                </tr>
            </thead>
        '''

        records = []
        for row in self.__body:
            record = []
            for value in row:
                if len(record) == 0:
                    record.append(f'<td scope="row">{value}</td>')
                else:
                    record.append(f'<td>{value}</td>')
            records.append(f'<tr>{"".join(record)}</tr>')

        tbody = f'''
            <tbody>
                {inject(*records)}
            </tbody>
        '''

        classes = 'table'
        if self.classes:
            classes += f' {self.classes}'

        return f'''
            <table id="{self.identifier}"
                {attr('class', classes)}>
                {thead} {tbody}
            </table>
        '''