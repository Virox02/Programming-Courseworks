import socket
import ds_protocol
import json, time


class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = 0


class DirectMessenger():
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        super().__init__()
    
    def send(self, message:str, recipient:str) -> bool:
        '''
        If connection to a server is successfully established (response from the server is 'ok'),
        then a token wil be produced and used along with a time stamp, message, and recipient to be translated into JSON format.
        This method interacts with ds_protocol module to recieve data from the server using the translated message.

        :param str message : a message that the user wants to send to another user
        :param str recipient : the receiver of the message
        :returns: True if the message is successfully sent, False if the message failed to send.
        :rtype: bool
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client: #connecting to server
                client.connect(('168.235.86.101', 3021))
                send = client.makefile('w')
                recv = client.makefile('r')

                print("You are connected to 168.235.86.101 on ",3021)

                join_ds_server = ds_protocol.join(self.username, self.password, "") #translates to JSON format
                send.write(join_ds_server + '\r\n') 
                send.flush()
                srv_msg = recv.readline() #read the response
                print("Response",srv_msg)
                if "ok" in srv_msg:
                    token_tuple = ds_protocol.extract_json(srv_msg)
                    the_token = token_tuple[0] #gets a token
                    obj_timestamp = time.time() #if timestamp has not been set, generate a new from time module
                    the_message = ds_protocol.send_dm(the_token, message, recipient, obj_timestamp) #translates to JSON format
                    send.write(the_message + '\r\n')
                    send.flush()
                    srv_msg = recv.readline() #read the response
                    print("Response",srv_msg)
                    return True
                else:
                    return False
        
		
    def retrieve_new(self) -> list:
        '''
        This method turns information obtained from the server into DirectMessage objects and stores them in a list.
        If connection to a server is successfully established (response from the server is 'ok'),
        then a token wil be produced to be used for JSON translation.
        This method interacts with ds_protocol module to recieve data from the server using the translated message.
        
        :returns: list of DirectMessage objects containing all the new messages that the user has received from another user.
        :rtype: list
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client: #connecting to server
                client.connect((self.dsuserver, 3021))
                send = client.makefile('w')
                recv = client.makefile('r')

                print("You are connected to",self.dsuserver,"on",3021)
                
                
                join_ds_server = ds_protocol.join(self.username, self.password, "") #translates to JSON format
                send.write(join_ds_server + '\r\n') 
                send.flush()
                srv_msg = recv.readline() #read the response
                print("Response",srv_msg)
                if "ok" in srv_msg:
                    token_tuple = ds_protocol.extract_json(srv_msg)
                    the_token = token_tuple[0] #gets the token
                    the_translation = ds_protocol.unread_mes(the_token, 'new') #translates to JSON format
                    send.write(the_translation + '\r\n') #write to server
                    send.flush()
                    srv_msg = recv.readline() #read the response
                    print("Response",srv_msg)
                    x = json.loads(srv_msg)
                    unread = x['response']['messages'] #gets the list of dictionaries
                    new_dm_objs = [] #create a new list to store DirectMessage objects
                    for item in unread: #iterate through the list 
                        dir_obj = DirectMessage()
                        #turns the messages, timestamp, and recipient obtained in the list of dictionaries into DirectMessage objects
                        dir_obj.message = item['message']
                        dir_obj.recipient = item['from']
                        dir_obj.timestamp = item['timestamp']
                        new_dm_objs.append(dir_obj) #add the DirectMessage objects into the list
                    return new_dm_objs #populate and return a new list with DirectMessage objects

 
    def retrieve_all(self) -> list:
        '''
        This method turns information obtained from the server into DirectMessage objects and stores them in a list.
        If connection to a server is successfully established (response from the server is 'ok'),
        then a token wil be produced to be used for JSON translation.
        This method interacts with ds_protocol module to recieve data from the server using the translated message.

        :returns: list of DirectMessage objects containing all the messages that the user has received.
        :rtype: list
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client: #connecting to server
            client.connect((self.dsuserver, 3021))
            send = client.makefile('w')
            recv = client.makefile('r')

            print("You are connected to",self.dsuserver,"on",3021)
                        
                        
            join_ds_server = ds_protocol.join(self.username, self.password, "") #translates to JSON format
            send.write(join_ds_server + '\r\n') 
            send.flush()
            srv_msg = recv.readline() #read the response
            print("Response",srv_msg)
            if "ok" in srv_msg:
                token_tuple = ds_protocol.extract_json(srv_msg)
                the_token = token_tuple[0] #gets the token
                the_translation = ds_protocol.all_mes(the_token, 'all') #translates to JSON format
                send.write(the_translation + '\r\n') #write to server
                send.flush()
                srv_msg = recv.readline() #read the response
                print("Response",srv_msg)
                x = json.loads(srv_msg)
                all_unread = x['response']['messages'] #gets the list of dictionaries
                all_dm_objs = [] #create a new list to store DirectMessage objects
                for item in all_unread: #iterate through the list 
                    dir_obj = DirectMessage()
                    #turns the messages, timestamp, and recipient obtained in the list of dictionaries into DirectMessage objects
                    dir_obj.message = item['message']
                    dir_obj.recipient = item['from']
                    dir_obj.timestamp = item['timestamp']
                    all_dm_objs.append(dir_obj) #add the DirectMessage objects into the list
                print(all_dm_objs) 
                return all_dm_objs #populate and return a new list with DirectMessage objects
