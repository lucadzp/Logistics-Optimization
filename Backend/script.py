from pathlib import Path
import os
import shutil

def delete_migrations_and_pycache(directory):
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                dir_path = os.path.join(root, dir_name)
                shutil.rmtree(dir_path)
                print(f"Archivo __pycache__ eliminado: {dir_path}")
            if dir_name == "migrations":
                dir_path = os.path.join(root, dir_name)
                shutil.rmtree(dir_path)
                print(f"Directorio migrations eliminado: {dir_path}")

        for file in files:
            if file == "db.sqlite3":
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Archivo db.sqlite3 eliminado: {file_path}")

# Ruta del directorio raíz del proyecto Django
BASE_DIR = Path(__file__).resolve().parent.parent
django_project_path = os.path.join(BASE_DIR, 'routes/')

print(django_project_path)

# Llamar a la función para eliminar los archivos de migraciones y los directorios __pycache__
delete_migrations_and_pycache(django_project_path)