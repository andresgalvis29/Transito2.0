from flask import Flask ,render_template, request, redirect,url_for, flash
from flask_mysqldb import MySQL

aplicativo = Flask(__name__)
aplicativo.config['MYSQL_HOST'] = 'localhost'
aplicativo.config['MYSQL_USER'] = 'root'
aplicativo.config['MYSQL_PASSWORD'] = 'password'
aplicativo.config['MYSQL_DB'] = 'Transito'
mysql = MySQL(aplicativo)

@aplicativo.route('/')
def Index():
    return render_template('index.html')

@aplicativo.route('/iniciar_sesion')
def iniciar_sesion():
    return render_template('login.html')

@aplicativo.route('/anadir_conductor')
def añadir_conductor():
    return 'Añadir Conductor'

@aplicativo.route('/editar_conductor')
def editar_conductor():
    return 'Editar Conductor'

@aplicativo.route('/anadir_multa')
def añadir_multa():
    return 'Añadir Multa'



if __name__ == '__main__':
    aplicativo.run(port = 3000, debug = True)