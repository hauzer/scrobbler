A command-line Last.fm scrobbler and a now-playing status updater.

Usage
-----

The program can be invoked with one of the following commands:

- *session-add* - Add a user to the database.

    - [--user, -u]
        A Last.fm username.
    
    - [--password, -p]
        The corresponding password.
        
    - [--session-key, -s]
        A Last.fm session key to be associated with the user name.
        May be useful for some scripts.

    If the command is invoked without any arguments, a Last.fm authorization
    web-page will be opened for you to grant access to the application.
    
    
- *session-list* - List database users and session-keys.

- *session-remove* - Remove a user from the database.
    
    - user
        The user to remove.

- *scrobble* - Scrobble one or more tracks.

    - user
        The username to scrobble with. It must be in the database.
        Case sensitive.
        
    - [--scrobble, -s]
        A scrobble. May be specified multiple times. A single scrobble
        consists of three or more arguments specified below:
        
            - artist
                The name of the artist.
            
            - track
                The name of the track.
            
            - timestamp
                The time of scrobbling. May be formatted with --format
                below. Otherwise it's a
                `UTC <http://en.wikipedia.org/wiki/Coordinated_Universal_Time>`_
                `Unix timestamp <http://www.unixtimestamp.com/>`_.
            
            - [--format, -f]
                Specifies the format of the timestamp, using
                the syntax of
                `strftime() <http://docs.python.org/dev/library/time.html#time.strftime>`_.
            
            - [--album, -a]
                The name of the album.
            
            - [--mbid, -m]
                The MBID of the track. This is currently not usable.
            
            - [--track-number, -t]
                The number of the track, as on the album.
            
            - [--album-artist, -aa]
                The album artist tag. As far as I know, this isn't used in any of
                Last.fm's services.
                
            - [--stream-id, -s]
                Useful only when scrobbling from Last.fm radio.
                Included for completeness' sake.
            
            - [--chosen-by-user, -c]
                A flag specifying that the user has chosen to listen to the track,
                rather than it being chosen for him, by a radio, for example.
            
            - [--context, -cx]
                This is enabled only for some Last.fm applications and it officially
                "isn't public". Included for completeness' sake.

- *update-now-playing* - Display a track as now-playing on a user's Last.fm profile.

    - user
        The username to use. It must be in the database.
        Case sensitive.
        
    - artist
        The name of the artist.
    
    - track
        The name of the track.
    
    - [--album, -a]
        The name of the album.
    
    - [--duration, -d]
        The duration of the track in seconds.
    
    - [--mbid, -m]
        The MBID of the track. This is currently not usable.
    
    - [--track-number, -t]
        The number of the track, as on the album.
    
    - [--album-artist, -aa]
        The album artist tag. As far as I know, this isn't used in any of
        Last.fm's services.
    
    - [--context, -cx]
        This is enabled only for some Last.fm applications and it officially
        "isn't public". Included for completeness' sake.

Examples
--------

Add a user to the database::

    C:\>scrobbler session-add
    The Last.fm authentication page will be opened, or its URL printed here.
    Press enter to continue.
    Press enter after granting access.
    
    
    C:\>
    
and::

    C:\>scrobbler session-add -u hauzzer -p ********
    
    
    C:\>
    
List all of the users in the database::
    
    C:\>scrobbler session-list
    hauzzer | b431328fc489a4f6e6eeee3e8a0f5537
    
    C:\>
    
Make "`Incomudro - Hymn to the Atman <http://www.last.fm/music/Kansas/_/Incomudro+-+Hymn+to+the+Atman>`_"
by `Kansas <http://www.last.fm/music/Kansas>`_ display as the now-playing track on the user's
Last.fm profile.

::
    
    C:\>scrobbler update-now-playing hauzzer Kansas "Incomudro - Hymn to the Atman"
    
    C:\>
    
Scrobble two tracks:

- "`Lamplight Symphony <http://www.last.fm/music/Kansas/_/Lamplight+Symphony>`_"
  by `Kansas <http://www.last.fm/music/Kansas>`_ at 17:23 26-07-2013,
  lasting about eight minutes.

- "`Boomerang <http://www.last.fm/music/Aziza+Mustafa+Zadeh/_/Boomerang>`_" by
  `Aziza Mustafa Zadeh <http://www.last.fm/music/Aziza+Mustafa+Zadeh>`_
  at 17:32 26-07-2013, lasting about four minutes.

::
    
    C:\>scrobbler scrobble hauzzer \
        -s "Kansas \"Lamplight Symphony\" 26-07-2013-17:23 -f %d-%m-%Y-%H:%M -a \"Song for America\" -d 657" \
        -s "\"Aziza Mustafa Zadeh\" Boomerang 26-07-2013-17:32 -f %d-%m-%Y-%H:%M -a \"Dance of fire\" -d 262"
    
    C:\>
    
Remove the user from the database::

    C:\>scrobbler session-remove hauzzer
    
    C:\>
    