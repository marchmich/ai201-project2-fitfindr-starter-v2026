"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""
import re
import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def parse_query(query: str) -> dict:
    """
    Regex parser. Pulls a max price and a size out of the query; whatever
    text is left becomes the description.
      "vintage graphic tee under $30, size M"
        -> {"description": "vintage graphic tee", "size": "m", "max_price": 30.0}
    """
    text = query.lower()

    max_price = None
    m = re.search(r"(?:under|below|less than|max|up to)\s*\$?(\d+(?:\.\d+)?)", text)
    if m:
        max_price = float(m.group(1))
        text = text.replace(m.group(0), " ")

    size = None
    m = re.search(r"\bsize\s+([a-z0-9]+)\b", text)
    if m:
        size = m.group(1)
        text = text.replace(m.group(0), " ")

    # Drop leftover punctuation like the comma in "..., size M"
    description = " ".join(re.findall(r"[a-z0-9]+", text))
    return {"description": description, "size": size, "max_price": max_price}


def run_agent(query: str, wardrobe: dict) -> dict:
    """(keep your existing docstring here)"""
    session = new_session(query, wardrobe)
    steps = 0

    # Step 1: parse
    steps += 1
    trace.check_iterations(steps)
    session["parsed"] = parse_query(session["query"])

    # Step 2: search, reading the parsed values back out of the session
    steps += 1
    trace.check_iterations(steps)
    parsed = session["parsed"]
    session["search_results"] = search_listings(
        parsed["description"],
        size=parsed["size"],
        max_price=parsed["max_price"],
    )

    # BRANCH: nothing came back -> tell the user what to change, and stop
    if not session["search_results"]:
        session["error"] = _no_results_message(session["parsed"])
        return session

    # Step 3: pick the top-ranked result
    session["selected_item"] = session["search_results"][0]

    # Step 4: outfit
    steps += 1
    trace.check_iterations(steps)
    session["outfit_suggestion"] = suggest_outfit(
        session["selected_item"], session["wardrobe"]
    )

    # Step 5: fit card
    steps += 1
    trace.check_iterations(steps)
    session["fit_card"] = create_fit_card(
        session["outfit_suggestion"], session["selected_item"]
    )

    return session


def _no_results_message(parsed: dict) -> str:
    """Build an error that says what the user could change, not just 'No results'."""
    if not parsed["description"]:
        return ("I couldn't tell what item you're looking for. "
                "Add a description, e.g. 'denim jacket size M under $40'.")

    filters = []
    if parsed["size"]:
        filters.append(f"size {parsed['size'].upper()}")
    if parsed["max_price"] is not None:
        filters.append(f"under ${parsed['max_price']:.0f}")

    msg = f"Nothing matched \"{parsed['description']}\""
    if filters:
        msg += " in " + ", ".join(filters)
    msg += ". Try "
    tips = []
    if parsed["max_price"] is not None:
        tips.append("raising your max price")
    if parsed["size"]:
        tips.append("a different size or dropping the size")
    tips.append("broader words (e.g. 'jacket' instead of 'cropped corduroy jacket')")
    return msg + ", ".join(tips) + "."

# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
