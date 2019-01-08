### Класс лабиринт

##### аргументы:

	locations
	items
	npcs
	players
листы экземпляров подклассов `LabyrinthObject` (далее сокращенно `LO`)

	adjacence_list
лист словарей вида `{[направление (куда можно пойти): str]: [локация: LO subclass], ...}`<br>

между `adjacence_list` и `locations` установленно соотношение:
i-ый словарь в `adjacence_list` соответствует i-ой локации в `locations`

(!) длины `adjacence_list` и `locations` должны совпадать

##### методы:

	make_turn(turn: str)

turn должным быть элементом множества доступных ходов 
(далее `ats` Available Turns Set)

	get_active_player_username()
	get_active_player_ats() 
 
### Локации, предметы

Новая локация/предмет должна быть унаследованна от класса `LabyrinthObject`

Логику поведения предмета или локации определяет метод main.<br>
Этод метод вызывается на каждом ходу  

можно использовать `self.<вставить_что-то_из_следующего_списка>`

	get_parent()
	set_parent(parent: LO subclass)
геттер и сеттер для рожительского объекта

	.type

тип объекта: `'location' or 'item' or 'npc' or 'player'`

	labyrinth.get_active_player()
	labyrinth.get_next_active_player()
	labyrinth.send_msg(msg: str, username: str)

### Новые действия

Используйте метод `new_at` (new available turn) чтобы создать действие доступное игроку

##### аргументы:
	function
Основная функция действия. Вызывается, если игрок совершил это действие

	condition_function 
Функция, возвращающая True или False в зависимости от того, 
должно соответствующее действие быть доступным игроку или нет

	turn_name 
Команда, которую должен ввести игрок, чтобы выполнить это действие


##### пример:

```
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