"""María Inés Vásquez Figueroa
18250
Redes 
Proyecto 1"""
import sys
import aiodns
import asyncio
import logging
import xmpp
from slixmpp.xmlstream import StanzaBase, ET
from slixmpp.plugins import BasePlugin, register_plugin
from slixmpp import ClientXMPP

"""if sys.platform == 'win32' and sys.version_info >= (3, 8):
     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())"""

# Done...


class EchoBot(ClientXMPP, BasePlugin):

    def __init__(self, jid, password, task, recipient ="", message=""):
        ClientXMPP.__init__(self, jid, password)
        
        self.recipient = recipient
        self.msg = message
        self.task = task

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)



    async def start(self, event):
        
        if (self.task == "1"):
            self.send_presence('chat', 'Ha llegado la colocha!')
            await self.get_roster()
            self.disconnect()
        elif (self.task == "2"):
            self.send_presence()
            await self.get_roster()
            self.send_message(mto=self.recipient,
                            mbody=self.msg,
                            mtype='chat')
            self.disconnect()
        
        

    def message(self, msg):
        print("........................")
        print(msg["from"])
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()

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


if __name__ == '__main__':
    # Ideally use optparse or argparse to get JID,
    # password, and log level.
    cliente = None
    user = ""
    psswrd = ""
    opcion = "Z"
    while opcion != "s":
        opcion = input("""
                        a: Create account
                        b: Log In
                        c: Log Out
                        d: Delete Account
                        e: Show ALL users and info about them
                        f: ENVIAR MENSAJE
                        g: RECIBIR MENSAJE
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
            