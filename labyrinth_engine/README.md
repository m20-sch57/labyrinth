### Класс лабиринт

##### аргументы:

	locations
	items
	npcs
	players
листы экземпляров подклассов `LabyrinthObject` (далее сокращенно `LO`)

	adjacence_list

лист словарей вида `{[направление (куда можно пойти): str]: [локация: LO subclass with type 'location'], ...}`<br>

между `adjacence_list` и `locations` установленно соотношение:<br>
`i`-ый словарь в `adjacence_list` соответствует `i`-ой локации в `locations`

**(!)** длины `adjacence_list` и `locations` должны совпадать

##### методы:

	make_turn(turn: str)

turn должным быть элементом множества доступных ходов 
(далее `ats` Available Turns Set)

	get_active_player_username()
	get_active_player_ats() 
 
### Локации, предметы

Новая локация/предмет должна быть унаследована от класса `LabyrinthObject`

Логику поведения предмета или локации определяет метод `main`.<br>
Это метод вызывается на каждом ходу  

можно использовать `self.<вставить_что-то_из_следующего_списка>`

	get_parent()
	set_parent(parent: LO subclass)

геттер и сеттер для родительского объекта

	get_neighbour(direction: str)
	set_neighbour(direction: str, neighbour: LO subclass with type 'location')

геттер и сеттер для соседей по направлению `'direction'`

	get_children(labtype: str or list of str, and_key: function, or_key: function)
Возвращает всех детей объекта удовлетворяющих `or_key`<br>
и всех детей типа из `labtype` удовлетворяющих условию `and_key`

	.type

тип объекта: `'location'` or `'item'` or `'npc'` or `'player'`

	get_msgs(username: str)

получение всех сообщений отправленных игроку с ником (именем) `username`

	get_turns(number: int, username: str)

Возвращает все ходы сделанные игроками <br>
Возвращает ходы сделанные только указанными игроками, если указан параметр `username` <br>
Возвращает ход под номером `number` с конца, если указан параметр `number` <br>
Например `get_turns(1, 'Вася')` вернёт последний ход Васи

	labyrinth.get_objects(labtype: str or list of str, and_key: function, or_key: function)
Работает аналогично `get_children` за исключением того, что возвращает не детей, а все объекты

	labyrinth.get_all_objects()
Равносильно вызову `get_objects` без параметров

	labyrinth.get_active_player()
	labyrinth.get_next_active_player()
	labyrinth.send_msg(msg: str, username: str)

### Новые действия

Используйте метод `new_at` (new available turn) чтобы создать действие доступное игроку

##### аргументы:
	function
Основная функция действия. Вызывается, если игрок совершил это действие

	condition_function 
Функция, возвращающая `True` или `False` в зависимости от того, 
должно соответствующее действие быть доступным игроку или нет

	turn_name 
Команда, которую должен ввести игрок, чтобы выполнить это действие

##### пример:

```python
class Legs(LabyrinthObject):
    def __init__(self):
        self.new_at(self.turn_move('up'), condition_function=self.condition, turn_name=UP_TURN)

    def turn_move(self):
        active_player = self.labyrinth.get_active_player()
        next_position = active_player.get_parent().get_neighbour('up')
        if type(next_position) is Wall:
            self.labyrinth.send_msg(WALL_MSG, active_player)
        else:
            active_player.set_parent(next_position)

    def condition(self):
        return True
```

### Сохранение игры
	save(filename: str)
Метод класса `Labyrinth`. Сохраняет игру в файл `filename`

	load_lrsave(filename: str)
Функция. Загружает игру из файла `filename` и возвращает объект класса `Labyrinth`<br>

	load_lrmap(filename: str, users: list of str)
Функция. Возвращает объект лабиринта с картой из файла `filename` и с игроками `users`
