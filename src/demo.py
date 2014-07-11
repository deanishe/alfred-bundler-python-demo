#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-07-10
#

"""
An example of how to use the the Alfred Dependency Bundler with Python.

To use the Bundler, include `bundle.py` in your workflow. Get it here:

https://github.com/shawnrice/alfred-bundler/blob/aries/wrappers/bundler.py

This workflow uses the Alfred-Workflow library, which helps with a lot
of the mundane aspects of building a workflow (generating XML, debugging).

If you're thinking of writing an Alfred workflow in Python you should
*strongly* consider using this, or another, workflow library. They take
care of a lot of the boilerplate for you.

Alfred-Workflow can be found here:

https://github.com/deanishe/alfred-workflow

Brief overview of the Bundler
=============================

The Bundler allows you to use a number of common workflow utilities to do
add functionality to your workflow, such as showing notifications or dialog
boxes for user input, using common OS X utilities (such as terminal-notifier
or cocoaDialog) without every author needing to include the utilities in
their workflows.

There is also an icon API that allows you access to ~1000 icons in the
colour of your choice.

Finally, the Python version of the Bundler allows you to transparently
install any Python libraries your workflow needs (using Pip and its
requirements.txt) without the need to include large libraries with your
workflow.

Overview of this Demo
=====================

Please see the docstrings and comments in the `Demo` class for a
detailed explanation of how this demo works.

As well as demonstrating how to use `bundler.py`, this workflow also
shows one way you can structure your workflow code.

Full Bundler details
====================

More information on the default utilities and the JSON file format can be
found on the Bundler homepage:

http://shawnrice.github.io/alfred-bundler/

The complete documentation for the Python version is in the source code
of the `bundler.py` wrapper.

The currently available icons can be viewed here:

http://icons.deanishe.net/

"""

#=====================================================================
# Imports
#=====================================================================

# Importing `unicode_literals` means that instead of using u"string" to
# represent a Unicode string and "string" to represent a byte string in
# source code, "string" is a Unicode string and b"string" is a byte
# string. In most cases, this will make coding easier, but you still
# have to be sure to properly encode/decode Unicode and bytestrings, so
# your workflow doesn't die in flames when given non-ASCII text.
from __future__ import print_function, unicode_literals

import sys
import random
import argparse
# Needed to call utilities
import subprocess
# Needed to validate colours specified by user
import re

# Helper library
from workflow import Workflow, ICON_WARNING

# Font Awesome character list
import fontawesome

# bundler wrapper
import bundler

# Initialise the bundler
# This method call will ensure that the bundler is installed and
# will install any Python dependencies specified in `requirements.txt`.
# This may take several seconds the first time it's called from this
# workflow. Subsequent calls will be very fast.
#
# ONLY call this method if you have a `requirements.txt` file.
# The Bundler will also be installed if you call any other `bundler.py`
# functions.
#
# Info on the format of `requirements.txt` can be found here:
# https://pip.pypa.io/en/1.1/requirements.html
#
# Basically, just use the "pip name" of your library (i.e. the name
# you'd call `pip` with *not* what you `import`, though they're often
# the same) plus `==` and the version you require, e.g.:
#
# requests==2.3.0
# pytz==2014.4
#
# `bundler.py` will notice if your `requirements.txt` has changed and
# will update your dependencies. If it hasn't changed, it won't do anything
bundler.init()


#=====================================================================
# Defaults, other globals
#=====================================================================

# Default icon colour
COLOUR_DEFAULT = '444444'

# Regex to validate a CSS colour
VALID_COLOUR = re.compile(r'^[a-f0-9]*$', re.IGNORECASE).match

# Global Logger. It's set to a valid Logger from Python's standard
# `logging` library at the bottom of the script
log = None

# Similarly, we'll populate this with `Workflow`'s method of the same
# name. It's *very* important to ensure all input is decoded to Unicode
# and all output is encoded to UTF-8 text, or your workflow may die in
# flames when given non-ASCII text. *Always* test your workflow with
# non-ASCII text to ensure it works okay.
decode = None


# Utilities
#---------------------------------------------------------------------

# We'll also get any dependencies we need here to ensure they're
# installed on the first run. We don't want our workflow to randomly
# fail in the future because the computer/GitHub is offline the first
# time a particular utility is called. Again, this first call may take
# several seconds, as the requested utility may need to be installed
# (the Bundler will inform the user if this is the case) but subsequent
# calls will be *extremely* fast (the Python wrapper caches the results,
# so the actual Bundler is not called unless the requested utility has
# disappeared, i.e. been uninstalled)

# terminal-nofitier is a utility to display notifications
terminal_notifier = bundler.utility('terminal-notifier')

# Pashua is a utility to display dialogs to get input from the user
pashua = bundler.utility('Pashua')

