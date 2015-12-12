from models import Person
from models import Event
from models import EventsGroup
from models import extend_event


class FileReader(object):
    pass


igor = Person('Igor')
den = Person('Den')
masha = Person('Masha', None, igor)
dima = Person('Dima')

sheregesh = EventsGroup([den, igor, masha, dima])
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
sheregesh.add_event(Event([(igor, 570)], [(dima, 570)]))
sheregesh.add_event(Event([(igor, 982)], [dima, igor, masha]))
sheregesh.add_event(Event([(masha, 2380)], [(dima, 800), (igor, 790), (masha, 790)]))
#sheregesh.add_event( , , {'dima': , 'igor': , 'masha': , 'den': })


# Test for add new user during the process
# test_user = Person('Test user')
# sheregesh.add_person(test_user)
# sheregesh.add_event(Event([(masha, 2380)], [(dima, 800), (igor, 790), (test_user, 790)]))


sheregesh.events = map(extend_event, sheregesh.events)
sheregesh_results = sheregesh.calculate_results()


print "Total amount: %.2f" % sheregesh_results['total_amount']

print "\nPayments:"
for payment in sheregesh_results['payments']:
    print "%s: %.2f" % (payment.name, sheregesh_results['payments'][payment])

print "\nCredits:"
for credit in sheregesh_results['credits']:
    print "%s: %.2f" % (credit.name, sheregesh_results['credits'][credit])

print "\nTotal results:"
for result in sheregesh_results['results']:
    print "%s: %.2f" % (result.name, sheregesh_results['results'][result])