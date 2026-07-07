import json
import os
import sqlite3



CUR_DIR = os.path.dirname(__file__)
DEFAULT_DATA_FILE = os.path.join(CUR_DIR, "data", "user.db")


DEFAULT_DATA_FILE_TRANSACTION = os.path.join(CUR_DIR, "data", "transaction.db")


def _ensure_parent_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


class JsonManager:

    __tablename__ = 'REPOSITORIES'

    def __init__(self, file_path=None):

        # les fichiers de save
        self.user_file = DEFAULT_DATA_FILE
        self.transaction_file = DEFAULT_DATA_FILE_TRANSACTION

        if file_path:
            base = os.path.basename(file_path).lower()
            if 'transaction' in base:
                self.transaction_file = file_path
                _ensure_parent_dir(self.transaction_file)
            else:
                self.user_file = file_path
                _ensure_parent_dir(self.user_file)
        else:
            _ensure_parent_dir(self.user_file)



    def __depot_users__(self):

        ok = True
        try:
            _ensure_parent_dir(self.user_file)
            conn = sqlite3.connect(self.user_file)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom text not null,
            prenom text not null,
            age integer not null,
            sexe text not null,
            numero integer not null,
            email text not null,
            mdp text not null,
            solde integer not null
            )''')
            conn.commit()
            conn.close()

        except Exception as e:
            ok = False
        return ok

    def sauvegarde_user(self, user):
        if self.__depot_users__():
            conn = sqlite3.connect(self.user_file)
            cursor = conn.cursor()
            try:
                cursor.execute("""INSERT INTO users (nom, prenom, age, sexe, numero, email, mdp, solde) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",user)
                conn.commit()
                conn.close()
            except ValueError as e:
                return str(e)

            conn.close()
        return True

    def supprimer_par_nom(self, nom):
        try:
            conn = sqlite3.connect(self.user_file)
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM users WHERE nom  = (?) """, (nom,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return str(e)
        return False


    def supprime_par_id(self, id):
        try:
            conn = sqlite3.connect(self.user_file)
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM users WHERE id  = (?) """, (id,))
            conn.commit()
            conn.close()
        except Exception as e:
            return str(e)
        return True

    def les_users(self):
        try:
            conn = sqlite3.connect(self.user_file)
            cursor = conn.cursor()
            data = cursor.execute("""SELECT * FROM users """).fetchall()
            conn.close()
            return data
        except Exception as e:
            return str(e)
        return

    def rechercher_par_nom(self, nom):
        try:
            conn = sqlite3.connect(self.user_file)
            cursor = conn.cursor()
            data = cursor.execute("""SELECT * FROM users WHERE nom  = (?) """, (nom,)).fetchall()
            return data
        except Exception as e:
            return str(e)
        conn.close()


    def rechercher_par_id(self, id):
        try:
            conn = sqlite3.connect(self.user_file)
            cursor = conn.cursor()
            data = cursor.execute("""SELECT * FROM users WHERE id  = (?) """, (id,)).fetchone()
            conn.close()
            return data
        except Exception as e:
            return str(e)


    def __transaction_table__(self):
        try:
            _ensure_parent_dir(self.transaction_file)
            conn = sqlite3.connect(self.transaction_file)
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source text not null,
            destination text not null,
            montant integer not null,
            date text not null
            )""")
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return str(e)
        return False

    def sauvegarde_transaction(self, historique):
        if self.__transaction_table__():
            try:
                conn = sqlite3.connect(self.transaction_file)
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO transactions (source, destination, montant, date) VALUES (?, ?, ?, ?)""", historique)
                conn.commit()
                conn.close()
                return True
            except ValueError as e:
                return str(e)

    def voir_les_transaction(self):
        try:
            conn = sqlite3.connect(self.transaction_file)
            cursor = conn.cursor()
            data = cursor.execute("""SELECT * FROM transactions """).fetchall()
            conn.close()
            return data
        except Exception as e:
            return str(e)

    def supprimer_transaction_par_id(self, id):
        try:
            conn = sqlite3.connect(self.transaction_file)
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM transactions WHERE id  = (?) """, (id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return str(e)
        return False

    def recherche_transaction_par_date(self, date):
        try:
            conn = sqlite3.connect(self.transaction_file)
            cursor = conn.cursor()
            data = cursor.execute("""SELECT * FROM transactions WHERE date  = (?) """, (date,)).fetchall()
            conn.commit()
            conn.close()
            return data
        except Exception as e:
            return str(e)
        return False

    def recherche_transaction_par_source(self, source):
        try:
            conn = sqlite3.connect(self.transaction_file)
            cursor = conn.cursor()
            data = cursor.execute("""SELECT * FROM transactions WHERE source  = (?) """, (source,)).fetchall()
            conn.commit()
            conn.close()
            return data
        except Exception as e:
            return str(e)
        return False

    def update_user(self, id, colonne, arg):
        user = self.rechercher_par_id(id)
        if user:
            try:
                conn = sqlite3.connect(self.user_file)
                cursor = conn.cursor()
                cursor.execute(f"""UPDATE users SET {colonne} = ?  WHERE id = ? """, (arg, id))
                conn.commit()
                return True
            except Exception as e:
                return str(e)

            finally:
                conn.close()

    def total_balance(self):
        try:
            conn = sqlite3.connect(self.user_file)
            cursor = conn.cursor()
            data = cursor.execute("""SELECT solde FROM users """).fetchall()
            return data
        except Exception as e:
            return str(e)

        finally:
            conn.close()





_DEFAULT_MANAGER = None

def get_manager(file_path=None):
    global _DEFAULT_MANAGER
    if file_path is None:
        if _DEFAULT_MANAGER is None:
            _DEFAULT_MANAGER = JsonManager()
        return _DEFAULT_MANAGER
    return JsonManager(file_path)




