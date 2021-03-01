# -*- coding: utf-8 -*-
"""
@author: Erika
"""
import imaplib
import email
import sqlite3
from email.header import decode_header


Email = input ("Introducir Email: ")
Password = input("Introducir Contraseña: ")


print("Iniciando aplicación....")
#****************Conexión MySQL*********************
conn = sqlite3.connect("KeywordBD.db")
c = conn.cursor()

#**************** Servidor IMAP*****************
ServidorImap= imaplib.IMAP4_SSL("imap.gmail.com",993)
ServidorImap.login(Email, Password)

#Seleccionar el Buzon "Inbox"
status, messages = ServidorImap.select("INBOX", readonly=False) 

#Buscar los mails no leidos (UNSEEN)
type, MessIds = ServidorImap.search(None, "UNSEEN")

#Crear lista con mails encontrados, separar registros y contarlos
MessIdsString = str(MessIds[0],encoding="utf8")
listSplitString = MessIdsString.split()
EmailNuevos=len(listSplitString)
#Validar si hay mails nuevos para avanzar ejecución, si no, finaliza
if  EmailNuevos == 0:
    print("No se encontraron emails nuevos")
else:
    print("Se encontraron",EmailNuevos,"emails nuevos")
    try:
    
        #Crear tabla "mails" con campos Id (), Fecha, De y Asunto
        c.execute("""CREATE TABLE mails
                  (Id integer primary key autoincrement,
                   Fecha text,
                   De text, 
                   Asunto text)""")
        print("¡Se creó la tabla mails!")
    
    #Carpturar y procesar exepción para mostrar mensaje en caso de que la tabla ya exista
    except sqlite3.OperationalError:
        print("¡La tabla mails ya existe!")
        
    #Mostrar cantidad de mails nuevos, en caso de haberlos
    messages = int(messages[0])
      
    #**************Leer mails nuevos*****************
    for i in range (messages, messages-(EmailNuevos),-1):
        res, msg = ServidorImap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                
                #Obtener Asunto-----------------------------------------
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                    
                #Obtener Fecha------------------------------------------
                date, encoding = decode_header(msg["Date"])[0]
                if isinstance(date, bytes):
                    date = date.decode(encoding)
                    
                #Obtener De---------------------------------------------
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type() 
                        try:
                            #Obtener cuerpo del mail y buscar palabra "DevOps"
                            body = part.get_payload(decode=True).decode()
                            ListaPalabras=body.split()
                            for palabra in ListaPalabras:
                                if palabra == "DevOps": 
                                    
                                    #Guardar registro en tabla "mails" en caso de encontrar la palabra "DevOps"
                                    c.execute("INSERT INTO mails (Fecha,De,Asunto) values (?,?,?)",(date,From,subject))
                                    conn.commit()          
                                else:
                                    pass
                        except:
                            pass
    #Imprimir los datos guardados en la tabla mails
    print(" ")
    print("------------------Contenido de Tabla mails-------------------")
    c.execute("Select Id,Fecha,De,Asunto from mails")
    for fila in c:
        print(fila)
#Cerrar conexiones (BD, servidor IMAP)
conn.close() 
ServidorImap.close()
ServidorImap.logout()
    
              

