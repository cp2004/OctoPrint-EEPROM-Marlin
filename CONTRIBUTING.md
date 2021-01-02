### Contribution Guidelines

**Thank you for taking the time to contribute to this plugin!**
Below are a couple of points to keep in mind while contributing to make the experience as smooth as possible.

#### Stylesheets

The plugin's stylesheets are created using SASS. Please **do not modify** just the compiled CSS!
Otherwise your changes would be overwritten as soon as I clone the repository by the file watcher I have setup.

To compile the CSS (Assuming project root, adjust the path otherwise):

* Install [Sass](https://sass-lang.com/install) using `npm install -g sass`

* Run `sass octoprint_eeprom_marlin/static/scss/eeprom_marlin.scss octoprint_eeprom_marlin/static/css/eeprom_marlin.css` to compile the CSS.

Then you can commit *both* changes to ensure they are not overriden.

#### Pre-commit

There's a pre-commit suite ready in this plugin that keeps an eye on code style, and a couple of performance optimisations.

It is recommended you install it, but it can also be run as a one-off or as a file watcher too. There is PR check that will validate this, and will complain if it does not pass.

* To install: `pre-commit install`
* To run against the entire codebase: `pre-commit run --hook-stage manual --all-files`
* For details of how to set this up with PyCharm Pro, please see the 'File Watcher/Pre-commit' section [OctoPrint documentation](https://docs.octoprint.org/en/master/development/environment.html#pycharm)

#### Adding yourself to the contributors section of the plugin

Make sure you take credit for your contribution! It's easy to add your name, please do so!

In the file [`octoprint_eeprom_marlin/sponsors_contributors.py`](https://github.com/cp2004/OctoPrint-EEPROM-Marlin/blob/master/octoprint_eeprom_marlin/sponsors_contributors.py) there is a list of contributors, that looks like this:

```python
CONTRIBUTORS = [
    {"name": "Anderson Silva (Previous maintainer)", "username": "amsbr"},
]
```

Add your name as another dictionary to this list, like so:
```diff
 CONTRIBUTORS = [
     {"name": "Anderson Silva (Previous maintainer)", "username": "amsbr"},
+    {"name": "Awesome Contributor", "username": "awesomecontributor"},
 ]
```

Your name should then show up under 'Show Contributors' in the plugin's settings pages.


#### Other points

* Please make your contributions against the `devel` branch, to make sure it has the latest codebase. Only exceptions are documentation fixes, such as this one.
* Please fill out the pull request template, to make things easier for me to process. I reply to a lot of things, and may not have the time to do the research myself!
