import socket
from datetime import datetime
import os.path

# Spuštění serveru
if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 4444
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    data = []
    print("------------------------------------------------------------------------")
    print(f"Server je spuštěn: {ip}:{port}")

    while True:
        j = 0

        # Připojení klineta
        client, adress = server.accept()
        print(f"Spojení s klientem navázáno: {adress[0]}:{adress[1]}")
        print("-------------------------------------------------------------------")
        # Přijetí zprávy od klienta
        while True:
            data.clear()
            patientID = 0
            dataType = 0

            ClientMessage = client.recv(1024)
            ClientMessage = ClientMessage.decode("utf-8")
            # print("Požadavek klienta:\n"+ClientMessage)
            # Rozparsování zprávy na řádky
            lines = ClientMessage.split("\n")
            # print(lines)
            for line in lines:
                # print(line)
                # rozpársování oddělovači
                splitLine = line.split('|')
                # print(splitLine[0])
                if splitLine[0] == "MSH":

                    now = datetime.now()
                    nowDateTime = now.strftime("%Y%m%d%H%M%S")
                    string = f"MSH|^~\&|SERVER_4444|SERVER_4444|CLIENT_4444|CLIENT_4444|{nowDateTime}||ORU^R01^ORU_R01|20110616000005|P|2.4|||NE|AL|CZE|ASCII||ASCII\n"


                    # client.send(bytes(string, "utf-8"))
                elif splitLine[0] == "PID":
                    patientID = splitLine[3]

                    path = f'./patientFiles/{patientID}.txt'
                    # Kontrola, zda soubor s daty pacienta existuje
                    check_file = os.path.isfile(path)

                    if check_file:
                        #print("Pacient:" + patientID)
                        string += f"PID|||2011021||^^^^^^L^A|||O\n" \
                                  f"PV1||I|^^OR-1^10.2.56.5:1\n" \
                                  f"ORC|RE\n"
                        client.send(bytes(string, "utf-8"))

                    else:
                        print(f"Pacient ID:{patientID} Neexistuje")
                        client.send(bytes(f"Nemáme záznamy o pacientovi s tímto ID : {patientID}", "utf-8"))
                        client.send(bytes(f"MSA|AA|{nowDateTime}", "utf-8"))

                elif splitLine[0] == "OBR":
                    dataType = splitLine[4]
                    dataType = dataType.split("^")
                    dataTime = splitLine[7]
                    endDataTime = splitLine[8]
                    if splitLine[8] != "":
                        endDataTime == splitLine[8]
                    else:
                        endDataTime = dataTime

                    #print(f" Data: {dataType}")
                    #print("Časový rozsah dat:" + dataTime + " - " + endDataTime)
                    client.send(bytes(line, "utf-8"))

                elif splitLine[0] == "MSA":
                    print(line)
                    a = 1
                    j=1
                    break
                    client.close()
                print(line)
            if check_file and patientID != 0:

                with open(path, 'r') as read_f:
                    fileLines = read_f.readlines()
                    for lin in fileLines:
                        spLine = lin.split('|')
                        # print(splitLine[0])
                        firstVar = spLine[0]
                        if firstVar == 'OBX' and dataTime <= spLine[14] <= endDataTime:
                            dType = spLine[3].split("^")[1]

                            if dType in dataType:
                                print(lin)
                                client.send(bytes(lin, "utf-8"))
                                data.append(lin)

                            # client.send(bytes(f"", "utf-8"))
                    if len(data) == 0:
                        client.send(
                            bytes(f"Žádná data nevyhovují vaším požadavkům pro pacienta ID: {patientID}", "utf-8"))
                client.send(bytes(f"MSA|AA|{nowDateTime}", "utf-8"))
            if(j==1):
                break
    client.close()
