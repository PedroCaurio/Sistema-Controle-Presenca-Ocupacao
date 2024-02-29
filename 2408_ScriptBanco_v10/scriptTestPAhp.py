import sqlite3
import paho.mqtt.client as mqtt

regE = "autoifrs/tcc/reg/env"
regR = "autoifrs/tcc/reg/rec"
dispE = "autoifrs/tcc/disp/env"
dispR = "autoifrs/tcc/disp/rec"

con = sqlite3.connect("database.db")
cur = con.cursor()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(regR)
    client.subscribe(dispR)

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    #print(msg.topic)
    #print(type(msg.topic))
    
    # -- Registro -- #
    
    if msg.topic == regR:
        mensg = msg.payload.decode()
        pesq = cur.execute("SELECT Tag FROM Cartao WHERE Tag={}".format(mensg))
        painel = pesq.fetchall()
        if not painel:
            crea = cur.execute("INSERT INTO Cartao(Tag, Estado) VALUES ('{}', 'Registro_Pendente')".format(mensg))
            con.commit()
            client.publish(regE, "Novo cartao registrado")
            print("Novo cartão registrado")
        else:
            print("erro 3: Cartão já registrado... SEU JUMENTO")
            client.publish(regE, "erro 3: Cartão já registrado... SEU JUMENTO")
    
    # -- Ocorrências no dispositivo --
    
    elif msg.topic == dispR:
        mensg = msg.payload.decode()
        me = mensg.split(";")
        
        
        #print(mensg)
        #print(type(mensg))
        pesq = cur.execute("SELECT Tag, Estado FROM Cartao WHERE Tag='{}'".format(me[0]))
        #print(pesq)
        
        painel = pesq.fetchall()
        #print (painel)
        if painel:            
            #print(painel[0][1])

            if painel[0][1] == 'Ativo' or 'Registro_Pendente':
                print("deu bom")
                pe = cur.execute("SELECT Pessoa FROM Credenciamento WHERE Tag='{}'".format(me[0]))
                pa = pe.fetchall()
                pessoa = pa[0][0]
                tag = painel[0][0]
                #print(painel[0][0])
                #print(type(painel[0][0]))                        
                cur.execute("INSERT INTO Controle(Credenciamento, Tag, Local) VALUES ('{}','{}', '{}')".format(pessoa, tag, me[1]))
                oco = cur.execute("SELECT Situacao From Acesso WHERE Cartao = '{}' Order by Instante desc Limit 1".format(tag))
                sit = oco.fetchall()
                print(sit)
                if sit:
                    if sit[0][0] == 'Entrada':
                        cur.execute("INSERT INTO Acesso(Cartao, Sala, Situacao) VALUES ('{}', '{}', 'Saida')".format(tag, me[1]))
                        cur.execute("UPDATE Locais SET ocupacao = ocupacao - 1")
                        est = '1'
                    else:
                        cur.execute("INSERT INTO Acesso(Cartao, Sala, Situacao) VALUES ('{}', '{}', 'Entrada')".format(tag, me[1]))
                        cur.execute("UPDATE Locais SET ocupacao = ocupacao + 1")
                        con.commit()
                        est = '0'
                else:
                    cur.execute("INSERT INTO Acesso(Cartao, Sala, Situacao) VALUES ('{}', '{}', 'Entrada')".format(tag, me[1]))
                    cur.execute("UPDATE Locais SET ocupacao = ocupacao + 1")
                    con.commit()
                    est = '0'
                cur.execute("SELECT niveldeacesso.nome as nivel as id from Credenciamento JOIN PESSOA on credenciamento.pessoa = pessoa.id join niveldeacesso on niveldeacesso.id = pessoa.papel")    
                search = pe.fetchall()
                nivel = search[0][0]
                print(nivel)
                client.publish(dispE, "0;{}".format(est))
                
            elif painel[0][1] == 'Desativado':
                client.publish(dispE, "1")
                cur.execute("INSERT INTO Acesso(Cartao, Sala, Situacao) VALUES ('{}', '{}', 'Desativado')".format(tag, me[1]))
                print("QUEM É TU NA FILA DO PÃO?")
                
            elif painel[0][1] == 'Desaparecido':
                client.publish(dispE, "2")
                cur.execute("INSERT INTO Acesso(Cartao, Sala, Situacao) VALUES ('{}', '{}', 'Desaparecido')".format(tag, me[1]))
                print("PEGA LADRÃO!")
                
            else:
                client.publish(dispE, "3")
                cur.execute("INSERT INTO Acesso(Cartao, Sala, Situacao) VALUES ('{}', '{}', 'Desconhecida')".format(tag, me[1]))
                
        else:
            print('erro 2')
            client.publish(dispE, "4")
            #cur.execute("INSERT INTO Acesso(Cartao, Sala, Situacao) VALUES ('{}', '{}', 'SemRegistro')".format(tag, me[1]))
    else:
        print('erro')
        

# --- Conexão MQTT ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()