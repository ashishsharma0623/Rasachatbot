import mysql.connector
from typing import Dict, Any

class WeatherDatabase:

    def __init__(self, host: str, database: str, user: str, password: str):
        self.connection = mysql.connector.connect(
            host="127.0.0.1:3306",
            database="webot",
            user="webot",
            password="webot"
        )
        self.create_weather_table()

    def create_weather_table(self):
        cursor = self.connection.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS weather (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city VARCHAR(255) NOT NULL,
                temperature FLOAT NOT NULL,
                description VARCHAR(255) NOT NULL
            );
        """
        cursor.execute(create_table_query)
        self.connection.commit()

    def insert_weather_data(self, data: Dict[str, Any]):
        cursor = self.connection.cursor()
        insert_query = """
            INSERT INTO weather (city, temperature, description)
            VALUES (%s, %s, %s);
        """
        values = (data['city'], data['temperature'], data['description'])
        cursor.execute(insert_query, values)
        self.connection.commit()

    def close(self):
        self.connection.close()

# Example usage:
if __name__ == "__main__":
    # Replace these values with your MySQL database credentials
    db = WeatherDatabase(
        host="127.0.0.1:3306",
        database="webot",
        user="webot",
        password="webot"
    )

    # Assuming you have weather_data from your API response
    weather_data = {
        'city': 'YourCity',
        'temperature': 25.5,
        'description': 'Sunny'
    }

    db.insert_weather_data(weather_data)
    db.close()
