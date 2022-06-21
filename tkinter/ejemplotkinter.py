from tkinter import *
from tkinter import messagebox
import sqlite3 as sq3 #importa la base de datos


raiz = Tk() #Objeto de la clase de la ventana ppal
raiz.title('Datos - Codo a Codo 2022') #pone tiotulo a la ventana ppal

'''
=============================
       PARTE FUNCIONAL
=============================
'''
# MENU

# MENUBBDD
def conectar():
    global con #global para llamarlo desde cualquier parte del programa
    global cur
    con = sq3.connect('mi_bbdd.db') #esto es para conectarlo con la bbdd
    cur = con.cursor()
    messagebox.showinfo("STATUS","¡Conectado a la BBDD!")
    
def salir():
    resp = messagebox.askquestion("CONFIRME","¿Desea salir del programa?")
    if resp == "yes":
        con.close()
        raiz.destroy()
    
# MENU LIMPIAR
def limpiar():
    legajo.set('')
    alumno.set('')
    email.set('')
    calificacion.set('')
    grado.set('')
    escuela.set('Seleccione') #se le pone seleccione porqeu va a ser un menu desplegable
    localidad.set('')
    provincia.set('')
    legajo_input.config(state='normal')


# MENU ACERCA DE...
#   LICENCIA
def licencia():
    # CREATIVE COMMONS GNU GPL https://www.gnu.org/licenses/gpl-3.0.txt
    gnuglp = '''
    Demo de un sistema CRUD en Python para gestión 
    de alumnos
    Copyright (C) 2022 - Morena Caparrós
    Email: morens217@gmail.com\n=======================================
    This program is free software: you can redistribute it 
    and/or modify it under the terms of the GNU General Public 
    License as published by the Free Software Foundation, 
    either version 3 of the License, or (at your option) any 
    later version.
    This program is distributed in the hope that it will be 
    useful, but WITHOUT ANY WARRANTY; without even the 
    implied warranty of MERCHANTABILITY or FITNESS FOR A 
    PARTICULAR PURPOSE.  See the GNU General Public License 
    for more details.
    You should have received a copy of the GNU General Public 
    License along with this program.  
    If not, see <https://www.gnu.org/licenses/>.'''
    messagebox.showinfo("LICENCIA",gnuglp)

#   ACERCA DE...
def acerca():
    messagebox.showinfo('ACERCA DE...','Creado por Morena Caparrós\npara Codo a Codo 4.0 - Big Data\nMayo, 2022\nEmail: morens217@gmail.com')

# FUNCIONES VARIAS
#le mando un parametro que si es true va a ser porque va a actualizar la base de datos
#sino es porque solo em interesan los nombres de las escuelas (cuando esta en false)
def buscar_escuela(actualiza): 
    con = sq3.connect('mi_bbdd.db')
    cur = con.cursor()
    if actualiza:
         cur.execute('SELECT _id, localidad, provincia FROM escuelas WHERE nombre = ?',(escuela.get(),))
         #se manda (escuela.get(),) con esta forma, es decir con la coma porque en resultados trae con , sino te tira error
         
    else:
        cur.execute('SELECT nombre FROM escuelas') #le digo que me seleccione de las escuelas los nombres  
        escuela.set("Seleccione")

    resultado = cur.fetchall() # RECIBO LISTA DE TUPLAS con un elemento "fantasma" 
    retorno = []
    for e in resultado: #cuando yo elijo una escuela, que me llenel los datos prov y localidad con los datos qwue corresponden a esa e, esa escuela
        if actualiza:
            provincia.set(e[2])#2 porque esta en la posicion 2 '_id, localidad, provincia(2)' (ver linea 118)
            localidad.set(e[1])# 1 por la posicion
        esc = e[0]
        retorno.append(esc)
    
    #print(resultado) #aca manda esto: [('Normal 1',), ('Gral. San Martín',), ('Belgrano',), ('EET Nro 2',), ('Esc. N° 2 Tomás Santa coloma',)][('Normal 1',), ('Gral. San Martín',), ('Belgrano',), ('EET Nro 2',), ('Esc. N° 2 Tomás Santa coloma',)]
    #sale una coma despues de  lo qeu esta entre '' entonces nada puede tirar error
    con.close()
    return retorno

