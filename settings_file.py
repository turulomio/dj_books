from colorama import Fore, Style
from datetime import timedelta, date, datetime
from logging import error, debug
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from configparser import ConfigParser
from decimal import Decimal
from os import path, makedirs
from gettext import gettext

_=gettext

############### COPIED FROM CASTS OF REUSING ##############


def list2string(lista):
        """Covierte lista a string"""
        if  len(lista)==0:
            return ""
        if str(lista[0].__class__) in ["<class 'int'>", "<class 'float'>"]:
            resultado=""
            for l in lista:
                resultado=resultado+ str(l) + ", "
            return resultado[:-2]
        elif str(lista[0].__class__) in ["<class 'str'>",]:
            resultado=""
            for l in lista:
                resultado=resultado+ "'" + str(l) + "', "
            return resultado[:-2]

## Reverse function of list2string where class is a str
def string2list_of_strings(s):
    arr=[]
    if s!="":
        arrs=s.split(", ")
        for a in arrs:
            arr.append(a[1:-1])
    return arr

def string2list_of_integers(s, separator=", "):
    """Convers a string of integer separated by comma, into a list of integer"""
    arr=[]
    if s!="":
        arrs=s.split(separator)
        for a in arrs:
            arr.append(int(a))
    return arr
    
## Converts strings True or False to boolean
## @param s String
## @return Boolean
def str2bool(value):
    if value=="0" or value.lower()=="false":
        return False
    elif value=="1" or value.lower()=="true":
        return True
#################################
############### COPIED FROM DATETIME_FUNCTIONS OF REUSING ##############


def string2dtnaive(s, format):
    allowed=["%Y%m%d%H%M","%Y-%m-%d %H:%M:%S","%d/%m/%Y %H:%M","%d %m %H:%M %Y","%Y-%m-%d %H:%M:%S.","%H:%M:%S"]
    if format in allowed:
        if format=="%Y%m%d%H%M":
            dat=datetime.strptime( s, format )
            return dat
        if format=="%Y-%m-%d %H:%M:%S":#2017-11-20 23:00:00
            return datetime.strptime( s, format )
        if format=="%d/%m/%Y %H:%M":#20/11/2017 23:00
            return datetime.strptime( s, format )
        if format=="%d %m %H:%M %Y":#27 1 16:54 2017. 1 es el mes convertido con month2int
            return datetime.strptime( s, format)
        if format=="%Y-%m-%d %H:%M:%S.":#2017-11-20 23:00:00.000000  ==>  microsecond. Notice the point in format
            arrPunto=s.split(".")
            s=arrPunto[0]
            micro=int(arrPunto[1])
            dt=datetime.strptime( s, "%Y-%m-%d %H:%M:%S" )
            dt=dt+timedelta(microseconds=micro)
            return dt
        if format=="%H:%M:%S": 
            tod=date.today()
            a=s.split(":")
            return datetime(tod.year, tod.month, tod.day, int(a[0]), int(a[1]), int(a[2]))
    else:
        error("I can't convert this format '{}'. I only support this {}".format(format, allowed))
#################################




############### COPIED FROM MYCONFIG PARSER OF REUSING ##############


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









#################################

############### COPIED FROM INPUT_TEXTS OF REUSING ##############

def input_string(text,default=None):
    while True:
        if default==None:
            res=input(Style.BRIGHT+text+": ")
        else:
            print(Style.BRIGHT+ Fore.WHITE+"{} [{}]: ".format(text, Fore.GREEN+str(default)+Fore.WHITE), end="")
            res=input()
        try:
            if res==None or res=="":
                res=default
            res=str(res)
            return res
        except:
            pass
            
def input_YN(pregunta, default="Y"):
    ansyes=_("Y")
    ansno=_("N")
    
    bracket="{}|{}".format(ansyes.upper(), ansno.lower()) if default.upper()==ansyes else "{}|{}".format(ansyes.lower(), ansno.upper())
    while True:
        print(Style.BRIGHT+ Fore.WHITE+"{} [{}]: ".format(pregunta,  Fore.GREEN+bracket+Fore.WHITE), end="")
        user_input = input().strip().upper()
        if not user_input or user_input=="":
            user_input=default
        if user_input == ansyes:
                return True
        elif user_input == ansno:
                return False
        else:
                print (_("Please enter '{}' or '{}'".format(ansyes, ansno)))

#################################
if __name__ == "__main__":

    print("Hidden settings are going to be generated in /etc/dj_books/settings.conf")
    config=MyConfigParser("/etc/dj_books/settings.conf")

    ans=input_YN("Do you want to change database settings?")
    if ans is True:
        ans = input_string("Add you database server", "127.0.0.1")
        config.set("db", "server", ans)
        ans = input_string("Add you database port", "5432")
        config.set("db", "port", ans)
        ans = input_string("Add you database user", "postgres")
        config.cset("db", "user", ans)
        ans = input_string("Add you database password", "your_pass")
        config.cset("db", "password", ans)

    ans=input_YN("Do you want to change smtp mail server settings?")
    if ans is True:
        ans = input_string("Add you smtp mail server. For example: smtp-mail.outlook.com","your.imapserver.com")
        config.set("smtp", "server", ans)
        ans = input_string("Add you smtp mail port", "25")
        config.set("smtp", "port", ans)
        ans = input_YN("Does your server use tls?", "Y")
        config.set("smtp", "tls", ans)
        ans = input_string("Add you smtp mail user", "your_user")
        config.cset("smtp", "user", ans)
        ans = input_string("Add you smtp mail password", "your_pass")
        config.cset("smtp", "password", ans)


    config.save()
