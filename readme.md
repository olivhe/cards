# Cards

Analyses the results of a random poker game. The results are printed to **analysis.txt.**

The game is played with the following settings: _"Three players each receive a random 5-card poker hand picked from a single deck."_ 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

##### Python (>3.5)

Make sure you have a recent version (>3.5) of [python](https://www.python.org/) installed. 

If running on Windows, the following examples expect that python is included in the [PATH system variable](https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path).

It is recommended to use a virtual environment to manage conflicts with package requirements. Create a virtual environment to your preferred location, e.g. as a subfolder to where you want to run the program from.

```
python3 -m venv /path/to/new/virtual/environment
```

### Installing

##### Unzip
Make sure the contents of the cards.zip are unzipped to the location this program is to be run from.

##### Requirements.txt
Install the requirements in the **requirements.txt** using e.g. the pip package manager of the virtual environment.

1. **Activate virtual environment**
```
/path/to/new/virtual/environment/Scripts/activate
```

2. **Use pip to install requirements.txt**

```
pip install -r /path/to/program/requirements.txt 
```

##### Test the program by running it

```
python3 /path/to/program/run.py
```
If the analysis.txt file was updated with a new date (and simulation), you're good to go!

## Running the tests

The program includes a number simple tests. These only cover a part of the card handling and hand ordering functions' outputs, and are likely to prove useful only in case of further development. 

The tests are found under the ```simple_tests()``` function in the cards.py file. These can be run e.g. as follows using a python console run from the program folder:
```python
from cards import simple_tests
simple_tests()
```

## Authors

* **Oliver Heinonen** - *Initial work* - [olivhe](https://github.com/olivhe)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details