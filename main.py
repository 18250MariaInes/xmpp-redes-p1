"""María Inés Vásquez Figueroa
18250
Redes 
Proyecto 1"""
import sys
import aiodns
#import asyncio
import threading
import logging
import xmpp
from slixmpp.xmlstream import StanzaBase, ET
from slixmpp.plugins import BasePlugin, register_plugin
from slixmpp import ClientXMPP



#Class to establish conection with server to initialize chat
#It executes different function depending of the action selected by the user
class EchoBot(ClientXMPP, BasePlugin):

    def __init__(self, jid, password, actionSelected, recipient ="", msg="", user=None, show=True, grp = ""):
        ClientXMPP.__init__(self, jid, password)
        
        self.recipient = recipient
        self.msg = msg
        self.actionSelected = actionSelected

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        if (actionSelected == "4" or actionSelected == "5"):
            print("CARGANDO AGENDA DE CONTACTOS")
            #self.add_event_handler("contacts", self.contacts)
            self.presences = threading.Event()
            self.contacts = []
            self.user = user
            self.show = show
            self.message = msg

        if (actionSelected == "6" or actionSelected == "7"):
            self.user = user

        if (actionSelected == "8"):
            self.msg = msg
            self.presences = threading.Event()
            self.contacts = []

        if (actionSelected == "9"):
            print("aqui", actionSelected)
            self.user = user
            self.grp = grp
            print("aqui")

        """if (actionSelected == "5"):
            print("ENTRA A SHOW-CONTACT")
            self.add_event_handler("contacts", self.contacts)
            self.presences = threading.Event()
            self.contacts = []
            self.user = user
            self.show = show
            self.message = msg"""

        self.add_event_handler("session_start", self.start)
        if (actionSelected == "9"):
            self.add_event_handler("groupchat_message", self.muc_message)
        if (actionSelected == "3"):
            self.add_event_handler("message", self.message)
        
    async def start(self, event):
        #Log in to server
        if (self.actionSelected == "1"):
            #self.send_presence('chat', 'Ha llegado la colocha!')
            print("ENTRO AQUI IGUAL")
            self.send_presence()
            await self.get_roster()
            self.disconnect()
        #send dm to contact
        elif (self.actionSelected == "2"):
            self.send_presence()
            await self.get_roster()
            self.send_message(mto=self.recipient,
                            mbody=self.msg,
                            mtype='chat')
            self.disconnect()
        #communication with one user in a chat
        elif (self.actionSelected == "3"):
            #self.send_presence('chat', 'Ha llegado la colocha!')
            print("CHAT PRIVADO DE COMUNICACIÓN")
            self.send_presence()
            await self.get_roster()
            print(str(msg['from'])+">>> "+str(msg['body']))
            reply = input("Respuesta>>> ")
            if (reply == "block"):
                self.disconnect()
            else:
                msg.reply(reply).send()
            
        #get info of one or multiple users  
        elif (self.actionSelected == "4" or self.actionSelected == "5"):
            self.send_presence()
            await self.get_roster()
            my_contacts = []
            try:
                self.get_roster()
            except IqError as e:
                print("ALGO MALO PASÓ MANO", e)
            except IqTimeout:
                print("LA SEÑAL CAYÓ HORRIBLE MANO")
            self.presences.wait(3)
            my_roster = self.client_roster.groups()
            for group in my_roster:
                for user in my_roster[group]:
                    status = show = answer = priority = ''
                    self.contacts.append(user)
                    subs = self.client_roster[user]['subscription']
                    conexions = self.client_roster.presence(user)
                    username = self.client_roster[user]['name'] 
                    for answer, pres in conexions.items():
                        if pres['status']:
                            status = pres['status']

                    my_contacts.append([
                        user,
                        status,
                        username
                    ])
                    self.contacts = my_contacts

            if(self.show):
                if(not self.user):
                    if len(my_contacts)==0:
                        print('NO TIENES AMIGOS')
                    else:
                        
                        print('\n CONTACTOS: \n')
                        for contact in my_contacts:
                            #print(contact)
                            if (str(type(contact)) == "<class 'list'>" ):
                                print('USUARIO: ' + str(contact[0]) + '\tESTADO: ' + str(contact[1]) )
                                print('-------------------------------------------------------------' )
                else:
                    print("\n CARGANDO CONTACTO SELECCIONADO: ")
                    for contact in my_contacts:
                        if(contact[0]==self .user):
                            #print(contact)
                            print('USUARIO:' + str(contact[0]) + '\tESTADO: ' + str(contact[1]))
                            print('-------------------------------------------------------------' )
            else:
                for JID in self.contacts:
                    self.notification_(JID, self.message, 'active')

            self.disconnect()
            print('\n\n')
        
        #add contact to list of friends
        elif(self.actionSelected == "6"):
            self.send_presence()
            await self.get_roster()
            try:
                self.send_presence_subscription(pto=self.user) 
            except IqTimeout:
                print("404 CAYÓ HORRIBLE LA CONEXIÓN MANO") 
            self.disconnect()
            print('\n\n')

        #delete account
        elif(self.actionSelected == "7"):
            self.send_presence()
            await self.get_roster()
            stanza = self.Iq()
            stanza['type'] = 'set'
            stanza['from'] = self.user
            fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
            stanza.append(fragment)

            try:
                stanza.send()
                print("¡TE HAS ELIMINADO DEL ALUMCHAT POR SIEMPRE!\n")
                self.disconnect()
            except IqError as e:
                print("ALGO MALO PASÓ MANO", e)
            except IqTimeout:
                print("LA SEÑAL CAYÓ HORRIBLE MANO")
            except Exception as e:
                print(e)  

        elif(self.actionSelected == "8"):
            print("ENTRO A MANDAR PRESENCIA")
            self.send_presence()
            await self.get_roster()
            my_contacts = []
            try:
                #Check the roster
                self.get_roster()
            except IqError as e:
                #If there is an error
                print("Something went wrong", e)
            except IqTimeout:
                #Server error
                print("THE SERVER IS NOT WITH YOU")
            
            #Wait for presences
            self.presences.wait(3)

            #For each client on roster
            my_roster = self.client_roster.groups()
            for group in my_roster:
                for user in my_roster[group]:
                    status = show = answer = priority = ''
                    self.contacts.append(user)
                    subs = self.client_roster[user]['subscription']                         #Get subscription
                    conexions = self.client_roster.presence(user)                           
                    username = self.client_roster[user]['name']                             #Get username
                    for answer, pres in conexions.items():
                        if pres['show']:
                            show = pres['show']                                             #Get show
                        if pres['status']:
                            status = pres['status']                                         #Get status
                        if pres['priority']:
                            priority = pres['priority']                                     #Get priority

                    my_contacts.append([
                        user,
                        subs,
                        status,
                        username,
                        priority
                    ])
                    self.contacts = my_contacts
            for JID in self.contacts:
                self.presenceMessage(JID, self.msg)
            self.disconnect()
            print('\n\n')

        elif(self.actionSelected == "9"):
            print("ENTRAR A GRP")
            self.send_presence()
            await self.get_roster()
            try:
                #Join room
                self.plugin['xep_0045'].join_muc(self.grp, self.user)
                print("TE HAN ACEPTADO EN EL GRUPO")
                self.send_message(mto=self.grp,
                                mbody="HOLA A TODOS Y TODAS",
                                mtype='groupchat')
            except IqError as e:
                print("ALGO SALIÓ MAL MANO", e)
            except IqTimeout:
                print("LA SEÑAL CAYÓ HORRIBLE MANO")
            
    
    def presenceMessage(self, to, msg):
        message = self.Message()
        message['to'] = to
        message['type'] = 'chat'
        message['body'] = msg

        stanza = ET.fromstring("<active xmlns='http://jabber.org/protocol/chatstates'/>")
        
        try:
            message.send()
        except IqError as e:
            print("ALGO SALIÓ MAL MANO\n", e)
        except IqTimeout:
            print("LA CONEXIÓN CAYÓ HORRIBLE MANO")

    def muc_message(self, msg):
        if(str(msg['from']).split('/')[1]!=self.user):
            print(str(msg['from']).split('/')[1] + ": " + msg['body'])
            message = input("Respuesta >>> ")
            self.send_message(mto=msg['from'].bare,
                              mbody=message,
                              mtype='groupchat')
    
        

    def message(self, msg):
        #while (reply != "block"):
        print(str(msg['from'])+">>> "+str(msg['body']))
        reply = input("Respuesta>>> ")
        msg.reply(reply).send()
        #msg.reply("Thanks for sending\n%(body)s" % msg).send()

    def wait_for_presences(self, pres):
        print("************")
        print(pres)
        self.received.add(pres['from'].bare)
        if len(self.recieved)>=len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

    def logout(self):
        print("SE LOGGEO out")
        self.disconnect(wait=False)

    def send_messageFunc(self, to, msg):
        print("ENVIANDO...")
        self.send_presence()
        self.get_roster()
        self.send_message(mto=to,
                          mbody=msg,
                          mtype='chat')
        print("SE HA MANDADO EL MENSAJE: "+msg+" A "+to)

    def deleteUser(self, user):
        name = "delete_user"
        xmpp['xep_0050'].start_command(
                jid=xmpp.JID(user),
                node='http://jabber.org/protocol/admin#%s' % name,
                session=None,
                ifrom=xmpp.JID(user))

