# -*- coding: utf-8 -*-

from models import Person, Event, EventsGroup
from models import combine_payments, combine_event_groups, total, who_pay
from models import calc_transactions


class FileReader(object):
    pass


def report(event_group):
    def print_table(table):
        for row in table:
            print "%s: %.2f" % (row[0].name, row[1])

    results = total(event_group)

    print
    print "************ Results for %s ************" % event_group.name
    print "Total amount payed: %.2f" % sum(map(lambda(x): x[1], results.payments))
    print "Total amount spent: %.2f" % sum(map(lambda(x): x[1], results.shares))

    print "\nPayments:"
    print_table(results.payments)

    print "\nCredits:"
    print_table(results.shares)


    balances = combine_payments(results.payments, results.shares)
    print "\nTotal results:"
    print_table(balances)

    aggregate_balances = combine_payments(balances, [], who_pay)
    print "\nTotal results with aggregates:"
    print_table(aggregate_balances)

    distribution = calc_transactions(aggregate_balances)
    print "\nWho pays whom:"
    for payment in distribution:
        print "%s pays %.2f to %s" % (payment[0].name, payment[2], payment[1].name)


###################### Define persons ######################
igor = Person('Igor')
den = Person('Den')
masha = Person('Masha', who_pay=igor)
dima = Person('Dima')
anton = Person('Anton')
slava = Person('Slava')
andrey = Person('Andrey')

###################### Sheregesh ######################
sheregesh = EventsGroup([den, igor, masha, dima], [], 'Sheregesh')
sheregesh.add_event(Event([(dima, 12000), (igor, 2000)], [dima, igor, masha], 'Жильё'))
sheregesh.add_event(Event([(dima, 3500)], [dima, igor, masha], 'Дорога в Геш'))
sheregesh.add_event(Event([(dima, 2471.25)], [dima, igor, masha], 'Магазин'))
sheregesh.add_event(Event([(dima, 900)], [dima, igor, masha], 'Магазин'))
sheregesh.add_event(Event([(dima, 400)], [dima, igor, masha, den], 'Такси'))
sheregesh.add_event(Event([(dima, 3066.35)], [dima, igor, masha], 'Еда в поезд'))
sheregesh.add_event(Event([(dima, 200)], [dima, igor, masha, den], 'Такси'))
sheregesh.add_event(Event([(dima, 100)], [dima, igor, masha], 'Лишние 100р за трансфер в Новосиб'))
sheregesh.add_event(Event([(igor, 1400)], [dima, igor, masha, den], 'Кафе'))
sheregesh.add_event(Event([(igor, 400)], [dima, igor, masha, den], 'Такси'))
sheregesh.add_event(Event([(igor, 200)], [dima, igor, masha, den], 'Такси'))
sheregesh.add_event(Event([(igor, 2360)], [dima, igor, masha, den], 'Еда в Плюще'))
sheregesh.add_event(Event([(igor, 2080)], [(dima, 720), (igor, 680), (masha, 680)], 'Еда в Грелке'))
sheregesh.add_event(Event([(igor, 400)], [dima, igor, masha, den], 'Такси'))
sheregesh.add_event(Event([(igor, 215)], [dima, igor, masha], 'Вода в Мария-Ра'))
sheregesh.add_event(Event([(igor, 400)], [dima, igor, masha, den], 'Такси'))
sheregesh.add_event(Event([(igor, 570)], [(dima, 570)], 'Еда в Грелке'))
sheregesh.add_event(Event([(igor, 982)], [dima, igor, masha]))
sheregesh.add_event(Event([(masha, 2380)], [(dima, 800), (igor, 790), (masha, 790)], 'Еда в Юрте'))


###################### Mamay ######################
mamay = EventsGroup([igor, masha, dima, anton, slava, andrey], [], 'Mamay')
mamay.add_event(Event([(dima, 860)], [igor], 'Дима заплатил за еду Игоря'))
mamay.add_event(Event([(dima, 1900)], [igor, dima, anton, andrey, masha], 'Рыба в баню'))
mamay.add_event(Event([(dima, 750)], [igor, dima, anton, andrey, masha], 'Пиво в баню'))
mamay.add_event(Event([(anton, 500)], [igor, dima, anton, andrey, masha], 'Пиво и рыба в баню'))
mamay.add_event(Event([(dima, 1000)], [igor], 'Дима дал Игорю 1000р на карманные расходы'))
mamay.add_event(Event([(slava, 6000)], [igor, dima, andrey, masha], 'Слава заплатил за наше жильё'))
mamay.add_event(Event([(dima, 420)], [anton], 'Билет на аэроэкспресс'))
mamay.add_event(Event([(anton, 550)], [dima], 'Антон перевёл все свои долги'))
mamay.add_event(Event([(igor, 6000)], [slava], 'Игорь перевёл Славе за жильё за себя, Машу, Андрея и Диму'))
mamay.add_event(Event([(igor, 9376.07)], [dima], 'Игорь Диме остаток долгов'))
mamay.add_event(Event([(andrey, 2130)], [dima], 'Андрей Диме остаток долгов'))


###################### Printing reports ######################
report(sheregesh)
report(mamay)
report(combine_event_groups(sheregesh, mamay))
