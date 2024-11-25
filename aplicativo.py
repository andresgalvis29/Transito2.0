from flask import Flask ,render_template, request, redirect,url_for, flash,session
from flask_mysqldb import MySQL
import logging
import hashlib

aplicativo = Flask(__name__)
aplicativo.config['MYSQL_HOST'] = 'appDB' # por si no se conecta docker conectar a 127.0.0.1
aplicativo.config['MYSQL_USER'] = 'root'
aplicativo.config['MYSQL_PASSWORD'] = 'admin'
aplicativo.config['MYSQL_DB'] = 'transito'
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
        cur.execute('SELECT * FROM Policia WHERE Usuario= %s AND Contraseña=%s',(Usuario,contraseña))
        logging.info('Contrasena: %s',contraseña )
        print(contraseña)
        cuenta = cur.fetchone()
        logging.info('Cuenta: %s', cuenta)
        print(cuenta)
        
    
    if cuenta:
            session['loggedin'] = True
            session['Usuario'] = cuenta[0]
            session['contraseña'] = cuenta[1]
            print(Usuario)
            return render_template('admin.html')
    else:
        flash("")
        return render_template('login.html')

@aplicativo.route('/logoutadministrador')
def logoutadministrador():
    session.pop('loggedin', None)
    session.pop('Usuario', None)
    session.pop('contraseña', None)
    session.clear()
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
           return render_template('admin.html')
        else: return 'No relleno todo los espacios'
    else: return 'Error'


@aplicativo.route('/anadircarro',methods=['GET','POST'])
def añadir_carro():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Marca')
    datamarca = cur.fetchall()
    cur.execute('SELECT idConductor FROM Conductor ')
    dataconductor = cur.fetchall()
    return render_template ('anadircarro.html',marca=datamarca,conductor=dataconductor)

@aplicativo.route('/guardarcarro',methods=['GET','POST'])
def guardar_carro():
    if request.method == 'POST':
        marca = request.form['marca']
        carro = request.form['carro']
        fechadefabricacion = request.form['fechadefabricacion']
        concesionaria = request.form['concesionaria']
        motor = request.form['motor']
        conductor = request.form['conductor']
        if (marca and carro and fechadefabricacion and concesionaria and motor and conductor != None):
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO Carro (idCarro,Concesionario,Motor,FechadeFabricacion,Conductor_idConductor,Marca_idMarca) VALUES(%s,%s,%s,%s,%s,%s)'
            ,(carro,concesionaria,motor,fechadefabricacion,conductor,marca))
            mysql.connection.commit()
            return render_template('admin.html')
        else: return 'no relleno los datos'
    else: return 'error'

@aplicativo.route('/anadirmulta',methods=['GET','POST'])
def añadir_multa():
    cur = mysql.connection.cursor()
    cur.execute('SELECT idConductor FROM Conductor ')
    dataconductor = cur.fetchall()
    cur.execute('SELECT Usuario FROM Policia ')
    datapolicia = cur.fetchall()
    return render_template('anadirmulta.html',conductor=dataconductor,policia=datapolicia)

@aplicativo.route('/guardarmulta',methods=['GET','POST'])
def guardar_multa():
    if request.method == 'POST':
        multa = request.form['multa']
        conductor = request.form['conductor']
        fechademulta = request.form['fechademulta']
        articulo = request.form['articulo']
        descripcion = request.form['descripcion']
        policia = request.form['policia']
        valor = request.form['valor']
        if(multa and conductor and fechademulta and articulo and descripcion and policia and valor != None):
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO Multa (CodigoMulta,ArticuloInfringido,Diamulta,ValorMulta,DescripcionMulta,Conductor_idConductor,Policia_Usuario) VALUES(%s,%s,%s,%s,%s,%s,%s)'
            ,(multa,articulo,fechademulta,valor,descripcion,conductor,policia))
            mysql.connection.commit()
            return render_template('admin.html')
        else: 'falta rellenar espacios'
    else: 'error'

@aplicativo.route('/loginmulta')
def pagar_multa():
    return render_template('loginmulta.html')

@aplicativo.route('/usuario1',methods=['GET','POST'])
def pago_de_multa():
    if request.method == 'POST' and 'Usuario' in request.form:
        Usuario = request.form['Usuario']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Multa WHERE Conductor_idConductor= {0}'.format(Usuario))
        print(Usuario)
        cuenta = cur.fetchone()

    if cuenta:
            session['loggedin'] = True
            session['Usuario'] = cuenta[0]
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM Multa WHERE Conductor_idConductor= {0}'.format(Usuario))
            cuenta = cur.fetchall()
            print(cuenta)
            return render_template('multa.html',multa=cuenta)
    else:
        flash("")
        return render_template('loginmulta.html')    

@aplicativo.route('/pagar/<string:id>')
def eliminar_multa(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE from Multa WHERE CodigoMulta = {0}'.format(id))
    mysql.connection.commit()
    flash("")
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('Index'))

@aplicativo.route('/informacion',methods=['GET','POST'])
def ver_datos():
    return render_template('login2.html')

@aplicativo.route('/datosusuario',methods=['GET','POST'])
def ver_datos2():
    if request.method == 'POST' and 'Usuario' in request.form:
        Usuario = request.form['Usuario']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Conductor WHERE idConductor= {0}'.format(Usuario))
        print(Usuario)
        cuenta = cur.fetchone()
    
    if cuenta:
            
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM Conductor WHERE idConductor= {0}'.format(Usuario))
            cuenta = cur.fetchall()
            print(cuenta)
            return render_template('usuario.html',usuario=cuenta)
    else:
        flash("")
        return render_template('loginmulta.html')    


if __name__ == '__main__':
    aplicativo.run(host='0.0.0.0',port = 3000, debug = True)