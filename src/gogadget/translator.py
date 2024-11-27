import warnings

import argos_spacy_compatibility.package as pkg
import argos_spacy_compatibility.translate as argos
import pandas as pd
from argos_spacy_compatibility.package import Package as pkg_type
from rich.progress import track

from .cli_utils import CliUtils


def translate_all_sentences(
    df: pd.DataFrame, from_lang: str, to_lang: str, source_column: str = "example"
) -> pd.DataFrame:
    """Translate all sentences in a dataframe. Write the translations to the dataframe."""

    # Suppress stanza warnings so that we can see more important output in the console
    warnings.filterwarnings("ignore", category=FutureWarning, module="stanza")

    # Check we have the required languages installed. If not, install them.
    langs_installed = install(from_lang, to_lang)

    if not langs_installed:
        CliUtils.print_warning(
            f"Translator: could not load models for translating from {from_lang} to {to_lang}"
        )
        return df

    for index, row in track(df.iterrows(), description="Translating sentences...", total=len(df)):
        sentence = str(row[source_column])
        translation = translate_sentence(sentence, from_lang, to_lang)
        df.at[index, "translation"] = translation

    return df


def translate_sentence(sentence: str, from_lang: str, to_lang: str) -> str:
    """Translate an individual sentence"""

    # Suppress stanza warnings so that we can see more important output in the console
    warnings.filterwarnings("ignore", category=FutureWarning, module="stanza")
    try:
        translation = argos.translate(sentence, from_lang, to_lang)
    except Exception as e:
        CliUtils.print_error(f"Could not translate sentence from {from_lang} to {to_lang}", e)
        translation = ""

    return translation


def install(from_lang: str, to_lang: str) -> bool:
    """Work out the translation route between languages and install the appropriate argos packages, if required"""

    # Check if the requires languages have been installed
    CliUtils.print_status("Translator: checking installed languages")

    if from_lang == to_lang:
        CliUtils.print_warning(
            f"""Translator: target language and native language are both set to '{from_lang}' so no translation will be undertaken. 
    Try specifying --translation-language [your-native-language-2-letter-code-here] next time you run the command.
    For more information, run gogadget [command_name] --help"""
        )
        return False

    installed_packages = pkg.get_installed_packages()
    required_packages = translation_route(installed_packages, from_lang, to_lang)

    # If not, try to install them
    if len(required_packages) == 0:
        # Try to work out the translation route from the package index
        CliUtils.print_status("Translator: attempting language installation")
        pkg.update_package_index()
        available_packages = pkg.get_available_packages()
        required_packages = translation_route(available_packages, from_lang, to_lang)

        # Exit with failure message if we can't find a translation route
        if len(required_packages) == 0:
            CliUtils.print_error(
                f"Could not find a translation route from {from_lang} to {to_lang}"
            )
            return False

        # If we do have a translation route, install the languages
        install_languages(required_packages)

    CliUtils.print_rich("Translation route achieved:")
    CliUtils.print_rich(required_packages)

    return True


def install_languages(required_packages: list[pkg_type]):
    """Install each argos package in the list"""

    for package in required_packages:
        CliUtils.print_rich(f"Installing {str(package)}")

        pkg.install_from_path(package.download())


def translation_route(available_packages: list[pkg_type], from_lang: str, to_lang: str) -> list:
    """Work out the route that needs to be taken to translate between languages based upon a provided list of packages"""

    # Try to find a direct translation route first
    required_packages = []
    for package in available_packages:
        if (package.from_code == from_lang) and (package.to_code == to_lang):
            required_packages.append(package)
            return required_packages

    # If not available, try going via English
    found_to_en = False
    found_from_en = False

    for package in available_packages:
        if (package.from_code == from_lang) and (package.to_code == "en"):
            required_packages.append(package)
            found_to_en = True
            break

    for package in available_packages:
        if (package.from_code == "en") and (package.to_code == to_lang):
            required_packages.append(package)
            found_from_en = True
            break

    if (not found_to_en) or (not found_from_en):
        return []

    return required_packages