def listar():
    class Table():
        def __init__(self,raiz2):
            nombre_cols = ['Legajo', 'Alumno', 'Calificación', 'Email', 
            'Escuela', 'Localidad', 'Provincia']
            for i in range(cant_cols):
                self.e = Entry(frameppal)
                self.e.config(bg='goldenrod', fg='lemon chiffon')
                self.e.grid(row=0, column=i)
                self.e.insert(END,nombre_cols[i])

            for fila in range(cant_filas):
                for col in range(cant_cols):
                    self.e = Entry(frameppal)
                    self.e.grid(row=fila+1, column=col)
                    self.e.insert(END, resultado[fila][col])
                    self.e.config(state='readonly')
    raiz2 = Tk()
    raiz2.title('Listado alumnos')
    frameppal = Frame(raiz2)    
    frameppal.pack(fill='both')
    framecerrar = Frame(raiz2)
    framecerrar.config(bg=color_texto_boton)
    framecerrar.pack(fill='both')

    boton_cerrar = Button(framecerrar,text="CERRAR", command=raiz2.destroy)
    boton_cerrar.config(bg=color_fondo_boton, fg=color_texto_boton, pady=10, padx=0)
    boton_cerrar.pack(fill='both')

    # obtengo los datos -> Messirve el query1 del ejemplo de sqlite
    con = sq3.connect('mi_bbdd.db')
    cur = con.cursor()
    query1 = '''SELECT alumnos.legajo, alumnos.nombre, alumnos.nota, alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id'''
    cur.execute(query1)
    resultado = cur.fetchall()
    cant_filas = len(resultado) # la cantidad de registros para saber cuántas filas
    cant_cols = len(resultado[0]) # obtengo la cantidad de columnas
    
    tabla = Table(frameppal)
    con.close()
    raiz2.mainloop()

# FUNCIONES CRUD (Create - read - Update - Delete)
# CREATE
def crear():
    id_escuela = int(buscar_escuela(True)[0])
    datos = id_escuela, legajo.get(), alumno.get(), calificacion.get(), email.get()
    cur.execute("INSERT INTO alumnos (id_escuela, legajo, nombre, nota, email) VALUES (?,?,?,?,?)", datos)
    con.commit() #cuano yo hago cambios tengo que poner esto sino no se actualiza, el values  es cuantos valores tengo y tiene 5 escuela, legajo, nombre nota email
    messagebox.showinfo("STATUS","Registro agregado!")
    limpiar()
# READ
def buscar():
    query_leer = '''SELECT alumnos.legajo, alumnos.nombre, alumnos.nota, alumnos.email, alumnos.grado,
    escuelas.nombre, escuelas.localidad, escuelas.provincia FROM alumnos 
    INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id WHERE alumnos.legajo ='''
    #LO QEU ESTOY HACIENDO ES UN SELECT de todas las escuelas y abajo lo qeu hago es que se me autocomplete otyros datos segun esa escuela que elegi
    #
    cur.execute(query_leer + legajo.get())
    resultado = cur.fetchall() #selecciono todos, los traigo a la memoria al a variable resultado
    if resultado == []:
        messagebox.showerror("ERROR","No existe ese N° de legajo") #si esta vacio tiro este error, y lo dejo vacio nuevamente
        legajo.set('')
    else:
        for campo in resultado: #sino lo qeu hago es recorrerlo y con set(lo qeu hago es)
            legajo.set(campo[0]) #decirle en que parte tengo que poner determinado resultado
            alumno.set(campo[1])
            calificacion.set(campo[2])
            email.set(campo[3])
            grado.set(campo[4])
            escuela.set(campo[5])
            localidad.set(campo[6])
            provincia.set(campo[7])
            legajo_input.config(state='disabled') #esto para que no se pueda volver a tocar el campo legajo
            
            
