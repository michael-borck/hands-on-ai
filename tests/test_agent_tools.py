"""
Tests for the built-in agent tools (hands_on_ai.agent.agents.*).

These are pure input -> output functions (no LLM, no network), so they can be
called and asserted directly. They cover the calculator, converter, datetime,
dictionary, education and text tools that student "agent" projects rely on.
"""

import datetime

from hands_on_ai.agent.agents.calculator import calc, advanced_calc, quadratic_solver
from hands_on_ai.agent.agents.converter import (
    detect_unit_type,
    convert_temperature,
    convert_unit,
    convert_length,
    convert_weight,
)
from hands_on_ai.agent.agents.datetime_tools import date_diff, format_date, days_until
from hands_on_ai.agent.agents.dictionary import (
    define,
    get_synonyms,
    get_antonyms,
    get_examples,
)
from hands_on_ai.agent.agents.education_tools import (
    periodic_table,
    multiplication_table,
    prime_check,
)
from hands_on_ai.agent.agents.text_tools import word_count, readability_score, summarize


# --- calculator -----------------------------------------------------------

def test_calc_basic_arithmetic():
    assert calc("2 + 3") == "5"
    assert calc("2 * 3 + 4") == "10"
    assert calc("abs(-7)") == "7"


def test_calc_reports_error_on_bad_expression():
    assert calc("2 +").startswith("Error")


def test_advanced_calc_functions():
    assert advanced_calc("sqrt(16)") == "4.0"
    assert advanced_calc("factorial(5)") == "120"
    assert advanced_calc("pi").startswith("3.14")


def test_quadratic_solver_branches():
    assert "Two real solutions" in quadratic_solver("1", "-3", "2")   # disc > 0
    assert "One real solution" in quadratic_solver("1", "2", "1")     # disc == 0
    assert "complex" in quadratic_solver("1", "0", "1")               # disc < 0
    assert quadratic_solver("a", "b", "c").startswith("Error")


# --- converter -------------------------------------------------------------

def test_detect_unit_type():
    assert detect_unit_type("km") == "length"
    assert detect_unit_type("kg") == "weight"
    assert detect_unit_type("c") == "temperature"
    assert detect_unit_type("zzz") is None


def test_convert_temperature_is_exact():
    assert convert_temperature(100.0, "c", "f") == 212.0
    assert convert_temperature(32.0, "f", "c") == 0.0
    assert convert_temperature(0.0, "c", "k") == 273.15


def test_convert_unit_happy_path():
    assert "= 1 km" in convert_unit("1000", "m", "km")
    assert "1000 g" in convert_unit("1", "kg", "g")
    assert "212 f" in convert_unit("100", "c", "f")   # temperature special case


def test_convert_unit_errors():
    assert "Cannot convert between" in convert_unit("5", "m", "kg")
    assert "Unknown unit" in convert_unit("5", "xyz", "m")
    assert "Invalid value" in convert_unit("abc", "m", "km")


def test_convert_length_and_weight():
    assert "1000 m" in convert_length("1", "km", "m")
    assert "1000 g" in convert_weight("1", "kg", "g")
    assert "Unknown length unit" in convert_length("1", "km", "kg")


# --- datetime --------------------------------------------------------------

def test_date_diff_counts_days():
    result = date_diff("2023-01-01", "2023-01-08")
    assert "- Days: 7" in result


def test_date_diff_swaps_out_of_order_dates():
    result = date_diff("2023-01-08", "2023-01-01")
    assert "earlier" in result
    assert "- Days: 7" in result


def test_date_diff_rejects_bad_format():
    assert date_diff("nope", "2023-01-01").startswith("Error")


def test_format_date():
    assert "04/15/2023" in format_date("2023-04-15", "us")
    assert "2023-04-15" in format_date("2023-04-15", "iso")
    assert "Invalid format code" in format_date("2023-04-15", "bogus")
    assert format_date("nope").startswith("Error")


def test_days_until_relative_to_today():
    today = datetime.date.today().isoformat()
    assert "today" in days_until(today)
    assert "ago" in days_until("2000-01-01")


# --- dictionary ------------------------------------------------------------

def test_define():
    assert define("hello") == "Used as a greeting or to begin a conversation."
    assert define("HELLO") == define("hello")   # case-insensitive
    assert "don't have a definition" in define("zxqw")


def test_synonyms_antonyms_examples():
    assert "joyful" in get_synonyms("happy")
    assert "sad" in get_antonyms("happy")
    assert "Examples for 'hello'" in get_examples("hello")
    assert "don't have synonyms" in get_synonyms("zxqw")


# --- education -------------------------------------------------------------

def test_periodic_table_by_name_and_symbol():
    by_name = periodic_table("hydrogen")
    assert "Symbol: H" in by_name
    assert "Atomic Number: 1" in by_name
    assert "Element: Hydrogen" in periodic_table("H")   # lookup by symbol
    assert "not found" in periodic_table("xx")


def test_multiplication_table():
    result = multiplication_table("5", "3")
    assert "5 × 1 = 5" in result
    assert "5 × 3 = 15" in result
    assert "positive integer" in multiplication_table("5", "0")
    assert "Maximum table size" in multiplication_table("5", "25")
    assert multiplication_table("abc").startswith("Error")


def test_prime_check():
    assert prime_check("7") == "7 is a prime number."
    assert "is not a prime number" in prime_check("12")
    assert "Factors of 12: 1, 2, 3, 4, 6, 12" in prime_check("12")
    assert "Prime numbers start at 2" in prime_check("1")
    assert "perfect square" in prime_check("9")
    assert prime_check("abc").startswith("Error")


# --- text ------------------------------------------------------------------

def test_word_count():
    result = word_count("Hello world. This is a test.")
    assert "Word count: 6" in result
    assert "Sentence count: 2" in result


def test_word_count_empty():
    assert word_count("") == "Empty text provided."
    assert word_count("   ") == "Empty text provided."


def test_readability_score():
    assert readability_score("") == "Empty text provided."
    result = readability_score("The cat sat on the mat. It was a sunny day outside.")
    assert "Flesch Reading Ease" in result
    assert "Statistics:" in result


def test_summarize_returns_text():
    paragraph = (
        "Loops repeat work. They are useful in programming. "
        "A loop runs until a condition is met. This makes them powerful. "
        "Beginners should learn them early."
    )
    summary = summarize(paragraph)
    assert isinstance(summary, str) and summary.strip()
