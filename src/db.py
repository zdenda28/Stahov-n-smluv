import mysql.connector as mysql
import ares
import time


def create_db_conn():
    for x in range(20):
        # MySQl kontejner má při spuštění vždy spoždění, je potřeba čekat než nastartuje
        try:
            db = mysql.connect(
                host="mysql",  # pokud pouštím v dockeru tak mysql, pokud na lokalu tak localhost
                user="root",
                passwd="root",
                database="mydb"
            )
            #cursor = db.cursor()
            if db:
                #break
                return db
        except mysql.Error as err:
            print("Waiting for database connection")
            time.sleep(5)
        else:
            print("Database failed to start")
            exit()


def insert_supplier(ico, nace, ict):
    db = create_db_conn()
    cursor = db.cursor()
    sql = ("INSERT INTO dodavatele "
           "(ico, nace, ict_supplier) "
           "VALUES (%s, %s, %s)")
    values = (ico, nace, ict)
    cursor.execute(sql, values)
    db.commit()


def find_ict_supplier(ico):
    db = create_db_conn()
    cursor = db.cursor()
    sql = "SELECT * FROM dodavatele WHERE ico=%s"
    cursor.execute(sql, (ico,))
    supplier = cursor.fetchall()
    if supplier:
        # vrací 1 nebo 0 - sloupec ict supplier
        return supplier[0][2]
    else:
        # dotazování do aresu a vložení do db
        ares.is_subject_ict(ico)

