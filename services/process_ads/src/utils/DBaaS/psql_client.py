import psycopg2

class PSQLConnector():
    def __init__(self, host, database, user, password, port) -> None:
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        print("Connected to the PostgreSQL server successfully")
        self.init_db()
        print("Initialized the database successfully")

    def init_db(self):
        """
            creates the ads table if it doesn't exist
        """
        self.create_table("ads", "id SERIAL PRIMARY KEY, description VARCHAR(255), email VARCHAR(255), state VARCHAR(255), category VARCHAR(255)")


    def create_table(self, table_name, columns):
        """
            creates a table with the given name and columns
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.execute_query(query)
    

    def insert_into_table(self, table_name, columns, values):
        """
            inserts values into the table
        """
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.execute_query(query)
        return self.select_from_table(table_name, "*", "id = (SELECT MAX(id) FROM ads)")
    

    def select_from_table(self, table_name, columns, condition):
        """
            selects columns from the table
        """
        query = f"SELECT {columns} FROM {table_name} WHERE {condition}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    

    def delete_from_table(self, table_name, condition):
        """
            deletes rows from the table
        """
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.execute_query(query)
    

    def update_table(self, table_name, column, value, condition):
        """
            updates the table
        """
        query = f"UPDATE {table_name} SET {column} = {value} WHERE {condition}"
        self.execute_query(query)
    

    def execute_query(self, query):
        """
            executes the query
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()