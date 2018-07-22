# -*- coding: utf-8 -*-
"""
Implementation of the media key capture.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import warnings

with warnings.catch_warnings():
    # This produces lots of DeprecationWarnings on Python 3.7,
    # and there's nothing we can do about it.
    warnings.simplefilter('ignore')
    from Foundation import NSAutoreleasePool
    from Cocoa import NSEvent
    from Cocoa import NSEventSubtypeScreenChanged

    import Quartz

    from Quartz import CGEventTapCreate
    from Quartz import CFRunLoopRun
    from Quartz import CFRunLoopAddSource
    from Quartz import CFRunLoopGetCurrent
    from Quartz import CFMachPortCreateRunLoopSource

    from Quartz import kCFRunLoopCommonModes
    from Quartz import kCFAllocatorDefault
    from Quartz import kCGSessionEventTap
    from Quartz import kCGHeadInsertEventTap
    from Quartz import kCGEventTapOptionDefault

    from ScriptingBridge import SBApplication
    from PyObjCTools import AppHelper

# IOHIDSystem
NX_SYSDEFINED = 14
NX_SYSDEFINEDMASK = (1 << NX_SYSDEFINED)

# IOHIDFamily ev_keymap.h
NX_KEYTYPE_PLAY = 16
NX_KEYTYPE_NEXT = 17
NX_KEYTYPE_PREVIOUS =	18
NX_KEYTYPE_FAST	= 19
NX_KEYTYPE_REWIND = 20

_MEDIA_KEYS = {
    NX_KEYTYPE_PLAY: 'play',
    NX_KEYTYPE_NEXT: 'next',
    NX_KEYTYPE_PREVIOUS: 'previous',
    NX_KEYTYPE_FAST: 'fast',
    NX_KEYTYPE_REWIND: 'rewind',
}

# itunes also supports fastForward and rewind
# actions, but no keyboard has keys for both next and fast
# and rewind and previous. The internal laptop keyboard
# generates rewind and fastForward, my external keyboard
# generates next and previous. The original HighSierraMediaKeyEnabler
# detects key down/key events and uses a state machine to
# determine when to generate next vs fastForward. However, I have
# never wanted to fastForward or rewind, only to move by track,
# so that's all I do here.
_MEDIA_ACTIONS = {
    NX_KEYTYPE_PLAY: 'playpause',

    NX_KEYTYPE_NEXT: 'nextTrack',
    NX_KEYTYPE_FAST: 'nextTrack',

    NX_KEYTYPE_PREVIOUS: 'backTrack',
    NX_KEYTYPE_REWIND: 'backTrack',

}

logger = __import__('logging').getLogger(__name__)

_cg_event_type_to_str = {
    getattr(Quartz, name): name
    for name in dir(Quartz)
    if name.startswith('kCGEvent')
}
_cg_event_type_to_str[NX_SYSDEFINED] = 'NX_SYSDEFINED'

_ns_event_subtype_to_str = {
    getattr(Quartz, name): name
    for name in dir(Quartz)
    if name.startswith('NSEventSub')
}

def tap_event_callback(_tap_proxy, event_type, event_ref, _user_info):
    if event_type != NX_SYSDEFINED:
        return event_ref
    pool = NSAutoreleasePool.alloc().init()

    try:
        event = NSEvent.eventWithCGEvent_(event_ref)

        if event.subtype() != NSEventSubtypeScreenChanged:
            # value of 8, for some reason.
            return event_ref # pragma: no cover

        key_code = (event.data1() & 0xFFFF0000) >> 16
        if key_code not in _MEDIA_KEYS:
            return event_ref # pragma: no cover

        iTunes = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
        if not iTunes.isRunning():
            return event_ref # pragma: no cover

        key_flags = event.data1() & 0x0000FFFF
        key_is_pressed = (((key_flags & 0xFF00) >> 8)) == 0xA

        if key_is_pressed:
            meth_name = _MEDIA_ACTIONS[key_code]
            getattr(iTunes, meth_name)()

    finally:
        del pool

def _make_tap_port():
    port = CGEventTapCreate(
        # Listen for events in this login section
        kCGSessionEventTap,
        # Get them first
        kCGHeadInsertEventTap,
        # We are an active filter
        kCGEventTapOptionDefault,
        # Events from the system
        NX_SYSDEFINEDMASK,
        # event handler
        tap_event_callback,
        # no data
        None)
    return port

def _make_run_loop_source(port):
    source = CFMachPortCreateRunLoopSource(kCFAllocatorDefault,
                                           port,
                                           0)
    assert source is not None
    CFRunLoopAddSource(CFRunLoopGetCurrent(),
                       source,
                       kCFRunLoopCommonModes)
    return source

def _run_run_loop():
    CFRunLoopRun()

def main():
    # This gets Ctrl-C handling working when we're in the
    # CFRunLoop.
    AppHelper.installMachInterrupt()

    port = _make_tap_port()
    assert port is not None
    run_source = _make_run_loop_source(port)

    assert run_source is not None
    _run_run_loop()


if __name__ == '__main__':
    main()