def registerNewUser(user, passw):
    usuario = user
    password = passw
    jid = xmpp.JID(usuario)
    cli = xmpp.Client(jid.getDomain(), debug=[])
    cli.connect()

    if xmpp.features.register(cli, jid.getDomain(), {'username': jid.getNode(), 'password': password}):
        return True
    else:
        return False       


#FUNCTION THAT INSTANTIATE THE ECHOBOT CLASS

#Log in to server
def login():
    print("BIENVENIDO OTRA VEZ")
    userName = input("Usuario (name@alumchat.xyz)>>> ")
    passWord = input("Contraseña>>> ")
    user = userName
    psswrd = passWord
    print("-----------------")
    print(user, psswrd)
    """xmpp = EchoBot(userName, passWord, "1")
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') 
    xmpp.connect()
    xmpp.process(timeout = 10)"""
    print("USUARIO LOGGEADO")
    # xmpp.process(forever=True)
    #return xmpp

#send direct messaje
def mandarMensaje(userName,mssg):
    xmpp = EchoBot(user, psswrd, "2", userName, mssg)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') 
    xmpp.connect()
    xmpp.process(timeout = 5)# XMPP Ping

#start chat with contact
def chat ():
    xmpp = EchoBot(user, psswrd, "3")
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199')
    xmpp.connect()
    xmpp.process()# XMPP Ping

