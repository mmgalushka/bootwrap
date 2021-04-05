import re
import inspect


def prettify(text):
    pattern = re.compile(r"\`[A-Za-z._\(\)]+\`")

    p = 0
    new_text = ''
    for m in pattern.finditer(text):
        s, e = m.span()
        new_text += text[p:s]
        new_text += ('<code>' + m.group(0)[1:-1] + '</code>')
        p = e
    new_text += text[p:]
    return new_text


def get_params(text):
    """Returns docstring parameters.

    Args:
        text (str): The raw docstring for extracting parameters.

    Returns:
        parameters (list): The extracted parameters.
    """
    pat = re.compile(r"\s*([A-Za-z_]+)\s*\(([A-Za-z_\|\.\<\>]+)\)\s*:\s*")

    tokens = []
    for m in pat.finditer(text):
        s, e = m.span()
        name, type_ = m.group(1).strip(), m.group(2).strip()
        tokens.append((s, e, name, type_))
    tokens.append((len(text), None, None, None))

    parameters = []
    for cur, nxt in zip(tokens, tokens[1:]):
        _, s, n, t = cur
        e, _, _, _ = nxt
        d = text[s:e].strip()
        parameters.append([n, t, d])
    return parameters


def get_sections(text):
    """Returns docstring sections.

    Args:
        text (str): The raw docstring for extracting sections.

    Returns:
        sections (list): The extracted sections.
    """
    pattern = re.compile(
        r"(?<=\s)(Args|Returns|Example|Demo)\s*:\n", flags=re.S
    )

    sections = []
    if text is not None:
        tokens = []
        tokens.append((None, 0, 'Overview'))
        for m in pattern.finditer(text):
            s, e = m.span()
            header = m.group(0)[:-2]
            tokens.append((s, e, header))
        tokens.append((len(text), None, None))

        for cur, nxt in zip(tokens, tokens[1:]):
            _, s, header = cur
            e, _, _ = nxt
            body = text[s:e]
            sections.append({'header': header, 'body': body})
    return sections


def parse_docstring(text):
    """Parses the raw Python-docstring.

    This string can belong to a class or a method.

    Args:
        text (str): The raw Python-docstring to parse.

    Returns:
        doc (dict): The arranged docstring elements.
    """
    overview, example, demo = '', '', ''
    arguments, returns = [], []
    for section in get_sections(prettify(str(text))):
        if section['header'] == 'Args':
            arguments.extend(get_params(section['body']))
        elif section['header'] == 'Returns':
            returns.extend(get_params(section['body']))
        elif section['header'] in ['Example']:
            example = section['body']
        elif section['header'] in ['Demo']:
            demo = section['body']
        elif section['header'] in ['Overview']:
            overview = section['body']
        else:
            continue

    paragraphs = list(map(str.strip, overview.split('\n\n')))
    paragraphs = list(filter(lambda x: len(x) > 0, paragraphs))

    summary = ''
    if len(paragraphs) > 0:
        summary = paragraphs[0]

    description = []
    if len(paragraphs) > 1:
        description = paragraphs[1:]

    return {
        'summary': summary,
        'description': description,
        'arguments': arguments,
        'returns': returns,
        'example': example,
        'demo': demo
    }


def generate_method_doc(m):
    """Generates the specified method documentation from docstring.

    Args:
        m (method): The method for generating documentation.

    Returns:
        doc (dict): The The docstring element arranged as a dictionary.
    """
    doc = parse_docstring(m.__doc__)
    return {
        'name': m.__name__,
        'init': str(inspect.signature(m))
        .replace('self, ', '').replace('self', ''),
        'summary': doc['summary'],
        'description':  doc['description'],
        'arguments': doc['arguments'],
        'returns': doc['returns'],
        'example': doc['example'],
        'demo': doc['demo']
    }


def generate_class_doc(c):
    """Generates the specified class documentation from docstring.

    Args:
        c (class): The class for generating documentation.

    Returns:
        doc (dict): The The docstring element arranged as a dictionary.
    """
    doc = parse_docstring(c.__doc__)
    methods = []
    for func in inspect.getmembers(c, predicate=inspect.isroutine):
        m = func[0]
        if callable(getattr(c, m)) and not m.startswith('_'):
            try:
                if m not in c.__dict__:
                    # Not defined in class: method inherited;
                    continue
                elif hasattr(super(c), m):
                    # Present in parent : method overloaded;
                    methods.append(generate_method_doc(getattr(c, m)))
                else:
                    # Not present in parent : newly defined method;
                    methods.append(generate_method_doc(getattr(c, m)))
            except NameError:
                continue

    return {
        'name': c.__qualname__,
        'super': [],
        'init': str(inspect.signature(c.__init__))
        .replace('self, ', '').replace('self', ''),
        'summary': doc['summary'],
        'description':  doc['description'],
        'arguments': doc['arguments'],
        'returns': [],
        'example': doc['example'],
        'demo': doc['demo'],
        'methods': methods
    }
