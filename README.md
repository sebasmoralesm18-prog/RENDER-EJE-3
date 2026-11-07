# Festival Vallenato - Sistema de Votaciones

## Instalación

### Crear entorno virtual

```powershell
python -m venv env_festival
```

### Instalar dependencias

```powershell
pip install django mysqlclient
```

### Crear la base de datos

```sql
CREATE DATABASE festival_db;
```

### Ejecutar migraciones

```powershell
python manage.py migrate
```

### Iniciar el servidor

```powershell
python manage.py runserver
```


