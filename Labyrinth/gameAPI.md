### Класс лабиринт

##### аргументы:

	field
	send_msg_function

##### методы:

	make_turn(turn)

turn должным быть элементом множества доступных ходов 

	get_active_player_user_id()
	get_active_player_ats() 

ats (available turns set) множество доступных ходов  

	ready()
необходимо вызвать перд началом игры
 

### Локации, предметы

новая локация/предмет должна быть унаследованна от класса `LabirinthObject`

логику поведения предмета или локации определяет метод main. он вызывается на каждом ходу  
можно использовать `self.<вставить_что-то_из_следующего_списка>`

	get_parent_id()
	get_object_id()
	set_parent_id(parent_id)
	set_object_id(object_id)
	field.get_object(object_id)
	field.get_neighbor_location(object_id, direction)
	labyrinth.get_active_player()
	labyrinth.get_next_active_player()
	labyrinth.send_msg(msg, user_id)

испульзуйте функцию `new_at` (new available turn) чтобы создать действие доступное игроку

##### аргументы:
	function
основная функция действия

	condition_function 
должен быть функцией возвращающей True или False в зависимости от того  
должно соответствующее действие быть доступным игроку или нет

	turn_name 
имя команды, которое должен ввести игрок, чтобы выполнить это действие


##### пример:

```
class Legs(LabyrinthObject):
	def __init__(self):
		self.new_at(self.up, condition_function = self.condition, turn_name = UP_TURN)

	def up(self):
		active_player = self.labyrinth.get_active_player()
		active_player.set_parent_id(self.field.get_neighbor_location(active_player.get_parent_id(), 'up'))
```


### Сделать

##### Настройки
Возможность добавить к предметам натройки.
Интеграция настроек в редактор.

##### Расстановка игроков
Придумать систему описания начальной расстановки игроков.

##### Панель состояния
Возможность добавлять игрокам различные свойства.
Интеграция табло в веб интерфейс.

