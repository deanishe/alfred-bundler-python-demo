
# Alfred Dependency Bundler Python Demo Workflow #

A simple, but hopefully nevertheless fairly comprehensive, demonstration of how to use the [Alfred Bundler](https://github.com/shawnrice/alfred-bundler/tree/master)'s Python wrapper in an Alfred workflow.

The Python wrapper can be found [here](https://github.com/shawnrice/alfred-bundler/blob/master/wrappers/bundler.py). Currently, the most detailed documentation can be found in the wrapper's source code. This demo workflow is also very heavy on the comments.

## Shameless plug ##

This workflow uses the [Alfred-Workflow library](https://github.com/deanishe/alfred-workflow), which takes care of a lot of the mundane boilerplate of writing a workflow (XML generation, logging/debugging etc.), and also provides some cool features that might be useful for your workflow (fairly smart search, caching, settings, background tasks, simple web access and more).

When writing a workflow, you should *strongly* consider using one of the available libraries: they're typically thoroughly tested and take care of a lot of the boilerplate for you. You can concentrate on what your workflow needs to do, not what Alfred needs it to do.

A list of libraries available for various languages can be found on [the Alfred forum](http://www.alfredforum.com/topic/2030-workflow-libraries-and-helpers/).

## Brief overview of the Bundler ##

The Bundler allows you to use a number of common workflow utilities to do add functionality to your workflow, such as showing notifications or dialog boxes for user input, using common OS X utilities (such as `terminal-notifier` or `cocoaDialog`) without every author needing to include the utilities in their workflows.

There is also an icon API that allows you access to ~1000 icons in the colour of your choice.

Finally, the Python version of the Bundler allows you to transparently install any Python libraries your workflow needs (using Pip and its requirements.txt) without the need to include large libraries with your workflow.

## Overview of this Demo ##

The demo has three Alfred keywords:

1. `bundleicons [<query>]` — Show 5 random [Font Awesome](http://fortawesome.github.io/Font-Awesome/) icons from the [Bundler icon service](http://icons.deanishe.net/). If `<query>` is specified, show up to 5 icons matching `<query>`.
2. `bundlecolour` — Show a dialog so you can specify a different CSS colour for the icons shown by `bundleicons`. (Be sure to try specifying an invalid colour.)
3. `bundletime` — Show the current time in a range of random timezones.

The functions are all fairly pointless, but they respectively show how to:

1. Use the [Bundler's icon API](http://icons.deanishe.net/).
2. Use the [Pashua](http://www.bluem.net/en/mac/pashua/), [cocoaDialog](http://mstratman.github.io/cocoadialog/) and [terminal-notifier](https://github.com/alloy/terminal-notifier) utilities.
3. Automatically install and use an external Python library (in this case, [pytz](http://pytz.sourceforge.net/)).

Please see the docstrings and comments in the source for a detailed explanation of how this demo and the Bundler work.

As well as demonstrating how to use `bundler.py`, this workflow also shows one way you can structure your workflow code and contains some useful pointers on Unicode/text handling for coders who aren't very familiar with Python 2's somewhat finicky behaviour in this regard.

## Full Bundler details ##

More information on the default utilities and the JSON file format for adding your own custom assets can be found on the [Bundler homepage](http://shawnrice.github.io/alfred-bundler/).

The complete documentation for the Python version is (currently) only available in the source code of the [bundler.py wrapper](https://github.com/shawnrice/alfred-bundler/blob/master/wrappers/bundler.py).

The currently available icons can be viewed [here](http://icons.deanishe.net/#fonts) and concise usage instructions [here](http://icons.deanishe.net/#python).

## Acknowledgements ##

The Alfred Bundler was created by [Shawn Rice](https://github.com/shawnrice), the estimable creator of [Packal.org](http://www.packal.org/).
