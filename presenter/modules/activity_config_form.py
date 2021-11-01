#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import dash_bootstrap_components as dbc
import dash_html_components as html

from logic import UserConfig, Activity


class ConfigForm:
    def make_configuration_modal(self, activity: Activity, config: UserConfig) -> html:
        config_modal = html.Div(
            [
                dbc.Button("Configuration", id="btn_open_configuration", color="link", n_clicks=0),
                dbc.Modal(
                    [
                        dbc.ModalTitle("Configuration"),
                        dbc.ModalBody(self.make_charts_selector(activity, config)),
                        dbc.ModalFooter(
                            [
                                dbc.Button("Save", id="btn_save_configuration", color="link", n_clicks=0),
                                dbc.Button("Close", id="btn_close_configuration", color="link", n_clicks=0)
                            ]
                        )
                    ],
                    id="configuration_modal_centered",
                    centered=True,
                    is_open=False,
                )
            ]
        )
        return config_modal

    @staticmethod
    def make_charts_selector(activity: Activity, config: UserConfig) -> html:
        def _make_options() -> list[dict]:
            streams = [s for s in activity.dataframe.columns]
            if "time" in streams:
                streams.remove("time")
            if "latlng" in streams:
                streams.remove("latlng")
            return [{"label": stream, "value": stream} for stream in streams]

        def _make_user_selected_options() -> list[str]:
            return config.activity_config.charts_to_plot if config else []

        options = _make_options()
        selected_option = _make_user_selected_options()
        switches = dbc.Checklist(options=options, value=selected_option, id="charts_config_switches", switch=True),

        config_input = html.Div(
            [
                dbc.Label("Select charts to plot"),
                dbc.Form(switches),
            ]
        )
        return config_input
