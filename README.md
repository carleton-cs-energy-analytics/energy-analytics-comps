# Carleton CS Energy Analytics Comps

<kbd>
    <img src="imgs/collage.png" alt="Joyous Collage"
    width="650">
</kbd>

*Revolutionizing the way Carleton notices that a building is being heated/cooled simultaneously!*

- **Team**: Zephyr Lucas, Jonathan Bisila, Kiya Govek, Carolyn Ryan, Dustin Michels, Jack Lightbody
- **Guided by:** Jeff Ondich
- Carleton College, Fall-Winter 2017

## Unit Testing
For every new file and method, add test(s) to the corresponding file or make a new test file in energy-analytics-comps/test
that must be named ```test*.py```.  Try to keep tests simple/each test only tests one thing.  Try to keep tests
realistic--have test cases covering what the functionality you have built will be relied upon doing.  The idea is that
if someone makes a change that would break some process or some core part of what your code was doing, a test should break
so that the person making the change knows that it is either breaking or changing functionality.

#### To run unit testing
```unix
python3 -m unittest discover --start-directory test
```

## Dashboard
To set up the flask app locally, cd to the dashboard directory and run
```
EXPORT FLASK_APP=routes.py
flask run
```
You can also optionally enable debug mode with `EXPORT FLASK_DEBUG=1`
