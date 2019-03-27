from database import Database, drop_db

drop_db()
db = Database()

print(db.users.number_of_users())
print()

print(db.users.get_by_name('lol'))
print(db.users.get_by_id(0))
print()

print(db.users.add('kek', '123456789'))
print(db.users.get_by_name('kek'))
print(db.users.get_by_id(0))
print(db.users.get_by_id(0).avatar)
print()

print(db.users.add('kek', '123'))
print(db.users.add('kek mek', '123'))           # checking username
print(db.users.add('kekos', '123 456 %^&$'))     # checking password
print()

print(db.users.add('cheburek', '987654321'))
print(db.users.add('None', '123'))
print()

print(db.users.check_password(' 123', 'None'))
print(db.users.check_password('123', 'None'))
# print(db.users.check_password('123', 'Nones'))
print()

print(db.users.set_password('qwerty1', 'cheburek'))
print(db.users.check_password('qwerty1', 'cheburek'))
print(db.users.set_password('qwerty1', 'chebureks'))
print()

print(db.users.get_avatar('kek'))
print(db.users.get_by_name('kek').avatar)
print(db.users.set_avatar('', 'kek'))
print(db.users.set_avatar('data:image/png;base64,', 'kek'))
print(db.users.set_avatar('data:image/png;base64,', 'keks'))
print()

print(db.users.number_of_users())
print()

print(db.rooms.get(1))
print(db.rooms.add('1', 'keks'))
print(db.rooms.add('1', 'kek'))
# print(db.rooms.add('1', 'kek'))
print(db.rooms.get(1))
print(db.rooms.delete(1))
print(db.rooms.get(1))
print()

print(db.rooms.add('20', 'kek'))
print(db.rooms.add('30', 'cheburek'))
print(db.rooms.add('40', 'None'))
print(db.rooms.add('41', 'None'))
print(db.rooms.add('42', 'None'))
print(db.rooms.add('43', 'None'))
print(db.rooms.add('44', 'None'))
print(db.rooms.add('45', 'None'))
print()


print(db.rooms.page_by_page(2))
print()

print(db.rooms.get(20))
print(db.rooms.get(20).description)
print(db.rooms.set_description(20, 'AAAA'))
print(db.rooms.get(20).description)
print(db.rooms.get(20).name)
print(db.rooms.set_name(20, 'AAAA'))
print(db.rooms.get(20).name)
print()

print(db.rooms.get(20).users)
print(db.rooms.add_user(20, 'lol'))
print(db.rooms.add_user(20, 'kek'))
print(db.rooms.add_user(20, 'cheburek'))
print(db.rooms.get(20).users)
print(db.rooms.remove_user(20, 'None'))
print(db.rooms.remove_user(20, 'kek'))
print(db.rooms.get(20).users)
