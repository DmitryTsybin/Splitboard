class Person(object):
    def __init__(self, name, email = None, who_pay = None):
        self.name = name
        self.email = email
        if not who_pay:
            self.who_pay = self
        else:
            self.who_pay = who_pay

    def __repr__(self):
        return '<Person %r>' % self.name


class Event(object):
    def __init__(self, pays, share, description = ''):
        '''
        :param pays: list of tuples [(person, amount)]
        :param share: list of tuples [(person, amount)]
        :param description: string, description of this event
        '''
        self.pays = pays
        self.share = share
        self.description = description


class EventsGroup(object):
    def __init__(self, persons, name=''):
        self.events = []
        self.persons = persons
        self.name = name

    def add_event(self, event):
        self.events.append(event)

    def add_person(self, person):
        self.persons.append(person)

def extend_event(event):
    if len(event.share) == 0:
        return event

    result_payment = 0
    result_share = []
    for pay in event.pays:
        result_payment += pay[-1]

    if type(event.share[0]) == Person:
        for elem in event.share:
            result_share.append((elem, -float(result_payment) / len(event.share)))
    elif type(event.share[0]) == tuple:
        sum = 0
        for elem in event.share:
            sum += elem[-1]

        for elem in event.share:
            if sum == 1:
                result_share.append((elem[0], -result_payment * elem[-1]))
            else:
                result_share.append((elem[0], -elem[1]))
    else:
        print "something went wrong. event.share[0]: %r" % event.share[0]
    return Event(event.pays, result_share, event.description)


def group_by(p, l):
    def cmp(x, y):
        return p(x) < p(y) and -1 or p(x) > p(y) and 1 or p(x) == p(y) and 0

    l_ = l[:]
    l_.sort(cmp)

    def r(x, y):
        if len(x) and p(x[-1][0]) == p(y):
            return x[:-1] + [x[-1] + [y]]
        else:
            return x + [[y]]
    return reduce(r, l_, [])


def first(x):
    return x[0]


def second(x):
    return x[1]


def sum_amounts(x):
    return (x[0][0], sum(map(second, x)))


def combine_payments(l1, l2, p = first):
    l = l1 + l2
    return map(sum_amounts, group_by(p, l))


def combine_events(event1, event2):
    event2 = extend_event(event2)
    return Event(combine_payments(event1.pays, event2.pays), combine_payments(event1.share, event2.share))
