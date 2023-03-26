dateTimeFrom = 0
dateTimeTo = 999999999999
patientID = 0
MDateTime = 0
newPac = 0
blok = []
bloks = []
endBlok = 0
error = 0
numPatient = 0
Patient = []
with open('comm_1.txt', 'r') as read_f:
    lines = read_f.readlines()

    for line in lines:
        # print(line)
        splitLine = line.split('|')
        # print(splitLine[0])
        firstVar = splitLine[0]

        if firstVar == 'MSH':
            # print(firstVar + ':' + splitLine[6] + ',' + splitLine[9])
            if splitLine[6] != "":
                MSHLine = line
                blok.clear()
                blok.append(line)


                MDateTime = splitLine[6]
            else:
                blok.append(line)

            if splitLine[9] != "":
                # dateTimeFrom = splitLine[9]
                ...
            MDateTime = splitLine[9]

        elif firstVar == "PID":
            # print(firstVar + ':' + splitLine[3])
            if patientID != splitLine[3]:
                newPac = 1
            patientID = splitLine[3]
            blok.append(line)

        elif firstVar == "PV1":
            # print(firstVar + ':')
            blok.append(line)
            ...

        elif firstVar == "ORC":
            # print(firstVar + ':')
            blok.append(line)
            ...

        elif firstVar == "OBR":
            # print(firstVar + ':' + splitLine[7])
            MDateTime = splitLine[7]
            blok.append(line)

        elif firstVar == "OBX":
            # print(firstVar + ':' + splitLine[14])
            MDateTime = splitLine[14]
            blok.append(line)

        elif firstVar == "MSA":
            # print(firstVar + ':' + splitLine[2])
            MDateTime = splitLine[2]
            blok.append(line)
            endBlok = 1

        else:
            # print("")
            ...

        if int(MDateTime) < int(dateTimeFrom):
            print('Time error')
            error = error + 1

        if newPac == 1:

            if patientID not in Patient:
                print("New patient:" + patientID)
                Patient.append(patientID)
            newPac = 0
            numPatient += 1

        if endBlok == 1:
           # with open('./patientFiles/%s.txt' % patientID, 'a') as write_f:
             #   write_f.writelines(blok)
                endBlok = 0
                bloks.append(blok)
                numBloks = len(bloks)
                # print('Blok :' + str(numBloks))
    dateTimeFrom=MDateTime

print('------------------------------------------------')
print('Blok count:' + str(numBloks))
print('Error count:' + str(error))
print('Patient count:' + str(len(Patient)))
