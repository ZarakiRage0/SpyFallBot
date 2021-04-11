class Player:
    def __init__(self, discord_user):
        self.user = discord_user
        self.role = None

    def set_role(self,role):
        self.role = role