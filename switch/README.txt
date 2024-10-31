This project adds a switch object

On creation the object stores cases withing a dictionary, where the key is the case and the value is the result

On call the object checks the value pased and returs the result for that value that matches a case.

A result can be a function which will run when a case is matched

The call statemet takes parameters for this case

Cases can be dynaimically changed by setting the values with __setitem__, and also accessed with __getitem__