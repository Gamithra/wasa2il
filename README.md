# Wasa2il - ‫وسائل
[![build status](https://gitlab.com/piratar/wasa2il/badges/development/build.svg)](https://gitlab.com/piratar/wasa2il/commits/development)
[![coverage report](https://gitlab.com/piratar/wasa2il/badges/development/coverage.svg)](https://gitlab.com/piratar/wasa2il/commits/development)

**Wasa2il** is a participatory democracy software project. It is based around the core
idea of polities - political entities - which users of the system can join or leave,
make proposals in, alter existing proposals, and adopt laws to self-govern.

The goal of this is to make it easy for groups on any scale - from the local
whiskey club to the largest nation - to self-organize and manage their intents,
goals and mutual understandings.

It's main development has been moved to **[Gitlab](https://gitlab.com/piratar/wasa2il)** but it will be updated on [Github](https://github.com/piratar/wasa2il) frequently.

# Staging/demo

The current development version is deployed to Heroku when changes are merged into the development branch.

The app can be found at [https://wasa2il-staging.herokuapp.com](https://wasa2il-staging.herokuapp.com)

# Setup

_Note: Setup instructions are OS-agnostic unless otherwise specified. We test on Linux, Mac OS X and Windows._

For production use, Wasa2il must be set up on a web server capable of running Django. Instructions on setting up a Django production environment are however beyond the scope of this project, as well as Git cloning, Python installation and how to use a command line. Plenty of tutorials on these topics exist in various places online and we suggest you take a look at them if any of this seems confusing.

Long story short, to set up Wasa2il for development and/or testing:

1. Install Python. You will need **pip** installed which is included by default in Python versions 2.7.9 and newer but can be downloaded separately for older versions. (URL: https://www.python.org/)

2. Clone the Wasa2il Git project (URL: https://gitlab.com/piratar/wasa2il.git)

3. In a command line, run the script **initial_setup.py**, which should guide you through the rest of the process.

4. Optional: Run **manage.py load_fake_data --full --reset**, which will reset the database and populate with a large volume of test data.

The 3rd step will populate the database with a small amount of random data, including four users with varying levels of access (users a, b, c and d - each with their own username as a password). The fourth (optional) step will do the same thing, only with much more data.

That should be it!

## Development process
1. Select an unassigned issue from the backlog, assign it to yourself, create a branch from the issue and check out the branch on your local machine

2. Make changes to the code that address the issue (and preferably don't stuff much more in there) and push them. Note: small changes will make for way quicker reviews

3. Monitor the pipeline on Gitlab, cross your fingers and hope for it to pass through

4. Create a merge request into development branch and assign it to someone.

5. If all is well the merge request will be approved into to development and the cahnges deployed to [staging](https://wasa2il-staging.herokuapp.com)

# Project concepts

## Polities

A polity is a political entity which consists of a group of people and a set of laws
the group has decided to adhere to. In an abstract sense, membership in a polity
grants a person certain rights and priviledges. For instance, membership in a
school's student body may grant you the right to attend their annual prom,
and membership in a country (i.e. residency or citizenship) grants you a right
to live there and do certain things there, such as start companies. stand in
elections, and so on.

Each polity has different rules - these are also called statutes, bylaws or laws -
which affect the polity on two different levels.

Firstly, there are meta-rules, which describe how rules are formed, how
decisions are made, how meetings happen, and how governance in general
happens. Wasa2il has to be flexible enough to accomodate the varying
meta-rules of a given polity, otherwise the polity may decide that Wasa2il isn't
useful to them. Sometimes these rules are referred to as "rules of procedure"
or "constitution", depending on the type of polity which is using them.

Secondly there are external rules, which are the decisions the polity makes which
don't affect its internal decisionmaking process.

Wasa2il needs to have the capacity to manage both types of rules and present
both in a coherent and comprehensive way. In particular, there needs to be an
available list of the laws which the polity has adopted, and changes to those
laws which have meta-effects must alter the way Wasa2il works for that polity.

## Topics, Issues, Documents and Votes

Within any polity, there can be any number of different topics that need to be
discussed. The members of a polity decide which topics are relevant to them.
The way in which this is decided depends on the meta-rules of the polity.

Topics are used to manage and display a list of issues. Issues are conversations
which have been brought to discussion within a polity, and can belong to 
numerous topics. The purpose of an issue and its associated conversation is to
arrive at a decision. The decision is represented by a document which can be
adopted or rejected.

Documents which have been adopted represent the law of the polity. Sometimes
laws need to change, so it needs to be possible to propose changes to a law
even after it has been adopted. Doing so would cause a new issue to be raised
and deliberated on.

The decision making process is normally concluded by a vote. Votes can take
many forms. There are multiple methods of voting and multiple ways of calculating
the results. While in most cases the correct approach for the creation of new
laws would be to decide on one unique result.

[As a side: If faced with multiple options for a particular article, for instance, the
Condorcet method may be the best way to get an acceptable result. It might even
be determined that if no Condorcet winner exists amongst the proposals, there
should be some process to push closer to a consensus. This is tricky, as if the
Schultze method is simply used to create a winner there could be a complaint that
results are being forced out, whereas if there is a simple method to postpone an
issue indefinitely opponents could gang up to game the system and eliminate the
possibility of a Condorcet winner. Some middle ground should exist, and Wasa2il
should support the creation of that.]


# Alternative installation instructions

If you don't know what a virtualenv or a docker is, you can safely ignore the
following and just use the [setup instruction above](#setup). Alternatives
are included for those who wish to develop and support the project using those
technologies.

## Virtualenv

    virtualenv venv
    venv/bin/python initial_setup.py --venv

The initial setup script guides you through the rest of the process.

## Docker

    docker build -t piratar/wasa2il .
    docker run --name wasa2il-dev-container -p 8000:8000 -it piratar/wasa2il

The first command builds a new docker image and gives it the name `piratar/wasa2il`
The second command starts a new docker container based of the latest version
of the `piaratar/wasa2il` image, forwards port 8000 of the docker host to the
same port on the docker container, and names it `wasa2il-dev-container`.  The
Docker CMD command runs `initial_setup.py` so when running the container for
the first time you will be prompted for username, e-mail and password.

Since the sqlite database is created inside the container on the first run,
and not for example mounted through a volume, if you want your test data to
persist you must re-use the container after building it.  You can stop and
start the named container like so:

    docker stop wasa2il-dev-container

and

    docker start wasa2il-dev-container

## Docker-compose

Detailed instructions in our wiki: 

https://gitlab.com/piratar/wasa2il/wikis/installation
