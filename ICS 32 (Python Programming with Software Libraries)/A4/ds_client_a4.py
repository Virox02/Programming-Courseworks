import socket
import ds_protocol_a4
import sys
from NaClProfile import NaClProfile

naclprf = NaClProfile()

'''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
'''
IMP: ASK WHAT EXACTLY DOES ENCRYPT_ENTRY DOES cuz if message is being passed in as encrypted
already then why do u need to encrypt again?
'''
def send(kpair:str, server:str, port:int, username:str, password:str, message:str, bio:str=None): #publickey, priv
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((server, port)) 
        except:
            print("ERROR connecting to the server, make sure you have entered a valid server and port", sys.exc_info())
        else:
            Send = client.makefile('w')
            recv = client.makefile('r')

            print("client connected to {} on {}".format(server, port))
            
            naclprf.import_keypair(kpair) #setting public and private key
            Join = ds_protocol_a4.join(username, password, naclprf.public_key)
            Send.write(Join + '\r\n')
            Send.flush()
            res = recv.readline()
            srv_msg = ds_protocol_a4.extract_msg(res)
            #print(srv_msg)
            #srvpubkey = srv_msg.token
            #print(srvpubkey)
            
            if srv_msg.typ == 'ok':
                tkn = srv_msg.token
                #print(type(tkn))
                encrpt = naclprf.encrypt_entry(message, tkn) #encrypting the message using the server's token as the key
                dec_encrpt = encrpt.decode(encoding = 'UTF-8') #decoding it to string
                #print(dec_encrpt)
                POST = ds_protocol_a4.post(naclprf.public_key, dec_encrpt, 0) 
                Send.write(POST + '\r\n')
                Send.flush()
                res = recv.readline()
                #srv_msg = ds_protocol_a4.extract_msg(res)
                #print(srv_msg)
            
                if bio != None:
                    BIO = ds_protocol_a4.Bio(tkn, bio, 0) 
                    Send.write(BIO + '\r\n')
                    Send.flush()
                    res = recv.readline()
                    srv_msg = ds_protocol_a4.extract_msg(res)
            else:
                print("error")
            print("Response", res)
            if srv_msg.typ == 'ok':
                print("Post successfully published!")
        
if __name__ == '__main__':
    send("caF6iELQvqshC3SlAqoDE5mqd86TPVlwFe81i5k6ggU=TZktDK7di4PrGRvx7Ziu23vDkGS3iy5JGhQ4XuQDtFU=", "168.235.86.101", 2021, "virox18", "bshfbj", "hello test")

    
