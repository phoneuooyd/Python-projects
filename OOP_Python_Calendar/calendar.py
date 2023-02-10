from __future__ import print_function
global GlobalCalendar
GlobalCalendar = []

class ListingStrategy:
    '''
        Klasa ListingStrategy jest odpowiedzialna za dodanie danych do globalnego kalendarza w odpowiednim formacie oraz wyświetlenia zdarzeń dodanych do kalendarza
    '''
    def begin(self):
        print('Wyswietlam zdarzenia... \n ')
        [print("Nazwa wydarzenia: %s \n Data wydarzenia: %s, %s\n"%(item['title'],item['date'],item['time'])) for item in GlobalCalendar]

    def event(self, title, date, time):
        self.title = title
        self.date = date
        self.time = time
        
        event = {
            'title' : title,
            'date' : date,
            'time' : time
        }
        GlobalCalendar.append(event)
                
    def end(self):
        print('Koniec wyświetlania...')

def list_calendar(GlobalCalendar, listing_strategy):
    '''
    funkcja wyswietlajaca dane za pomocą strategii ListingStrategy
    '''
    listing_strategy.begin()
    
    listing_strategy.end()
