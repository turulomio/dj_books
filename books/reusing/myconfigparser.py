from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from casts import str2bool, string2list_of_integers, string2list_of_strings, list2string
from datetime_functions import string2dtnaive
from base64 import b64encode, b64decode
from configparser import ConfigParser
from datetime import datetime
from decimal import Decimal
from logging import debug
from os import path, makedirs


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * bytes(chr(BS - len(s) % BS).encode("utf8") )
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESCipher:
       def __init__( self, key ):
           self.key = key

       ## @param raw bytes
       def encrypt( self, raw ):
           raw = pad(raw)
           iv = Random.new().read( AES.block_size )
           cipher = AES.new( self.key, AES.MODE_CBC, iv )
           return b64encode( iv + cipher.encrypt( raw ) ) 

       ## @param enc bytes
       def decrypt( self, enc ):
           enc = b64decode(enc)
           iv = enc[:16]
           cipher = AES.new(self.key, AES.MODE_CBC, iv )
           return unpad(cipher.decrypt( enc[16:] ))

class MyConfigParser:
    def __init__(self, filename):
        self.filename=filename
        self.config=ConfigParser()
        if path.exists(self.filename):
            self.config.read(self.filename)
        else:
            print("Configuration file {} doesn't exist".format(self.filename))
        self.__generate_id()
        self.id=self.get("MyConfigParser","id")[:16]

    def cset(self, section, option, value):
        a=AESCipher(self.id.encode("utf8"));
        ci=a.encrypt(value.encode("utf8"))
        self.set(section,option,ci.decode("utf8"))

    def cget(self, section, option, default=None):
        a=AESCipher(self.id.encode("utf8"));
        value=self.get(section,option,default).encode("utf8")
        deci=a.decrypt(value)
        return deci.decode("utf8")

    def get(self, section, option, default=None):
        if self.config.has_option(section, option)==True:
            return self.config.get(section, option)
        else:
            self.set(section, option, default)
            return self.get(section, option)

    def getDecimal(self, section,option, default=None):
        try:
            value=self.get(section, option, default)
            return Decimal(value)
        except:
            debug("I couldn't convert to Decimal {} ({})".format(value, value.__class__))

    def getFloat(self, section,option, default=None):
        try:
            value=self.get(section, option, default)
            return float(value)
        except:
            debug("I couldn't convert to float {} ({})".format(value, value.__class__))

    def getInteger(self, section,option, default=None):
        try:
            value=self.get(section, option, default)
            return int(value)
        except:
            debug("I couldn't convert to int {} ({})".format(value, value.__class__))

    def getBoolean(self, section,option, default=None):
        try:
            value=self.get(section, option, default)
            return str2bool(value)
        except:
            debug("I couldn't convert to boolean {} ({})".format(value, value.__class__))

    ## Example: self.value_datetime_naive("Version", "197001010000", "%Y%m%d%H%M")
    def getDatetimeNaive(self, section, option, default=None, format="%Y%m%d%H%M"):
        try:
            value=self.get(section, option, default)
            return string2dtnaive(value, format)
        except:
            debug("I couldn't convert to datetime naive {} ({})".format(value, value.__class__))

    def getList(self, section, option, default):
        try:
            value=self.get(section, option, default)
            return string2list_of_strings(value)
        except:
            debug("I couldn't convert to list of strings {} ({})".format(value, value.__class__))

    def getListOfIntegers(self, section, option, default):
        try:
            value=self.get(section, option, default)
            return string2list_of_integers(value)
        except:
            debug("I couldn't convert to list of integers {} ({})".format(value, value.__class__))

    def set(self, section, option, value):
        if isinstance(value, list):
            value=list2string(value)
        if section not in self.config:
            self.config.add_section(section)
            self.config[section]={}
        self.config.set(section, option, str(value))

    def save(self):
        dirname=path.dirname(self.filename)
        if dirname != "":
            makedirs(dirname, exist_ok=True)
        with open(self.filename, 'w') as f:
            self.config.write(f)

    ## Generate a [MyConfigParser] -> id if it's not created yet
    def __generate_id(self):
        if self.config.has_option("MyConfigParser","id") is False:
            h = SHA256.new()
            h.update(str(datetime.now()).encode("utf8"))
            self.set("MyConfigParser","id", h.hexdigest())

if __name__ == '__main__':
    c=MyConfigParser("prueba.ini")
    c.set("Example", "integer", 12134)
    print ("Getting a integer",  c.getInteger("Example", "integer"))
    print ("Getting a integer con default",  c.getInteger("Example", "integerdefault",  1))
    print ("Getting a decimal",  c.getDecimal("Example", "decimal", 1212))
    print("Getting a list", c.getList("Example", "list", ["hi", "bye"]))
    print("Getting a list of integers", c.getList("Example", "list_integers", [1, 2, 3]))

    c.cset("Example", "cstring", "Mi texto")
    print("Getting a cstring", c.cget("Example", "cstring"))

    c.save()
