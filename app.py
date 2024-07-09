from flask import Flask

# Importar función para permitir el render de los templates
from flask import render_template, request, redirect, send_from_directory

# Conexión la base de datos en mysql
from flask_mysqldb import MySQL

# Importamos datetime para nombre de las fotos y evitar sobrescritura
from datetime import datetime

#Importamos paquetes de intergaz con el sistema operativo
import os

# Crear aplicación

app = Flask(__name__)

mysql  = MySQL()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'menu'

mysql = MySQL(app)

# Ruta de la raiz del sitio
@app.route('/')
def index():
    conn = mysql.connection  # Nos conectamos a la bbdd

    # Obtener datos de la tabla cafe
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cafe;")
    db_cafe = cursor.fetchall()
    cursor.close()

    # Obtener datos de la tabla postres
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM postres;")
    db_postres = cursor.fetchall()
    cursor.close()

    #Devolvemos el código HTML renderizado
    return render_template('coffee/index.html', cafes=db_cafe, postres=db_postres)

#--------------------------------------------------------------------------------------

# Ruta admin
@app.route('/admin')
def admin():
    conn = mysql.connection  # Nos conectamos a la bbdd

    # Obtener datos de la tabla cafe
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cafe;")
    db_cafe = cursor.fetchall()
    cursor.close()

    # Obtener datos de la tabla postres
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM postres;")
    db_postres = cursor.fetchall()
    cursor.close()

    #Devolvemos el código HTML renderizado
    return render_template('coffee/admin.html', cafes=db_cafe, postres=db_postres)

#--------------------------------------------------------------------------------------

#Función para entrar a la pestaña en donde se agregan datos
@app.route('/create')
def create():
    return render_template('coffee/create.html')

#--------------------------------------------------------------------------------------
# Función para recibir los valores del formulario y pasarlos a variables locales
@app.route('/store', methods=['POST'])
def storage():
    if 'txtCafe' in request.form and 'txtPrecio' in request.form:
        _nombre = request.form['txtCafe']
        _precio = request.form['txtPrecio']
        
        # Armamos tupla con esos valores:
        datos = (_nombre, _precio)
        
        # Armamos la sentencia SQL que va a almacenar estos datos en la DB:
        sql = "INSERT INTO `menu`.`cafe` \
            (`id`,`nombre`,`precio`) \
                VALUES(NULL, %s, %s);"
    elif 'txtPostre' in request.form and 'txtPrecio2' in request.form:
        _nombre = request.form['txtPostre']
        _precio = request.form['txtPrecio2']
        
        # Armamos tupla con esos valores:
        datos = (_nombre, _precio)
        
        # Armamos la sentencia SQL que va a almacenar estos datos en la DB:
        sql = "INSERT INTO `menu`.`postres` \
            (`id`,`nombre`,`precio`) \
                VALUES(NULL, %s, %s);"
    else:
        return "Error: Datos del formulario no válidos", 400

    conn = mysql.connection  # Nos conectamos a la bbdd
    cursor = conn.cursor()  # En cursor vamos a realizar las operaciones
    cursor.execute(sql, datos)  # Ejecutamos la sentencia SQL en el cursor
    conn.commit()  # Hacemos el commit
    cursor.close()
    
    return redirect('/admin')  # Volvemos al admin

#--------------------------------------------------------------------------------------

# Función para editar un registro
@app.route('/edit/<form_type>/<int:id>')
def edit(form_type, id):
    conn = mysql.connection
    cursor = conn.cursor()

    if form_type == 'cafe':
        cursor.execute("SELECT * FROM cafe WHERE id=%s", (id,))
        cafes = cursor.fetchall()
        cursor.close()
        return render_template('coffee/edit.html', cafes=cafes)
    elif form_type == 'postres':
        cursor.execute("SELECT * FROM postres WHERE id=%s", (id,))
        postres = cursor.fetchall()
        cursor.close()
        return render_template('coffee/edit.html', postres=postres)

#--------------------------------------------------------------------------------------

# Función para actualizar los datos de una pelicula
@app.route('/update', methods=['POST'])
def update():
    form_type = request.form.get('form_type')
    if form_type == 'cafe':
        _cafe = request.form['txtCafe']
        _precio = request.form['txtPrecio']
        _id = request.form['txtID']
    
        conn = mysql.connection
        cursor = conn.cursor()
    
        sql = "UPDATE menu.cafe SET nombre=%s, precio=%s WHERE id=%s"
        params = (_cafe, _precio, _id)
    
        cursor.execute(sql, params)
    
        conn.commit()
        conn.close()
        return redirect('/admin')
    
    elif form_type == 'postres':
        _postre = request.form['txtPostre']
        _precio = request.form['txtPrecio2']
        _id = request.form['txtID2']
    
        conn = mysql.connection
        cursor = conn.cursor()
    
        sql = "UPDATE menu.postres SET nombre=%s, precio=%s WHERE id=%s"
        params = (_postre, _precio, _id)
    
        cursor.execute(sql, params)
    
        conn.commit()
        conn.close()
        return redirect('/admin')

#--------------------------------------------------------------------------------------

# Función para eliminar registro
@app.route('/destroy/<form_type>/<int:id>')
def destroy(form_type, id):
    
    if form_type == 'cafe':
        conn = mysql.connection # Nos conectamos a la bbdd
        cursor = conn.cursor() # Almacenamos lo que devuelva la consulta
        cursor.execute("DELETE FROM `menu`.`cafe` WHERE id=%s", (id,)) # Ejecutamos la secuencia SQL
        conn.commit()
        return redirect('/admin')
    
    elif form_type == 'postres':
        conn = mysql.connection # Nos conectamos a la bbdd
        cursor = conn.cursor() # Almacenamos lo que devuelva la consulta
        cursor.execute("DELETE FROM `menu`.`postres` WHERE id=%s", (id,)) # Ejecutamos la secuencia SQL
        conn.commit()
        return redirect('/admin')

#--------------------------------------------------------------------------------------

# Lineas requeridas por python para empezar a trabajar cn la app

if __name__ == '__main__':
    app.run(debug=True)