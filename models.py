class Person(object):
    def __init__(self, name, email = None, who_pay = None):
        self.name = name
        self.email = email
        self.who_pay = who_pay


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
            self.payments[person] = 0
            self.credits[person] = 0
            self.results[person] = 0

    def add_event(self, event):
        self.events.append(event)

    def add_person(self, person):
        self.persons.append(person)
        self.payments[person] = 0
        self.credits[person] = 0
        self.results[person] = 0

    def calculate_results(self):
        for event in self.events:
            for pay in event.pays:
                self.total_amount += pay[1]
                self.payments[pay[0]] += pay[1]

            for elem in event.share:
                self.credits[elem[0]] += elem[-1]

        for person in self.persons:
            if person.who_pay:
                self.results[person.who_pay] += self.payments[person] - self.credits[person]
            else:
                self.results[person] += self.payments[person] - self.credits[person]

        return {'total_amount': self.total_amount,
                'payments': self.payments,
                'credits': self.credits,
                'results': self.results
                }


def extend_event(event):
    result_payment = 0
    result_share = []
    for pay in event.pays:
        result_payment += pay[-1]

    if type(event.share[0]) == Person:
        for elem in event.share:
            result_share.append((elem, float(result_payment) / len(event.share)))
    elif type(event.share[0]) == tuple:
        sum = 0
        for elem in event.share:
            sum += elem[-1]

        if sum == 1:
            result_share.append((elem[0], result_payment * elem[-1]))
        else:
            result_share.append((elem[0], elem[-1]))
    else:
        print "something went wrong. event.share[0]: %r" % event.share[0]
    return Event(event.pays, result_share, event.description)
