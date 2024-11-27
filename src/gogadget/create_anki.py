import random
from pathlib import Path

import genanki
import pandas as pd

from .cli_utils import CliUtils
from .config import get_resources_directory
from .frequency_analyser import frequency_analyser
from .lookup import copy_all_word_audio, lookup_all_words
from .translator import translate_all_sentences
from .utils import (
    dataframe_to_excel,
    generate_output_path,
    load_json,
    read_file_to_string,
    sanitise_string_html,
)
from .video_manipulation import extract_sentence_media, match_subtitles_to_media


def create_anki(
    input_directory: Path,
    language: str,
    subs_offset: int,
    subs_buffer: int,
    max_cards: int,
    lemma: bool,
    filter_stop_words: bool,
    extract_media: bool,
    include_no_definition: bool,
    native_language: str,
    word_audio_path: Path | None = None,
    dictionary_path: Path | None = None,
    excluded_words: Path | None = None,
) -> Path | None:
    """Main entry point for the anki deck builder"""

    # Config
    CliUtils.print_status("Anki builder: configuring paths")
    anki_media_dir = input_directory / "media"
    anki_sentence_audio_dir = anki_media_dir / "sentence_audio"
    anki_screenshot_dir = anki_media_dir / "screenshots"
    anki_word_dir = anki_media_dir / "word_audio"
    anki_media_dir.mkdir(parents=True, exist_ok=True)
    anki_sentence_audio_dir.mkdir(parents=True, exist_ok=True)
    anki_screenshot_dir.mkdir(parents=True, exist_ok=True)
    anki_word_dir.mkdir(parents=True, exist_ok=True)

    deck_output_path = generate_output_path(input_directory, anki_media_dir, "deck", "apkg")
    deck_name = deck_output_path.stem

    # Frequency analysis
    CliUtils.print_status("Anki builder: running frequency analysis")
    df = frequency_analyser(
        input_path=input_directory,
        output_directory=anki_media_dir,
        language=language,
        lemmatise_words=lemma,
        filter_stop_words=filter_stop_words,
        exclude_spreadsheet_path=excluded_words,
    )

    if df is None:
        return None

    CliUtils.print_status("Anki builder: preparing dataframe")
    # Add in additional columns that we will use to store information for the Anki cards
    df = df.assign(screenshot_path="", sentence_audio_path="", word_audio_path="")
    df = df.assign(definition="", translation="")

    # Get the definitions. Do this before everything else since we want to limit cards asap
    if dictionary_path:
        CliUtils.print_status("Anki builder: getting definitions")
        df = lookup_all_words(df=df, dictionary_path=dictionary_path)

    CliUtils.print_status("Anki builder: pruning cards")
    # If specified by user, remove cards without a definition
    if not include_no_definition:
        df = filter_no_definition(df=df)

    # Limit the number of cards
    df = limit_cards(df=df, max_cards=max_cards)

    # Work out the media files for each subtitle
    CliUtils.print_status("Anki builder: matching subtitles to media files")
    subs_to_media = match_subtitles_to_media(input_directory)
    if len(subs_to_media) == 0:
        return None

    # Get sentence audio and screenshots and update dataframe with paths
    if extract_media:
        CliUtils.print_status("Anki builder: extracting media to use in cards")
        df = extract_sentence_media(
            audio_dir=anki_sentence_audio_dir,
            screenshot_dir=anki_screenshot_dir,
            subs_to_media=subs_to_media,
            df=df,
            subs_offset=subs_offset,
            subs_buffer=subs_buffer,
        )

    # Get the word audio
    if word_audio_path:
        CliUtils.print_status("Anki builder: getting example audio for individual words")
        df = copy_all_word_audio(
            df=df, library_path=word_audio_path, output_directory=anki_word_dir
        )

    CliUtils.print_status("Getting translations")
    df = translate_all_sentences(df=df, from_lang=language, to_lang=native_language)

    # Build deck
    CliUtils.print_status("Building deck")
    anki_notes, media_files = produce_anki_notes(
        df=df, deck_name=deck_name, include_no_definition=include_no_definition
    )

    package = create_package(deck_name=deck_name, anki_notes=anki_notes, media_files=media_files)

    # Save the df and the Anki package
    CliUtils.print_status("Anki builder: saving data")
    write_package(deck_output_path, package)
    save_deck_definition_sheet(df, input_directory, anki_media_dir)

    return None


def limit_cards(df: pd.DataFrame, max_cards: int) -> pd.DataFrame:
    """Limit cards in a deck to a specified value by modifying the dataframe used to build it"""
    df = df.head(max_cards)
    return df


def filter_no_definition(df: pd.DataFrame) -> pd.DataFrame:
    """Remove cards that have a blank entry for definiton"""
    df = df[df["definition"] != ""]

    return df


