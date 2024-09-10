import dash
import dash_mantine_components as dmc
from dash import html, callback, Output, Input, no_update, State, ctx, dcc

from components.charts import t_rh_pmv, chart_selector
from components.dropdowns import (
    model_selection,
)
from components.functionality_selection import functionality_selection
from components.input_environmental_personal import input_environmental_personal
from components.my_card import my_card
from components.show_results import display_results
from utils.get_inputs import get_inputs
from utils.my_config_file import (
    URLS,
    ElementsIDs,
    Dimensions,
    UnitSystem,
    Models,
    Charts,
    ChartsInfo,
    MyStores,
)

from components.store_state import StoreState

dash._dash_renderer._set_react_version('18.2.0')
app = dash.Dash(__name__)

PERSIST_IDS = [
    ElementsIDs.t_db_input.value,
    ElementsIDs.t_r_input.value,
    ElementsIDs.v_input.value,
    ElementsIDs.rh_input.value,
    ElementsIDs.met_input.value,
    ElementsIDs.clo_input.value,
]

store_id = "input_environmental_personal"

store_state = StoreState(PERSIST_IDS, store_type='local')

dash.register_page(__name__, path=URLS.HOME.value)

layout = dmc.Stack(
    [
        dmc.Grid(
            children=[
                dmc.GridCol(
                    model_selection(),
                    span={"base": 12, "sm": Dimensions.left_container_width.value},
                ),
                dmc.GridCol(
                    functionality_selection(),
                    span={"base": 12, "sm": Dimensions.right_container_width.value},
                ),
            ],
            gutter="xl",
        ),
        dmc.Grid(
            children=[
                my_card(
                    title="Inputs",
                    children=input_environmental_personal(),
                    id=ElementsIDs.INPUT_SECTION.value,
                    span={"base": 12, "sm": Dimensions.left_container_width.value},
                ),
                my_card(
                    title="Results",
                    children=dmc.Stack(
                        [
                            html.Div(
                                id=ElementsIDs.RESULTS_SECTION.value,
                            ),
                            html.Div(
                                id=ElementsIDs.charts_dropdown.value,
                                children=html.Div(id=ElementsIDs.chart_selected.value),
                            ),
                            html.Div(
                                id=ElementsIDs.CHART_CONTAINER.value,
                            ),
                            dmc.Text(id=ElementsIDs.note_model.value),

                            store_state.get_store_component(store_id),
                            dcc.Location(id='url', refresh=False),
                        ],
                    ),
                    span={"base": 12, "sm": Dimensions.right_container_width.value},
                ),
            ],
            gutter="xl",
        ),
    ]
)

@callback(
    Output(ElementsIDs.INPUT_SECTION.value, "children"),
    Input(ElementsIDs.MODEL_SELECTION.value, "value"),
    Input(ElementsIDs.UNIT_TOGGLE.value, "checked"),
)
def update_inputs(selected_model, units_selection):
    # todo here I should first check if some inputs are already stored in the store
    if selected_model is None:
        return no_update
    units = UnitSystem.IP.value if units_selection else UnitSystem.SI.value
    return input_environmental_personal(selected_model, units)


@callback(
    Output(ElementsIDs.note_model.value, "children"),
    Input(ElementsIDs.MODEL_SELECTION.value, "value"),
)
def update_note_model(selected_model):
    if selected_model is None:
        return no_update
    if Models[selected_model].value.note_model:
        return html.Div(
            [
                dmc.Text("Limits of Applicability: ", size="sm", fw=700, span=True),
                dmc.Text(Models[selected_model].value.note_model, size="sm", span=True),
            ]
        )


@callback(
    Output(ElementsIDs.charts_dropdown.value, "children"),
    Input(ElementsIDs.MODEL_SELECTION.value, "value"),
)
def update_note_model(selected_model):
    if selected_model is None:
        return no_update
    return chart_selector(selected_model=selected_model)


@callback(
    Output(ElementsIDs.CHART_CONTAINER.value, "children"),
    Input(MyStores.input_data.value, "data"),
    prevent_initial_call=True  # 1. 添加 prevent_initial_call=True
)
def update_chart(inputs):
    if inputs is None:
        return no_update

    selected_model: str = inputs.get(ElementsIDs.MODEL_SELECTION.value, None)
    if not selected_model:
        return no_update

    units: str = inputs.get(ElementsIDs.UNIT_TOGGLE.value, UnitSystem.SI.value)
    chart_selected = inputs.get(ElementsIDs.chart_selected.value, None)

    image = html.Div(
        [
            dmc.Title("Unfortunately this chart has not been implemented yet", order=4),
            dmc.Image(
                src="assets/media/chart_placeholder.png",
            ),
        ]
    )

    if chart_selected == Charts.t_rh.value.name:
        if selected_model == Models.PMV_EN.name:
            image = t_rh_pmv(inputs=inputs, model="iso")
        elif selected_model == Models.PMV_ashrae.name:
            image = t_rh_pmv(inputs=inputs, model="ashrae")

    note = ""
    chart: ChartsInfo
    for chart in Models[selected_model].value.charts:
        if chart.name == chart_selected:
            note = chart.note_chart

    return dmc.Stack(
        [
            image,
            html.Div(
                [
                    dmc.Text("Note: ", size="sm", fw=700, span=True),
                    dmc.Text(note, size="sm", span=True),
                ]
            ),
        ]
    )


@callback(
    Output(ElementsIDs.RESULTS_SECTION.value, "children"),
    Input(MyStores.input_data.value, "data"),
)
def update_outputs(inputs):
    if inputs is None:
        return no_update

    return display_results(inputs)

@callback(
    Output(store_id, "data", allow_duplicate=True),
    [Input(id, "value") for id in PERSIST_IDS],
    State(store_id, "data"),
    prevent_initial_call=True,
)
def callback_update_local_storage(*args):
    return store_state.update_local_storage(*args)


@callback(
    Output(store_id, "data", allow_duplicate=True),
    [Input("url", "href")],
    State(store_id, "data"),
    prevent_initial_call=True,
)
def callback_update_store_from_url(url, store_data):
    return store_state.update_store_from_url(url, store_data)

@callback(
    [Output(id, 'value', allow_duplicate=True) for id in PERSIST_IDS],
    Input(store_id, 'modified_timestamp'),
    State(store_id, 'data'),
    prevent_initial_call=True
)
def callback_load_data(modified_timestamp, store_data):
    return store_state.load_data(modified_timestamp, store_data)


@callback(
    Output('url', 'href'),
    [Input(id, 'value') for id in PERSIST_IDS],
    State(store_id, 'data'),
    prevent_initial_call=True
)
def callback_update_url(*args):
    return store_state.update_url(*args)
