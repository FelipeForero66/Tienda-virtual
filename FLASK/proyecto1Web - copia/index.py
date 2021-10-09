from datetime import date
from flask import Flask, render_template, request ,redirect ,url_for, session ,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors 
import re 
import pandas as pd
import pymysql
from sqlalchemy import create_engine

app = Flask(__name__)

##MySQL Connection 
app.config['MYSQL_HOST'] = 'bdgrupo206263.czo3ixoe3xoe.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'bdgrupo206263'
app.config['MYSQL_DB'] = 'bdgrupo206263'
mysql = MySQL(app)

##MySQL Connection2 
conn = pymysql.connect(
    host='bdgrupo206263.czo3ixoe3xoe.us-east-1.rds.amazonaws.com',
    port=3306,
    user='admin',
    password='bdgrupo206263',
    database='bdgrupo206263',
    charset='utf8'
)

## setting
app.secret_key = 'mysecretkey'

@app.route('/')
def about():
    return render_template('Login.html')

@app.route('/Cliente') 
def Cliente():
    cur = mysql.connection.cursor()
    cur.execute('Select * from Clientes ')
    data = cur.fetchall()
    # print(data)
    return render_template('Cliente.html',contacts = data)


@app.route('/addCli', methods=['POST']) 
def addCli():
    if request.method == 'POST':
        cedula = request.form['ced']
        nombre = request.form['name']
        correo = request.form['mail']
        usuario = request.form['usua']
        contraseña = request.form['passwd']
        cur = mysql.connection.cursor()
        # if class=="boton"
        cur.execute('INSERT INTO Clientes VALUES (%s,%s,%s,%s,%s)',
            (cedula,nombre,correo,usuario,contraseña))
        mysql.connection.commit()
        flash('Usuario agregado!')
        return redirect(url_for('Cliente'))


@app.route('/lookCli', methods=['GET','POST']) 
def lookCli():
    if request.method == 'POST':
        # cedula = request.form['ced']
        # print (cedula)
        # cur = mysql.connection.cursor()
        # cur.execute('SELECT * FROM Clientes WHERE (%s)',
        #     (cedula))
        # mysql.connection.commit()
        # flash('Usuario consultado!')
        return redirect(url_for('Cliente'))

@app.route('/deleteCli/<string:id>') 
def deleteCli(id):
    print(id)
    return id

@app.route('/Proveedor') 
def Proveedor():
    return render_template('Proveedor.html')

@app.route('/addPro', methods=['POST']) 
def addPro():
    if request.method == 'POST':
        nitPro = request.form['nitt']
        nombrePro = request.form['NomPro']
        direccion = request.form['dire']
        telUsuario = request.form['telusua']
        city = request.form['ciudad']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO Proveedores VALUES (%s,%s,%s,%s,%s)',
            (nitPro,nombrePro,direccion,telUsuario,city))
        mysql.connection.commit()
        flash('Proveedor agregado!')
        return redirect(url_for('Proveedor'))


@app.route('/Productos',methods=["GET","POST"]) 
def Productos():
    return render_template('Productos.html')

@app.route('/data',methods=['GET','POST'])
def data():
    if request.method=='POST':
        file = request.form['upload-file']
        data = pd.read_excel(file, sheet_name='Hoja1', header=None
        ,dtype={'Cod_Pro': int, 'ivaCompra': int, 'nitPro': int, 'Nombre': str, 'precioCompra': int, 'precioVenta': int})
        
        redords = data.to_records(index=False)
        result = list(redords)
        print(result)
        cur = mysql.connection.cursor()

        cont=0
        for i in result:
            print(i)
            cur.execute('INSERT INTO productos VALUES (%s,%s,%s,%s,%s,%s)',          
            (int(result[cont][0]),int(result[cont][1]),int(result[cont][2]),result[cont][3],int(result[cont][4]),int(result[cont][5])))
            cont= cont+1
        mysql.connection.commit()
        flash('Productos agregador a la base de datos!')
        return redirect(url_for('Productos'))
        # return render_template('data.html',data=data.to_html())


@app.route('/Ventas') 
def Ventas():
    return render_template('ventas.html')


@app.route('/Reporte') 
def Reporte():
    return render_template('reporte.html')

@app.route('/ListaUsuarios') 
def ListaUsuarios():
    cur = mysql.connection.cursor()
    cur.execute('Select * from usuarios')
    data = cur.fetchall()
    print(data)
    return render_template('listaUsuario.html',contacts = data)
    # return render_template('Cliente.html',contacts = data)

@app.route('/ListaClientes') 
def ListaClientes():
    cur = mysql.connection.cursor()
    cur.execute('Select * from Clientes')
    data = cur.fetchall()
    print(data)
    return render_template('listaClientes.html',contacts = data)


#####################################################


@app.route('/tabla') 
def tabla():
    return render_template('tabla.html')

@app.route('/addContact', methods=['POST']) 
def addContact():
    if request.method == 'POST':
        identificacion = request.form['id']
        nombre = request.form['name']
        apellido = request.form['ape']
        dirreccion = request.form['dir']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO pruebaCon VALUES (%s,%s,%s,%s)', (identificacion,nombre,apellido,dirreccion))
        mysql.connection.commit()
        return 'Recibido'


@app.route('/edit') 
def editar():
    return 'editar'

@app.route('/delete') 
def borrar():
    return 'borrar'


if __name__== '__main__':
    app.run(debug=True)
