from flask import Flask ,render_template, request, redirect,url_for, flash,session
from flask_mysqldb import MySQL
import hashlib

aplicativo = Flask(__name__)
aplicativo.config['MYSQL_HOST'] = '127.0.0.1'
aplicativo.config['MYSQL_USER'] = 'root'
aplicativo.config['MYSQL_PASSWORD'] = ''
aplicativo.config['MYSQL_DB'] = 'Transito'
mysql = MySQL(aplicativo)
aplicativo.secret_key = '666'

@aplicativo.route('/')
def Index():
    return render_template('index.html')

@aplicativo.route('/iniciar_sesion')
def iniciar_sesion():
    return render_template('login.html')

@aplicativo.route('/administrador',methods=['GET','POST'])
def administrador():
    if request.method == 'POST' and 'Usuario' in request.form and 'contra' in request.form:
        Usuario = request.form['Usuario']
        contra = request.form['contra']
        contraseña = (hashlib.sha1((contra).encode('utf-8')).hexdigest())
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Policia WHERE usuario= %s AND contraseña=%s',(Usuario,contraseña,))
        print(contraseña)
        cuenta = cur.fetchone()
        
    
    if cuenta:
            session['loggedin'] = True
            session['Usuario'] = cuenta[0]
            session['contraseña'] = cuenta[1]
            print(Usuario)
            return render_template('admin.html')
    else:
        flash("Datos incorrectos","warning")
        return render_template('login.html')

@aplicativo.route('/logoutadministrador')
def logoutadministrador():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('Index'))
        
@aplicativo.route('/anadirconductor')
def añadir_conductor():
    return render_template ('anadirconductor.html')

@aplicativo.route('/guardarconductor',methods=['POST'])
def guardar_conductor():
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        fechadenacimiento = request.form['fechadenacimiento']
        direccion = request.form['direccion']
        celular = request.form['celular']
        print (cedula)
        if (cedula and nombre and fechadenacimiento and direccion and celular != None):
           cur = mysql.connection.cursor()
           cur.execute('INSERT INTO Conductor (idConductor,NombreConductor,FechaNacimientoConductor,DireccionConductor,CelularConductor ) VALUES(%s,%s,%s,%s,%s)'
           ,(cedula,nombre,fechadenacimiento,direccion,celular))
           mysql.connection.commit() 
           return 'datos guardados'
        else: return 'No relleno todo los espacios'
    else: return 'Error'


@aplicativo.route('/editar_conductor')
def editar_conductor():
    return 'Editar Conductor'

@aplicativo.route('/anadir_multa')
def añadir_multa():
    return 'Añadir Multa'



if __name__ == '__main__':
    aplicativo.run(port = 3000, debug = True)