# Update
def actualizar():
    id_escuela = int(buscar_escuela(True)[0])
    datos = id_escuela, alumno.get(), calificacion.get(), email.get() #el legajo no se puede modificar al igual qeu la prov y localidad entonces lo que hago es no ponerlos
    cur.execute("UPDATE alumnos SET id_escuela =?, nombre=?, nota=?, email=? WHERE legajo =" + legajo.get(), datos)
    con.commit()
    messagebox.showinfo("STATUS", "Registro actualizado")
    limpiar()

# Delete
def borrar():
    resp = messagebox.askquestion("ELIMINAR","¿Desea eliminar el registro?")
    if resp == "yes":
        cur.execute("DELETE FROM alumnos WHERE legajo =" + legajo.get())
        con.commit()
        messagebox.showinfo("STATUS","Registro eliminado")
        limpiar()





'''
=============================
       INTERFAZ GRÁFICA
=============================
'''
#BARRAMENU
barramenu = Menu(raiz) # lo que hago es decirle donde va a estar mi menu que es en mi raiz
raiz.config(menu=barramenu) #indica a al ventana ppal que ubique al menu

bbddmenu = Menu(barramenu, tearoff=0) # crea submenu BBDD

#framebotones
fondo_framebotones = 'goldenrod'
color_fondo_boton = 'lemon chiffon'
color_texto_boton = fondo_framebotones
#framecampos
color_fondo = 'lemon chiffon' # frame & labels
color_letra = 'goldenrod' # labels

#Boton Conectar
bbddmenu.add_command(label='Conectar', command=conectar)
# Botón Listado de alumnos
bbddmenu.add_command(label = 'Listado de alumnos', command = listar)
#Boton Salir
bbddmenu.add_command(label='SALIR', command=salir)

limpiarmenu = Menu(barramenu, tearoff=0)
# creo el Boton Limpiar
limpiarmenu.add_command(label='Limpiar campos', command=limpiar)

ayudamenu = Menu(barramenu, tearoff=0)
ayudamenu.add_command(label='Licencia', command=licencia)
ayudamenu.add_command(label='Acerca de...', command=acerca)

barramenu.add_cascade(label='BBDD', menu=bbddmenu) # agrega el botón ppal del submenú BBDD y le asigna sus botones
barramenu.add_cascade(label='Limpiar',menu=limpiarmenu)
barramenu.add_cascade(label='Acerca de...',menu=ayudamenu)

# FRAMECAMPOS
fondo = 'lemon chiffon'
color_fuente = 'goldenrod'
framecampos = Frame(raiz) #Creación del Frame permite hacer los campos
framecampos.config(bg=fondo)
framecampos.pack(fill='both') #Empaquetamiento del Frame ajusta el contenido a la ventana 

# Variables de control para los Entry es lo qeu va a crear cada una de las 'categorias'
legajo = StringVar()
alumno = StringVar()
email = StringVar()
calificacion = DoubleVar()
grado = IntVar()
escuela = StringVar()
localidad = StringVar()
provincia = StringVar()

'''
entero = IntVar()  # Declara variable de tipo entera
flotante = DoubleVar()  # Declara variable de tipo flotante
cadena = StringVar()  # Declara variable de tipo cadena
booleano = BooleanVar()  # Declara variable de tipo booleana
'''
# Campos Entry
legajo_input = Entry(framecampos,textvariable=legajo) #siempre se maneja string entonces por mas que sea un boolean o lo que sea se pone textvariable
legajo_input.grid(row=0, column=2, padx=10, pady=10)

alumno_input = Entry(framecampos, textvariable=alumno)
alumno_input.grid(row=1, column=2, padx=10, pady=10)

email_input = Entry(framecampos, textvariable=email)
email_input.grid(row=2, column=2, padx=10, pady=10)

calificacion_input = Entry(framecampos,textvariable=calificacion)
calificacion_input.grid(row=3, column=2, padx=10, pady=10)

grado_input = Entry(framecampos,textvariable=grado)
grado_input.grid(row=4, column=2, padx=10, pady=10)

