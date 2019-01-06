import sys
import code
import time
import logging
import readline
import argparse
import rlcompleter
import webbrowser

from textwrap import dedent

from athom.cloud import AthomCloudAPI

default_formatter = logging.Formatter(
    "%(asctime)s.%(msecs)03d [%(levelname)-.1s]: %(message)s",
    "%H:%M:%S"
)

banner = """\
         Welcome to the Athom API console. The following variables are available:

         api:    AthomAPI object\
         """

log = logging.getLogger('athom')

def parse_args():
    p = argparse.ArgumentParser(description="Example script for python-athom-api module")
    p.add_argument('-d', help="Show debug output", action="store_true", default=False, dest='debug')
    p.add_argument('--client-id', help="Client ID to access Athom API", dest='clientId', required=True)
    p.add_argument('--client-secret', help="Client secret to access Athom API", dest='clientSecret', required=True)
    p.add_argument('--return-url', help="Return URL for OAUTH2 authentication", default='http://localhost', dest='returnURL')

    return p.parse_args()


def setup_logging(args):
    # Logging of the API can be accomplished by getting logger named athom. DEBUG level is used to log all requests
    # made by the module
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(default_formatter)
    log.addHandler(ch)

    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)


def main():
    args = parse_args()
    setup_logging(args)

    # Start by getting an instance of the AthomCloudAPI, providing the client id/secret and
    # returnURL for OATH authentication
    api = AthomCloudAPI(args.clientId, args.clientSecret, args.returnURL)

    # Verify if there exists an acive session, if not get one
    if not api.hasAuthorizationCode():
        oauth_url = api.getLoginUrl()

        log.info("No active session found, opening URL to get OATH token")
        time.sleep(5)

        log.info("OATH URL: %s", oauth_url)
        webbrowser.open(oauth_url, new=2)

        log.info("Enter OATH token")
        oath = input("OATH token: ")
        api.authenticateWithAuthorizationCode(oath)

    # Start interactive console
    # TODO: extend symbolic table to include all module classes/functions
    symbolic_table = globals()
    symbolic_table.update(locals())
    readline.set_completer(rlcompleter.Completer(symbolic_table).complete)
    readline.parse_and_bind('tab: complete')

    console = code.InteractiveConsole()
    console.locals['api'] = api
    console.interact(banner=dedent(banner))


if __name__ == "__main__":
    main()