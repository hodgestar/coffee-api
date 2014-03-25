An HTTP API for brewing virtual coffee (and maybe tea).

API documentation
=================

See current queues at http://powerful-sierra-2165.herokuapp.com/.

Schedule coffee to be brewed using::

  $ curl -d "" http://powerful-sierra-2165.herokuapp.com/api/v1/person/simon/brew/coffee
  {
    "brew": {
      "beverage": "coffee",
      "person": "simon",
      "status": "brewing"
    }
  }

The person's name may be any unicode string. The beverage may be either ``coffee`` or ``tea``.

Retrieve the status of your beverages using::

  $ curl http://powerful-sierra-2165.herokuapp.com/api/v1/person/simon/status
  {
    "brews": [
      {
        "beverage": "coffee",
        "person": "simon",
        "status": "brewing"
      }
    ]
  }

Once a beverage is ready it'll disappear from the queue.
