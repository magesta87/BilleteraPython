# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 09:41:26 2021

@author: Mariano Agesta
"""
import requests
from datetime import datetime
import string
import random




url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
    'start': '1',
    'limit': '5000',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'b0eed337-d8cd-44e2-82e6-5df76ae8d1ff',
}

### VARIABLES GLOBALES ###

#historical = open("historical.txt", "w+") #Creo el archivo borrando el contenido antiguo
monedas_dic = {} #se almacenan monedas obtenidas en binance
saldo_individual = {} #almaceno el saldo de cada moneda
menu = True

### FUNCION OBTENER PRECIO ###

def fetching_data(endpoint):
    response = requests.get(
        f"https://api.binance.com/api/v3/ticker/price?symbol={endpoint}USDT")
    results = response.json()
    price = results["price"]
    return price

### GENERADOR DE DIRECCIONES ###
def generar_addres(size = 20, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


### INSERTAR HISTORIAL ###
def guardar_historial_recibir(cripto, cantidad, addres):
    historical = open("historical.txt", "a")
    now = datetime.now()
    format = now.strftime("%d/%m/%Y Hora: %H:%M:%S")
    historical.writelines(f"{format} - Recibiste {cantidad}{cripto} de addres: {addres}\n")
    historical.close()
    
def guardar_historial_transferir(cripto, cantidad, addres):
    historical = open("historical.txt", "a")
    now = datetime.now()
    format = now.strftime("%d/%m/%Y Hora: %H:%M:%S")
    historical.writelines(f"{format} - Transferiste {cantidad}{cripto} a addres: {addres}\n")
    historical.close()
    
### MOSTRAT HISTORIAL ###

def mostrar_historial():
    historical = open("historical.txt", "r+")
    lineas = historical.read()
    print("--------HISTORIAL---------")
    print(lineas, "\n")
    historical.close()


### PETICION API BINANCE ###
data = requests.get(url, headers=headers, params=parameters).json()

### ALMACENO NOMBRES DE CRIPTO EN DICCIONARIO ###
i = 0
for id in data["data"]:
    monedas_dic[i] = id["symbol"]
    i +=1

### SUMO VALORES REPETIDOS A DICCIONARIO SALDOS ###

def suma_valores_dic(cripto, cantidad, saldo_individual):
       suma = 0
       for key in saldo_individual.keys():
           if cripto == key:
               for v in saldo_individual.values():
                   suma = float(v) + float(cantidad)
           return suma
        
       
### FUNCION SUMAR SALDOS ###
def suma_saldos(cripto, cantidad):
    if cripto in saldo_individual.keys():
        saldo_individual[cripto] = suma_valores_dic(cripto, cantidad, saldo_individual)            
    else: 
        saldo_individual[cripto] = cantidad
              
                                                                                       
###  FUNCION MOSTRAS SALDO INDIVIDUAL  ###
def mostrar_saldo():
    print("---------Saldos----------")
    for key in saldo_individual:
        print(f"{key} | cantidad: {saldo_individual[key]} | saldo: USD {float(saldo_individual[key]) * float(fetching_data(key))}")
             

###  FUNCION MOSTRAR BALANCE TOTAL  ####
def mostrar_balance_total():
    total = 0
    print("---------Balance total----------")
    for key in saldo_individual:
        total += float(saldo_individual[key]) * float(fetching_data(key))
        
    print(f"Usted posee un saldo total de: USD {total}")
    

###  VALIDAR MONEDA PARA RECIBIR ###
def validar_moneda(cripto):
        
    return cripto in monedas_dic.values()                                                     

### FUNCION RECIBIR ###
def recibir_cripto(cripto):
        cantidad = input(f"Ingresa la cantidad de {cripto} a recibir: ")
        addres = generar_addres()
        guardar_historial_recibir(cripto, cantidad, addres)
        suma_saldos(cripto, cantidad)
        print("La operacion se realizo exitosamente.")
        
      
## FUNCION TRANSFERIR ### 

def transferir_cripto(cripto): 
    resultado = 0
    if cripto not in saldo_individual.keys():
        print(f"No posees saldo de {cripto}")
    else:
        cantidad = float(input("Ingresa la cantidad a transferir: "))
        if cantidad > float(saldo_individual[cripto]):
            print("No posees esa cantidad, posees {saldo_individual[cripto]}.")
        else:
            resultado = float(saldo_individual[cripto]) - float(cantidad)
            saldo_individual[cripto] = resultado
            addres = generar_addres()
            guardar_historial_transferir(cripto, cantidad, addres)
            print("La operacion se realizo exitosamente.")
                         

### MENU DE OPCIONES ###
def opcionesMenu():
    print("-------------------------------")
    print("------------WALLET-------------")
    print(".MENU.")
    print("0. Salir")
    print("1. Recibir")
    print("2. Transferir")
    print("3. Monstrar balance")
    print("4. Mostrar balance general")
    print("5. Mostrar historial")
  
    
### LOGICA MENU ###

def Menu():
    historical = open("historical.txt", "w+")
    
    while menu:
        opcionesMenu()
        try:
            entrada_usuario = int(input("Seleccione una opcion: "))

            if entrada_usuario in range(6):

                if entrada_usuario == 0:
                    historical.close()
                    print("Gracias por utilizar nuestro servicio")
                    break
                   
                elif entrada_usuario == 1:
                    cripto = input("Ingresa la moneda que quieres recibir: ")
                    while True:
                        if validar_moneda(cripto):
                            recibir_cripto(cripto)
                            break
                        else: 
                            cripto = input("moneda invalida, intentelo nuevamente: ")
                        
                                                                                
                elif entrada_usuario == 2: 
                    cripto = input("Que criptomoneda desea transferir: ")
                    while True:
                        if validar_moneda(cripto):
                            transferir_cripto(cripto)
                            break
                        else: 
                            cripto = input("moneda invalida, intentelo nuevamente: ")
                      
                    
                elif entrada_usuario == 3:
                    mostrar_saldo()
                    
                elif entrada_usuario == 4:
                    mostrar_balance_total()
                  
                elif entrada_usuario == 5:
                    
                    mostrar_historial()
                    
                    
                
            else:
                print('Error, no escogio una opcion valida.')

        except ValueError:
            print("Error, ingrese solamente numeros")

        
Menu()        
        