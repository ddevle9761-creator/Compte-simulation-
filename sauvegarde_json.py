import json
import os



CUR_DIR = os.path.dirname(__file__)
DEFAULT_DATA_FILE = os.path.join(CUR_DIR, "data", "user.json")


DEFAULT_DATA_FILE_TRANSACTION = os.path.join(CUR_DIR, "data", "transaction.json")


def _ensure_parent_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


class JsonManager:
   
    def __init__(self, file_path=None):

        # Conserver deux fichiers logiques : un pour les utilisateurs, un pour
        # transactions, on l'utilise pour les transactions, sinon c'est le
        # fichier d'utilisateurs qui est pris en compte.

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


    def charger_json(self):
        try:
            with open(self.user_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []


    def save_user(self, user):
        _ensure_parent_dir(self.user_file)
        with open(self.user_file, 'w', encoding='utf-8') as f:
            json.dump(user, f, indent=4, ensure_ascii=False)
        return

    def list_transactions(self):
        try:
            with open(self.transaction_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []


    def save_transaction(self, transaction):
        _ensure_parent_dir(self.transaction_file)
        with open(self.transaction_file, 'w', encoding='utf-8') as f:
            json.dump(transaction, f, indent=4, ensure_ascii=False)
        return





_DEFAULT_MANAGER = None

def get_manager(file_path=None):
    global _DEFAULT_MANAGER
    if file_path is None:
        if _DEFAULT_MANAGER is None:
            _DEFAULT_MANAGER = JsonManager()
        return _DEFAULT_MANAGER
    return JsonManager(file_path)




