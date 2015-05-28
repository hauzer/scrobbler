Usage
=====

The program can be invoked with one of the following commands:

- *add-user* - Add a user to the list of known users.

    - [user]
        A Last.fm username.
    
    - [--password, -p]
        The corresponding password.

    If a username is provided, you will be prompted for a password.
    If the command is invoked without any arguments, a Last.fm authorization
    web-page will be opened for you to grant access to the application.
    

- *list-users* - List known users and their corresponding session keys.

- *remove-user* - Remove a user from the list of known users.
    
    - user
        The user to remove.


- *scrobble* - Scrobble a track.

    - user
        The username to scrobble with. If the user isn't known,
        you will be prompted for a password.

    - artist
        The name of the artist.
    
    - track
        The name of the track.
    
    - time
        The time of listening. Formatted by --time-format. It may also be *now*,
        in which case the current time is used.
    
    - [--time-format, -tf]
        Specifies the format of *time*, using
        the syntax of
        `strftime() <http://docs.python.org/dev/library/time.html#time.strftime>`_.
        Defaults to *%Y-%m-%d.%H:%M*.
    
    - [--album, -a]
        The name of the album.

    - [--duration, -d]
        Has the format of XXhYYmZZs. At least one of those has to be present,
        but any number of them can be specified, and in any order.
    

- *now-playing* - Update the now-playing status.

    - user
        The username to use. If the user isn't known,
        you will be prompted for a password.
        
    - artist
        The name of the artist.
    
    - track
        The name of the track.
    
    - [--album, -a]
        The name of the album.
    
    - [--duration, -d]
        Has the format of XXhYYmZZs. At least one of those has to be present,
        but any number of them can be specified, and in any order.


Examples
========

Add a user to the list of known users::

    $ scrobbler add-user
    The Last.fm authentication page will be opened, or its URL printed here.
    Press enter to continue.
    Press enter after granting access.
    User hauzzer added.

    $
    
and::

    $ scrobbler add-user hauzzer
    Password:
    User hauzzer added.
    
    $
    
also::

    $ scrobbler add-user hauzzer --password ******
    User hauzzer added.

    $

List all known users::
    
    $ scrobbler list-users
    hauzzer | b431328fc489a4f6e6eeee3e8a0f5537
    
    $
    
Scrobble a track, "`Lamplight Symphony <http://www.last.fm/music/Kansas/_/Lamplight+Symphony>`_"
by `Kansas <http://www.last.fm/music/Kansas>`_, which was listened to on 07/15/2013 at 15:32::
    
    $ scrobbler scrobble hauzzer Kansas "Lamplight Symphony" 2013-15-07.15:32 -a "Song for America" -d 8m16s
    Track scrobbled.

    $

Update the now-playing status with "`Incomudro - Hymn to the Atman <http://www.last.fm/music/Kansas/_/Incomudro+-+Hymn+to+the+Atman>`_"
by `Kansas <http://www.last.fm/music/Kansas>`_.::
    
    $ scrobbler now-playing hauzzer Kansas "Incomudro - Hymn to the Atman" -a "Song for America" -d 12m17s
    Status updated.
    
    $
    
Remove a user from the list of known users::

    $ scrobbler remove-user hauzzer
    User hauzzer removed.
    
    $
    
