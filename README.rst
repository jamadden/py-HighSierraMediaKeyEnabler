=================================
 Media Keys on macOS High Sierra
=================================

This project is a version of `HighSierraMediaKeyEnabler`_ written in
Python for simplicity using PyObjC.

In short, it makes it so that Safari cannot steal the media keys: the
media keys always control iTunes. (I usually have TweetDeck open in a
Safari window, and if TweetDeck has tried to send a notification,
Safari would grab the media keys to just replay the tweet sound; the
only way to get them back to iTunes was to click the mouse---ugh!)

Using
=====

After installing, you will have a command ``mediakeyenabler``. Run it.
End it with Ctrl-C or sending the equivalent signal to the PID.

Known Limitations
=================

- I don't use spotify, so this only supports iTunes.
- I don't ever want it to start iTunes, so it only does anything if
  iTunes is already running.
- I've never wanted to fast forward or rewind, only restart the track
  or go to the next one (in fact I didn't know FF and rewind were
  possible) so this program doesn't do that.
- No GUI (at least not yet), it's just a command line program.

Known Limitations in the Original
=================================

There are some known limitations in the original that this project
inherites due to the basic design using a CGEventTap. Notably, certain
operations cannot be done when the program is running:

- Changing the Safari search engine (`issue 43`_)
- Enabling kernel extensions (`issue 42`_)

If those are fixed in the original, they might get fixed here.

.. _HighSierraMediaKeyEnabler: https://github.com/milgra/highsierramediakeyenabler
.. _issue 43: https://github.com/milgra/highsierramediakeyenabler/issues/43
.. _issue 42: https://github.com/milgra/highsierramediakeyenabler/issues/42
