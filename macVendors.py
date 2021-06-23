from scapy.all import *
import sqlite3
import sys

def showBanner():
    print("                      ::::    ::::      :::      ::::::::                      ")
    print("                      +:+:+: :+:+:+   :+: :+:   :+:    :+:                     ")
    print("                      +:+ +:+:+ +:+  +:+   +:+  +:+                            ")
    print("                      +#+  +:+  +#+ +#++:++#++: +#+                            ")
    print("                      +#+       +#+ +#+     +#+ +#+                            ")
    print("                      #+#       #+# #+#     #+# #+#    #+#                     ")
    print("                      ###       ### ###     ###  ########                      ")
    print(":::     ::: :::::::::: ::::    ::: :::::::::   ::::::::  :::::::::   ::::::::  ")
    print(":+:     :+: :+:        :+:+:   :+: :+:    :+: :+:    :+: :+:    :+: :+:    :+: ")
    print("+:+     +:+ +:+        :+:+:+  +:+ +:+    +:+ +:+    +:+ +:+    +:+ +:+        ")
    print("+#+     +:+ +#++:++#   +#+ +:+ +#+ +#+    +:+ +#+    +:+ +#++:++#:  +#++:++#++ ")
    print(" +#+   +#+  +#+        +#+  +#+#+# +#+    +#+ +#+    +#+ +#+    +#+        +#+ ")
    print("  #+#+#+#   #+#        #+#   #+#+# #+#    #+# #+#    #+# #+#    #+# #+#    #+# ")
    print("    ###     ########## ###    #### #########   ########  ###    ###  ########  ")
    print("")

def showHelp():
    showBanner()
    print("Uso:")
    print("    macVendors.py -h - Mostra este menu")
    print("    macVendors.py xxx.xxx.xxx.xxx/xx - Scan MAC")
    print("     Importante: o argumento deve ser fornecido na notação CIDR!")
    print("")

def scanNet(ip):
    # Cria um frame para ser enviado para o endereço
    # broadcast de camada 2
    arpRequest = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arpRequestBroadcast = broadcast/arpRequest
    
    #Envia o Frame
    response = srp(arpRequestBroadcast, timeout=1, verbose=False)[0]
    
    # Organiza os resultados em uma lista de dicionários
    # para facilitar o acesso
    returnList = []
    for element in response:
        client = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        returnList.append(client)
    
    return returnList

def searchMac(mac):
    try:
        #Conecta na database
        con = sqlite3.connect('macV.db')
        cur = con.cursor()
        macShort=mac[0:8] #Primeiros digitos do MAC Address
        macResponse=cur.execute("SELECT * FROM macVendor WHERE oui LIKE ? ", (macShort,))
        macResponse=macResponse.fetchall()
        cur.close()
        # macResponse é uma tupla, então é retornado 
        # apenas o primeiro elemento
        return macResponse[0]
    except:
        # Em caso do MAC Address não estar listado na database
        # é retornada a label "Não identificado"
        other='Não identificado'
        macResponse=[macShort,other]
        return macResponse

delim = '-' *80

if ( sys.argv.count == 0 or network == '-h'):
    showHelp()
else:
    network=sys.argv[1]
    showBanner()
    print(delim)
    print('{:^17s}{:^48s}{:^15s}'.format("MAC", "Vendor", "IP"))
    print(delim)
    macAdd=scanNet(network)
    for mac in macAdd:
        temp = searchMac(mac['mac'])
        print('{:^17s}{:^48s}{:^15s}'.format(mac['mac'], temp[1], mac['ip']))
    print(delim)
