# Contributing to gearpy

## Reporting issues

When reporting issues please include as much detail as possible about 
your operating system, python version, dependencies version and geapy 
version.  
Whenever possible, please also include a brief, self-contained code 
example that demonstrates the problem.

## Contributing code

Thanks for your interest in contributing code to gearpy!

Please be sure to follow the convention for commit messages, similar to
the [numpy commit message convention](https://numpy.org/devdocs/dev/development_workflow.html#writing-the-commit-message).  
Commit messages should be clear and follow a few basic rules. Example:

```
ENH: add functionality X gearpy.<submodule>.

The first line of the commit message starts with a capitalized acronym
(options listed below) indicating what type of commit this is.  Then a 
blank line, then more text if needed.  Lines shouldn't be longer than 72
characters.  If the commit is related to a ticket, indicate that with
"See #3456", "See ticket 3456", "Closes #3456" or similar.
```

Describing the motivation for a change, the nature of a bug for bug 
fixes or some details on what an enhancement does are also good to 
include in a commit message. Messages should be understandable without 
looking at the code changes. A commit message like 
`MNT: fixed another one` is an example of what not to do; the reader has
to go look for context elsewhere.  
Standard acronyms to start the commit message with are:

```
BUG: bug fix
DEP: deprecate something or remove a deprecated object
DEV: development tool or utility
DOC: documentation
ENH: enhancement
MNT: maintenance commit (refactoring, typos, etc.)
REV: revert an earlier commit
STY: style fix (whitespace, PEP8)
TST: addition or modification of tests
REL: related to releasing gearpy
MRG: merging commit
```
