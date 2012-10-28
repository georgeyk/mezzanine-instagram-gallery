mezzanine instagram gallery
===========================

This is a django application to create a [mezzanine][0] gallery using the
instagram images of a certain user.

Here is an [example][1] of the gallery created with this application:

You will need to setup a cron job (or alike) to get the pictures from time to
time.


Requirements
------------

* python-instagram
* requests


Installation
------------

Run the following command:

    $ pip install -e git+https://github.com/georgeyk/mezzanine-instagram-gallery.git#egg=mezzanine_instagram_gallery

Add `mezzanine_instagram_gallery` in your `INSTALLED_APPS` after all the
mezzanine applications. Then run migrate:

    $ python manage migrate mezzanine_instagram_gallery

There is a management command that you can run on regular basis to update your
pictures from instagram (you'll need to setup your access token first):

    $ python manage.py sync_instagram_medias

It will try to download your recent medias and add it to your configured
gallery, I suggest you add a cron entry for this script.


Settings
--------

In order to access the instagram API we need an access token.
You can use this application to get one, to do this you should set this
variables in your *settings.py*:

    INSTAGRAM_CLIENT_ID = 'client-id'
    INSTAGRAM_SECRET = 'secret'
    INSTAGRAM_REDIRECT_URL = 'your-redirect-url'

And configure the *urls.py*, here is an example:

    [...]
    url(r"^instagram-authorize/$",
        "mezzanine_instagram_gallery.views.authorize"),
    url(r"^instagram-callback/$",
            "mezzanine_instagram_gallery.views.callback"),
    [...]

Then run your project and access the configured url that calls *authorize*
view. If everything is set correctly, you should see a page with a successful
message.
You might want to read the [python-instagram][2] documentation for further details
on the authentication process.

Actually, this step is optional. You can use the script
[*get_access_token.py*][3] and get the access token.
Once with the access token, just open a python shell:

    >>> from mezzanine_instagram_gallery.models import InstagramUser
    >>> InstagramUser(access_token='your-access-token').save()

And your are done.

NOTE: if you are going to use the second way, remeber to this after you
complete the application installation.

You need to create a gallery inside mezzanine to associate with the
downloaded imges, use the gallery slug as shown:

    INSTAGRAM_GALLERIES = [('gallery-slug', 'gallery-type'),]

We currently support only galleries using the user pictures, but in the future
it might be possible to set several galleries, so we use the syntax above. You
should set gallery-type to 'user'.

The number of items to fetch from instagram at a time (defaults to 50):

    INSTAGRAM_FETCH_COUNT = 50


TODO
====

* Complete support for multiple galleries


Final Note
-----------

This is a work in progress application, so you should expect many bugs!


[0]: http://mezzanine.jupo.org/
[1]: http://georgeyk.com.br/gallery/
[2]: https://github.com/Instagram/python-instagram
[3]: https://github.com/Instagram/python-instagram/blob/master/get_access_token.py
