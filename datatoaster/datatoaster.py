import collections

""" constants """
XValue = lambda _: ""
Single = lambda _: ""

class DataSet:

    def NumberOfAppearance(self, key_function):
        self.number_of_appearance = True
        if key_function is XValue:
            self.single_dict = True

        def yfunc(li):
            os_list = {}
            for i in li:
                key = key_function(i)
                os_list[key] = os_list.get(key, 0) + 1
            return os_list

        return yfunc

    def Percentage(self, key_function):
        self.percentage = True
        if key_function is XValue:
            self.single_dict = True

        def yfunc(li):
            os_list = {}
            for i in li:
                key = key_function(i)
                os_list[key] = os_list.get(key, 0) + 1
            return os_list

        return yfunc

    def PercentageWithinGroup(self, key_function):
        self.percentage_within_group = True
        if key_function is XValue:
            self.single_dict = True

        def yfunc(li):
            os_list = {}
            for i in li:
                key = key_function(i)
                os_list[key] = os_list.get(key, 0) + 1
            return os_list

        return yfunc

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.x_function = None
        self.y_function = None
        self.number_of_appearance = False
        self.percentage = False
        self.percentage_within_group = False
        self.single_dict = False
        self.constraints = []
        self.pre_constraints = []
        self.single = False
        self.order_key = None

    def set_x(self, func):
        if not callable(func):
            raise ValueError("Expect the argument to be a function.")

        self.x_function = func

        return self

    def set_y(self, param):
        if not callable(param):
            raise ValueError("Expect the argument to be a function.")

        self.y_function = param

        return self

    def add_constraint(self, constraint, is_pre=False):
        if not callable(constraint):
            raise ValueError("Expect the argument to be a function.")

        if is_pre:
            self.pre_constraints.append(constraint)
        else:
            self.constraints.append(constraint)

        return self

    def set_single(self, param):
        self.single = param
        return self

    def ordered_by(self, order_key):
        if not callable(order_key):
            raise ValueError("Expect the argument to be a function.")
        self.order_key = order_key
        return self

    def get_result(self):
        def process_result(result):
            if self.single_dict:
                for key in result.keys():
                    result[key] = result[key][""]
            if self.single:
                if len(result) != 1:
                    raise ValueError("Single mode set while there are more than one result. "
                                     "Results: " + str(result))
                return next(iter(result.values()))
            else:
                if self.order_key is not None:
                    return collections.OrderedDict(sorted(result.items(), key=self.order_key))
                else:
                    return result

        if self.x_function is None:  # x_function should not be None
            raise ValueError("set_x not called when calling get_result")

        filtered_data = []  # data that passed all constraints
        number_of_valid_data = 0  # save the total unfiltered number for percentage
        all_appearance = {}  # save the unfiltered number per group for percentage_within_group

        for item in self.raw_data:
            pass_constraints = True
            for pre_constraint in self.pre_constraints:  # pre constraints
                if not pre_constraint(item):
                    pass_constraints = False
                    break
            if not pass_constraints:
                continue

            number_of_valid_data += 1

            for constraint in self.constraints:  # constraints
                if not constraint(item):
                    pass_constraints = False
                    break

            if pass_constraints:
                filtered_data.append(item)

            if self.percentage_within_group:  # for percentage within group
                key = self.x_function(item)
                all_appearance[key] = all_appearance.get(key, 0) + 1

        # handle y_function
        if self.y_function:
            values = {}
            for item in filtered_data:
                key = self.x_function(item)
                if key in values:
                    values[key].append(item)
                else:
                    values[key] = [item]

            for key, value in values.items():
                values[key] = self.y_function(value)
                if self.percentage:
                    for k in values[key].keys():
                        values[key][k] /= number_of_valid_data
                elif self.percentage_within_group:
                    for k in values[key].keys():
                        values[key][k] /= all_appearance[key]

            return process_result(values)

        raise ValueError("set_y not called when calling get_result")
