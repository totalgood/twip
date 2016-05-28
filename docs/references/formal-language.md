# Formal Language

## Text Adventure

Have you ever read a choose your own adventure book or played a text-based role polaying or text-adventure game online (Collosal Cave, Adventure, Zork, Hitchhiker's Guide)? If so then
  
  - you were generating a "word" (sequence of symbols) from a regular expression
  - the computer was using a large regular expression to recognize a "valid" sequence of symbols that solved the game
  - the computer was `grep`ping your string (all the commands you entered concatenated together) for a match to the solution pattern
  - searching a Finite State Machine for an "accept" state
  - searching a Directed Acyclic Graph for a solution or goal node
  - checking your sequence of commands (Formal Language symbols) against a Context-Free Grammar for a "valid" statement.

Obviously these are all just ways of describing the same thing. This "thing" is the most basic logic structure capable of modeling complex, seemingly intelligent behavior or problems. But they are simple enough to be evaluatable in a reasonable amount of time. Their complexity is linear:

  $$O(N)$$

The entire sequence of game play actions for a single session can be thought of as a string with N symbols. 

Let's play a quick text adventure designed by my 9-yr-old niece and show you the data structure we used to instantiate the finite state machine that makes it possible. 

If you wanted to automate play (build an AI agent) and have it search for a solution, each attempt would takes O(N) time. There are straightforward search algorithms that can optimally find a solution in linear time. This is because Regular Expressions and Context Free Grammars are the most restrictive and limited form of information processing in [Chomsky's Hierarchy][Chomsky-svg]


  <img src="../../static/Chomsky-hierarchy.png alt="formal language hierarchy: recursively enumerable, context-sensitive, context-free, then regular grammars (languages)">


If you are like most 9 year olds, you'll quickly become bored of the illusion of complexity that these games offered. If you're a game designer you'll want to break out of the finite state machine restrictions to build a Subto show you what a finite state machine looks like

tools used Have you ever interracted with Eliza or a basic chatbot
In bioinformatics