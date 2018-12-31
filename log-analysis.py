logcsv = "server_audit.csv"



with open(logcsv) as csvfile:
    for line in csvfile:
        logdata = line.strip().split(";")

        querydata = logdata[-2]
        querydata2 = querydata.strip("'")
        f = open("log.rdf", "a+")



        # A query (i.e. not a connect or disconnect) AND the query was successful
        if logdata[-4] == "QUERY" and int(logdata[-1]) == 0:

            if "SELECT" in querydata2:
                if "SELECT DATABASE()" not in querydata2:

                    log="Example1"
                    line1="<http://example.org/" + log + "> " + "<http://www.w3.org/1999/02/22-rdf-syntax-ns#> " + "<http://www.specialprivacy.eu/langs/splog#Log>.\n"
                    print(line1)
                    f.write(line1)


                    # splog:logEntry (Query number automatically assigned by the MariaDB Audit Plugin
                    logEntryNumber = logdata[6]
                    logEntry = "<http://example.org/" + log + "> " + "<http://www.specialprivacy.eu/langs/splog#logEntry> " + "<http://example.org/" + logEntryNumber + ">.\n"
                    print(logEntry)
                    f.write(logEntry)

                    # splog:message containing query
                    splog_message = "<http://example.org/" + logEntryNumber + "> " + "<http://www.specialprivacy.eu/langs/splog#message> " + "\"" + querydata2 + "\".\n"
                    print(splog_message)
                    f.write(splog_message)

                    # Reformat time and date to format suggested by SPLog for splog:transactionTime and splog:validityTime
                    splog_transactionTime = "<http://example.org/" + logEntryNumber + "> " + "<http://www.specialprivacy.eu/langs/splog#transactionTime> " + \
                                          "\"" + logdata[0][:4] + "-" + logdata[0][4:6] + "-" + logdata[0][6:] + "T"+logdata[1] + "Z\^^xsd:dateTimeStamp" + "\".\n"
                    print(splog_transactionTime)
                    f.write(splog_transactionTime)

                    splog_validityTime = "<http://example.org/" + logEntryNumber + "> " + "<http://www.specialprivacy.eu/langs/splog#validityTime> " + \
                                          "\"" + logdata[0][:4] + "-" + logdata[0][4:6] + "-" + logdata[0][6:] + "T"+logdata[1] + "Z\^^xsd:dateTimeStamp" + "\".\n"
                    print(splog_validityTime)
                    f.write(splog_validityTime)

                    # splog:dataSubject --> assumption for show purposes: correlation between subject and query ID. "_:subject29" in figure 10
                    splog_dataSubject = "<http://example.org/" + logEntryNumber + "> " + "<http://www.specialprivacy.eu/langs/splog#dataSubject> " + "\"_subject" + logEntryNumber + "\".\n"
                    print(splog_dataSubject)
                    f.write(splog_dataSubject)

                    # splog:logEntryContent
                    splog_logEntryContent = "<http://example.org/" + logEntryNumber + "> " + "<http://www.specialprivacy.eu/langs/splog#logEntryContent> " + "<http://example.org/EntryContent" + logEntryNumber + ">.\n"
                    print(splog_logEntryContent)
                    f.write(splog_logEntryContent)

                    # spl:hasProcessing
                    spl_hasProcessing = "<http://example.org/EntryContent" + logEntryNumber + "> " + "<http://spinrdf.org/spl#hasProcessing> " + "<http://www.specialprivacy.eu/vocabs/processing#Query>.\n"
                    print(spl_hasProcessing)
                    f.write(spl_hasProcessing)

                    # spl:hasStorage
                    spl_hasStorage = "<http://example.org/EntryContent" + logEntryNumber + "> " + "<http://spinrdf.org/spl#hasStorage> " + "<http://example.org/storage>.\n"
                    print(spl_hasStorage)
                    f.write(spl_hasStorage)

                    # spl:hasLocation --> assumption: storage for GDPR compliance in the EU
                    spl_hasLocation = "<http://example.org/storage> " + "<http://spinrdf.org/spl#hasLocation> " + "<http://www.specialprivacy.eu/vocabs/locations#EU>."
                    print(spl_hasLocation)
                    f.write(spl_hasLocation)

                    # Data Category mapping for the tables in the employee sample database using a dictionary.
                    mapping_dict= {
                        "emp_no": "<http://www.specialprivacy.eu/vocabs/data#uniqueid>",
                        "birth_date": "<http://www.specialprivacy.eu/vocabs/data#bdate>",
                        "first_name": "<http://www.specialprivacy.eu/vocabs/data#given>",
                        "last_name": "<http://www.specialprivacy.eu/vocabs/data#family>",
                        "gender": "<http://www.specialprivacy.eu/vocabs/data#gender>",
                        "hire_date": "<http://example.org/HireDate>",
                        "dept_no": "<http://www.specialprivacy.eu/vocabs/data#uniqueid>",
                        "dept_name": "<http://www.specialprivacy.eu/vocabs/data#department>",
                        "from_date": "<http://example.org/DateFrom>",
                        "to_date": "<http://example.org/DateUntil>",
                        "title": "<http://www.specialprivacy.eu/vocabs/data#jobtitle>",
                        "salary": "<http://www.specialprivacy.eu/vocabs/data#financial>"
                    }

                    # Eliminating the possibility of mapping from anywhere after the FROM statement of the SQL query. That way there is no mapping for columns mentioned in the WHERE statement.
                    stripdataFROM = querydata2.split("FROM")[0]

                    check = stripdataFROM.replace(",", "").split(" ")
                    check = list(filter(None, check))
                    del check[0]

                    # Unions with previously defined mapping
                    owl_UnionOf = "<http://example.org/EntryContent" + logEntryNumber + "> " + "<http://www.w3.org/2002/07/owl#UnionOf> " + "\"_:U1\".\n"
                    print(owl_UnionOf)
                    f.write(owl_UnionOf)
                    for i in check:
                        whichindex = check.index(i)
                        union = "\"_:U" + str(whichindex+1) + ".\"" + "<http://www.w3.org/1999/02/22-rdf-syntax-ns#first> " + mapping_dict[i] + ".\n"
                        print(union)
                        f.write(union)
                        newcheck = len(check)
                        if newcheck > whichindex+1:
                            union_rest = "\"_:U" + str(whichindex+1) + ".\"" + "<http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> " + "\"_:U" + str(whichindex + 2) + ".\"" + ".\n"
                            print(union_rest)
                            f.write(union_rest)

        f.close()





