studygroup
==========

Prototype application to allow creation of study groups within a given Meetup
group.

This application isn't functional yet. If you want to help, the sketch of how
it should work is on the wiki: [StudyGroup Sketch](https://github.com/BostonPython/studygroup/wiki/StudyGroup-sketch).
There are also a few [issues](https://github.com/BostonPython/studygroup/issues)
describing work that needs to be done.

Developing
==========

Study Group uses OAuth authentication with meetup.com, so you will need to
configure to be able to perform that authentication.  You will run your
development machine so that it pretends to be
"dev-studygroup.bostonpython.com":

1. Go to http://www.meetup.com/meetup_api/, and click "OAuth Consumers".

2. Create a new consumer, with these details:

        Consumer Name: Boston Python Study Groups (Dev)
        Redirect URI: http://localhost:8080/

3. Create a settings_local.py alongside settings.py, with details from the
    OAuth consumer you just created:

        MEETUP_GROUP_ID = 469457    # Boston Python, use this exactly.
        MEETUP_OAUTH_KEY = "esgls3vaf5k7d9ufrvj0jtuvo0"     # Fill in with your own key
        MEETUP_OAUTH_SECRET = "mgi9mlaagc24o8a3f4hcvu0mb0"  #   .. and secret.
        SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/studygroup.db"

4. Create the database tables:

        $ python manage.py db upgrade

5. Install The javascript builder:

        Depending on your operating system install the npm package
        (OSX) $
            * Brew
                - $ brew install npm
            * Mac Ports
                - $ port install npm

        (Linux)
            $ apt-get install npm

        $ npm install
        $ bower install
        $ gulp

6. Start the server:

        $ python run_server.py -p 8080

7. Visit the page in your browser using the URL http://localhost:8080.
    You should see the Study Group page, and your server window should show
    URLs being served.

8. If you click the Sign In Now button, it should take you to meetup.com and
    ask you to authorize Boston Python Study Groups.


Running tests
=============

Tests are run with unittest in the standard library:

        $ python -m unittest discover

