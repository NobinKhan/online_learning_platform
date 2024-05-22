
def read_sql_file(sql_file_path: str) -> str:
    with open("sql/" + sql_file_path, "r") as sql_file:
        return sql_file.read()