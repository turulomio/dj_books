# dj_books Application

## Snapshots

![Snapshot](https://github.com/turulomio/dj_books/blob/master/doc/Screenshot_20200811_000430.png)

## Installation

1. `git clone https://github.com/turulomio/dj_books.git`
1. `python settings_file.py`, to setup your settings.
1. Create database. For example mylibrary. I tested this app with postgres: "createdb -U postgres mylibrary"
1. `python manage.py migrate`
1. `python manage.py createsuperuser`
1. Log into application