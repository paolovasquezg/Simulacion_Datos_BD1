import psycopg2
import random

#pgAdmin:
 # database: Maintenance database
 # user: Username
 # password: password
 # host: Host name/addres
 # options: -c search_path=[squema in use]
conn = psycopg2.connect(database="postgres", user="postgres", password="1234", host="localhost", port="5432", options="-c search_path=prueba100k")

cursor = conn.cursor()

conn.autocommit = True

#Gist de github con la creacion de tablas y consultas sql: https://gist.github.com/paolovasquezg/a7330d266671230063c5c3b16d9d15c6


def generar_usuario():
    with open("Usuario.txt") as archivo:
        for linea in archivo:
            cursor.execute(f"INSERT INTO Usuario(nombre) VALUES ('{linea}');")
    

def generar_Formato():
    opciones_formato = ["OU", "UU", "PU", "RU", "NU", "12VGC2022"]
    for e in opciones_formato:
        cursor.execute(f"INSERT INTO Formato(nombre) VALUES ('{e}')")

def generar_PokemonBase():
    cursor.execute("SELECT nombre FROM Formato;")
    res1 = cursor.fetchall()
    with open("pokemones.txt") as archivo:
        for line in archivo:
            formato = random.choice(res1)[0]
            cursor.execute(f"INSERT INTO PokemonBase(nombre, nombre_formato) VALUES ('{line}', '{formato}');")

def generar_Equipo(n):
    cursor.execute("SELECT nombre FROM Usuario;")
    res1 = cursor.fetchall()
    cursor.execute("SELECT nombre FROM Formato;")
    res2 = cursor.fetchall()
    i = n//6
    with open("Equipos.txt") as archivo:
        for linea in archivo:
            nombre = random.choice(res1)[0]
            print(nombre)
            nombre_formato = random.choice(res2)[0]
            cursor.execute(f"INSERT INTO Equipo(nombre, nombre_usuario , nombre_formato) VALUES ('{linea}', '{nombre}', '{nombre_formato}');")
            i -= 1
            if i == 0: 
                break


def generar_Habilidad():
    with open("habilidades.txt") as archivo:
        for nombre in archivo:
            cursor.execute(f"INSERT INTO Habilidad(nombre) VALUES ('{nombre}');")

def generar_Movimiento():
    with open("movimientos.txt") as archivo:
        for nombre in archivo:
            cursor.execute(f"INSERT INTO Movimiento(nombre) VALUES ('{nombre}');")

def generar_Objeto():
    with open("objetos.txt") as archivo:
        for nombre in archivo:
            cursor.execute(f"INSERT INTO Objeto(nombre) VALUES ('{nombre}');")

def generar_Naturaleza():
    with open("Naturalezas.txt") as archivo:
        for nombre in archivo:
            cursor.execute(f"INSERT INTO Naturaleza(nombre) VALUES ('{nombre}')")

def generar_PokemonCreado():
    lvl = 50
    cursor.execute("SELECT id FROM Equipo;")
    res = cursor.fetchall() 
    n = len(res)
    lista_naturalezas = []
    with open("Naturalezas.txt") as archivo:
        for line in archivo:
            lista_naturalezas.append(line)
    cursor.execute("SELECT nombre FROM Habilidad;")
    res2 = cursor.fetchall()
    i = 0
    while i < n:
        idpkm = []   
        j = 0    
        while j < 6:
            num = random.randint(1,906)
            while num not in idpkm:
                idpkm.append(num)
                j+=1
        equipo = res[i][0]
        print(equipo)
        cursor.execute(f"SELECT nombre_usuario FROM Equipo WHERE id={equipo};")
        usuario = cursor.fetchone()
        habilidad = []
        naturaleza = []
        for a in range(6):
            habilidad.append(random.choice(res2)[0])
            naturaleza.append(lista_naturalezas[random.randint(0, 24)])
        print(idpkm[0])
        
        cursor.execute(f"INSERT INTO PokemonCreado(nivel, id_pkmn, id_eq, nombre_usuario, nombre_habilidad, nombre_nat) VALUES ({lvl}, {idpkm[0]}, {equipo}, '{usuario[0]}', '{habilidad[0]}', '{naturaleza[0]}');")
        cursor.execute(f"INSERT INTO PokemonCreado(nivel, id_pkmn, id_eq, nombre_usuario, nombre_habilidad, nombre_nat) VALUES ({lvl}, {idpkm[1]}, {equipo}, '{usuario[0]}', '{habilidad[1]}', '{naturaleza[1]}');")
        cursor.execute(f"INSERT INTO PokemonCreado(nivel, id_pkmn, id_eq, nombre_usuario, nombre_habilidad, nombre_nat) VALUES ({lvl}, {idpkm[2]}, {equipo}, '{usuario[0]}', '{habilidad[2]}', '{naturaleza[2]}');")
        cursor.execute(f"INSERT INTO PokemonCreado(nivel, id_pkmn, id_eq, nombre_usuario, nombre_habilidad, nombre_nat) VALUES ({lvl}, {idpkm[3]}, {equipo}, '{usuario[0]}', '{habilidad[3]}', '{naturaleza[3]}');")
        cursor.execute(f"INSERT INTO PokemonCreado(nivel, id_pkmn, id_eq, nombre_usuario, nombre_habilidad, nombre_nat) VALUES ({lvl}, {idpkm[4]}, {equipo}, '{usuario[0]}', '{habilidad[4]}', '{naturaleza[4]}');")
        cursor.execute(f"INSERT INTO PokemonCreado(nivel, id_pkmn, id_eq, nombre_usuario, nombre_habilidad, nombre_nat) VALUES ({lvl}, {idpkm[5]}, {equipo}, '{usuario[0]}', '{habilidad[5]}', '{naturaleza[5]}');")

        i+=1

