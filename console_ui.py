# -*- coding: utf-8 -*-

from models import Person
from models import Event
from models import EventsGroup
from models import combine_events
from models import combine_payments


class FileReader(object):
    pass


def total(event_group):
    '''
    :param event_group:
    :return: combined event from all events from event_group
    '''
    return reduce(combine_events, event_group.events, Event([], []))


def combine_event_groups(group1, group2):
    print group1.persons + group2.persons
    print group1.events + group2.events
    return EventsGroup(group1.persons + group2.persons, group1.events + group2.events, "%s and %s" % (group1.name, group2.name))


def report(event_group):
    def who_pay(x):
        return x[0].who_pay or x[0]

    def print_table(table):
        for row in table:
            print "%s: %.2f" % (row[0].name, row[1])

    results = total(event_group)

    print
    print "************ Results for %s ************" % event_group.name
    print "Total amount payed: %.2f" % sum(map(lambda(x): x[1], results.pays))
    print "Total amount spent: %.2f" % sum(map(lambda(x): x[1], results.share))

    print "\nPayments:"
    print_table(results.pays)

    print "\nCredits:"
    print_table(results.share)


    balances = combine_payments(results.pays, results.share)
    print "\nTotal results:"
    print_table(balances)

    aggregate_balances = combine_payments(balances, [], who_pay)
    print "\nTotal results with aggregates:"
    print_table(aggregate_balances)


igor = Person('Igor')
den = Person('Den')
masha = Person('Masha', None, igor)
dima = Person('Dima')
anton = Person('Anton')
slava = Person('Slava')
andrey = Person('Andrey')

###################### Sheregesh ######################

sheregesh = EventsGroup([den, igor, masha, dima], [], 'Sheregesh')
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


###################### Mamay ######################

mamay = EventsGroup([igor, masha, dima, anton, slava, andrey], [], 'Mamay')
mamay.add_event(Event([(dima, 860)], [igor], 'Дима заплатил за еду Игоря'))
mamay.add_event(Event([(dima, 1900)], [igor, dima, anton, andrey, masha], 'Рыба в баню'))
mamay.add_event(Event([(dima, 750)], [igor, dima, anton, andrey, masha], 'Пиво в баню'))
mamay.add_event(Event([(anton, 500)], [igor, dima, anton, andrey, masha], 'Пиво и рыба в баню'))
mamay.add_event(Event([(dima, 1000)], [igor], 'Дима дал Игорю 1000р на карманные расходы'))
mamay.add_event(Event([(slava, 6000)], [igor, dima, andrey, masha], 'Слава заплатил за наше жильё'))


###################### Printing reports ######################
report(sheregesh)
report(mamay)
report(combine_event_groups(sheregesh, mamay))