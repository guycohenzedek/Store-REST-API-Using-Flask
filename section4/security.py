from user import User

# Table of users
users = [ User(1, 'guy', '1234') ]

# Mapping users detailes by name
username_mapping = { user.username: user for user in users }

# Mapping users detailes by ID
userid_mapping = { user.id: user for user in users }


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user

def identity(payload):
    userid = payload['identity']
    return userid_mapping.get(userid, None)
                          