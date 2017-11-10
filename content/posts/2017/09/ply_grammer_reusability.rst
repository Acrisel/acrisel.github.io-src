:title: Python Lex and Yacc with PLY
:slug: python-lex-yacc-play
:date: 2017-09-01 23:12:44
:authors: Arnon Sela
:tags: Python, Grammer, lex, yacc, ply, domain specific language

-------------------
Grammer Reusability
-------------------

Synopsis
========

In many cases, grammar is used in a singular scope of actions. That is, any sentence in the grammar yields distinct action.
In some cases, we want to produce different outcomes in different compiling passes of the same text. This post focuses on how to use Python/PLY to accomplish just that using the same grammar definitions.

A normal course of action is to duplicate the grammar definitions and change the action associated with its rules. This creates a situation where the grammar needs to be maintained in multiple locations.

The idea of grammar reusability lies in the ability to bind different actionable objects to the same grammar definitions. For that, actions are defined externally to the grammar. Each parser pass will provide PLY with its unique action objects.


Definitions
===========

To remove confusion, let's define some ground definitions.

   | Grammer rule: YACC based rule definition; e.g., add : x '+' rest;
   | Grammer definition: set of grammer rules defining a language

.. _classcalc: https://github.com/dabeaz/ply/tree/master/example/classcalc
.. _PLY: http://www.dabeaz.com/ply
.. _calcaction: https://github.com/Acrisel/references/blob/master/ply_examples/calcact.py


Motivation
==========

We were using PLY_ to write a parser for Cobol.  That was done to analyze code and to produce artifacts that would be used in programming interfaces to Cobol programs.

Very quickly we ran into the need to apply different actions to grammar rules according to the parsing that we needed to do. As usually the case in modern programming practices - namely lazy programming,  developers copy the grammar and change the action associated with rules according to their need.

Then developers run into situations where a grammar rule was found buggy and needed to change.  Now they had to change multiple grammar definition files. This naturally prompt the need to centralize grammar definition and to allow its reusability with different parsing actions.

Design
======

For grammar definitions to be come reusable, the rules needed to be separated from the action they apply. This devises three guiding principles.

1. rules will need to be shaped to call a shared object that would perform their action.
#. each instantiation of parser will include binding of an actionable object.
#. an actionable object will be sensitive to the rule it is called upon.

This discussion will use basic calculator called classcalc_ provided as an example in PLY. We will make changes to this example that will create it as reusable grammar. The complete code can be found in calcaction_.

Actionable Object
-----------------

An actionable object is a callable that defines the actions each grammar rule would perform. For this discussion, the object is scaled down. We will note however some feature that project will most probably want.

General Actionable Object
~~~~~~~~~~~~~~~~~~~~~~~~~

ParserActions_ is a base class defining basic actions for actionable objects. An object is instantiated using an action map (shown in CalcActions_).  It callable method accepts PLY parser object (**p**), and key into action_map (**tag**). *___call__()* uses **tag** to find the proper action. It then applies the action to parser object **p**.

.. _ParserActions:

    .. code-block:: python

        class ParserActions(object):

            def __init__(self, action_map={},):
                self.action_map=action_map

            def __call__(self, p, tag):
                try: action=self.action_map[tag]
                except:
                    try: action=self.action_map['']
                    except: return p
                p[0]=action(p)

Special Actionable Object
~~~~~~~~~~~~~~~~~~~~~~~~~

Specializing parser action is done simply by inheriting from ParserActions_ and providing a map of actions.

CalcActions_ does just that. It defined a mapping between rule tags and actions need to be performed on them.

Action can be a simple lambda function or a more complicated mechanism implemented as a method. Since ParserActions_ uses the return from an action to set the rule return value **p[0]**, methods need to return value to their rule.

