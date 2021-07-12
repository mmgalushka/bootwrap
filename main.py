"""
The Bootwrap command launcher.
"""

import sys
import argparse

from docs import doc_app, doc_to_html
from demo import demo_app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'action',
        choices=['preview', 'docs', 'demo'],
        help='action to run'
    )

    args = parser.parse_args(sys.argv[1:])

    if args.action == 'preview':
        doc_app.run(debug=True)
    elif args.action == 'docs':
        doc_to_html()
    else:  # args.action == 'demo'
        demo_app.run(debug=True)
