import unittest
from datatoaster import *


class BasicTestSuite(unittest.TestCase):
    test_set_1 = [{"OS": "Android", "PaidAmount": 20},
                  {"OS": "Android", "PaidAmount": 0},
                  {"OS": "Android", "PaidAmount": 0},
                  {"OS": "iOS", "PaidAmount": 172},
                  {"OS": "iOS", "PaidAmount": 0},
                  {"OS": "iOS", "PaidAmount": 20},
                  {"OS": "iOS", "PaidAmount": 0},
                  {"OS": "iOS", "PaidAmount": 18}]

    def test_exceptions(self):
        data_set = datatoaster.DataSet([])
        self.assertRaises(ValueError, data_set.set_x, 0)
        self.assertRaises(ValueError, data_set.set_x, "0")
        self.assertRaises(ValueError, data_set.set_x, [])

    def test_case_number_of_appearance(self):
        """ get the user number of each OS """
        result = datatoaster.DataSet(self.test_set_1) \
            .set_x(lambda i: i["OS"]) \
            .set_y(datatoaster.DataSet.NumberOfAppearance) \
            .get_result()
        desired_result = {"Android": 3, "iOS": 5}

        self.assertDictEqual(result, desired_result)

    def test_case_percentage(self):
        """ get the user number percentage of each OS """
        result = datatoaster.DataSet(self.test_set_1) \
            .set_x(lambda i: i["OS"]) \
            .set_y(datatoaster.DataSet.Percentage) \
            .get_result()
        desired_result = {"Android": 3 / (3 + 5), "iOS": 5 / (3 + 5)}

        self.assertDictEqual(result, desired_result)

    def test_case_constraint(self):
        """ get the paid user number of each OS """
        result = datatoaster.DataSet(self.test_set_1) \
            .set_x(lambda i: i["OS"]) \
            .set_y(datatoaster.DataSet.NumberOfAppearance) \
            .add_constraint(lambda i: i["PaidAmount"] != 0) \
            .get_result()
        desired_result = {"Android": 1, "iOS": 3}

        self.assertDictEqual(result, desired_result)

    def test_case_percentage_within_group(self):
        """ get the paid user number percentage of each OS """
        result = datatoaster.DataSet(self.test_set_1) \
            .set_x(lambda i: i["OS"]) \
            .set_y(datatoaster.DataSet.PercentageWithinGroup) \
            .add_constraint(lambda i: i["PaidAmount"] != 0) \
            .get_result()
        desired_result = {"Android": 1 / 3, "iOS": 3 / 5}

        self.assertDictEqual(result, desired_result)


if __name__ == '__main__':
    unittest.main()
