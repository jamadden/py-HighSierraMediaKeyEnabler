# -*- coding: utf-8 -*-
"""
Tests for mediakeyenabler.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest
try:
    from unittest import mock
except ImportError: # pragma: no covers
    # Python 2
    import mock

import objc
from scs import mediakeyenabler

class TestSetupFunctions(unittest.TestCase):

    def test_make_tap_port(self):
        port = mediakeyenabler._make_tap_port()
        self.assertIsNotNone(port)

    def test_make_run_loop_source(self):
        port = mediakeyenabler._make_tap_port()
        source = mediakeyenabler._make_run_loop_source(port)
        self.assertIsNotNone(source)

    @mock.patch('scs.mediakeyenabler.CFRunLoopRun')
    def test_main(self, _mock_run):
        mediakeyenabler.main()

PLAY_KEY_DOWN_DATA = (
    b"\x00\x00\x00\x02\x00\x01@5"
    b"\x00\x00\x00\x03\x00\x01@6\x00\x00\x00\x00\x00\x01@7\x00\x00\x00"
    b"\x0e\x00\x02\xc08D\xea\xdf\x00Db\xa7\x00\x00\x02\xc09\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x01\x00:\xb5;\xb2M\x00\x01@P\x00\x01@;\x00"
    b"\x00\x01\x00\x00\x01@3\x00\x00\x00\x00\x00\x01@4\x00\x00\x00\x00\x00"
    b"\x01\x00\xa9\xb5;\xb2M\x00\x01@P\x00\x01@j\x00\x00\x00\x00\x00\x01@k"
    b"\x00\x00\x05\xa0\x00\x01@S\x00\x00\x00\x08\x00\x0f@T\x00\x10\n\x00"
    b"\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
)

class TestCallback(unittest.TestCase):

    def test_invalid_event_type(self):
        result = mediakeyenabler.tap_event_callback(
            None,
            -1,
            self,
            None
        )
        self.assertIs(result, self)

    def test_invalid_event_ref_exception(self):
        with self.assertRaises(objc.error) as exc:
            mediakeyenabler.tap_event_callback(
                None,
                mediakeyenabler.NX_SYSDEFINED,
                None,
                None
            )

        self.assertIn("eventWithCGEvent", exc.exception.args[0])

    @mock.patch("scs.mediakeyenabler.SBApplication")
    def test_play_key_down(self, _mock_application):
        # Python 3 can directly pass the byte string to CGEventCreateFromData,
        # but on Python 2 we need to make a CFDataRef
        data = mediakeyenabler.Quartz.CFDataCreate(None, PLAY_KEY_DOWN_DATA, len(PLAY_KEY_DOWN_DATA))
        event_ref = mediakeyenabler.Quartz.CGEventCreateFromData(None, data)
        mediakeyenabler.tap_event_callback(
            None,
            mediakeyenabler.NX_SYSDEFINED,
            event_ref,
            None
        )
