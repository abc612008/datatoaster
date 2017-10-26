class DataSet:
    """ constants """
    NumberOfAppearance = 0
    Percentage = 1
    PercentageWithinGroup = 2

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.x_function = None
        self.y_function = None
        self.number_of_appearance = False
        self.percentage = False
        self.percentage_within_group = False
        self.constraints = []
        self.pre_constraints = []

    def set_x(self, func):
        if not callable(func):
            raise ValueError("Expect the argument to be a function.")

        self.x_function = func

        return self

    def set_y(self, param):
        if param == self.NumberOfAppearance:
            self.number_of_appearance = True
            self.percentage = False
            self.percentage_within_group = False
            self.y_function = None
            return self

        if param == self.Percentage:
            self.number_of_appearance = False
            self.percentage = True
            self.percentage_within_group = False
            self.y_function = None
            return self

        if param == self.PercentageWithinGroup:
            self.number_of_appearance = False
            self.percentage = False
            self.percentage_within_group = True
            self.y_function = None
            return self

        if not callable(param):
            raise ValueError("The argument is neither DataSet.NumberOfAppearance, "
                             "DataSet.Percentage nor a function.")

        self.number_of_appearance = False
        self.percentage = False
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

    def get_result(self):
        filtered_data = []
        number_of_valid_data = 0
        all_appearance = {}
        for item in self.raw_data:
            pass_constraints = True
            for pre_constraint in self.pre_constraints:
                if not pre_constraint(item):
                    pass_constraints = False
                    break
            if not pass_constraints:
                continue

            number_of_valid_data += 1

            for constraint in self.constraints:
                if not constraint(item):
                    pass_constraints = False
                    break
            if pass_constraints:
                filtered_data.append(item)
            if self.percentage_within_group:  # for percentage within group
                key = self.x_function(item)
                if key in all_appearance:
                    all_appearance[key] += 1
                else:
                    all_appearance[key] = 1

        if self.number_of_appearance or self.percentage or self.percentage_within_group:
            appearance = {}
            for item in filtered_data:
                key = self.x_function(item)
                if key in appearance:
                    appearance[key] += 1
                else:
                    appearance[key] = 1
            if self.percentage:
                for key in appearance:
                    appearance[key] /= number_of_valid_data
            if self.percentage_within_group:
                for key in appearance:
                    appearance[key] /= all_appearance[key]
            return appearance
        assert False

    def get_series(self):
        return []
