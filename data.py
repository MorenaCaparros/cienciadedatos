from asyncio.windows_events import NULL #Esto es porque quiero una cosa de windows events q  es NULL y lo necesito porqeu lo tengo en una de las listas
import sqlite3 as sq3 #importa la libreria que maneja la BBDD

#sqlitebrowser.org

con = sq3.connect('mi_bbdd.db')
cur = con.cursor() #EL CURSOR ES permite manejar la base de datos, ejecutar comandos (por ejemplo el metodo que esta mas abajo qeu es "execute")

instruct1 = '''CREATE TABLE IF NOT EXISTS escuelas (
  _id INTEGER PRIMARY KEY AUTOINCREMENT,  
  nombre varchar(45) DEFAULT NULL,
  localidad varchar(45) DEFAULT NULL,
  provincia varchar(45) DEFAULT NULL,
  capacidad INTEGER DEFAULT NULL)'''

instruct2 = '''CREATE TABLE  IF NOT EXISTS alumnos (
  _id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_escuela INTEGER DEFAULT NULL,
  legajo INTEGER DEFAULT NULL,
  nombre varchar(45) DEFAULT NULL,
  nota decimal(10,0) DEFAULT NULL,
  grado INTEGER DEFAULT NULL,
  email varchar(45) NOT NULL,
  FOREIGN KEY (id_escuela) REFERENCES escuelas(id))'''

cur.execute(instruct1)
cur.execute(instruct2)

lista1 = [(1,'Normal 1','Quilmes','Buenos Aires',250),(2,'Gral. San Martín','San Salvador','Jujuy',100),(3,'Belgrano','Belgrano','Córdoba',150),(4,'EET Nro 2','Avellaneda','Buenos Aires',500),(5,'Esc. N° 2 Tomás Santa coloma','Capital Federal','Buenos Aires',250)]

lista2 = [(1,2,1000,'Ramón Mesa',8,1,'rmesa@mail.com'),(2,2,1002,'Tomás Smith',8,1,''),(4,1,101,'Juan Perez',10,3,''),(5,1,105,'Pedro González',9,3,''),(6,5,190,'Roberto Luis Sánchez',8,3,'robertoluissanchez@gmail.com'),(7,2,106,'Martín Bossio',NULL,3,''),(8,4,100,'Paula Remmi',3,1,'mail@mail.com'),(9,4,1234,'Pedro Gómez',6,2,'')]

#cur.executemany('INSERT INTO escuelas VALUES (?,?,?,?,?)', lista1) #va a recibir la instruccion sql otro arguimento que es la lista de datos que yo necesito cargar
#notacion parametrica dependiendo los datos cantidad que tenmga son los ? que le pongo
#cur.executemany('INSERT INTO alumnos VALUES (?,?,?,?,?,?,?)', lista2) #esto es para que conecxte instruct 2 con list2

query1 = '''SELECT alumnos.legajo, alumnos.nombre, alumnos.nota, alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id'''

for registro in cur.execute(query1): #aca registro es el elemento dentro de mi query
    print(registro)

con.commit() #sirve para cerrar las trasnacciones qeu en las bbdd son, empezar a hacer operaciones, y si todas son correctas, el comit confirma todos, y si hay un solo error deshace los cambios y no confirma nada, 
#es como un rollback
con.close() #cierra la conexion con la bbdd

