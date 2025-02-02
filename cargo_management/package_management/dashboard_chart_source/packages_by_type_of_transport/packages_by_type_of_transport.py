import frappe
from frappe.desk.doctype.dashboard_chart.dashboard_chart import get as build_chart_data


@frappe.whitelist(methods='POST')
def get(chart_name=None, chart=None, no_cache=None, filters=None, from_date=None, to_date=None, timespan=None,
        time_interval=None, heatmap_year=None, refresh=None):
    """ Custom Chart using core Dashboard Chart Data.
    We need a Count Chart for each transportation_type. We request each data and create a single Cross Chart.
    If we @cache_source in core we get a trouble because Core tries to find a Dashboard Chart from Database.

    # TODO: Make this with some dynamic variable.
    chart['yMarkers'] = [{ 'label': "Marker", 'value': 70 }]
    chart['yRegions'] = [{ 'label': "Region", 'start': 5, 'end': 50 }]
    """
    filters = frappe.parse_json(filters)  # Converting Filters

    chart_config = {
        'from_date': from_date or None,
        'to_date': to_date or None,
        'timespan': timespan or 'Last Quarter',
        'time_interval': time_interval or 'Weekly',
        'refresh': refresh,
        # We request a count of packages and time series based on creation (This data is stored in Doc)
        'chart_type': 'Count',     # Unnecessary
        'based_on': 'creation',
        'document_type': 'Package',
        'group_by_type': 'Count',  # Unnecessary
        # TODO: Append filters Dynamically
        'filters_json': [
            ['Package', 'transportation_type', '=', 'Sea', False],
            ['Package', 'assisted_purchase', '=', filters['assisted_purchase'], False],
        ],
        'name': 'SEA'  # Readable label name
    }

    chart = build_chart_data(chart=chart_config, no_cache=True)  # Fetching initial 'Sea' Chart

    chart_config['name'], chart_config['filters_json'][0][3] = 'AIR', 'Air'  # Change filter to 'Air'

    chart['datasets'].append(build_chart_data(chart=chart_config, no_cache=True)['datasets'][0])  # append only dataset

    return chart
