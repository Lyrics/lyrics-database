# Contributing

* [Docs Home](https://github.com/Lyrics/lyrics/tree/master/docs/README.md)
* [Format](https://github.com/Lyrics/lyrics/tree/master/docs/Format.md)
* [Credits](https://github.com/Lyrics/lyrics/tree/master/docs/Credits.md)
* [FAQ](https://github.com/Lyrics/lyrics/tree/master/docs/FAQ.md)
* Fork the repository.
* Add files following the structure \(see below\).
* Make a PR.

Alternatively, please feel free to open an issue if it's a song or correction request.

## The database structure:

```text
A
 /Artist Name
             /Album Title
                         /Song Name
B
C
...
X
Y
Z
```

## FAQ

### There's a forward slash in album/artist/song name

Use this Unicode symbol instead: `∕`

### Some part of the song can't be heard properly

Searching for lives or covers sometimes helps. Putting in your best guess is preferable over using a placeholder.

### I want to save trees and use things like "Repeat x3" and "Chorus:"

Don't do it. That's not how you save trees.

### I'm not sure who to trust when it comes to song/artist/album names

Popular websites such as Wikipedia may be a little off when it comes to naming. [MusicBrainz.org](https://musicbrainz.org) happens to be extremely useful in such cases.

### Lyrics in the music video differ from the album version

Stick to the album version. Video edits rarely hold extra lyrics, they're most of the time just shortened versions. If feels necessary they can be put into the `video-versions/` directory, tagged with metadata key `Variant` set to `Video Version`.

### The song is a single that does not belong to an album

Use the song name as the album name. For example, Six Shooter by Coyote Kisses would end up being `C/Coyote Kisses/Six Shooter/Six Shooter`

