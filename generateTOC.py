#!/usr/bin/env python3

"""Wrapper script delegating to the reusable TOC generator package.

All logic lives inside the ``toc_generator`` package so it can be
installed and imported from other projects in the future.
"""

import sys

from toc_generator.cli import main

if __name__ == "__main__":
    sys.exit(main())
