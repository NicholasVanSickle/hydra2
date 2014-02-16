import hydracommands
import irc.bot
import irc.strings

class BotParser(hydracommands.HydraCommands):
    buffer = ''
    def _print(self, x):
        self.buffer += x + '\n'

    def readAll(self):
        data = self.buffer.rstrip()
        self.buffer = ''
        return data

class HydraBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.parser = BotParser()
        
    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")        
        
    def on_welcome(self, c, e):
        c.join(self.channel)

    def do_command(self, c, e, destination):
        line = e.arguments[0]
        if not line.startswith('!'):
            return
        self.parser.execute(line[1:])
        output = self.parser.readAll()
        if output:
            try:
                for line in output.split('\n'):
                    c.privmsg(destination, line)
            except:
                c.privmsg(destination, "Error running command.")
        
    def on_privmsg(self, c, e):
        self.do_command(c, e, e.source.nick)
        
    def on_pubmsg(self, c, e):
        self.do_command(c, e, self.channel)
        
if __name__ == '__main__':
    server = 'irc.nac.net'
    port = 6667
    channel = '#conduit'
    nick = 'HydraBot'
    bot = HydraBot(channel, nick, server, port)
    bot.start()