class Person(object):
    def __init__(self, name, email=None, creditcard=None, who_pay=None):
        self.name = name
        self.email = email
        self.creditcard = creditcard
        if not who_pay:
            self.who_pay = self
        else:
            self.who_pay = who_pay

    def __repr__(self):
        return '<Person %r>' % self.name


class Event(object):
    def __init__(self, payments, shares, description = ''):
        '''
        :param payments: list of tuples [(person, amount)]
        :param shares: list of tuples [(person, amount)]
        :param description: string, description of this event
        '''
        self.payments = payments
        self.shares = shares
        self.description = description


class EventsGroup(object):
    def __init__(self, persons, events = [], name=''):
        self.events = events
        self.persons = persons
        self.name = name

    def add_event(self, event):
        self.events.append(event)

    def add_person(self, person):
        self.persons.append(person)


def extend_event(event):
    '''
    :param event: event in relaxed form
    :return: event in normal form: ( [(payer, amount), ... ], [(consumer, amount), ...] )
    '''
    if len(event.shares) == 0:
        return event

    total_payment = sum(map(second, event.payments))

    if type(event.shares[0]) == Person:
        f  = lambda(x): (x, -float(total_payment) / len(event.shares))
    elif type(event.shares[0]) == tuple:
        if 1 == sum(map(second, event.shares)):
            f = lambda(x): (x[0], -total_payment * x[1])
        else:
            f = lambda(x): (x[0], -x[1])
    else:
        print "something went wrong. event.shares[0]: %r" % event.shares[0]

    return Event(event.payments, map(f, event.shares), event.description)


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
    return Event(combine_payments(event1.payments, event2.payments), combine_payments(event1.shares, event2.shares))


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


def signum(x):
        if x < 0:
            return -1
        else:
            return 1


def compose(f, g):
    return lambda(x): f(g(x))


def calc_transactions(balances):
    (debitors, creditors) = group_by(compose(signum, second), balances)
    return distribute(debitors, creditors)


def who_pay(x):
    return x[0].who_pay or x[0]


def distribute(debitors, creditors):
    def distribute_(result, debitors, creditors):
        if len(debitors) == 0 or len(creditors) == 0:
            return result

        debitor = debitors[0]
        creditor = creditors[0]
        debitors_ = len(debitors) > 1 and debitors[1:] or []
        creditors_ = len(creditors) > 1 and creditors[1:] or []

        debt = creditor[1] + debitor[1]
        left_debitor = []
        left_creditor = []

        if debt < 0:
            transaction = (debitor[0], creditor[0], creditor[1])
            left_debitor = [(debitor[0], debt)]
        elif debt > 0:
            transaction = (debitor[0], creditor[0], debitor[1])
            left_creditor = [(creditor[0], debt)]
        else:
            transaction = (debitor[0], creditor[0], debitor[1])

        return distribute_(
            result + [transaction],
            left_debitor + debitors_,
            left_creditor + creditors_
        )

    return distribute_([], debitors, creditors)
