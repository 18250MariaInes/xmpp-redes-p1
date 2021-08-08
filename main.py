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

"""if sys.platform == 'win32' and sys.version_info >= (3, 8):
     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())"""

# Done...


class EchoBot(ClientXMPP, BasePlugin):

    def __init__(self, jid, password, actionSelected, recipient ="", msg="", user=None, show=True):
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
            print("ENTRA A SHOWCONTACTS")
            #self.add_event_handler("contacts", self.contacts)
            self.presences = threading.Event()
            self.contacts = []
            self.user = user
            self.show = show
            self.message = msg

        """if (actionSelected == "5"):
            print("ENTRA A SHOW-CONTACT")
            self.add_event_handler("contacts", self.contacts)
            self.presences = threading.Event()
            self.contacts = []
            self.user = user
            self.show = show
            self.message = msg"""

        self.add_event_handler("session_start", self.start)

        if (actionSelected == "3"):
            self.add_event_handler("message", self.message)
        
        




    async def start(self, event):
        
        if (self.actionSelected == "1"):
            #self.send_presence('chat', 'Ha llegado la colocha!')
            print("ENTRO AQUI IGUAL")
            self.send_presence()
            await self.get_roster()
            self.disconnect()
        elif (self.actionSelected == "2"):
            self.send_presence()
            await self.get_roster()
            self.send_message(mto=self.recipient,
                            mbody=self.msg,
                            mtype='chat')
            self.disconnect()
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
                        if pres['show']:
                            show = pres['show']
                        if pres['status']:
                            status = pres['status']
                        if pres['priority']:
                            status = pres['priority']

                    my_contacts.append([
                        user,
                        subs,
                        status,
                        username,
                        priority
                    ])
                    self.contacts = my_contacts

            if(self.show):
                if(not self.user):
                    if len(my_contacts)==0:
                        print('NO TIENES AMIGOS')
                    else:
                        print("CARGANDO TODOS LOS CONTACTOS")
                        print('\n CONTACTOS: \n')
                    for contact in my_contacts:
                        print('USUARIO:' + str(contact[0]) + '\tSUBSCRIPTION:' + str(contact[1]) )
                else:
                    print('\n\n')
                    print("CARGANDO CONTACTO SELECCIONADO")
                    for contact in my_contacts:
                        if(contact[0]==self .user):
                            print('USUARIO:' + str(contact[0]) + '\tSUBSCRIPTION:' + str(contact[1]) + '\n\tSTATUS:'  + '\n\tUSERNAME:' + str(contact[3]) + '\n\tPRIORITY:' + str(contact[4]))
            else:
                for JID in self.contacts:
                    self.notification_(JID, self.message, 'active')

            self.disconnect()
            print('\n\n')
        

    def message(self, msg):
        #while (reply != "block"):
        print(str(msg['from'])+">>> "+str(msg['body']))
        reply = input("Respuesta>>> ")
        """if (reply == "block"):
            return True"""
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
        '''StanzaForDelete = self.Iq()
        StanzaForDelete['type'] = 'set'
        StanzaForDelete['id'] = 'delete-user-1'
        StanzaForDelete['from'] = xmpp.JID(user)
        StanzaForDelete['to'] = "alumchat.xyz"'''
        #StanzaForDelete.add_command(xmpp.JID(user), "http://jabber.org/protocol/admin#delete-user", "delete-user")
        """itemStanza = ET.fromstring("<query xmlns='jabber:iq:roster'>\
                                 <x xmlns='jabber:x:data' type='submit'>\
                                    <field type='hidden' var='FORM_TYPE'>\
                                        <value>jabber:iq:roster</value>\
                                    </field>\
                                    <field var='Username'>\
                                        <value>1</value>\
                                    </field>\
                                    <field var='search'>\
                                        <value>*</value>\
                                    </field>\
                                    <field var='Name'>\
                                        <value>1</value>\
                                    </field>\
                                    <field var='Email'>\
                                        <value>1</value>\
                                    </field>\
                                </x>\
                                </query>")"""
        """StanzaForDelete['command']['xmlns'] = "http://jabber.org/protocol/commands"
        StanzaForDelete['command']['action'] = 'execute'
        StanzaForDelete['command']['node'] = 'http://jabber.org/protocol/admin#delete-user'"""
        #StanzaForDelete['register']['remove'] = "True"
        #try:
        #StanzaForDelete.append(itemStanza)
        #print(StanzaForDelete)
        #print("*************************")
        #print(itemStanza)
        #StanzaForDelete.send()
        #print("Account deleted succesfuly")
        """except IqError as e:
            raise Exception("We could not Delete the account", e)
            sys.exit(1)
        except IqTimeout:
            raise Exception("Server redes2020.xyz not responding")"""

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

def mandarMensaje(userName,mssg):
    xmpp = EchoBot(user, psswrd, "2", userName, mssg)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') 
    xmpp.connect()
    xmpp.process(timeout = 5)# XMPP Ping

def chat ():
    xmpp = EchoBot(user, psswrd, "3")
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199')
    xmpp.connect()
    xmpp.process()# XMPP Ping

def showUsers ():
    xmpp = EchoBot(user, psswrd, "4")
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
    xmpp.register_plugin('xep_0096') # Jabber Search
    xmpp.connect()
    xmpp.process(forever=False)

def showUser ():
    contact = input("Usuario de interés (name@alumchat.xyz)>>> ") 
    xmpp = EchoBot(user, psswrd, "4", user = contact)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
    xmpp.register_plugin('xep_0096') # Jabber Search
    xmpp.connect()
    xmpp.process(forever=False)


if __name__ == '__main__':
    # Setup the command line arguments.
    """parser = ArgumentParser(description=EchoBot.__doc__)

    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')"""
    cliente = None
    user = ""
    psswrd = ""
    opcion = "Z"
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
            userName = input(
                "Type username please:   ")
            cliente.deleteUser(userName)
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

            