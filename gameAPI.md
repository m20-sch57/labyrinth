###Класс лабиринт

#####аргументы:

	field
	user_id_list
	send_msg_function

#####методы:

	make_turn(turn)

turn - ход сделанный игроком. должным быть элементом множества доступных ходов 

	get_active_player_user_id() 
	get_active_player_ats() 

ats - available turns set - множество доступных ходов  

	add_player(user_id)
	start_game()
 

###Локации, предметы

<!-- новая локация/предмет должна быть унаследованна от класса `LabirinthObject` -->

логику поведения предмета или локации определяет метод main. он вызывается на каждом ходу  
можно использовать `self.<вставить_что-то_из_следующего_списка>`

	get_parent_id()
	get_object_id()
	set_parent_id(parent_id)
	set_object_id(object_id)
	field.object_with_id(object_id)
	field.up(object_id) и другие
	labyrinth.get_active_player_id()
	labyrinth.set_active_player(object_id)
	labyrinth.send_msg(msg, user_id)

###`new_at`
испульзуйте декоратор `new_at` (new available turn) чтобы создать действие доступное игроку

#####аргументы:

	-condition_function 
должент быть функцией возвращающей True или False в зависимости от того  
должно соответствующее действие быть доступным игроку или нет

	-turn_name имя команды, которое должен ввести игрок, чтобы выполнить это действие


#####пример:

```
@self.new_at(condition_function = lambda: self.parent_id == self.active_player.parent_id,
	    turn_name = 'Поднять предмет')
def rise(self):
	self.parent_id = self.active_player.object_id	
```
