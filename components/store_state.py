import re
from urllib.parse import urlparse, parse_qs
from dash import no_update, ctx, dcc
from dash.dependencies import Input, Output, State, ALL

class ParsedURL:
    def __init__(self, path, query_params, fragment, path_parts):
        self.path = path  # The path part of the URL
        self.query_params = query_params  # Query parameters in the URL
        self.fragment = fragment  # The fragment part of the URL
        self.path_parts = path_parts  # The different parts of the URL path

class StoreState:
    def __init__(self, persist_ids, store_type="session"):
        """Initialize StoreState class, set the storage type for dcc.Store, and set persistent IDs."""
        self.store_type = store_type  # Set storage type
        self.persist_ids = persist_ids  # Set persistent IDs

    def get_store_component(self, store_id):
        """Return the dcc.Store component using the specified storage type."""
        return dcc.Store(id=store_id, storage_type=self.store_type)

    @staticmethod
    def save_state_to_store(store_data, key, value):
        """Save data to dcc.Store."""
        if store_data is None or not isinstance(store_data, dict):
            store_data = {}
        store_data[key] = value
        return store_data

    @staticmethod
    def load_state_from_store(store_data, key):
        """Read data from dcc.Store."""
        if store_data and key in store_data:
            return store_data[key]
        return None

    @staticmethod
    def parse_url(url):
        """Parse the URL and extract useful information, returning a ParsedURL object."""
        url = str(url)
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        path_parts = parsed_url.path.strip("/").split("/")

        # Return a ParsedURL object
        return ParsedURL(
            path=parsed_url.path,
            query_params=query_params,
            fragment=parsed_url.fragment,
            path_parts=path_parts
        )

    def setup_dash_callbacks(self, app, store_id):
        """Set up Dash callbacks to manage dcc.Store data, supporting multiple dynamic input components."""

        @app.callback(
            Output(store_id, "data"),
            [Input(id, "value") for id in self.persist_ids],
            [Input("url", "href")],
            State(store_id, "data"),
            prevent_initial_call=True,
        )
        def manage_store_data(*args):
            print(args)
            *id, url, store_data = args

            if store_data is None:
                store_data = {}

            # Update store data with dynamic input values
            if ctx.triggered:
                triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

                # Save dynamic input values
                value = ctx.triggered[0]["value"]
                store_data = StoreState.save_state_to_store(store_data, triggered_id, value)

                # Save URL
                if "url" in triggered_id:
                    parsed_url = StoreState.parse_url(url)

                    path = parsed_url.path
                    query_params = parsed_url.query_params
                    path_parts = parsed_url.path_parts

                    # Extract model and type based on URL path
                    if len(path_parts) == 2:
                        model = path_parts[0]
                        type_part = path_parts[1]
                        store_data = StoreState.save_state_to_store(store_data, "model", model)
                        store_data = StoreState.save_state_to_store(store_data, "type", type_part)
                    elif len(path_parts) == 1:
                        model = path_parts[0]
                        if model in ["single", "range", "compare"]:
                            store_data = StoreState.save_state_to_store(store_data, "model", model)
                        else:
                            store_data = StoreState.save_state_to_store(store_data, "model", None)
                        store_data = StoreState.save_state_to_store(store_data, "type", None)

                    for key, value in query_params.items():
                        value = value[0]
                        store_data = StoreState.save_state_to_store(store_data, key, value)

            return store_data

        @app.callback(
            [Output(id, "value") for id in self.persist_ids] + [Output("url", "href")],
            [Input(id, "value") for id in self.persist_ids] + [Input("url", "href")],
            State(store_id, "data"),
            prevent_initial_call=True,
        )
        def manage_data_and_url(*args):
            # Separate input parameters
            input_values = args[:len(self.persist_ids)]
            url = args[len(self.persist_ids)]
            store_data = args[-1]

            # Initialize the return values for input components, defaulting to no_update
            output_values = [no_update] * len(self.persist_ids)
            new_url = no_update

            # Check if any events were triggered
            if ctx.triggered:
                triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

                # Handle data storage and loading logic
                if store_data is None:
                    store_data = {}

                # If the triggered change is from input values
                if triggered_id in self.persist_ids:
                    store_data[triggered_id] = ctx.triggered[0]["value"]

                # If the triggered change is from URL
                elif triggered_id == "url":
                    parsed_url = StoreState.parse_url(url)

                    # Parse URL path and query parameters
                    path_parts = parsed_url.path_parts
                    query_params = parsed_url.query_params

                    # Update model and type based on the URL
                    if len(path_parts) == 2:
                        model = path_parts[0]
                        type_part = path_parts[1]
                        store_data["model"] = model
                        store_data["type"] = type_part
                    elif len(path_parts) == 1:
                        model = path_parts[0]
                        if model in ["single", "range", "compare"]:
                            store_data["model"] = model
                        else:
                            store_data["model"] = None
                        store_data["type"] = None

                    # Store query parameters
                    for key, value in query_params.items():
                        store_data[key] = value[0]

                # Load data into components
                for i, key in enumerate(self.persist_ids):
                    output_values[i] = store_data.get(key, no_update)

                # Update the URL
                url_tmp = store_data.get("url", None)
                model_tmp = store_data.get("model", None)
                type_tmp = store_data.get("type", None)

                if url_tmp:
                    url_match = re.match(r"^https?://[^/]+", url_tmp)
                    if url_match:
                        base_url = url_match.group(0)
                    else:
                        return output_values + [no_update]

                    if model_tmp in ["single", "range"]:
                        if not base_url.endswith("/"):
                            base_url += "/"
                        base_url += f"{model_tmp}?"
                    elif model_tmp == "compare":
                        if not base_url.endswith("/"):
                            base_url += "/"
                        base_url += f"{model_tmp}/{type_tmp}?"
                    else:
                        if not base_url.endswith("/"):
                            base_url += "/"

                    query_params = []
                    processed_keys = set()

                    for key, value in store_data.items():
                        if key not in ["url", "model", "compare"] and value is not None:
                            if key not in processed_keys:
                                query_params.append(f"{key}={value}")
                                processed_keys.add(key)

                    full_url = base_url
                    if query_params:
                        full_url += "&".join(query_params)

                    new_url = full_url

            return output_values + [new_url]