def generar_Carga():
    cursor.execute("SELECT idc FROM PokemonCreado;")
    res = cursor.fetchall()
    n = len(res) 
    lista_objetos = []
    with open("objetos.txt") as archivo:
        for linea in archivo:
            lista_objetos.append(linea)
    for i in range(n):
        objeto = lista_objetos[random.randint(0, 782)] #785
        idpkm = res[i][0]
        cursor.execute(f"SELECT id_pkmn, id_eq, nombre_usuario FROM PokemonCreado WHERE idc={idpkm}")
        datos = cursor.fetchone()
        cursor.execute(f"INSERT INTO Carga(idc_pkmn, id_pkbase, id_eq, nombre_usuario, nombre_objeto) VALUES ({idpkm}, {datos[0]}, {datos[1]}, '{datos[2]}', '{objeto}');")
            

def generar_Aprendido():
    cursor.execute("SELECT idc FROM PokemonCreado;")
    res = cursor.fetchall()
    cursor.execute("SELECT nombre FROM Movimiento;")
    res1 = cursor.fetchall()
    i = 0
    n = len(res)
    while i < n:
        idpkm = res[i][0]
        e = 0
        arr = []
        while e < 4:
            movimiento = random.choice(res1)[0]
            if movimiento not in arr:
                arr.append(movimiento)
                e+=1
        cursor.execute(f"SELECT id_pkmn, id_eq, nombre_usuario FROM PokemonCreado WHERE idc={idpkm}")
        datos = cursor.fetchone()
        cursor.execute(f"INSERT INTO Aprendido(idc_pkmn, id_pkbase, id_equipo, nombre_usuario, nombre_mov) VALUES ({idpkm}, {datos[0]}, {datos[1]}, '{datos[2]}', '{arr[0]}');")
        cursor.execute(f"INSERT INTO Aprendido(idc_pkmn, id_pkbase, id_equipo, nombre_usuario, nombre_mov) VALUES ({idpkm}, {datos[0]}, {datos[1]}, '{datos[2]}', '{arr[1]}');")
        cursor.execute(f"INSERT INTO Aprendido(idc_pkmn, id_pkbase, id_equipo, nombre_usuario, nombre_mov) VALUES ({idpkm}, {datos[0]}, {datos[1]}, '{datos[2]}', '{arr[2]}');")
        cursor.execute(f"INSERT INTO Aprendido(idc_pkmn, id_pkbase, id_equipo, nombre_usuario, nombre_mov) VALUES ({idpkm}, {datos[0]}, {datos[1]}, '{datos[2]}', '{arr[3]}');")
        i += 1
        
generar_usuario()
generar_Formato()
generar_PokemonBase()
generar_Equipo(n=100000) #cambiar el n por la cantidad de pokemones que se desean crear y ejecutar el programa
generar_Habilidad()
generar_Movimiento()
generar_Objeto()
generar_Naturaleza()
generar_PokemonCreado()
generar_Carga()
generar_Aprendido()