# cocoaDialog is another utility for showing dialogs. It's not as
# configurable as Pashua, but also does simple error/message dialogs
# and progressbars.
# Either Pashua or cocoaDialog would be sufficient for the needs of
# this workflow, but as it's a demo, why not show how to use both?
cocoa_dialog = bundler.utility('cocoaDialog')

# Icons
#---------------------------------------------------------------------

# Normally, we'd also want to grab any icons we're going to use in the
# workflow in addition to the utilities (to ensure they're installed on
# first run), but as this workflow displays a random set of icons, this
# would most probably slow the workflow down on every single run until all
# 300+ icons are in the cache. Even then, if you change the colour (one of
# the functions of this demo), the whole caching business would start
# again.
#
# So just one sample icon this time.

icon_adjust = bundler.icon('adjust', 'fontawesome', COLOUR_DEFAULT)


#=====================================================================
# Implementation
#=====================================================================

# Helper functions
#---------------------------------------------------------------------

def notify(title, message):
    """Simple wrapper function around `terminal-notifier`

    `terminal-notifier` supports a lot of arguments, but this simple
    wrapper covers this workflow's needs.

    """
    log.debug('title: `{}`\tmessage: {}'.format(title, message))
    # Build a command for `subprocess` based on the path to
    # terminal-notifier we got from `bundler.py` at the top of
    # the script.
    cmd = [terminal_notifier, '-title', title, '-message', message]
    log.debug('cmd : {}'.format(cmd))
    return subprocess.call(cmd)


def show_error(title, message):
    """Simple wrapper around `cocoaDialog` to show an error dialog

    `cocoaDialog can do *a lot* more than this.

    """
    # cocoaDialog works fine without encoding its arguments
    cmd = [cocoa_dialog, 'ok-msgbox',
           '--title', 'Error',
           '--text', title,
           '--informative-text', message,
           '--button1', 'OK',
           '--icon-file', ICON_WARNING]
    subprocess.call(cmd)


# Workflow implementation
#---------------------------------------------------------------------

