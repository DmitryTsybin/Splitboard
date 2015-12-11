class Person(object):
    def __init__(self, name):
        self.name = name


class Event(object):
    def __init__(self, pays, share, description = ''):
        self.pays = pays
        self.share = share
        self.description = description


class EventsGroup(object):
    def __init__(self, persons):
        self.events = []
        self.persons = persons
        self.total_amount = 0
        self.payments = {}
        self.credits = {}
        self.results = {}

        for person in self.persons:
            self.payments[person.name] = 0
            self.credits[person.name] = 0
            self.results[person.name] = 0

    def add_event(self, event):
        self.events.append(event)

    def calculate_results(self):

        for event in self.events:
            for pay in event.pays:
                self.total_amount += event.pays[pay]
                self.payments[pay] += event.pays[pay]

            for person in event.share:
                self.credits[person] += event.share[person]

        for person in self.persons:
            self.results[person.name] = self.payments[person.name] - self.credits[person.name]

        return {'total_amount': self.total_amount,
                'payments': self.payments,
                'credits': self.credits,
                'results': self.results
                }


class FileReader(object):
    pass


igor = Person('igor')
den = Person('den')
masha = Person('masha')
dima = Person('dima')

sheregesh = EventsGroup((den, igor, masha, dima))
sheregesh.add_event(Event([(dima, 12000), (igor, 2000)], [dima, igor, masha]))
sheregesh.add_event(Event([(dima, 3500)], [dima, igor, masha]))
sheregesh.add_event(Event([(dima, 2471.25)], [dima, igor, masha]))
sheregesh.add_event(Event([(dima, 900)], [dima, igor, masha]))
sheregesh.add_event(Event([(dima, 400)], [dima, igor, masha, den]))
sheregesh.add_event(Event([(dima, 3066.35)], [dima, igor, masha]))
sheregesh.add_event(Event([(dima, 200)], [dima, igor, masha, den]))
sheregesh.add_event(Event([(dima, 100)], [dima, igor, masha]))
sheregesh.add_event(Event([(igor, 1400)], [dima, igor, masha, den]))
sheregesh.add_event(Event([(igor, 400)], [dima, igor, masha, den]))
sheregesh.add_event(Event([(igor, 200)], [dima, igor, masha, den]))
sheregesh.add_event(Event([(igor, 2360)], [dima, igor, masha, den]))
sheregesh.add_event(Event([(igor, 2080)], [(dima, 720), (igor, 680), (masha, 680)]))
sheregesh.add_event(Event([(igor, 400)], [dima, igor, masha, den]))
sheregesh.add_event(Event([(igor, 215)], [dima, igor, masha]))
sheregesh.add_event(Event([(igor, 400)], [dima, igor, masha, den]))
sheregesh.add_event(Event([(igor, 570)], [dima, 570]))
sheregesh.add_event(Event([(igor, 982)], [dima, igor, masha]))
sheregesh.add_event(Event([(masha, 2380)], [(dima, 800), (igor, 790), (masha, 790)]))
#sheregesh.add_event( , , {'dima': , 'igor': , 'masha': , 'den': })

sheregesh_results = sheregesh.calculate_results()

print "Total amount: %f" % sheregesh_results['total_amount']

print "\nPayments:"
for payment in sheregesh_results['payments']:
    print "%s: %f" % (payment, sheregesh_results['payments'][payment])

print "\nCredits:"
for credit in sheregesh_results['credits']:
    print "%s: %f" % (credit, sheregesh_results['credits'][credit])

print "\nTotal results:"
for result in sheregesh_results['results']:
    print "%s: %f" % (result, sheregesh_results['results'][result])
