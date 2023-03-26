# ********************************************************************************************************************
#           Požadovaná data:
DataType = ["VITAL HR", "VITAL TEMP2", "VITAL ART(S)"]

# Zadejde rozmezí, ve kterém chcete data zobrazit
#              OD:
StartDateTime = 20110616122516
#              DO:
EndDateTime = 20110616123916

#         Zadajte PID pacienta:
PatientID = 2011021
# ********************************************************************************************************************

import socket
from datetime import datetime
import matplotlib.pyplot as plt
import time

# Definice proměných
data = []
X = []
Y = []
Graph = []
e = 0
DataTypeString = ""
connection = 0
# Nastavení IP a připojení na server
if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 4444
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while e <= 5:
        try:
            server.connect((ip, port))
            connection = 1
            print("Uspěšné připojení k serveru")
            break
        except:
            e += 1
            print(f"Pokus {e} připojení k serveru se nezdařilo")
            time.sleep(1)
    if connection == 1:
        # Aktuální datum a čas
        now = datetime.now()
        nowDateTime = now.strftime("%Y%m%d%H%M%S")

        # Zadefinování dotazu pro server
        for i in DataType:
            if DataType[0] == i:
                DataTypeString += f"{i}"
            else:
                DataTypeString += f"^{i}"
        string = f"MSH|^~\&|CLIENT_4444|CLIENT_4444|SERVER_4444|SERVER_4444|{nowDateTime}||ORU^R01^ORU_R01|20110616000005|P|2.4|||NE|AL|CZE|ASCII||ASCII\n" \
                 f"PID|||{PatientID}||^^^^^^L^A|||O\n" \
                 f"PV1||I|^^OR-1^10.2.56.5:1\n" \
                 f"ORC|RE\n" \
                 f"OBR|1|||{DataTypeString}|||{StartDateTime}|{EndDateTime}|||||||||||||||||A"

        server.send(bytes(string, "utf-8"))
        # print(string)
        while True:
            # přijetí zprávy
            buffer = server.recv(1024)
            buffer = buffer.decode("utf-8")

            if buffer.split("|")[0] == "MSA":

                for l in data:
                    print(l)
                    ...
                print(buffer)
                # print("Vše přijato")
                stringEnd = f"MSH|^~\&|CLIENT_4444|CLIENT_4444|SERVER_4444|SERVER_4444|{nowDateTime}||ORU^R01^ORU_R01|20110616000005|P|2.4|||NE|AL|CZE|ASCII||ASCII\n" \
                            f"MSA|AA|{nowDateTime}"
                server.send(bytes(stringEnd, "utf-8"))
                # Data pro graf:
                if len(data) != 0:
                    print(f"Data pro graf: {Graph}")
                for k in DataType:
                    X.clear()
                    Y.clear()
                    # print(z)
                    for z in range(len(Graph)):

                        # print(Graph[z][0])
                        if Graph[z][0] == k:
                            s = str(Graph[z][1])
                            s1 = str(StartDateTime)
                            s2 = str(EndDateTime)
                            # print(s[8:14])
                            # rok
                            if s1[0:4] != s2[0:4]:
                                X.append(int(s[0:4]))
                                plt.xlabel(f'{StartDateTime} - {EndDateTime} [rok]')
                            # měsíc
                            elif s1[4:6] != s2[4:6]:
                                X.append(int(s[4:6]))
                                plt.xlabel(f'{StartDateTime} - {EndDateTime} [měsíc]')
                            # den
                            elif s1[6:8] != s2[6:8]:
                                X.append(int(s[6:8]))
                                plt.xlabel(f'{StartDateTime} - {EndDateTime} [dny]')

                            # hodina
                            elif s1[8:10] != s2[8:10]:
                                X.append(int(s[9:10]))
                                plt.xlabel(f'{StartDateTime} - {EndDateTime} [hod]')

                            # minuta
                            elif s1[10:12] != s2[10:12]:
                                X.append(int(s[10:12]))
                                plt.xlabel(f'{StartDateTime} - {EndDateTime} [min]')

                            # sekunda
                            else:
                                X.append(int(s[12:14]))
                                plt.xlabel(f'{s1[12:14]}sec - {s2[12:14]} sec')

                            Y.append(float(Graph[z][2]))

                        for p in Graph:
                            if k == Graph[z][0]:
                                # Název Y-osy
                                plt.ylabel(f'{k} [{Graph[z][3]}]')
                            break

                    # Graf
                    plt.plot(X, Y, color='green', linestyle='dashed', linewidth=3, marker='o',
                             markerfacecolor='red', markersize=4)

                    # Titulek
                    plt.title(f'Patient: {PatientID}')

                    plt.show()
                break
            elif buffer.split("|")[0] == "OBX":
                data.append(buffer)
                Xaxis = buffer.split("|")[14]
                MdataType = buffer.split("|")[3].split("^")[1]
                Yaxis = buffer.split("|")[5]
                Unit = buffer.split("|")[6]
                Graph.append([MdataType, Xaxis, Yaxis, Unit])
            elif buffer is not None:
                print(buffer)

        server.close()