class Demo(object):
    """This class encapsulates the functionality of this Script Filter

    The `run` method is the entry point and takes care of command-line
    arguments and the query.

    The `do_*` methods implement the specific functionality of
    individual workflow actions.

    """

    def run(self, wf):
        """Main entry-point to the class"""
        # Workflow object from the Alfred-Workflow library.
        # More info at:
        # https://github.com/deanishe/alfred-workflow
        self.wf = wf
        # Build a parser to handle command-line arguments.
        # This workflow performs multiple actions from one script
        # and uses arguments to decide which one to run
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--icons', dest='action', action='store_const', const='icons')
        parser.add_argument(
            '--notify', dest='action', action='store_const',
            const='notify')
        parser.add_argument(
            '--colour', dest='action', action='store_const',
            const='colour')
        parser.add_argument(
            '--dates', dest='action', action='store_const',
            const='dates')
        # Optional query
        parser.add_argument('query', nargs='?')

        # Feed command line arguments to the parser.
        # Use `wf.args` as `Workflow` ensures that the arguments are
        # correctly decoded to normalised Unicode. This can help avoid
        # a lot of subtle errors in your workflow.
        args = parser.parse_args(wf.args)

        log.debug('args: {}'.format(args))

        # Set query
        self.query = args.query

        # The following is a common Python idiom for "dispatching"
        # command line arguments to the appropriate function. It's more
        # concise and elegant than a massive if-else construction and
        # will automatically handle any new options.

        # Get the corresponding method based on what `action` is set to
        method_name = 'do_{}'.format(args.action)
        if hasattr(self, method_name):
            # Run the corresponding method
            return getattr(self, method_name)()
        else:
            # This error will be caught by the Workflow object and
            # displayed in Alfred if it occurs within a Script Filter.
            # In this case, it invariably means programmer error, not
            # user error.
            raise ValueError('Unknown action : `{}`'.format(args.action))
        return 0

    def do_icons(self):
        """Show a bunch of icons in Alfred"""
        # Get the colour from settings or use the default
        colour = self.wf.settings.get('colour', COLOUR_DEFAULT)
        if not self.query:
            # Grab 10 random icons from Font Awesome
            icons = random.sample(fontawesome.CHARACTERS, 5)
        else:
            # Filter icons by `query`
            icons = self.wf.filter(self.query, fontawesome.CHARACTERS,
                                   max_results=5, min_score=30)

        if not icons:
            # Show a warning (this is preferable to Alfred's default
            # of showing the fallback web searches)
            self.wf.add_item('No matching icons', icon=ICON_WARNING)

        # Generate list of icons and send them to Alfred
        for icon in icons:
            # Get the path to the icon from the Bundler.
            # `bundler.icon()` takes the name of the icon, the name of
            # the font and the CSS colour. It returns the path to the
            # locally cached icon, downloading it first if necessary. As
            # above, it will take some time to download the icon the
            # first time, but will be extremely fast if the icon is in
            # the cache.
            icon_path = bundler.icon(icon, 'fontawesome', colour)
            self.wf.add_item(icon, 'Font Awesome // #{}'.format(colour),
                             arg='{}|{}|{}'.format(icon, 'fontawesome', colour),
                             valid=True,
                             icon=icon_path)

        # Return results to Alfred
        self.wf.send_feedback()

    def do_notify(self):
        """Display a notification based on `query` (show the selected icon,
        font and colour)

         """

        # Parse the argument passed
        icon, font, colour = self.query.split('|')
        title = 'Bundler Icon'
        message = '`{}` from `{}`'.format(icon, font)
        return notify(title, message)

    def do_colour(self):
        """Use Pashua to get a colour from the user"""
        # The configuration to pass to Pashua. Note, I've added a few
        # "metal umlauts" to the configuration to ensure that it works
        # properly with non-ASCII text. *Always* test your code with
        # non-ASCII text!
        pashua_config = """
        current.type = textfield
        current.label = Cürrent CSS cölour
        current.disabled = 1
        current.default = {current}

        default.type = defaultbutton
        default.label = Save colour

        cancel.type = cancelbutton

        colour.type = textfield
        colour.label = New CSS colour
        colour.tooltip = Enter a CSS colour (without #)

        """.format(current=self.wf.settings.get('colour', COLOUR_DEFAULT))

        while True:

            # NOTE: It's *essential* to pass the `-e utf8` argument to
            # Pashua, or encode/decode your input/output to `macroman`,
            # which is Pashua's default encoding. If you don't,
            # non-ASCII input/output will cause bad things to happen
            proc = subprocess.Popen([pashua, '-e', 'utf8', '-'],
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE)

            # Call Pashua. Remeber to encode the input to UTF-8!
            (output, err) = proc.communicate(pashua_config.encode('utf-8'))
            # Ensure `output` is Unicode
            output = decode(output)

            # Parse Pashua output
            data = {}
            for line in [l.strip() for l in output.split('\n') if l.strip()]:
                key, val = line.split('=')
                data[key] = val

            # Cancelled, so forget it
            if data['cancel'] == '1':
                return 0

            # Validate new colour
            colour = data['colour'].lstrip('#')  # remove preceding #

            if len(colour) not in (3, 6) or not VALID_COLOUR(colour):
                # Colour invalid, so show an error and go again
                show_error('Invälid CSS colour', colour)

            else:
                # Save the new colour
                self.wf.settings['colour'] = colour.lower()
                notify('New colour', '#{}'.format(colour.lower()))
                break

            # It's a good idea to log variables, as it makes debugging user
            # problems much easier. `Workflow` will automatically keep the
            # logfile's size sane.
            log.debug(data)

    def do_dates(self):
        """Show today's date in a bunch of timezones

        Uses `pytz` as a demo of the Python Bundler's ability to auto-install
        a workflow's dependencies

        """
        # No point importing stuff before we need it
        import pytz
        import datetime
        # Get local time and UTC time
        localnow = datetime.datetime.now()
        utcnow = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        # Random collection of timezone names
        timezones = random.sample(pytz.common_timezones, 10)

        # Convert them to pytz timezone objects
        timezones = [pytz.timezone(zone) for zone in timezones]

        # Initialise the list of times
        times = [(localnow.strftime('%H:%M'), 'Local time'),
                 (utcnow.strftime('%H:%M'), 'UTC')]

        # Calculate the time in the various timezones and add to list
        for tz in timezones:
            tm = utcnow.astimezone(tz).strftime('%H:%M')
            times.append((tm, tz.zone.replace('_', ' ')))

        times.sort()

        # Display times in Alfred
        for tm, name in times:
            self.wf.add_item('{} {}'.format(tm, name))

        self.wf.send_feedback()


# This is a standard Python idiom for running a .py file when it's
# called directly. It's good practice to do this, as it means the file
# can be imported by other files without it executing.
if __name__ == '__main__':
    # Create an instance of our helper
    wf = Workflow()
    # Set the global `log` instance
    log = wf.logger
    # Set the global `decode` function
    decode = wf.decode
    # Create our workflow object
    demo = Demo()
    # Run it. If the inner function (demo.run) returns a non-zero
    # (`None` counts as zero) value, Alfred will recognise the workflow
    # as having failed. `wf.run` will catch any exceptions raised by
    # `demo.run`, display them in Alfred and return 1 to `sys.exit`,
    # indicating that the workflow failed.
    sys.exit(wf.run(demo.run))
