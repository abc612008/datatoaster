# datatoaster
[![Build Status](https://travis-ci.org/abc612008/datatoaster.svg?branch=master)](https://travis-ci.org/abc612008/datatoaster) [![codecov](https://codecov.io/gh/abc612008/datatoaster/branch/master/graph/badge.svg)](https://codecov.io/gh/abc612008/datatoaster) [![license](https://img.shields.io/github/license/abc612008/datatoaster.svg)](https://github.com/abc612008/datatoaster/blob/master/LICENSE)

datatoaster is a Python 3 library that can convert raw data to chart data so that it can used to generate charts easily. If you like this project or find it useful please consider giving me a GitHub star. Much appreciated! :)

Suggestions are welcome!

## Installation
You can install it via pip
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

For more examples, you can run `python3 ./demo/server.py`.

## Documentation

DataSet.set_x(DataSet.Single / function): Set X value

    DataSet.Single: equivalent to (lambda i:"")
    
    function: data_item -> desired_x_value
    
DataSet.set_y(DataSet.NumberOfAppearance/DataSet.Percentage/DataSet.PercentageWithinGroup/function): Set Y value
    NumberOfAppearance: Y value will be the number of appearance of X.
    
    Percentage: Y value will be the percentage of appearance of X over the whole data set.
    
    PercentageWithinGroup: Y value will be the percentage of appearance of X over the group.
    
    function: [data_item] -> y_value / [y_values] Y value will be what your function returns.

DataSet.get_result(): Get the final result
    Example 1: {"x":y, "x2":y2}
    Example 2: {"x":[y11,y12], "x2":[y21,y22]}

DataSet.add_constraint(function, is_single): Add a constraint
    function: data_item -> boolean (indicates whether the value should be used)
    
    is_single: indicates if the constraint applies to "whole data set"(Only makes difference when .SetY(Percentage)), defaults to False.

It may seem confusing. You can refer to [unit tests](https://github.com/abc612008/datatoaster/blob/master/tests/tests.py) or [demo](https://github.com/abc612008/datatoaster/blob/master/demo/server.py) for more examples.
## Licenses

datatoaster is released under the MIT License. See [LICENSE](https://github.com/abc612008/datatoaster/blob/master/LICENSE) for more information.
