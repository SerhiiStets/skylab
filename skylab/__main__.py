#!/usr/bin/env python3
"""Skylab entry point."""

from skylab import SkylabApp


def main():
    """Entry point for running skylab TUI."""
    app = SkylabApp()
    app.run()


if __name__ == "__main__":
    main()
