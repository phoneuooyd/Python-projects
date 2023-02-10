from menu import Menu,ListCals, ExitCommand, AddNewEvent, ExportToiCal

'''
Menu programu Kalendarz. Funkcja main wykorzystuje metody klasy Menu aby dodać poszczególne pozycje do listy menu w pliku menu.py
'''
def main():

    menu = Menu()

    menu.register(ListCals())
    menu.register(AddNewEvent())
    menu.register(ExportToiCal())
    menu.register(ExitCommand(menu))

    menu.run()

    
if __name__ == "__main__":
    main()
    