def write_package(file_path: Path, package: genanki.Package) -> None:
    """Save Anki package to file"""
    package.write_to_file(file_path)


def create_package(deck_name, anki_notes: list, media_files: list) -> genanki.Package:
    """Build the Anki package in memory"""

    deck = create_deck(
        deck_id=generate_anki_id(),
        deck_name=deck_name,
        note_cards=anki_notes,
    )

    package = genanki.Package(deck)

    if len(media_files) > 0:
        package.media_files = media_files

    return package


def produce_anki_notes(
    df: pd.DataFrame, deck_name: str, include_no_definition: bool
) -> tuple[list, list]:
    """Convert the data from the dataframe into Anki notes. Return the required media files as the second variable in the tuple"""

    # Configure paths
    html_path = get_resources_directory() / "html" / "anki"
    css_path = html_path / "anki_card.css"
    front_path = html_path / "front.html"
    back_path = html_path / "back.html"
    model_fields_path = html_path / "fields.json"

    # Build model
    model_fields = load_json(model_fields_path)
    assert isinstance(model_fields, list)

    model_template = [
        {
            "name": deck_name,
            "qfmt": read_file_to_string(front_path),
            "afmt": read_file_to_string(back_path),
        },
    ]

    model = create_model(
        model_id=generate_anki_id(),
        model_name=deck_name,
        fields=model_fields,
        template=model_template,
        css=read_file_to_string(css_path),
    )

    i = 0
    note_cards = []
    media_files = []
    for _, row in df.iterrows():
        # Get data from row
        word = str(row["word"])
        example = str(row["example"])
        word_frequency = str(row["frequency"])
        image_path = Path(str(row["screenshot_path"]))
        sentence_audio_path = Path(str(row["sentence_audio_path"]))
        word_audio_path = Path(str(row["word_audio_path"]))
        definition = str(row["definition"])
        translation = str(row["translation"])
        card_index = str(i)

        # Put the file names for the audio into Anki card format
        sentence_audio_field_anki = format_audio_field(sentence_audio_path.name)
        word_audio_field_anki = format_audio_field(word_audio_path.name)
        image_field_anki = format_image_field(image_path.name)

        # Set the field values for the card
        note_fields = [
            card_index,
            sanitise_string_html(word),
            sanitise_string_html(example),
            sanitise_string_html(translation),
            definition,
            word_frequency,
            sentence_audio_field_anki,
            word_audio_field_anki,
            image_field_anki,
        ]

        # Create an Anki note
        note = create_note(model, note_fields)
        note_cards.append(note)

        # Media files
        if sentence_audio_path.exists() and sentence_audio_path.is_file():
            media_files.append(sentence_audio_path)

        if word_audio_path.exists() and word_audio_path.is_file():
            media_files.append(word_audio_path)

        if image_path.exists() and image_path.is_file():
            media_files.append(image_path)

        i += 1

    return note_cards, media_files


def save_deck_definition_sheet(df: pd.DataFrame, input_path: Path, output_path: Path):
    """Save the dataframe used to build the Anki deck to file"""

    save_path = generate_output_path(input_path, output_path, "deck_resources", "xlsx")
    dataframe_to_excel(df, save_path)


def create_note(model: genanki.Model, fields: list) -> genanki.Note:
    """Generate an individual Anki note"""
    note = genanki.Note(model=model, fields=fields)
    return note


def create_model(
    model_id: int, model_name: str, fields: list, template: list, css: str = ""
) -> genanki.Model:
    """Create an Anki model with the fields and card formatting"""
    model = genanki.Model(
        model_id=model_id, name=model_name, fields=fields, templates=template, css=css
    )

    return model


def create_deck(deck_id: int, deck_name: str, note_cards: list) -> genanki.Deck:
    """In memory, add Anki notes to a deck object"""
    deck = genanki.Deck(deck_id=deck_id, name=deck_name)

    if len(note_cards) > 0:
        for note in note_cards:
            deck.add_note(note)

    return deck


def generate_anki_id() -> int:
    """Generate a random number to act as the Anki deck ID"""
    model_id = random.randrange(1 << 30, 1 << 31)

    return model_id


def format_audio_field(file_name: str) -> str:
    """Format the file name so that it can be used in an Anki field. Input string should only be the file stem plus file file suffix.
    Note to self. You cannot specify audio/sound.mp3 as Anki has a flat file structure.
    All media files must therefore have unique names
    """
    if file_name == "":
        return ""

    output_string = f"[sound:{file_name}]"

    return output_string


def format_image_field(file_name: str) -> str:
    """Format the file name so that it can be used in an Anki field. Input string should only be the file stem plus file file suffix.
    Note to self. You cannot specify images/image.jpg as Anki has a flat file structure.
    All media files must therefore have unique names
    """
    if file_name == "":
        return ""

    output_string = f"<img src='{file_name}'>"

    return output_string
