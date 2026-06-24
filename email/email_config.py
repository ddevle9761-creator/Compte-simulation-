import os

# Charger la configuration SMTP depuis les variables d'environnement.
# Utiliser les variables suivantes : SMTP_EMAIL, SMTP_PASSWORD,
# SMTP_SERVER, SMTP_PORT. Laisser la valeur vide force l'utilisateur à
# configurer correctement l'environnement.
config_email = os.environ.get('SMTP_EMAIL', '')
config_password = os.environ.get('SMTP_PASSWORD', '')
config_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
config_port = int(os.environ.get('SMTP_PORT', '587'))