#show all my contacts
def showUsers ():
    xmpp = EchoBot(user, psswrd, "4")
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
    xmpp.register_plugin('xep_0096') # Jabber Search
    xmpp.connect()
    xmpp.process(forever=False)

#show info of only one user
def showUser ():
    contact = input("Usuario de interés (name@alumchat.xyz)>>> ") 
    xmpp = EchoBot(user, psswrd, "4", user = contact)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
    xmpp.register_plugin('xep_0096') # Jabber Search
    xmpp.connect()
    xmpp.process(forever=False)

#add contact to my friend list
def addContact ():
    contact = input("Usuario de futuro amigo (name@alumchat.xyz)>>> ") 
    xmpp = EchoBot(user, psswrd, "6", user = contact)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
    xmpp.register_plugin('xep_0096') # Jabber Search
    xmpp.connect()
    xmpp.process(forever=False)

def deleteUser(contact):
    xmpp = EchoBot(user, psswrd, "7", user = contact)
    xmpp.connect()
    xmpp.process(forever=False)

def sendPresence(msg):
    xmpp = EchoBot(user, psswrd, "8", msg=msg)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
    xmpp.register_plugin('xep_0096') # Jabber Search
    xmpp.connect()
    xmpp.process(forever=False)

def enterGrp(grp, name):
    print("entra")
    xmpp = EchoBot(user, psswrd, "9", grp = grp, user = name)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0045')
    xmpp.register_plugin('xep_0199')
    xmpp.connect()
    xmpp.process(forever=False)



if __name__ == '__main__':
    cliente = None
    user = ""
    psswrd = ""
    opcion = ""
    print("""       ESTE ES EL CHAT XMPP DE MARÍA INÉS VÁSQUEZ FIGUEROA 18250""")
    print("""       ---------------------------------------------------------""")
    while opcion != "s":
        
        opcion = input("""
                        a: CREAR CUENTA
                        b: INICIO SESIÓN
                        c: CERRAR SESIÓN
                        d: ELIMINAR CUENTA
                        e: MOSTRAR TODOS MIS CONTACTOS
                        f: ENVIAR MENSAJE
                        g: CHAT
                        h: MOSTRAR INFO DE UN CONTACTO
                        i: AGREGAR USUARIO COMO CONTACTO
                        j: MANDAR TU PRESENCIA A TUS CONTACTOS
                        k: ENTRAR A CONVERSACIÓN VIRTUAL
                        s: SALIR
                        INGRESA LA ACCIÓN QUE DESEAS HACER>>> """)
        if (opcion == "a"):
            print("BIENVENDID@ AL CHAT DE MARÍA INÉS VÁSQUEZ")
            userName = input("Usuario (name@alumchat.xyz)>>> ")
            passWord = input("Contraseña>>> ")
            user = userName
            psswrd = passWord
            ansRegister = registerNewUser(userName, passWord)
            if (ansRegister):
                print("TE HAS REGISTRADO")
            else:
                print("404 CAYÓ LA SEÑAL HORRIBLE MANO")
        elif (opcion == "b"):
            print("BIENVENIDO OTRA VEZ")
            userName = input("Usuario (name@alumchat.xyz)>>> ")
            passWord = input("Contraseña>>> ")
            user = userName
            psswrd = passWord
        elif (opcion == "d"):
            dec = input("¿Seguro que te quieres eliminar? Es permanente (Y/N)>>> ")
            if (dec == "Y"):
                deleteUser(userName)
            else:
                print("Me alegro que no te vayas amig@")
        elif (opcion == "c"):
            cliente.logout()
        elif (opcion == "f"):
            userName = input("Destinatario (name@alumchat.xyz)>>> ")
            mssg = input("Mensaje>>> ")
            mandarMensaje(userName,mssg)
        elif (opcion == "g"):
            chat()
        elif (opcion == "e"):
            showUsers()
        elif (opcion == "h"):
            showUser()
        elif (opcion == "i"):
            addContact()
        elif (opcion == "j"):
            msg = input("¿Cuál quieres que sea tu presencia?>>> ") 
            sendPresence(msg)
        elif (opcion == "k"):
            grp = input("¿A qué grupo quieres entrar? (test@conference.alumchat.xyz) >>> ") 
            name = input("¿Cuál quieres que sea tu pseudónimo? ")
            enterGrp(grp,name)
            

            