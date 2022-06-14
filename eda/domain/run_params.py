from typing import List, Dict


class RunInputParametersDo:
    def __init__(self, target_column: str,
                 distribution_plot: List[dict],
                 correlation_plot: List[dict]):
        self.target_column = target_column
        self.distribution_plot = distribution_plot
        self.correlation_plot = correlation_plot

    @staticmethod
    def from_dict(input_params: dict):
        return RunInputParametersDo(target_column=input_params['target_column'],
                                    distribution_plot=input_params['distribution_plot'],
                                    correlation_plot=input_params['correlation_plot'])