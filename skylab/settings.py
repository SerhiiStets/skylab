"""Skylab const and settings module."""

import os

import tzlocal

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_TIMEZONE = tzlocal.get_localzone()
CSS_PATH = os.path.join(CURR_DIR, "css/styles.css")
