"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings
import re


# ── Tool 1: search_listings ───────────────────────────────────────────────────


def search_listings(description, size=None, max_price=None):
    results = load_listings()

    # Price filter (inclusive)
    if max_price is not None:
        results = [l for l in results if l["price"] <= max_price]

    # Size filter: whole-token match, so "m" matches "S/M" but "s" doesn't match "US 9"
    if size is not None:
        wanted = size.strip().lower()
        results = [
            l for l in results
            if wanted in re.split(r"[\s/,\-]+", l["size"].strip().lower())
        ]

    # Keyword scoring
    words = set(re.findall(r"[a-z0-9]+", description.lower()))
    scored = []
    for l in results:
        parts = [l["title"], l["description"], l["category"],
                 *l["style_tags"], *l["colors"]]
        if l["brand"]:  # brand is often None
            parts.append(l["brand"])
        text_words = set(re.findall(r"[a-z0-9]+", " ".join(parts).lower()))
        score = len(words & text_words)
        if score > 0:
            scored.append((score, l))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [l for _, l in scored[:config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    item_desc = (
        f"{new_item['title']} ({new_item['category']}), "
        f"colors: {', '.join(new_item['colors'])}, "
        f"style: {', '.join(new_item['style_tags'])}, "
        f"size {new_item['size']}, ${new_item['price']:.2f}"
    )
    if new_item.get("brand"):
        item_desc += f", brand: {new_item['brand']}"

    system = (
        "You are a friendly thrift-fashion stylist. Suggest one or two outfits "
        "built around the item the user is considering. "
        "If the user lists pieces they own, build outfits only from those "
        "pieces, naming them exactly as listed, and never invent items they "
        "don't own. "
        "If the user has no wardrobe, give general styling advice describing "
        "the kinds of pieces that pair well (e.g. 'wide-leg jeans', 'white "
        "sneakers') and do not refer to their wardrobe. "
        "Keep it under 150 words."
    )

    items = wardrobe.get("items", [])
    if not items:
        prompt = (
            f"Item I'm considering:\n{item_desc}\n\n"
            "I don't have a wardrobe listed. Give me general styling ideas."
        )
    else:
        wardrobe_lines = "\n".join(
            f"- {w['name']}" + (f" ({w['category']})" if w.get("category") else "")
            for w in items
        )
        prompt = (
            f"Item I'm considering:\n{item_desc}\n\n"
            f"What I already own:\n{wardrobe_lines}"
        )

    response = generate(prompt, system=system)

    if not response:
        return "Couldn't generate outfit suggestions this time. Please try again."
    return response
       

# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    # TODO: replace this with your implementation
    return ""
