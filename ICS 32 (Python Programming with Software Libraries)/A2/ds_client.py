import socket
import ds_protocol
import sys

'''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''


def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((server, port)) 
        except:
            print("ERROR connecting to the server, make sure you have entered a valid server and port", sys.exc_info())
        else:
            Send = client.makefile('w')
            recv = client.makefile('r')

            print("client connected to {} on {}".format(server, port)) 
            
            Join = ds_protocol.join(username, password)
            Send.write(Join + '\r\n')
            Send.flush()
            res = recv.readline()
            srv_msg = ds_protocol.extract_msg(res)
            if srv_msg.typ == 'ok':
                tkn = srv_msg.token
                POST = ds_protocol.post(tkn, message, 0) 
                Send.write(POST + '\r\n')
                Send.flush()
                res = recv.readline()
            
                if bio != None:
                    BIO = ds_protocol.Bio(tkn, bio, 0) 
                    Send.write(BIO + '\r\n')
                    Send.flush()
                    res = recv.readline()
            else:
                print("error")
            print("Response", res)
            print("Post successfully published!")
        


    
