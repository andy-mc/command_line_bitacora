#!/usr/bin/env python

from collections import OrderedDict
from time import sleep
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('diary.db')


class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    '''create the db and tables if they don't exist'''
    db.connect()
    db.create_tables([Entry], safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    '''Show the menu'''
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('({}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def add_entry():
    '''Add an entry.'''
    print('Enter your entry. Press ctrl+d when finished.')
    data = sys.stdin.read().strip()  # exit if ctrl+d

    if data:
        if input('\nSave entry ? [Y/n] ').lower() != 'n':
            Entry.create(content=data)
            print('Saved successfully !!')
            sleep(2)


def view_entries(search_query=None):
    '''View previous entries.'''
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    total = len(entries)
    for idx, entry in enumerate(entries):
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print('=' * len(timestamp))
        print(entry.content)
        print('{}/{}'.format((idx + 1), total))
        print('\n' + '-' * len(timestamp))
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input('Action: [Ndq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            deleted = delete_entry(entry)
            if deleted:
                break


def search_entries():
    '''Search entries for a query.'''
    view_entries(input('Seach query: '))


def delete_entry(entry):
    '''Delete an entry.'''
    if input('Are you sure ? [yN] ').lower() == 'y':
        entry.delete_instance()
        print('Entry deleted!!')
        sleep(2)
        return True


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
])

if __name__ == '__main__':
    initialize()
    menu_loop()
