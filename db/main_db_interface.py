import sqlite3


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    cur = conn.cursor()
    cur.execute(
        """SELECT count(name) FROM sqlite_master WHERE type='table' AND name = ?""",
        (table_name,),
    )
    return cur.fetchone()[0] == 1


def record_exists(
    conn: sqlite3.Connection, field_name: str, value: any, table_name: str
) -> bool:
    cur = conn.cursor()
    cur.execute(
        """SELECT count({}) FROM {} WHERE {} = ?""".format(
            field_name, table_name, field_name
        ),
        (value,),
    )
    return cur.fetchone()[0] == 1

def _record_exists(
    conn: sqlite3.Connection, query: str, parameters
) -> bool:
    cur = conn.cursor()
    
    cur.execute(
        query,
        parameters
    )
    return cur.fetchone()[0] == 1


def create_talbe(
    conn: sqlite3.Connection, fields: dict[str, str], table_name: str
) -> None:
    cur = conn.cursor()
    query = "CREATE TABLE {} ({})".format(
        table_name, ",".join("{} {}".format(key, val) for key, val in fields.items())
    )
    cur.execute(query)


def create_record(
    conn: sqlite3.Connection,
    fields_names: list[str],
    values: list[any],
    table_name: str,
) -> None:
    cur = conn.cursor()
    query = "INSERT INTO {} ({}) VALUES ({})".format(
        table_name,
        ",".join(str(f) for f in fields_names),
        ",".join(str(v) for v in values),
    )
    cur.execute(query)
    conn.commit()


def update_record(
    conn: sqlite3.Connection,
    condition_field_name: str,
    condition_field_value: any,
    fields_names: list[str],
    values: list[any],
    table_name: str,
) -> None:
    cur = conn.cursor()
    query = """UPDATE {} SET {} WHERE {} = ?""".format(
        table_name,
        ",".join(
            "{} = {}".format(str(f), str(v)) for f, v in zip(fields_names, values)
        ),
        condition_field_name,
    )
    cur.execute(query, (condition_field_value,))
    conn.commit()


def update_record_and_operator(
    conn: sqlite3.Connection,
    first_condition_field_name: str,
    first_condition_field_value: any,
    second_condition_field_name: str,
    second_condition_field_value: any,
    fields_names: list[str],
    values: list[any],
    table_name: str,
) -> None:
    cur = conn.cursor()
    query = """UPDATE {} SET {} WHERE {} = ? AND {} = ?""".format(
        table_name,
        ",".join(
            "{} = {}".format(str(f), str(v)) for f, v in zip(fields_names, values)
        ),
        first_condition_field_name,
        second_condition_field_name,
    )
    cur.execute(
        query,
        (
            first_condition_field_value,
            second_condition_field_value,
        ),
    )
    conn.commit()


def remove_record(
    conn: sqlite3.Connection,
    condition_field_name: str,
    condition_field_value: any,
    table_name: str,
) -> None:
    cur = conn.cursor()
    query = """DELETE FROM {} WHERE {} = ?""".format(table_name, condition_field_name)
    cur.execute(query, condition_field_value)
    conn.commit()


def select_record(
    conn: sqlite3.Connection,
    condition_field_name: str,
    condition_field_value: any,
    table_name: str,
) -> dict[str, any]:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """SELECT * FROM {} WHERE {} = ?""".format(table_name, condition_field_name),
        (condition_field_value,),
    )
    for row in cur.fetchall():
        return dict(row)


def select_records(
    conn: sqlite3.Connection,
    condition_field_name: str,
    condition_field_value: any,
    table_name: str,
) -> list[dict[str, any]]:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """SELECT * FROM {} WHERE {} = ?""".format(table_name, condition_field_name),
        (condition_field_value,),
    )
    result = list()
    for row in cur.fetchall():
        result.append(dict(row))
    return result


class DBInterface:
    table_exists = staticmethod(table_exists)
    record_exists = staticmethod(record_exists)
    create_talbe = staticmethod(create_talbe)
    create_record = staticmethod(create_record)
    update_record = staticmethod(update_record)
    remove_record = staticmethod(remove_record)
    select_record = staticmethod(select_record)
    select_records = staticmethod(select_records)
    update_record_and_operator = staticmethod(update_record_and_operator)
    _record_exists = staticmethod(_record_exists)
