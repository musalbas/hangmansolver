# This is a proof-of-concept I wrote at 2 o'clock in the morning. There are
# probably quite a few bugs. It's really bad code, mkay?

from hangmansolver import HangmanSolver
import re
from slackconfig import INCOMING_WEBHOOK
import json
import urllib
import urllib2
import web

HANGMAN_BOT_NAME = 'PresidentBot'

urls = ('/slack_outgoing', 'SlackOutgoing')
app = web.application(urls, globals())
hangmansolvers = {}
guessrecv = False
staterecv = False


def send_message(message, channel):
    payload = {'text': message, 'channel': '#'+channel}
    post_values = {'payload': json.dumps(payload)}
    post_data = urllib.urlencode(post_values)
    req = urllib2.Request(INCOMING_WEBHOOK, post_data)
    urllib2.urlopen(req)


class SlackOutgoing(object):

    _re_end_game = re.compile('^The [0-9]+ letter word was: [A-Z]+$')
    _re_state = re.compile('^The ([0-9]+) letter word is: (.+)$')
    _re_letter_guessed = re.compile('^(Yes, there is one|Yes, there are [0-9]+|Sorry, there are no|You already tried) ([A-Z])(\'s| so let\'s pretend that never happened, shall we\?)*$')

    @staticmethod
    def _parse_word_letters(word_letters_text):
        word_letters = []

        word_letters_text = word_letters_text.replace(' ', '')
        for char in word_letters_text:
            if char == '_':
                word_letters.append(None)
            else:
                word_letters.append(char.lower())

        return word_letters

    def POST(self):
        global guessrecv, staterecv

        input = web.input()
        print input

        letter_guessed_match = self._re_letter_guessed.match(input.text)
        if letter_guessed_match:
            if input.channel_name in hangmansolvers:
                hangmansolvers[input.channel_name].guess_letter(letter_guessed_match.group(2))
                guessrecv = True

        state_match = self._re_state.match(input.text)
        if state_match:
            if input.channel_name not in hangmansolvers:
                hangmansolvers[input.channel_name] = HangmanSolver(int(state_match.group(1)))
                guessrecv = True
            hangmansolvers[input.channel_name].set_word_letters(self._parse_word_letters(state_match.group(2)))
            staterecv = True

        if guessrecv and staterecv:
            guessrecv = False
            staterecv = False
            next_move = hangmansolvers[input.channel_name].get_next_move()
            send_message("Statistically, best letter to play now is " + next_move.upper() + ".", input.channel_name)

        if bool(self._re_end_game.search(input.text)):
            if input.channel_name in hangmansolvers:
                del hangmansolvers[input.channel_name]

if __name__ == '__main__':
    app.run()