#para dibujar la interfaz con las listas desplegables necesito las escuelas
#va a tener dos modalidades para actualizar, en donde yo voy a elegir y por otro lado 
#cuando necesito buscar
escuelas = buscar_escuela(False)
escuela.set('Seleccione')
escuela_option = OptionMenu(framecampos, escuela, *escuelas)
escuela_option.grid(row=5, column=2, padx=10, pady=10)


localidad_input = Entry(framecampos, textvariable=localidad, state='readonly') #esto es para que yo nunca pueda tocarlo el state =readonly
localidad_input.grid(row=6, column=2, padx=10, pady=10)

provincia_input = Entry(framecampos, textvariable=provincia, state='readonly')
provincia_input.grid(row=7, column=2, padx=10, pady=10) #row es para indicar que numero de columna

# Labels: etiquetas
def config_labels(label, fila): #son las dos unicas cosas qeu se modifican entonces es lo qeu necesito en mi funcion
    espaciado_labels = {'column':1, 'padx':10, 'pady': 10, 'sticky': 'e'}
    color_labels ={'bg':fondo, 'fg':color_fuente}
    label.grid(row=fila,**espaciado_labels) #como esto es un diccionario para mandar los parametros uso **
    label.config(**color_labels) 
    
legajo_label = Label(framecampos, text='Legajo:')
config_labels(legajo_label, 0)
#legajo_label.grid(row=0, column=1, padx=10, pady=10, sticky='e')

alumno_label = Label(framecampos, text='Alumno:')
config_labels(alumno_label, 1)
#alumno_label.grid(row=1, column=1, padx=10, pady=10, sticky='e')

email_label = Label(framecampos, text='Email:')
config_labels(email_label, 2)
#email_label.grid(row=2, column=1, padx=10, pady=10, sticky='e')

calificacion_label = Label(framecampos, text='Calificación:')
config_labels(calificacion_label, 3)
#calificacion_label.grid(row=3, column=1, padx=10, pady=10, sticky='e')

grado_label = Label(framecampos,text='Grado')
config_labels(grado_label, 4) 
#grado_label.grid(row=4, column=1, padx=10, pady=10, sticky='e')

escuela_label = Label(framecampos, text='Escuela:')
config_labels(escuela_label, 5) 
#escuela_label.grid(row=5, column=1, padx=10, pady=10, sticky='e')

localidad_label = Label(framecampos, text='Localidad: ')
config_labels(localidad_label,5)
#localidad_label.grid(row=5, column=0, padx=10, pady=10, sticky='e')

provincia_label = Label(framecampos, text='Provincia: ')
config_labels(provincia_label,6)
#provincia_label.grid(row=7, column=1, padx=10, pady=10, sticky='e') #sticky es para justificarlo segun los numeros cardinales 

'''
"STICKY"
     n
  nw   ne
w         e
  sw   se
     s
'''
# FRAME BOTONERA -> Maneja las funciones CRUD (create, read, update, delete)
framebotones = Frame(raiz)
framebotones.pack(fill='both')

boton_crear = Button(framebotones, text='Crear', command=crear)
boton_crear.grid(row=0, column=1, padx=5, pady=10, ipadx=10)

boton_buscar = Button(framebotones, text='Buscar', command=buscar)
boton_buscar.grid(row=0, column=2, padx=5, pady=10, ipadx=10)

boton_actualizar = Button(framebotones, text='Actualizar', command=actualizar)
boton_actualizar.grid(row=0, column=3, padx=5, pady=10, ipadx=10)

boton_eliminar = Button(framebotones, text='Eliminar', command=borrar)
boton_eliminar.grid(row=0, column=4, padx=5, pady=10, ipadx=10)

# FRAME PIE
framecopy = Frame(raiz)
framecopy.pack(fill='both')
copylabel = Label(framecopy, text='(2022) por Morena Caparrós para CaC 4.0 - Big Data')
copylabel.grid(row=0, column=0, padx=10, pady=10)

buscar_escuela(False)
raiz.mainloop() #mantiene mi venta abierta hasta que alguien al cierra,  en algunos sistemas operativos no hace falta pero en este si