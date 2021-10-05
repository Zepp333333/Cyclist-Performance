#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from logic.datafields import DataField, ActivityFields
import logic.datafield_strategies as dss


class TestDataField:
    def test_init(self, mock_activity):
        norm_power = DataField(strategy=dss.Normalized(), name='NP', measure='wt')
        assert(isinstance(norm_power, DataField))

    def test_calculate_no_config(self, mock_activity):
        average_power = DataField(strategy=dss.AveragePower(), name='AP', measure='wt')
        average_power.calculate(mock_activity.dataframe)
        assert (isinstance(average_power, DataField))
        assert round(average_power.value) == 259

    def test_calculate_with_config(self, mock_activity):
        tss = DataField(strategy=dss.Load(), name='AP', measure='wt', config={'ftp': 290})
        tss.calculate(mock_activity.dataframe)
        assert (isinstance(tss, DataField))
        assert round(tss.value) == 79

    def test_str(self, mock_activity):
        average_power = DataField(strategy=dss.AveragePower(), name='AP', measure='wt')
        average_power.calculate(mock_activity.dataframe)
        assert (isinstance(average_power, DataField))
        assert average_power.__str__() == f"Ap: 259wt"


class TestActivityFields:
    def test_init(self, mock_activity):
        fields = ActivityFields(mock_activity, {'ftp': 290})
        assert isinstance(fields, ActivityFields)

    def test_populate(self, mock_activity):
        fields = ActivityFields(mock_activity, {'ftp': 290})
        fields.populate()
        print(fields.fields)
        assert round(fields.fields['load'].value) == 79
        assert round(fields.fields['intensity'].value, 2) == 0.94
        assert round(fields.fields['average power'].value) == 259
        assert round(fields.fields['normalized'].value) == 274
