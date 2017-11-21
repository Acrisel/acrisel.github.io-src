:title: Python Ordered Class
:slug: python-ordered-class
:date: 2017-08-12 23:01:44
:athuors: Arnon Sela
:tags: Python, Metadata, Class, Ordered, Trick, Tip

-----------------------------------
Maintain Ordered of Fields in Class
-----------------------------------

Introduction
============

We saw many questions on the WEB regarding having Python class maintain order of its fields.  Reason being that __dict__ is dict, therefore, class doesn't register the order of the fields presented to it.

We decided to share our version of such a class.

We use OrderedClass were we need to maintain record like structure.  Such that when we package the record, it always packages the fields in the same order.

It is also useful when comparing fields between objects.  Having fields being printed out in the same order is very useful.

Keep in mind that without using OrderedDict, object __dict__ will print in order.  However, Python does not guarantee that order.  When using OrderedDict instead, order is guaranteed.

OrderedClass
============

Using metaclass features of Python we can simply override __prepare__ returning OrderedDict object.

    .. code-block:: python

        from collections import OrderedDict

        class OrderedClassMeta(type):
            @classmethod
            def __prepare__(cls, name, bases, **kwds):
                return OrderedDict()

        class OrderedClass(metaclass=OrderedClassMeta):
            pass

Example use
===========

To use, we just inherent from OrderedClass instead of object.

    .. code-block:: python

        class A(OrderedClass):
            def __init__(self):
                self.b=1
                self.a=2

        class B(OrderedClass):
            def __init__(self):
                self.a=1
                self.b=2

Examine Output
==============

Printing the dictionaries of the above examples.

    .. code-block:: python

        a=A()
        print(a.__dict__)
        b=B()
        print(b.__dict__)

    .. code-block:: python

        {'b': 1, 'a': 2}
        {'a': 1, 'b': 2}

References
==========

Python `PEP 520`__

.. _pep_520: http://legacy.python.org/dev/peps/pep-0520/
__ pep_520_

| Give us your feedback: support@acrisel.com
| Visit us at our home_

.. _home: http://www.acrisel.com