.. _CalcActions:

    .. code-block:: python

        class CalcActions(ParserActions):
            def __init__(self,):
                action_map={'statement_assign': self.set_name,
                            'statement_expr': self.print_result,
                            'expression_binop': self.calc_expr,
                            'expression_uminus': lambda p: -p[2],
                            'expression_group': lambda p: p[2],
                            'expression_number': lambda p: p[1],
                            'expression_name': self.exp_name,
                            }
                super().__init__(action_map=action_map)
                self.names=dict()

            def print_result(self, p):
                print(p[1])

            def set_name(self, p):
                self.names[p[1]] = p[3]

            def calc_expr(self, p):
                if   p[2] == '+':    p[0] = p[1] + p[3]
                elif p[2] == '-':  p[0] = p[1] - p[3]
                elif p[2] == '*':  p[0] = p[1] * p[3]
                elif p[2] == '/':  p[0] = p[1] / p[3]
                elif p[2] == '**': p[0] = p[1] ** p[3]
                return p[0]

            def exp_name(self, p):
                try: p[0] = self.names[p[1]]
                except LookupError:
                    print("Undefined name '%s'" % p[1])
                    p[0] = 0
                return p[0]

Grammer Hooks
=============

There are two steps to hook into the grammar.

    1. Pass actionable parser object to a parser.
    #. Let rules call that object to initiate action.

Initiate Parser with Actions
----------------------------

Call to parser will look as follows:

    .. code-block:: python

        rule_action=CalcActions()
        calc = Calc(rule_action=rule_action)

In parser initialization, rule_action is set so it can be used within parser object.

    .. code-block:: python

        self.rule_action=rule_action

Hook Rules
----------

Rules are hooked with actions by calling ParserAction specialized object, in calc case: CalcActions_. The original *p_statement_assign* was defined follows:

    .. code-block:: python

        def p_statement_assign(self, p):
            'statement : NAME EQUALS expression'
            self.names[p[1]] = p[3]

With reusability mechanism, the method will be changed to call an actionable

    .. code-block:: python

        def p_statement_assign(self, p):
            'statement : NAME EQUALS expression'
            self.rule_action(p, 'statement_assign')

Call to **rule_action** passes the parser object and the rule's key to *action_map*.

Change Actions
==============

To change actions, we can define a new actionable object with new action map. This is done without changing the grammar.

For example (CountOpsActions_), if we want to add a count of the number of operations when we print calc result, the following would be done. Create a new actionable class similar to the one before but with a counter *self.count_ops_in_expr=0* initiated to 0.

*calc_expr()* will advance the counter. *print_result* will be changed to print the counter and to rest its value for the next operation.

The complete actionable object will look as follows:

.. _CountOpsActions:

    .. code-block:: python

        class CountOpsActions(CalcActions):
            def __init__(self,):
                super().__init__()
                self.count_ops_in_expr=0

            def print_result(self, p):
                print("result: %s (ops count: %s)" % (p[1], self.count_ops_in_expr))
                self.count_ops_in_expr=0

            def calc_expr(self, p):
                result=super().calc_expr(p)
                self.count_ops_in_expr+=1
                return result

To make this work, we only need to initiate parser with the new actionable object.

    .. code-block:: python

        rule_action=CountOpsActions()
        calc = Calc(rule_action=rule_action)


In a more complicated scenarios, a complete new action can be provided.

Additional Notes
================

In the CalcAct example, only parser object is passed to the action. In a more complex grammar, it may be beneficial to structure action to also receive the tag. In close enough actions, it would be then possible to reuse same code with different actions using the tag as a differentiator.

In the above example, ParserActions_ will initiate action with add **tag**.

    .. code-block:: python

         p[0]=action(p, tag)

Mapping actions will also add **tag** to the call.  For example:

    .. code-block:: python

        'expression_uminus': lambda p, tag: -p[2],

Callable methods will also need to change to accept **tag**.

Some time a default action could also be introduced. In this case, an action with an empty key can be added.

    .. code-block:: python

        '': self.some_default_action,

ParserActions_ as described above already built to accommodate such default action.

Limitation
==========

If a new PLY object is created with new action map, it affects previously instantiated objects.

Therefore, to work with multiple parser action sets in the same program, you have to re-initiate the parser each time action set is changed.


Conclusion
==========

It is possible to override parser rules by inheriting from class rules and overriding rules of interest. Doing so still, results with replication of rules.

The method shown here allows complete isolation of grammar rules from their actions. Hence allowing reusability of grammar code with different actions.

References
==========

   | PLY_ by David Beazley
   | classcalc_ by David McNab
