#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from logic.metrics import Metric, ActivityMetrics
import logic.metric_calculator as dss


class TestMetrics:
    def test_init(self, mock_activity):
        norm_power = Metric(strategy=dss.Normalized(), name='NP', measure='wt')
        assert(isinstance(norm_power, Metric))

    def test_calculate_no_config(self, mock_activity):
        average_power = Metric(strategy=dss.AveragePower(), name='AP', measure='wt')
        average_power.calculate(mock_activity.dataframe)
        assert (isinstance(average_power, Metric))
        assert round(average_power.value) == 259

    def test_calculate_with_config(self, mock_activity):
        tss = Metric(strategy=dss.Load(), name='AP', measure='wt', config={'ftp': 290})
        tss.calculate(mock_activity.dataframe)
        assert (isinstance(tss, Metric))
        assert round(tss.value) == 79

    def test_str(self, mock_activity):
        average_power = Metric(strategy=dss.AveragePower(), name='AP', measure='wt')
        average_power.calculate(mock_activity.dataframe)
        assert (isinstance(average_power, Metric))
        assert average_power.__str__() == f"Ap: 259wt"


class TestActivityFields:
    def test_init(self, mock_activity):
        fields = ActivityMetrics(mock_activity, {'ftp': 290})
        assert isinstance(fields, ActivityMetrics)

    def test_populate(self, mock_activity):
        fields = ActivityMetrics(mock_activity, {'ftp': 290})
        fields.populate()
        assert round(fields.load.value) == 79
        assert round(fields.intensity.value, 2) == 0.94
        assert round(fields.average_power.value) == 259
        assert round(fields.normalized.value) == 274

        assert round(fields.work.value) == 827
        assert round(fields.average_hr.value) == 183
        assert round(fields.max_hr.value) == 190
        assert round(fields.average_cad.value) == 83
