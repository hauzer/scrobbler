A command-line Last.fm scrobbler and a now-playing status updater.

Usage
-----

The program can be invoked with one of the following commands:

- session-add - Add a user to the database.

    - [--user, -u]
    
        A Last.fm username.
    
    - [--password, -p]
    
        The corresponding password.
        
    - [--session-key, -s]
    
        A Last.fm session key to be associated with the user name.
        May be useful for some scripts.

    If the command is invoked without any arguments, a Last.fm authorization
    web-page will be opened for you to grant access to the application.
    
    
- session-list - List all users in the database and their session keys.

- session-remove - Remove a user from the database.
    
    - user
        The user to remove.

- scrobble - Scrobble one or more tracks.

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
            
            .. _scrobble-timestamp:
            
            - timestamp
                The time of scrobbling. May be formatted with `--format <scrobble-format>`_
                below. Otherwise it's a
                `UTC <http://en.wikipedia.org/wiki/Coordinated_Universal_Time>`_
                `Unix timestamp <http://www.unixtimestamp.com/>`_.
            
            .. _scrobble-format:
            
            - [--format, -f]
                Specifies the format of `timestamp <scrobble-timestamp>`_ using
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
            
            - [--chosed-by-user, -c]
                A flag specifying that the user has chosen to listen to the track,
                rather than it being chosen for him, by a radio, for example.
            
            - [--context, -cx]
                This is enabled only for some Last.fm applications and officially
                "isn't public". Included for completeness' sake.

- update-now-playing

    - user
        The username to scrobble with. It must be in the database.
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
        This is enabled only for some Last.fm applications and officially
        "isn't public". Included for completeness' sake.

Examples
--------

::

    C:\>scrobbler session-add
    The Last.fm authentication page will be opened, or its URL printed here.
    Press enter to continue.
    Press enter after granting access.

    C:\>scrobbler session-list
    hauzzer | b431328fc489a4f6e6eeee3e8a0f5537

    C:\>scrobbler update-now-playing hauzzer Kansas "Hold On"

    C:\>scrobbler scrobble hauzzer \
        -s "Kansas \"Lamplight Symphony\" 26-07-2013-17:23 -f %d-%m-%Y-%H:%M -a \"Song for America\" -d 657" \
        -s "\"Aziza Mustafa Zadeh\" Boomerang 26-07-2013-17:32 -f %d-%m-%Y-%H:%M -a \"Dance of fire\" -d 262"
