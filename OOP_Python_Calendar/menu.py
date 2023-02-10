import re
from calendar import ListingStrategy, list_calendar, GlobalCalendar
'''

'''
class Menu:
    def __init__(self):
        '''
        metoda init dla szkieletu menu, za pomocą tej metody menu działa w pętli, a polecenia są przechowywane w liście
        '''
        self._commands = []
        self._should_run = True

    def register(self, command):
        '''
        metoda rejetrująca polecenia z podklas
        '''
        self._commands.append(command)

    def run(self):
        '''
        metoda uruchamiająca menu, sprawdza wartości na wejściu i zwraca odpowiedni komunikat gdy wartosc jest bledna
        '''
        while self._should_run:
            try:
                print(" Menu\n======")
                for i, cmd in enumerate(self._commands):
                    print("{}. {}".format(i + 1, cmd.description()))

                print('Select menu item 1 - '+ str(len(self._commands)))

                wybor = int(input("Choise: "))
                if (wybor) < 1 or (wybor) >= len(self._commands) + 1:
                    print("Unknown option")
                else:
                    self._commands[wybor - 1].execute()
            except ValueError:
                print('Given value is not a number!')
                print(wybor)
            except:
                print('Error! Going back to menu')

		
    def stop(self):
        '''
        metoda stop, zatrzymuje dzialanie programu
        '''
        self._should_run = False

class MenuCommand:
    def execute(self):
        raise NotImplementedError("you should implement this method in subclass")

    def description(self):
        raise NotImplementedError("you should implement this method in subclass")

class ListCals(MenuCommand):
    '''
        metoda wyswietlajaca wszystkie przechowywane w programie kalendarze
        '''
    def __init__(self) -> None:
        self.listing_strtegy = ListingStrategy()

    def execute(self):
        list_calendar(GlobalCalendar, self.listing_strtegy)  

    def description(self):
        return "List calendars"

class AddNewEvent(MenuCommand):
    '''
        Klasa dodająca kalendarz do globalnej listy. Metoda posiada execute mechanizm sprawdzający poprawność danych za pomocą regex oraz instrukcji warunkowych
        '''
    def __init__(self) -> None:
        self.listing_strtegy = ListingStrategy()
        self._takeValues = True
    def execute(self):
        pattern_Title = "[a-zA-Z0-9]|[\s]|[\.]|[\,]|[\-]"
        pattern_Date = "^([0-3][0-9]+[\.]+[0-1][0-9]+[\.]+[0-9][0-9][0-9][0-9])"
        pattern_Time = '^((2[0-3]|[01][1-9]|10|00):([0-5][0-9]|00))$'
        
        while self._takeValues:
            self.title = str(input('Title: '))
            if(re.search(pattern_Title, self.title)):
                pass
            else:
                print('Given title is not right! Try again.')
                break 
            self.date = str(input('Date: (DD.MM.YYYY) '))
            if(re.search(pattern_Date, self.date)):
                pass
            else:
                print('Given date is not right! Try again.')
                break
            self.time = str(input('Time: (HH:MM) '))
            if(re.search(pattern_Time, self.time)):
                pass
            else:
                print('Given time is not right! Try again.')
                break
            break
        self.listing_strtegy.event(self.title, self.date, self.time)
    def description(self):
        return 'Add new event'

class ExportToiCal(MenuCommand):
    '''
        Klasa exportujaca kalendarz do formau .ics
        metoda execute wykorzystuje zmienne tymczasowe do konwersji danych do porządanego formatu za pomocą funkcji split()
        tutaj tez jest zaimplementowane sprawdzanie poprawnosci danych wejsciowych 
        po wykonaniu metody, w folderze w którym znajduję się pliki programu zostanie utworzony plik calendar.ics gotowy do uzycia
    '''
    def __init__(self) -> None:
        self.listing_strtegy = ListingStrategy()
        self._shouldParse = True
    def execute(self):
        self._Calendar = GlobalCalendar
        self._vCalendar = []
        self._beginEvent = ""
        self.title = ""
        i = 1
        for item in self._Calendar:
            print("%s. %s"%(i, item['title'])) 
            i+=1
        if(len(self._Calendar) == 0):
            print('No calendars for export! Add a new one.')
        else:
            wybor = int(input('Choose the number you want to export (1 - '+ str(len(self._Calendar))+')? '))
            try:
                if(wybor) < 1 or (wybor) > len(self._Calendar):
                    print('No calendar is matching the given number!')
                else:
                    temp = self._Calendar[wybor-1].values()
                    parser = []
                    for i in temp:
                        parser.append(i)
                    self.title = parser[0]
                    del parser[0]
                    dateCov = parser[0].split('.')
                    timeCov = parser[1].split(':')
                    self._beginEvent = str(dateCov[2]+dateCov[1]+dateCov[0]+"T"+timeCov[0]+timeCov[1]+"00")
                    self._calDict = {
                        'DTSTART' : self._beginEvent,
                        'DTEND' : self._beginEvent,
                        'SUMMARY' : self.title,
                    }
                    with open("calendar.ics", 'w') as f: 
                        f.write('BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VTIMEZONE\nTZID:Europe/Warsaw\nX-LIC-LOCATION:Europe/Warsaw\nEND:VTIMEZONE\nBEGIN:VEVENT\n')
                        for key, value in self._calDict.items(): 
                            f.write('%s:%s\n' % (key, value))
                        f.write('END:VEVENT\nEND:VCALENDAR')
            except ValueError:
                print('Given value is not a number!')
            except:
                print('An error has occured')
        print('Operation done! Check the directory for calendar.ics!')

    def description(self):
        return 'Export calendar to iCal'


class ExitCommand(MenuCommand):
    '''
    Klasa zawierająca metody które umożliwiają wyłączenie programu
    '''
    def __init__(self, menu):
        self._menu = menu

    def execute(self):
        self._menu.stop()
        print('Goodbye')

    def description(self):
        return "Exit"  