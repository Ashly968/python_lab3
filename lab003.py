# Core Functions – Data Handling and User Input
def get_username():
    user_name = input("Enter your desired Username: ").strip().upper()
    return user_name

def get_group():
    group_name = input("Name of the group wished to join: ").strip().upper()
    return group_name

def get_message():
    type_message = input("Message you would like to send: ").strip()
    return type_message

#Combining the Functions to Create the Peer-to-Peer Chat
import lab_chat as lc

def init_chat():
    user = get_username()  # get user
    group = get_group()  # get group
    connect = lc.get_peer_node(user)  # connect as peer node
    lc.join_group(connect, group)  # join the group
    return lc.get_channel(connect, group)  # return a chat channel

def start_chat():
    channel = init_chat()

    while True:
        try:
            msg = get_message()
            channel.send(msg.encode('utf_8'))
        except (KeyboardInterrupt, SystemExit):
            break
    channel.send("$$STOP".encode('utf_8'))
    print("FINISHED")
    return get_username(), get_group(), get_message()

start_chat()