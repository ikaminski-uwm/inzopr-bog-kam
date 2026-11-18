import sqlite3
import time
from datetime import datetime

db_file = "local.db"
nominaly = [10, 20, 50, 100, 200]

def wartosci_dict_to_list(input: dict) -> list:
    output = []
    for i in nominaly:
        output.append(input[i])
    return output

class ZestawZetonow():
    zetony: dict
    
    def __init__(self, wartosci: list):
        if(len(wartosci) != len(nominaly)):
            return None

        self.zetony = {}
        for i, nominal in enumerate(nominaly):
            self.zetony[nominal] = wartosci[i]


    def __str__(self):
        return self.zetony.__str__()

    def __add__(self, other):
        output = {}
        for key in other.zetony.keys():
            output[key] = self.zetony[key] + other.zetony[key]
        return output

    def __sub__(self, other):
        output = {}
        for key in other.zetony.keys():
            output[key] = self.zetony[key] - other.zetony[key]
        return output

    def contains(self, other):
        for key in other.zetony.keys():
            if(self.zetony[key] < other.zetony[key]): return False
        return True

class Transakcja():
    id_maszyny: int 
    is_wplata: bool
    data_czas: int
    zawartosc: ZestawZetonow
    was_noted: bool


    def __init__(self, id_maszyny, is_wplata, data_czas, zawartosc):
        self.id_maszyny = id_maszyny
        self.is_wplata = is_wplata
        self.data_czas = data_czas
        self.zawartosc = zawartosc
        self.was_noted = False

    def commit_to_database(self):
        if(self.was_noted): return

        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        command = f"""
            INSERT INTO historia (id_maszyny, is_wplata, data_czas, '10', '20', '50', '100', '200')
            VALUES ({self._to_sql()})
        """
        cursor.execute(command)
        connection.commit()
        connection.close()
        self.was_noted = True

    def _to_sql(self):
        return f"""
            {self.id_maszyny}, {int(self.is_wplata)}, {self.data_czas},
            {self.zawartosc.zetony[10]}, {self.zawartosc.zetony[20]}, {self.zawartosc.zetony[50]}, 
            {self.zawartosc.zetony[100]}, {self.zawartosc.zetony[200]}
        """

    def _bool_to_localized_string(self, boolean: bool):
        if(boolean): return "Tak"
        return "Nie"

    def to_list(self) -> list[str]:
        return [datetime.fromtimestamp(self.data_czas).strftime("%d-%m-%y, %H:%M"), "Magazyn", self._bool_to_localized_string(self.is_wplata),
            str(self.zawartosc.zetony[10]), str(self.zawartosc.zetony[20]), str(self.zawartosc.zetony[50]), 
            str(self.zawartosc.zetony[100]), str(self.zawartosc.zetony[200])]


def add_zetony(new_zestaw: ZestawZetonow, id_maszyny:int = 1):
    current = get_zetony_by_machine_id(id_maszyny)
    total = current + new_zestaw
    
    _set_zetony_by_machine_id(total, 1)

    unix_now:int = int(time.time())
    transankcja = Transakcja(id_maszyny, True, unix_now, new_zestaw)
    transankcja.commit_to_database()
    

def remove_zetony(new_zestaw: ZestawZetonow, id_maszyny:int = 1):
    #unix_now:int = time.unix_now
    current = get_zetony_by_machine_id(id_maszyny)
    if(current.contains(new_zestaw) == False):
        print("Not enough available")
        return
    total = current - new_zestaw

    _set_zetony_by_machine_id(total, 1)

    unix_now:int = int(time.time())
    transankcja = Transakcja(id_maszyny, False, unix_now, new_zestaw)
    transankcja.commit_to_database()

def _set_zetony_by_machine_id(total: ZestawZetonow, id_maszyny:int = 1):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    command = f"""
        UPDATE maszyny
        SET 
            '10' = {total[10]},
            '20' = {total[20]},
            '50' = {total[50]},
            '100' = {total[100]},
            '200' = {total[200]}
        WHERE id_maszyny = {id_maszyny}
    """
    cursor.execute(command)
    connection.commit()
    connection.close()


def get_zetony_by_machine_id(id_maszyny) -> ZestawZetonow:
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    command = f"""
        SELECT *
        FROM maszyny
        WHERE id_maszyny = {id_maszyny}; 
    """
    cursor.execute(command)
    sql_output = cursor.fetchone()
    connection.close()

    sql_output = sql_output[2:]
    output = ZestawZetonow([sql_output[0], sql_output[1], sql_output[2], sql_output[3], sql_output[4]])
    
    return output

def get_historia() -> list[Transakcja]:
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    command = """
        SELECT * FROM historia
    """
    cursor.execute(command)
    db_output = cursor.fetchall()
    connection.close()

    historia: list[Transakcja] = []
    for record in db_output:
        zestaw = ZestawZetonow(record[4:])
        new_element = Transakcja(record[1], record[2], record[3], zestaw)
        historia.append(new_element)

    return historia

def init_db():
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    output = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='maszyny';")
    if(output.fetchone() == None):
        #TODO Proceduralna ilość kolumn na podstawie nominałów
        cursor.execute("""
        CREATE TABLE maszyny(
            id_maszyny INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa TEXT,
            '10' INT,
            '20' INT,
            '50' INT,
            '100' INT,
            '200' INT
            );
        """)
        cursor.execute("""
        CREATE TABLE historia(
            id_transakcji INTEGER PRIMARY KEY AUTOINCREMENT,
            id_maszyny INTEGER,
            is_wplata INT,
            data_czas INT,
            '10' INT,
            '20' INT,
            '50' INT,
            '100' INT,
            '200' INT
            );
        """) #data_czas w Unix Time
        cursor.execute("""
            INSERT INTO maszyny
            VALUES(1, 'Główny Magazyn', 0, 0, 0, 0, 0);
        """)
        connection.commit()
        connection.close()
        

if __name__ == "__main__":
    init_db()
    historia = get_historia()
    for trans in historia:
        print(trans.to_list())