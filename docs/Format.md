* [Docs Home](https://github.com/Lyrics/lyrics/tree/master/docs/README.md)
* [FAQ](https://github.com/Lyrics/lyrics/tree/master/docs/FAQ.md)
* [Credits](https://github.com/Lyrics/lyrics/tree/master/docs/Credits.md)
* [Contributing](https://github.com/Lyrics/lyrics/tree/master/docs/Contributing.md)

# Intro
The lyrics are stored in plain text, with no filename extension.

We avoid using "formulas" in lyrics.
That means no things like `[x2]`, `[chorus]` or other ways to compress texts.\
The idea is basically to have a full text, which you can read as you listen to the song.

Having duplicate files is fine, as long as the artist really does have the same song across multiple albums.\
Using symlinks for that, however, is not a good idea. We've tried.\
It basically prevents the lyrics from being viewed easily via GitHub's interface and unnecessarily complicates things.

Any language is welcome, including translations.\
Most likely we'll put translations into `/translations/` which will mirror the `/database/` directory structure.

Punctuation marks are fine to use.\
Currently we use parenthesis to highlight that the bit is being sung by another voice.

Samples are harder to deal with. It's okay to skip them, but eventually we'll either create a separate `/samples/` directory for those, or put them inside square braces within the song text.

We stay away from censoring texts. This means it's okay to commit explicit words.

# Metadata
Metadata goes to the bottom of the song, under a sequence of underscores. Make it equal in length to the
line of the first metadata field (including its value).

The name of the variable and the actual value are separated with two spaces.

## Possible metadata values

  * Language - Contains language code (how is this decided exactly, link people to some standard?), can be multiple. If there are multiple, generally put the language the song is mainly in first, but if you can't decide, don't sweat it, the order is not that important.
```
Language  American English
```

  * Name - Song name
```
Name  Runaway Train
```

  * Artist - Artist's name
```
Artist  Oleander
```

  * Album - Album name
```
Album  Joyride
```

  * Disc no - Disc # (if part of a multi-disc album release)
```
Disc no   2
```

  * Track no - Track #
```
Track no  11
```

  * Year - Year the song was released in
```
Year  2003
```

  * Recording ID in MusicBrainz database
```
MusicBrainz ID  29f4ca0c-6e1e-4e1b-a850-983e542f7e5a
```

  * Cover of - Add this field if the song is a cover version
```
Cover of  ...
```

  * Samples - (optional)
```
Samples   ...
```

  * Original text by - Artists who wrote the song
```
Original text by  Douglas James Eldridge,  Richard C. Ivanisevich,  Thomas Allan Flowers
```

  * Original text copyright - Who currently owns the copyright to the original text of the song
```
Original text copyright  Universal Music Publishing Group
```

# Example song
```
I took a cheap shot,
A clean miss.
Burnin' my defenses by the shakin of her hips,

And then she
Moves in,
A quick kiss,
Breathing down my neck,
She had me wrapped around her wrist.

I try to
Break loose,
Tight grip,
Knocking me unconscious when she bit her bottom lip.

<<Major part of the song cut off here to not bloat the wiki page>>

Loaded the bullets with my blood in the rounds.
Yeah she's a sweet six shooter,
She knows how to get down.
Until the kick-back,
When my heart hits the ground.
She said,
"You think you're so tough,
Baby put your hands up."
Yeah.


__________________________
Language  American English
```

# template

This is a template you can copy and paste into your lyrics file. Add
text for all fields, starting at column 25. Remove fields that do not apply.

```


________________________________
Language
Name
Artist
Album
Disc no
Track no
Year
MusicBrainz ID
Cover of
Samples
Original text by
Original text copyright
```
