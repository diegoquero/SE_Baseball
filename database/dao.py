from database.DB_connect import DBConnect
from model.TEAM import Team
from model.salary import Salary


class DAO:
    @staticmethod
    def readAllTeams():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM team """

        cursor.execute(query)

        for row in cursor:
            team = Team(row['id'], row['year'], row['team_code'], row['name'])
            result[team.id] = team

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def readAllSalary():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM salary """

        cursor.execute(query)

        for row in cursor:
            salary = Salary(**row)
            result[salary.id] = salary

        cursor.close()
        conn.close()
        return result