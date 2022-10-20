from google.cloud.bigtable import Client, row_filters


def get_formatted_data(project_id, instance_id, table_id, row_key):
    limit_filter = row_filters.CellsColumnLimitFilter(1)
    table = get_table(project_id, instance_id, table_id)
    row = table.read_row(row_key, limit_filter)
    return format_row(row)


def write_formatted_data(project_id, instance_id, table_id, formatted_data):
    table = get_table(project_id, instance_id, table_id)

    row_key = formatted_data[0]
    row = table.direct_row(row_key)

    families = formatted_data[1]
    for cf_name, cf in families.items():
        for column_name, value in cf.items():
            row.set_cell(cf_name, column_name, value)

    status = row.commit()
    if status.code != 0:
        raise IOError(status.message)


def get_table(project_id, instance_id, table_id):
    client = Client(project=project_id, admin=False)
    instance = client.instance(instance_id)
    return instance.table(table_id)


def format_row(row):
    v = (row.row_key.decode("utf-8"), {})
    for cf, cols in sorted(row.cells.items()):
        v[1][cf] = {}
        for col, cells in sorted(cols.items()):
            for cell in cells:
                column_name = col.decode("utf-8")
                cell_value = cell.value
                v[1][cf][column_name] = cell_value
    return v
