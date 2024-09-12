def get_peer_node(username):                            # function name is get_peer_node
    n = Pyre(username)                                  # parameter
    #n.set_header("CHAT_Header1","example header1")     # comment
    #n.set_header("CHAT_Header2","example header2")     # comment
    n.start()
    return n                                           # it should return our peer username

def join_group(node, group):                            # function name is join_group and it has two function objects
    node.join(group)                                    # 
    print(f"Joined group: {group}")                     # it will print and you will be able to see "Joined group:"

def chat_task(ctx, pipe, n, group):                     # function name is chat_task and it has 4 function objects
    poller = zmq.Poller()
    poller.register(pipe, zmq.POLLIN)
    # print(n.socket())                                 # comment
    poller.register(n.socket(), zmq.POLLIN)
    # print(n.socket())                                 # comment
    while(True):                                        # keyword passed as long as its true
        items = dict(poller.poll())
        # print(n.socket(), items)                      # comment
        if pipe in items and items[pipe] == zmq.POLLIN:
            message = pipe.recv()
            # message to quit                           # comment
            if message.decode('utf-8') == "$$STOP":
                break
            print(f"YOU: {message.decode('utf-8')}")    # it will print and you will be able to see "YOU:"
            n.shouts(group, message.decode('utf-8'))
        else:                                           # keyword
            cmds = n.recv()
            msg_type = cmds.pop(0).decode('utf-8')
            peer_id = uuid.UUID(bytes=cmds.pop(0))
            peer_username = cmds.pop(0).decode('utf-8')
            match msg_type:
                case "SHOUT":
                    intended_group = cmds.pop(0).decode('utf-8')
                    if intended_group == group:
                        # print(f"{peer_username}({peer_id}): {cmds}")
                        print(f"{peer_username}: {cmds.pop(0).decode('utf-8')}")
                case "ENTER":
                    headers = json.loads(cmds.pop(0).decode('utf-8'))
                    # print(f"NODE_MSG HEADERS: {headers}")
                    # for key in headers:
                    #    print("key = {0}, value = {1}".format(key, headers[key]))
                    # print( f"{peer_username}({peer_id}): is now connected." )
                    print( f"{peer_username}: is now connected." )
                case "JOIN":
                    #print( f"{peer_username}({peer_id}): joined {cmds.pop(0).decode('utf-8')}." )
                    print( f"{peer_username}: joined {cmds.pop( 0 ).decode( 'utf-8' )}." )
            # print(f"NODE_MSG CONT: {cmds}")             # it will print and you will be able to see "NODE_MSG CONT: "
    n.stop()                                              # i think it stops the loop from repeat it self

def get_channel(node, group):                             # function name is get_channel and it has 2 function objects
    ctx = zmq.Context()
    return zhelper.zthread_fork(ctx, chat_task, n=node, group=group)   # it should return the username, the name of the group you joined...