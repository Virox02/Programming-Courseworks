import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from Profile import Profile, Post, DsuFileError, DsuProfileError
import NaClDSEncoder
from pathlib import Path
import json, time, os



# TODO: Import the Profile and Post classes
# TODO: Import the NaClDSEncoder module
    
# TODO: Subclass the Profile class
class NaClProfile(Profile):
    def __init__(self):
        self.public_key = None
        self.private_key = None
        self.keypair = None
        #nacl_keypair = NaClDSEncoder.NaClDSEncoder() #encode into a string
        #self.strnacl = str(nacl_keypair)
        #print(nacl_keypair)
        #self.strnacl = nacl_keypair.decode(encoding = 'UTF-8')
        genkey = self.generate_keypair()
        #self.encpost = None
        #super()._posts()
        super().__init__()
        
        """
        TODO: Complete the initializer method. Your initializer should create the follow three 
        public data attributes:

        public_key:str
        private_key:str
        keypair:str

        Whether you include them in your parameter list is up to you. Your decision will frame 
        how you expect your class to be used though, so think it through.
        """
        #pass

    #def naclkeypair():
        #nacl_keypair = NaClDSEncoder.NaClDSEncoder()
        

    def generate_keypair(self) -> str:
        nacl_keypair = NaClDSEncoder.NaClDSEncoder()
        #nacl_keypair = json.loads(self.strnacl)
       # print(nacl_keypair)
        nacl_keypair.generate()
        self.public_key = nacl_keypair.public_key
        self.private_key = nacl_keypair.private_key
        self.keypair = nacl_keypair.keypair
        
        
        """
        Generates a new public encryption key using NaClDSEncoder.

        TODO: Complete the generate_keypair method.

        This method should use the NaClDSEncoder module to generate a new keypair and populate
        the public data attributes created in the initializer.

        :return: str    
        """
        return str(self.keypair)

    def import_keypair(self, keypair: str):
        self.keypair = keypair
        self.public_key = keypair[:44]
        self.private_key = keypair[44:]
        
        """
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.

        TODO: Complete the import_keypair method.

        This method should use the keypair parameter to populate the public data attributes created by
        the initializer. 
        
        NOTE: you can determine how to split a keypair by comparing the associated data attributes generated
        by the NaClDSEncoder
        """
        #pass

    """
    TODO: Override the add_post method to encrypt post entries.

    Before a post is added to the profile, it should be encrypted. Remember to take advantage of the
    code that is already written in the parent class.

    NOTE: To call the method you are overriding as it exists in the parent class, you can use the built-in super keyword:
    
    super().add_post(...)
    """
    def add_post(self, post: Post) -> None:
        #print(post)
        #print(self.private_key, self.public_key)
        nacl_keypair = NaClDSEncoder.NaClDSEncoder()
        encpubkey = nacl_keypair.encode_public_key(self.public_key)
        encprivkey = nacl_keypair.encode_private_key(self.private_key)
        #print(encpubkey, encprivkey)
        postmsg = post['entry']
        encbox = Box(encprivkey, encpubkey)
        encodepost = postmsg.encode(encoding = 'UTF-8')
        encpost = encbox.encrypt(encodepost, encoder=nacl.encoding.Base64Encoder)
        decodepost = encpost.decode(encoding = 'UTF-8')
        post.set_entry(decodepost)
        #print(encodepost)
        #print(encpost)
        super().add_post(post)
        

    """
    TODO: Override the get_posts method to decrypt post entries.

    Since posts will be encrypted when the add_post method is used, you will need to ensure they are 
    decrypted before returning them to the calling code.

    :return: Post
    
    NOTE: To call the method you are overriding as it exists in the parent class you can use the built-in super keyword:
    super().get_posts()
    """
    def get_posts(self):
        nacl_keypair = NaClDSEncoder.NaClDSEncoder()
        encpubkey = nacl_keypair.encode_public_key(self.public_key)
        encprivkey = nacl_keypair.encode_private_key(self.private_key)
        encbox = Box(encprivkey, encpubkey)
        posts = super().get_posts()
        postlist = []
        for encp in posts:
            decpost = encbox.decrypt(encp.get_entry(), encoder=nacl.encoding.Base64Encoder)
            decodepost = decpost.decode(encoding = 'UTF-8')
            postlist.append(Post(decodepost))
        #print(postlist)
        return postlist
        #encmsg = self. add_post("hello").encpost
        
        
        
        
    
    """
    TODO: Override the load_profile method to add support for storing a keypair.

    Since the DS Server is now making use of encryption keys rather than username/password attributes, you will 
    need to add support for storing a keypair in a dsu file. The best way to do this is to override the 
    load_profile module and add any new attributes you wish to support.

    NOTE: The Profile class implementation of load_profile contains everything you need to complete this TODO. Just add
    support for your new attributes.
    """
    def load_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self.keypair = obj['keypair']
                self.private_key = obj['private_key']
                self.public_key = obj['public_key']
                for post_obj in obj['_posts']:
                    #print(post_obj)
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuFileError("An error occurred while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")
        
    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        nacl_keypair = NaClDSEncoder.NaClDSEncoder()
        encprivkey = nacl_keypair.encode_private_key(self.private_key)
        encpubkey = nacl_keypair.encode_public_key(public_key)
        encbox = Box(encprivkey, encpubkey)
        encode_entry = entry.encode(encoding = 'UTF-8')
        #print(encode_entry)
        encentry = encbox.encrypt(encode_entry, encoder=nacl.encoding.Base64Encoder)
        #print(encentry)
        return encentry
        """
        Used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.

        TODO: Complete the encrypt_entry method.

        NOTE: A good design approach might be to create private encrypt and decrypt methods that your add_post, 
        get_posts and this method can call.
        
        :return: bytes 
        """
if __name__ == '__main__':
    hello = NaClProfile()
    print(hello.keypair)
    #hello.load_profile("/Users/virajvijaywargiya/Desktop/ICS 32 Assignments/A3/hello.dsu")
    hello.encrypt_entry("hello", hello.public_key)
    #print(hello.get_posts())
    #print(hello.keypair)
    #print(hello.public_key)
    #print(hello.private_key)
    #print(hello.import_keypair(hello.keypair))

    
