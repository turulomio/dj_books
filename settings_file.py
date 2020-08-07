from sys import path
path.append("dj_books/reusing/")
from myconfigparser import MyConfigParser
from text_inputs import input_YN,  input_string

print("Hidden settings are going to be generated")
config=MyConfigParser("/etc/dj_books/settings.conf")

ans=input_YN("Do you want to change database settings?")
if ans is True:
    ans = input_string("Add you database server")
    config.set("db", "server", ans)
    ans = input_string("Add you database port")
    config.set("db", "port", ans)
    ans = input_string("Add you database user")
    config.cset("db", "user", ans)
    ans = input_string("Add you database password")
    config.cset("db", "password", ans)

ans=input_YN("Do you want to change smtp mail server settings?")
if ans is True:
    ans = input_string("Add you smtp mail server")
    config.set("smtp", "server", ans)
    ans = input_string("Add you smtp mail port")
    config.set("smtp", "port", ans)
    ans = input_YN("Does your server use tls?")
    config.set("smtp", "tls", ans)
    ans = input_string("Add you smtp mail user")
    config.cset("smtp", "user", ans)
    ans = input_string("Add you smtp mail password")
    config.cset("smtp", "password", ans)


config.save()
