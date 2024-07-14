from flask import Flask

# Importar función para permitir el render de los templates
from flask import render_template, request, redirect, flash, url_for

# Conexión la base de datos en mysql
from flask_mysqldb import MySQL

# Crear aplicación

app = Flask(__name__)

app.secret_key = '3210'

mysql  = MySQL()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'menu'

mysql = MySQL(app)

# Ruta de la raiz del sitio y función para mostrar los registros en el index
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

# Ruta admin y función para mostrar los registros en la página de admin
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
    # Condicional para seleccionar la tabla correspondiente (cafe o postres)
    # Tabla cafe
    if 'txtCafe' in request.form and 'txtPrecio' in request.form:
        _nombre = request.form['txtCafe']
        _precio = request.form['txtPrecio']
        
        # Armamos tupla con esos valores:
        datos = (_nombre, _precio)
        
        # Armamos la sentencia SQL que va a almacenar estos datos en la DB:
        sql = "INSERT INTO `menu`.`cafe` \
            (`id`,`nombre`,`precio`) \
                VALUES(NULL, %s, %s);"
    # Tabla postres           
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
    conn = mysql.connection # Nos conectamos a la bbdd
    cursor = conn.cursor() # En cursor vamos a realizar las operaciones
    # Condicional para seleccionar la tabla correspondiente (cafe o postres)
    # Tabla cafe
    if form_type == 'cafe':
        cursor.execute("SELECT * FROM cafe WHERE id=%s", (id,))
        cafes = cursor.fetchall()
        cursor.close()
        return render_template('coffee/edit.html', cafes=cafes)
    # Tabla postres 
    elif form_type == 'postres':
        cursor.execute("SELECT * FROM postres WHERE id=%s", (id,))
        postres = cursor.fetchall()
        cursor.close()
        return render_template('coffee/edit.html', postres=postres)

#--------------------------------------------------------------------------------------

# Función para actualizar los datos de un registro
@app.route('/update', methods=['POST'])
def update():
    conn = mysql.connection # Nos conectamos a la bbdd
    cursor = conn.cursor() # En cursor vamos a realizar las operaciones
    # Condicional para seleccionar la tabla correspondiente (cafe o postres)
    # Tabla cafe
    if 'txtCafe' in request.form and 'txtPrecio' in request.form:
        _nombre = request.form['txtCafe']
        _precio = request.form['txtPrecio']
        _id = request.form['txtID']
 
        # Definimos la sentencia SQL
        sql = "UPDATE menu.cafe SET nombre=%s, precio=%s WHERE id=%s"
        params = (_nombre, _precio, _id)
        # Ejecutamos la sentencia SQL en el cursor
        cursor.execute(sql, params)
        conn.commit()
        return redirect('/admin')
    # Tabla postres 
    elif 'txtPostre' in request.form and 'txtPrecio2' in request.form:
        _nombre = request.form['txtPostre']
        _precio = request.form['txtPrecio2']
        _id = request.form['txtID2']
        # Definimos la sentencia SQL
        sql = "UPDATE menu.postres SET nombre=%s, precio=%s WHERE id=%s"
        params = (_nombre, _precio, _id)
        # Ejecutamos la sentencia SQL en el cursor
        cursor.execute(sql, params)
        conn.commit()
        return redirect('/admin')

#--------------------------------------------------------------------------------------

# Función para eliminar registro
@app.route('/destroy/<form_type>/<int:id>')
def destroy(form_type, id):
    conn = mysql.connection # Nos conectamos a la bbdd
    cursor = conn.cursor() # Almacenamos lo que devuelva la consulta
    
    # Condicional para seleccionar la tabla correspondiente (cafe o postres)
    # Tabla cafe
    if form_type == 'cafe':
        cursor.execute("DELETE FROM `menu`.`cafe` WHERE id=%s", (id,)) # Ejecutamos la secuencia SQL
        conn.commit()
        return redirect('/admin')
    # Tabla postres
    elif form_type == 'postres':
        cursor.execute("DELETE FROM `menu`.`postres` WHERE id=%s", (id,)) # Ejecutamos la secuencia SQL
        conn.commit()
        return redirect('/admin')

#--------------------------------------------------------------------------------------

# Lineas requeridas por python para empezar a trabajar cn la app

if __name__ == '__main__':
    app.run(debug=True)