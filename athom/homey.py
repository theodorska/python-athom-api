from athom.managers.apps import ManagerApps
from athom.managers.users import ManagerUsers
from athom.managers.sessions import ManagerSessions
from athom.managers.speech import ManagerSpeechInput

class HomeyAPI:

    def __init__(self, url, token):
        self.url = url

        # Use delegationToken to create sessionToken to access API
        self.ManagerUsers = ManagerUsers(homey=self)
        self.token = self.ManagerUsers.login(token)

        # Ensure to get a valid Session
        self.ManagerApps = ManagerApps(homey=self, token=self.token)
        self.ManagerSessions = ManagerSessions(homey=self, token=self.token)
        self.ManagerSpeechInput = ManagerSpeechInput(homey=self, token=self.token)


    def forCurrentHomey(self):
        raise NotImplementedError("This function is not supported by this module")
