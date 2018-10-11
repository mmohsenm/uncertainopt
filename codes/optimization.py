__author__ = "Mohsen Moarefdoost"
__copyright__ = ""
__license__ = ""
__version__ = ""
__doc__ = ""

import logging
import os
import time
import pandas as pd
import pulp

logger = logging.getLogger(__name__ + ': ')


class Data(object):
    def __init__(self, data_loader):
        logger.info("loading optimization data")

        self.data_loader = data_loader
        _demand_scenarios = self.data_loader.input_df_dict["demand_scenario"]
        self.scenarios_probability = _demand_scenarios[["scenario", "probability"]].groupby(
            by=["scenario"]).mean()["probability"].to_dict()
        self.demands = _demand_scenarios.set_index(["product", "period", "scenario"])["demand"].to_dict()
        self.product_details = self.data_loader.input_df_dict["product_details"].set_index("product").to_dict(
            orient="index")
        self.capacity = self.data_loader.input_df_dict["capacity"].set_index("period")["capacity"].to_dict()
        self.time_periods = self.data_loader.input_df_dict["time_period"].set_index("period")["date"].to_dict()
        self.output_mapping = {"production": ["product", "period"],
                               "overage": ["product", "period", "scenario"],
                               "underage": ["product", "period", "scenario"]}

    def get_output_reports(self, optimizer):
        output_df_dict = {}
        for key, var in optimizer.__dict__.items():
            if key.endswith('_variables'):
                name = key[:-len('_variables')]
                cols = self.output_mapping[name]
                opt_dict = {k: v.varValue for k, v in var.items()}
                opt_series = pd.Series(opt_dict)
                _idx = opt_series.index.values
                try:
                    _midx = pd.MultiIndex.from_tuples(_idx)
                except TypeError:
                    _midx = pd.Index(_idx)
                _midx.names = cols
                opt_series.name = "optimal_"+name
                df = pd.DataFrame(data=opt_series, index=_midx)
                df = df.reset_index()
                output_df_dict[name] = df
        return output_df_dict


class DataLoader(object):
    def __init__(self, input_files=None):
        self._input_df_dict = {}
        self.input_files = input_files
        self.read_csv_files()

    @property
    def input_df_dict(self):
        return self._input_df_dict

    @input_df_dict.setter
    def input_df_dict(self, df_dict):
        self._input_df_dict = df_dict

    def read_csv_files(self):
        """
        :return:
        """
        input_df_dict = {}
        logger.info('reading csv files')
        for _file in self.input_files:
            if _file.endswith(".csv"):
                file_name = os.path.basename(_file)[:-4]
                df = pd.read_csv(_file, encoding='utf8')
                logger.info('read csv file: %s with %d records' % (file_name, len(df)))
                input_df_dict[file_name] = df
        self._input_df_dict.update(input_df_dict)


class Optimizer(object):
    def __init__(self, data):
        self.data = data
        logger.info("initializing pulp optimization model")
        self.model = pulp.LpProblem(name="OptimizationModel", sense=pulp.LpMaximize)
        self.is_solved = False
        self._build_model()

    def _add_pulp_constraint(self, constraint):
        self.model.addConstraint(constraint)
        return constraint

    def _build_model(self):
        """

        :return:
        """
        self.production_variables = {
            (product, period): pulp.LpVariable(name="ProductionAmount_{0}_AtPeriod_{1}".format(product, period),
                                               cat=pulp.LpContinuous,
                                               lowBound=0)
            for product in self.data.product_details
            for period in self.data.time_periods}

        self.overage_variables = {
            (product, period, scenario): pulp.LpVariable(
                name="OverProductionAmount_{0}_AtPeriod_{1}_InScenario_{2}".format(product, period, scenario),
                cat=pulp.LpContinuous,
                lowBound=0)
            for (product, period, scenario) in self.data.demands}

        self.underage_variables = {
            (product, period, scenario): pulp.LpVariable(
                name="UnderProductionAmount_{0}_AtPeriod_{1}_InScenario_{2}".format(product, period, scenario),
                cat=pulp.LpContinuous,
                lowBound=0)
            for (product, period, scenario) in self.data.demands}

        self.capacity_constraints = {period: self._add_pulp_constraint(pulp.LpConstraint(
            e=pulp.lpSum(self.production_variables[product, period] * v["efficiency_rate"]
                         for product, v in self.data.product_details.items()),
            sense=pulp.LpConstraintLE,
            name="CapacityLimitAt_{0}".format(period),
            rhs=self.data.capacity[period]))
            for period in self.data.time_periods}

        self.overage_constraints = {(product, period, scenario): self._add_pulp_constraint(pulp.LpConstraint(
            e=self.production_variables.get((product, period), 0) - var,
            sense=pulp.LpConstraintLE,
            name="OverageLimitForProduct_{0}_AtPeriod_{1}_In_{2}".format(product, period, scenario),
            rhs=self.data.demands[product, period, scenario]))
            for (product, period, scenario), var in self.overage_variables.items()}

        self.underage_constraints = {(product, period, scenario): self._add_pulp_constraint(pulp.LpConstraint(
            e=self.production_variables.get((product, period), 0) + var,
            sense=pulp.LpConstraintGE,
            name="UnderageLimitForProduct_{0}_AtPeriod_{1}_In_{2}".format(product, period, scenario),
            rhs=self.data.demands[product, period, scenario]))
            for (product, period, scenario), var in self.underage_variables.items()}

    def get_objective(self):
        """

        :return:
        """

        self.revenue = pulp.lpSum(var * (self.data.product_details[product]["normal_price"]
                                         - self.data.product_details[product]["production_cost"]) for
                                  (product, period), var in self.production_variables.items()) + \
                       pulp.lpSum(var * (self.data.product_details[product]["lower_price"]
                                         - self.data.product_details[product]["production_cost"]) *
                                  self.data.scenarios_probability[scenario]
                                  for (product, period, scenario), var in self.overage_variables.items()) - \
                       pulp.lpSum(var * self.data.product_details[product]["higher_price"] *
                                  self.data.scenarios_probability[scenario]
                                  for (product, period, scenario), var in self.underage_variables.items())
        return self.revenue

    def optimize(self, **param):
        """

        :param
        :return:
        """
        _write_mps_flag = False
        _write_lp_flag = False
        if len(param) > 0:
            if "WriteLpFlag" in param:
                _write_lp_flag = param["WriteLpFlag"]
            if "WriteMpsFlag" in param:
                _write_mps_flag = param["WriteMpsFlag"]

        logger.info("setting model objective ... ")
        self.model.setObjective(self.get_objective())

        if _write_lp_flag:
            logger.info("writing optimization lp model")
            self.model.writeLP("".join(["./", self.model.name, '.lp']))

        if _write_mps_flag:
            logger.info("writing optimization mps model")
            self.model.writeMPS("".join(["./", self.model.name, '.lp']))

        logger.info('Optimization starts')
        _run_time = time.time()
        status = self.model.solve()
        _run_time = time.time() - _run_time
        logger.info("optimization completed in {0:.2f} "
                    "seconds and the solution is {1}".format(_run_time, pulp.LpStatus[self.model.status]))
        return status
