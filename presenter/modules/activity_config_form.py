#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import dash_bootstrap_components as dbc
import dash_html_components as html

from logic import UserConfig, Activity


class ConfigForm:

    def make_configuration_modal(self, activity: Activity, config: UserConfig) -> html:
        config_modal = html.Div(
            [
                dbc.Button("Configuration", id="btn-configuration", color="link", n_clicks=0),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Configuration"),
                        dbc.ModalBody(self.make_charts_selector(activity, config)),
                        dbc.ModalFooter(
                            [
                                dbc.Button("Save", id="btn-save-configuration", color="link", n_clicks=0),
                                dbc.Button("Close", id="btn-close-configuration", color="link", n_clicks=0)
                            ]
                        )
                    ],
                    id="configuration-modal-centered",
                    centered=True,
                    is_open=False,
                )
            ]
        )
        return config_modal

    @staticmethod
    def make_charts_selector(activity: Activity, config: UserConfig) -> html:
        def _make_options(activity: Activity) -> list[dict]:
            streams = [s for s in activity.dataframe.columns]
            if "time" in streams:
                streams.remove("time")
            if "latlng" in streams:
                streams.remove("latlng")
            return [{"label": stream, "value": stream} for stream in streams]

        def _make_user_selected_options(config: UserConfig) -> list[str]:
            return config.activity_config.charts_to_plot if config else []

        options: list[dict] = _make_options(activity)
        selected_option = _make_user_selected_options(config)
        switches = dbc.FormGroup(
            [
                dbc.Label("Select charts to plot"),
                dbc.Checklist(options=options, value=selected_option, id="charts_config_switches", switch=True),
            ],
        )
        config_input = html.Div(
            [
                dbc.Form(switches),
                html.P(id="charts_config_switches-output")
            ]
        )
        return config_input
