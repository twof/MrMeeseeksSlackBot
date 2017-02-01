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
All plugins must be run through the plugin test suite.
To run the test suite, `cd` into the root project directory and run `python3 -m unittest tests.test_plugins`

## Writing Plugins

A plugin consists of a `.py` file placed in the `Plugins` directory.

### Requirements  
* Import the following
    * `from ..Models.Plugin import Plugin, Plugin_Type`

* All plugins must implement the following
    * `Plugin`
        * In `__init__` call `super().__init__(<Plugin_Type>, <query>)`. `super().__init__` takes two parameters.
            * `query` which is a string that will be matched against messages to determine how the bot should respond.
            * `Plugin_Type` which determines how an incoming message could trigger your plugin. Plugin_Type can be one of the following
                * `everything`: Respond to everything
                * `equals`: Respond only when messages equal your query
                * `starts_with`: Respond only when messages start with your query
                * `contains`: Respond only when messages contain your query
                * `regex`: Responds only when messages match the regular expression represented by the query

        * Implement `callback`. This is the meat of your plugin. `callback` will be called in the event that a message sent to the bot matches the `query` that the plugin tests for. `callback` takes a `Message` object and returns the response that the bot will send to the target channel.
        * Implement `tests`. All this function has to do is return a few test cases that you will define. Test cases are in the form of an array of tuples where the first item in each tuple is a hypothetical message and the second item is the expected output. Expected output can either be the exact expected output in the form of a string, or a boolean (True if you expect some output) in the case that you're unsure what the exact output will be (ex: `Eight_Ball`).
        * Implement `usage`. Just needs to return usage information for your plugin as a string.

### Recommended
* In the case that the user misuses your plugin, return a helpful hint as a part of `callback`.

* Document your code. I'm not going to enforce this, but it'll make everyone's lives easier.

### Plugin Suggestions
Want to start writing plugins but don't know where to start? Here are some ideas!
Be if you start work on a concept listed here, be sure to remove it from this list in the same commit you start so we don't get redundant development. Thanks!

#### Port Plugins from MilkBot
Mr Meeseeks takes a lot of inspiration from [MilkBot](https://github.com/DanH42/mi1kb0t). If you want something easy, you could port the plugins that already exist in MilkBot to Mr Meeseeks. Note that MilkBot is written in Node so you may need some JS knowledge to start. Here's a list of plugins that haven't been ported yet:
* [CatFacts](https://github.com/DanH42/mi1kb0t/blob/master/plugins/CatFacts.js)
* [Hedgehogs](https://github.com/DanH42/mi1kb0t/blob/master/plugins/hedgehogs.js)
* [Image](https://github.com/DanH42/mi1kb0t/blob/master/plugins/hedgehogs.js)
* [PingPong](https://github.com/DanH42/mi1kb0t/blob/master/plugins/pingpong.js) (This set would be the easiest. It's all straight call and response)
* [random](https://github.com/DanH42/mi1kb0t/blob/master/plugins/random.js)
* [reddit](https://github.com/DanH42/mi1kb0t/blob/master/plugins/reddit.js) (This should be split into multiple plugins)
* [Urban](https://github.com/DanH42/mi1kb0t/blob/master/plugins/urban.js)

#### Other Ideas
If anyone has an idea for a plugin, but either don't have the knowhow or motivation to make it, feel free to add it to this list.
* Get stats from your favorite game (LoL, DoTA, WoW, Overwatch, etc)
* Get weather for an area
* Github info (Streak leaderboard?)
* Get schedule for the day (Make School)
* Get headlines from Google News

#### [Example Plugin](https://github.com/twof/MrMeeseeksSlackBot/blob/master/src/Plugins/Eight_Ball.py)

## Code Style Guide
Tabs for indentation.
