'''
Librería creada por 
Adrián Fernández Roa.

'''
import bcrypt
from flask import Flask, render_template, request
import mysql.connector
import requests

def connectBD():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "04112002Aa",
        database = "Libreria"
    )
    return db


def createUser(name,apellidos,correo,passwordhash):
    db=connectBD()
    cursor=db.cursor()
    query = f"insert into Usuario (Nombre,Apellidos,Correo,Contraseña) VALUES(%s,%s,%s,%s);"
    valores=(name,apellidos,correo,passwordhash)
    cursor.execute(query,valores)
    db.commit()
    db.close()
    return


def checkUser (name,password):
    db=connectBD()
    cursor = db.cursor()
    query= "SELECT Nombre,Contraseña FROM Usuario WHERE Nombre=%s"
    valo=(name, )
    cursor.execute(query, valo)
    userData = cursor.fetchone()
    if userData is None:
        return False
    
    paswordhash = userData[1]
    if bcrypt.checkpw(password.encode('utf-8'), paswordhash.encode('utf-8')):
        return userData
    else:
        return False


def createLibro(NombreA,NombreE,NombreL,estilo):
    db=connectBD()
    cursor=db.cursor()
    query = "insert into Libro (NombreLibro,NombreyApellidosAutor,NombreEditorial,Estilo) VALUES(%s,%s,%s,%s);"
    valores=(NombreL,NombreA,NombreE,estilo)
    cursor.execute(query,valores)
    db.commit()
    db.close()
    return


def dropLibro(NombreL):
    db=connectBD()
    cursor=db.cursor()
    query = "Delete FROM Libro where NombreLibro =  %s;"
    valor= NombreL
    cursor.execute(query, (valor,))
    db.commit()
    db.close()
    return


def showdb():
    db=connectBD()
    cursor=db.cursor()
    cursor.execute('select * from libro')
    resultados = cursor.fetchall()
    db.commit()
    db.close()
    return resultados


def buscar_libro(nombre_libro):
    print(nombre_libro)
    url = f'https://www.googleapis.com/books/v1/volumes?q={nombre_libro}'
    print(url)
    response = requests.get(url)
    data = response.json()
    bookfinal = []
    count = 0
    if 'items' in data:
        for item in data['items']:
            if count == 10:
                break

            titulo = item['volumeInfo']['title']
            autores = item['volumeInfo'].get('authors', 'Autor desconocido')
            editorial = item['volumeInfo'].get('publisher', '')
            categoria = item['volumeInfo'].get('categories', '')

            if isinstance(autores, list):
                autores = ', '.join(autores)
            if isinstance(categoria, list):
                categoria = ', '.join(categoria)

            bookfinal.append([titulo, autores, editorial, categoria])
            count += 1
            print(bookfinal)
        return bookfinal
    print(bookfinal)


# Secuencia principal del programa
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signin")
def signin():
    return render_template("signin.html")


@app.route("/resultshash",methods=('GET', 'POST'))
def resultshash():
    if request.method == ('POST'):
        formData = request.form
        name=formData['Nombre']
        password=formData['Contrasena']
        userData = checkUser(name,password)
        if userData == False:
            return render_template("login.html",login=False)
        else:
            return render_template("funcionalidad.html",login=True,userData=userData)


@app.route("/newuser",methods=('GET', 'POST'))
def newuser():
    if request.method == ('POST'):
        formData = request.form
        name=formData['Nombre']
        apellidos=formData["Apellidos"]
        correo=formData["Correo"]
        password=formData['Contrasena']
        password= password.encode()
        sal=bcrypt.gensalt()
        passwordhash=bcrypt.hashpw(password,sal) 
        
        nuevouser = createUser(name,apellidos,correo,passwordhash)
        if nuevouser == False:
            return render_template("newuser.html",login=False)
        else:
            return render_template("login.html",login=True)
        

@app.route("/funcionalidad1",methods=('GET', 'POST'))
def funcionalidad1():
    if request.method == ('POST'):
        formData = request.form
        NombreA=formData['NombreA']
        NombreE=formData["Editorial"]
        NombreL=formData["NombreL"]
        estilo=formData['EstiloL']
        
        nuevolibro = createLibro(NombreA,NombreE,NombreL,estilo)
        
        if nuevolibro == False:
            return render_template("funcionalidad.html",login=False)
        else:
            return render_template("funcionalidad.html",login=True)
        
@app.route("/funcionalidad2",methods=('GET', 'POST'))
def funcionalidad2():
    if request.method == ('POST'):
        formData = request.form
        NombreL=formData["NombreL"]
        deletelibro = dropLibro(NombreL)
        
        if deletelibro == False:
            return render_template("funcionalidad2.html",login=False)
        else:
            return render_template("funcionalidad2.html",login=True)
  
        
@app.route("/principal",methods=('GET', 'POST'))
def principal():
    return render_template("principal.html")

@app.route("/funcionalidad",methods=('GET', 'POST'))
def funcionalidad():
    return render_template("funcionalidad.html")

@app.route("/funcionalidadborrar",methods=('GET', 'POST'))
def funcionalidadborrar():
    return render_template("funcionalidad2.html")

@app.route("/funcionalidaddb",methods=('GET', 'POST'))
def funcionalidaddb():
    resultados = showdb()
    return render_template("funcionalidad3.html",resultadosHtml=resultados)


@app.route("/funcionalidadbuscar",methods=('GET', 'POST'))
def funcionalidadbuscar():
    if request.method == ('POST'):
        formData = request.form
        nombre_libro=formData["nombre_libro"]
        resultados= buscar_libro(nombre_libro)
        return render_template("funcionalidad4.html",resultHtml1=resultados)
    elif request.method == ('GET'):
        return render_template("funcionalidad4.html",resultHtml1=[])


app.config['TEMPLATES_AUTO_RELOAD']=True
app.run(host='localhost',port=5000, debug=True)
