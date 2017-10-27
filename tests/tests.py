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
        # wrong argument being passed into set_x
        self.assertRaises(ValueError, datatoaster.DataSet(self.test_set_1).set_x, 0)
        self.assertRaises(ValueError, datatoaster.DataSet(self.test_set_1).set_x, "0")
        self.assertRaises(ValueError, datatoaster.DataSet(self.test_set_1).set_x, [])

        # get_result without set_x, set_y being called
        self.assertRaises(ValueError, datatoaster.DataSet(self.test_set_1).get_result)

        # get_result without set_y being called
        self.assertRaises(ValueError, datatoaster.DataSet(self.test_set_1)
                          .set_x(datatoaster.DataSet.Single).get_result)

        # get_result without set_x being called
        self.assertRaises(ValueError, datatoaster.DataSet(self.test_set_1)
                          .set_y(datatoaster.DataSet.Percentage).get_result)

        # single mode set wrongly
        self.assertRaises(ValueError, datatoaster.DataSet(self.test_set_1)
                          .set_x(lambda i: i["OS"])
                          .set_y(datatoaster.DataSet.Percentage)
                          .set_single(True)
                          .get_result)

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

    def test_case_y_value(self):
        """ get the total paid money of each OS """
        result = datatoaster.DataSet(self.test_set_1) \
            .set_x(lambda i: i["OS"]) \
            .set_y(lambda d: sum([v["PaidAmount"] for v in d])) \
            .get_result()
        desired_result = {"Android": 20, "iOS": 210}

        self.assertDictEqual(result, desired_result)

    def test_case_percentage_constraint_single(self):
        """ how much users pay more than 100 """
        result = datatoaster.DataSet(self.test_set_1) \
            .set_x(datatoaster.DataSet.Single) \
            .set_y(datatoaster.DataSet.Percentage) \
            .add_constraint(lambda i: i["PaidAmount"] > 100)\
            .set_single(True)\
            .get_result()
        desired_result = 1/8

        self.assertEqual(result, desired_result)

    def test_case_y_value_multiple_values(self):
        """ how much users pay more than 100 """
        result = datatoaster.DataSet(self.test_set_1) \
            .set_x(lambda i: i["OS"]) \
            .set_y(lambda d: [i["PaidAmount"] for i in d]) \
            .get_result()
        desired_result = {"Android": 20, "iOS": 210}

        self.assertDictEqual(result, desired_result)


if __name__ == '__main__':
    unittest.main()
