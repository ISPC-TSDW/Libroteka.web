# Tecnicatura Superior en Desarrollo web y Aplicaciones Digitales
## Programación Web 1

- Equipo: Bookster
- Proyecto: Libroteka
- Cohorte: 2023

Dependencies: 
- Node: "^18"
- Angular: "^17"
- Python: "^3.8"
- Django: "^4.2"
- SQLITE3: Incluido en Django

Puntos claves:
- Formulario IEEE830: [Link](https://github.com/ISPC-Bookster/Libroteka/wiki/Formulario-IEEE830)
- Ceremonias - Scrum: [Link](https://github.com/ISPC-Bookster/Libroteka/wiki/Scrum:-Registro-de-ceremonias)
- Historias de Usuario: [Link](https://github.com/ISPC-Bookster/Libroteka/wiki/Historias-de-Usuario)
- Milestones: [Link](https://github.com/ISPC-Bookster/Libroteka/milestones)
- Branching Strategy:

| Branch	| Naming Convention |
| -- | -- |
| Master |	"main"
| Desarrollo	| "dev"
| Rama Integrantes | "iniciales-feature"

## Descargar Mysql para poder usar la base de datos.
  # Windows:
    Descarga el instalador de MySQL desde [el sitio web oficial de MySQL.](https://dev.mysql.com/downloads/installer/)
    Durante la instalación, selecciona "MySQL Server"

  # Linux (Ubuntu):
    sudo apt update
    sudo apt install mysql-server
    sudo service mysql start
  # macOS:
    brew install mysql
    brew services start mysql

## Crear base de datos
  mysql -u root -p  ##si lo haces desde la terminal, 
                    ##si tenes MySQL Command Line Client no es necesario solo te va a pedir la password(2920 o la que configuraste cuando instalaste)

  CREATE DATABASE libroteka2024; # despues de crear la Db sigan con las instalaciones de abajo

## Credenciales Django Admin
- user: superadmin
- password: libroteka

## Librerías
- FrontEnd: fortawesome, nodemailer, bootstrap, rxjs, smtpjs, tslib, zone.js
- BackEnd: django, djangorestframework, django-cors-headers, Pillow, jsonfield, mysqlclient

## Correr localmente
<table>
<tr>
<th> FrontEnd </th>
<td>
Clone the project

```bash
  git clone https://github.com/LibrotekaISPC2023/Libroteka.git
``` 

Go to the project directory

```bash
  cd Frontend
```

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm start
```
</td>
</tr>
</table>
<table>
<tr>
<th> BackEnd </th>
<td>
Clone the project

```bash
  git clone https://github.com/LibrotekaISPC2023/Libroteka.git
``` 

Go to the project directory

```bash
  cd Backend/Libroteka
```

Activate Virtual environment  

```bash
# Windows users: create your branch, delete the linux folder '.backendLibroteka-env' as it has linux/mac configuration and you must create a virtual environment for Windows to install the requirements, remember not to include '.backendLibroteka-env' in your commits.
1. python -m venv .backendLibroteka-env
2. .backendLibroteka-env\Scripts\activate

# Linux users
source backendLibroteka-env/bin/activate 
```

Install Libraries

```bash
  pip install -r requirements.txt
```
## If you made changes to models.py:

```bash 
  python manage.py makemigrations
```
## Executes the necessary operations to synchronize the models with the database tables, 
## such as creating new tables, modifying columns, deleting tables, etc.

```bash
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```
</td>
</tr>
</table>

<table>
<tr>
<th> Docker <br> (Optional) </th>
<td>
Clone the project

```bash
  git clone https://github.com/LibrotekaISPC2023/Libroteka.git
``` 

Go to the project directory

```bash
  cd Frontend
```

Install dependencies

```bash
  npm install
```

Go back and Start the Docker Compose

```bash
  cd ..
```
```bash
  sudo docker compose up --build
```
</td>
</tr>
</table>
<table>

