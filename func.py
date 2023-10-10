import sqlite3
from conf import Connect


def CreateElement(username, textTopic, id_chat_user, chat_id, usernameunical, id_topic_user):
    conn = Connect()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Users (username, textTopic, id_chat_user, id_topic_user, chat_id, usernameunical) VALUES (?, ?, ?, ?, ?, ?)',
        (username, textTopic, id_chat_user, id_topic_user, chat_id, usernameunical))

    conn.commit()
    conn.close()


def GetElement(id_chat_user):
    conn = Connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE id_chat_user = ?', (id_chat_user,))
    results = cursor.fetchall()
    for res in results:
        return res


def GetPhoneElement(username):
    conn = Connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    results = cursor.fetchall()
    for res in results:
        return res


def GetElementChatUser(id_chat_user):
    conn = Connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id_chat_user FROM Users WHERE id_chat_user = ?', (id_chat_user,))
    results = cursor.fetchall()
    for res in results:
        return res


def GetElementChat2User(id_chat_user):
    conn = Connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id_chat_user FROM Users WHERE id_topic_user = ?', (id_chat_user,))
    results = cursor.fetchall()
    for res in results:
        return res


def GetElementIdTopicChat(id_chat_user):
    conn = Connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id_topic_user FROM Users WHERE id_chat_user = ?', (id_chat_user,))
    results = cursor.fetchall()
    for res in results:
        return res


def UpdateElement(id_chat_user, id_topic_user):
    conn = Connect()
    cursor = conn.cursor()
    cursor.execute('UPDATE Users SET id_topic_user = ? WHERE id_chat_user = ?', (id_topic_user, id_chat_user,))
    conn.commit()
    conn.close()
def UpdatePhoneElement(id_chat_user, username):
    conn = Connect()
    cursor = conn.cursor()
    cursor.execute('UPDATE Users SET id_chat_user = ? WHERE username = ?', (id_chat_user, username,))
    conn.commit()
    conn.close()