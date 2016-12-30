# Contributing
You are welcome to [report Issues](https://github.com/twof/MrMeeseeksSlackBot/issues) or [pull requests](https://github.com/twof/MrMeeseeksSlackBot/pulls). It's recommended that you read the following Contributing Guide first before contributing.


## Issues
Github Issues is used to track public bugs and feature requests.

### Search Known Issues First
Please search existing issues to see if any similar issue or feature request has already been filed. You should make sure your issue isn't redundant.

### Reporting New Issues
If you open an issue, the more information you provide the better. An example of a well reported issue might be one that includes a screenshot, what was expected to happen and what actually occurred.

## Pull Requests
Pull requests are welcome so that Mr. Meeseeks may better server everyone!

### Which Branch?
Pull requests should be made to the `dev` branch whether you're contributing a plugin or to the bot core itself.
The only exception is edits to documentation (README, inline documentation, etc.). Those requests can be made into `master`.

### Testing
(Applicable only once test suite exists)
All plugins must be run through the plugin test suite. Pull request will only be accepted if they contain pasted output from tests.

## Writing Plugins

A plugin consists of a `.py` file placed in the `Plugins` directory.

### Requirements  
* Import the following
    * `from Utils.constants import Plugin_Type`
    * `from Models.Plugin import Plugin`
    * `from Models.Singleton import Singleton`


* All plugins must implement the following
    * `Plugin`
        * In `__init__` call `super(<Class_Name>, self).__init__(<Plugin_Type>, <query>)`. `super.__init__` takes two parameters.
            * `query` which is a string that will be matched against messages to determine how the bot should respond.
            * `Plugin_Type` which determines how an incoming message could trigger your plugin. Plugin_Type can be one of the following
                * `everything`: Respond to everything
                * `equals`: Respond only when messages equal your query
                * `starts_with`: Respond only when messages start with your query
                * `contains`: Respond only when messages contain your query
        * Implement `callback`. This is the meat of your plugin. `callback` will be called in the event that a message sent to the bot matches the `query` that the plugin tests for. `callback` takes a `Message` object and returns the response that the bot will send to the target channel.
    * `Singleton`

* Add the name of your plugin to `__all__` in `Plugins/__init__.py`.


### Recommended
* In the case that the user misuses your plugin, return a helpful hint as a part of `callback`.

* Document your code. I'm not going to enforce this, but it'll make everyone's lives easier.

#### [Example Plugin](https://github.com/twof/MrMeeseeksSlackBot/blob/master/Plugins/Eight_Ball.py)

## Code Style Guide
Tabs for indentation.
