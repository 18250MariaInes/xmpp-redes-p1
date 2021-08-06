import logging
import asyncio
from getpass import getpass
from argparse import ArgumentParser
from slixmpp.xmlstream import StanzaBase, ET
from slixmpp.exceptions import IqTimeout, IqError 
from xml.etree.ElementTree import fromstring, ElementTree
import slixmpp


class SendMsgBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        # The message we wish to send, and the JID that
        # will receive it.
        self.recipient = recipient
        self.msg = message

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        await self.get_roster()

        """self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')"""

        self.listALLServerUsers()

        self.disconnect()

    def listALLServerUsers(self):
        print("ENTRA A TRAER USERS")
        users = self.Iq()
        print(users)
        print(self.boundjid.bare)
        users['type'] = 'get'
        users['to'] = 'alumchat.xyz'
        users['from'] = 'mvasquez@alumchat.xyz/pda'
        users['id'] = 'search_result'
        print(users)
        itemStanza = ET.fromstring("<command xmlns='http://jabber.org/protocol/commands'"
           "action='execute'"
           "node='http://jabber.org/protocol/admin#get-registered-users-list'/>")
        print("CREA STANZA")
        users.append(itemStanza)
        print(users)
        try:
            print("ENTRA A TRY")
            response = users.send()
            print("pasa response")
            print(response)
            tree = ElementTree(fromstring(str(response)))
            root = tree.getroot()
            print("casting")
            print(tree)
            print(root)
            ET.tostring(root, encoding='utf8').decode('utf8')
            for record in root.iter():
                print(record.attrib)
                if record.text != None:
                    print(record.text)

        except IqError as e:
            raise Exception("Unable list users", e)
            sys.exit(1)
        except IqTimeout:
            raise Exception("Server not responding")
        


if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser(description=SendMsgBot.__doc__)

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
    parser.add_argument("-t", "--to", dest="to",
                        help="JID to send the message to")
    parser.add_argument("-m", "--message", dest="message",
                        help="message to send")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Username: ")
    if args.password is None:
        args.password = getpass("Password: ")

    
    xmpp = SendMsgBot(args.jid, args.password, args.to, args.message)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
    xmpp.connect()
    xmpp.process(forever=False)

    