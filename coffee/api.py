""" A JSON HTTP API for brewing virtual coffee (and maybe tea).
"""

import time

from flask import Flask, jsonify, abort, render_template

app = Flask(__name__)


def time_ms():
    return time.time() * 1000.0


class KitchenError(Exception):
    """ Raised when there is an error in the kitchen.
    """


class Brewable(object):
    """ Something that is brewing in a queue.
    """

    WAITING = "waiting"
    BREWING = "brewing"
    READY = "ready"

    def __init__(self, beverage, person, subtype=None):
        self.beverage = beverage
        self.person = person
        self.subtype = subtype
        self.created_at = time_ms()
        self.brewing_at = None
        self.ready_at = None

    def set_times(self, brewing_at, ready_at):
        self.brewing_at = brewing_at
        self.ready_at = ready_at

    @property
    def status(self):
        now = time_ms()
        if now > self.ready_at:
            return self.READY
        elif now > self.brewing_at:
            return self.BREWING
        else:
            return self.WAITING

    @property
    def ready(self):
        return self.status == self.READY

    @classmethod
    def from_dict(cls, data):
        beverage = data.get("beverage")
        if not isinstance(beverage, unicode):
            raise KitchenError("Invalid beverage %r" % (beverage,))
        person = data.get("person")
        if not isinstance(person, unicode):
            raise KitchenError("Invalid person %r" % (person,))
        subtype = data.get("subtype", None)
        if not (isinstance(subtype, unicode) or subtype is None):
            raise KitchenError("Invalid subtype %s" % (subtype,))
        return cls(beverage, person)

    def to_dict(self):
        return {
            "beverage": self.beverage,
            "person": self.person,
            "status": self.status,
            "subtype": self.subtype,
        }


class Kitchen(object):
    """ A virtual kitchen.
    """

    BREWING_TIME_MS = {
        "coffee": 30 * 1000.0,
        "tea": 60 * 1000.0,
    }

    def __init__(self):
        self._queues = {}
        for beverage in self.beverages:
            self._queues[beverage] = []

    @property
    def beverages(self):
        return sorted(self.BREWING_TIME_MS.keys())

    def beverage_queue(self, beverage):
        queue = self._queues.get(beverage)
        if queue is None:
            raise KitchenError("Unknown beverage %r" % (beverage,))
        return queue

    def brewables(self, person):
        brewables = []
        for queue in self._queues.itervalues():
            items = [b for b in queue if b.person == person]
            for b in items:
                if b.ready:
                    queue.remove(b)
            brewables.extend(items)
        brewables.sort(key=lambda b: b.ready_at)
        return brewables

    def brew(self, data):
        brewable = Brewable.from_dict(data)
        queue = self.beverage_queue(brewable.beverage)
        brewing_at = time_ms()
        if queue and queue[-1].ready_at > brewing_at:
            brewing_at = queue[-1].ready_at
        ready_at = brewing_at + self.BREWING_TIME_MS[brewable.beverage]
        brewable.set_times(brewing_at, ready_at)
        queue.append(brewable)
        return brewable


@app.route('/')
def index():
    return render_template(
        "index.html",
        title="Coffee API v1.0",
        kitchen=kitchen,
    )


@app.route('/api/v1/person/<person>/brew/<beverage>', methods=['POST'])
def api_v1_brew(person, beverage, subtype=None):
    data = request.get_json(silent=True)
    data = data if data is not None else None
    try:
        brewable = kitchen.brew({
            "person": person,
            "beverage": beverage,
            "subtype": data.get("subtype", None),
        })
    except KitchenError:
        abort(400)
    return jsonify(brew=brewable.to_dict()), 201


@app.route('/api/v1/person/<person>/status', methods=['GET'])
def api_v1_status(person):
    brewables = kitchen.brewables(person)
    return jsonify(brews=[brewable.to_dict() for brewable in brewables]), 200


kitchen = Kitchen()
