# datatoaster
[![Build Status](https://travis-ci.org/abc612008/datatoaster.svg?branch=master)](https://travis-ci.org/abc612008/datatoaster) [![codecov](https://codecov.io/gh/abc612008/datatoaster/branch/master/graph/badge.svg)](https://codecov.io/gh/abc612008/datatoaster) [![license](https://img.shields.io/github/license/abc612008/datatoaster.svg)](https://github.com/abc612008/datatoaster/blob/master/LICENSE)

datatoaster is a Python 3 library that can convert raw data to chart data so that it can used to generate charts easily. If you like this project or find it useful please consider giving me a GitHub star. Much appreciated! :)

## Installation
You can install it via pip (NOT AVAILABLE YET)
```
$ pip install datatoaster
```
or manually install by
```
$ python3 setup.py install
```
You can run unit tests by
```
$ python3 ./tests/tests.py
```

## Examples

Given a data set, I want to know how many percent of my users paid money (per OS).

```python
>>> data = [{"PaidAmount": 0, "OS": "iOS"}, {"PaidAmount": 0, "OS": "Android"}, {"PaidAmount": 301, "OS": "Android"}, {"PaidAmount": 0, "OS": "Windows"}, {"PaidAmount": 14, "OS": "Windows"}, {"PaidAmount": 56, "OS": "iOS"}, {"PaidAmount": 2, "OS": "Windows"}, {"PaidAmount": 0, "OS": "Windows"}]
>>> datatoaster.DataSet(data) \
        .set_x(lambda i: i["OS"]) \
        .set_y(datatoaster.DataSet.PercentageWithinGroup) \
        .add_constraint(lambda i: i["PaidAmount"] != 0) \
        .get_result()
        
{'Windows': 0.5, 'iOS': 0.5, 'Android': 0.5}
```

I can now know 50% users in each OS paid money to me! I can also use this data to draw chart.

For more examples, you can run `python3 ./demo/server.py` or try the [live version](not_available_yet.com).

## Documentation

NOT AVAILABLE YET.

## Licenses

datatoaster is released under the MIT License. See [LICENSE](https://github.com/abc612008/datatoaster/blob/master/LICENSE) for more information.
