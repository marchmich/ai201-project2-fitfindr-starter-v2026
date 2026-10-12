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

import re
import config

STOPWORDS = {"a", "an", "the", "for", "with", "and", "or", "in", "of", "to", "under", "size"}

def _tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOPWORDS

def search_listings(description, category=None, size=None, max_price=None):
    results = load_listings()

    if max_price is not None:
        results = [l for l in results if l["price"] <= max_price]

    if category is not None:
        cat = category.strip().lower()
        results = [l for l in results if l["category"].lower() == cat]

    # Whole-token size match: "m" matches "S/M", "s" doesn't match "US 9"
    if size is not None:
        wanted = size.strip().lower()
        results = [l for l in results
                   if wanted in re.split(r"[\s/,\-]+", l["size"].strip().lower())]


    words = _tokens(description)
    scored = []
    for l in results:
        parts = [l["title"], l["description"], l["category"], *l["style_tags"], *l["colors"]]
        if l["brand"]:
            parts.append(l["brand"])
        score = len(words & _tokens(" ".join(parts)))
        if score > 0:
            scored.append((score, l))

    # Best match first; cheaper listing wins a tie
    scored.sort(key=lambda p: (-p[0], p[1]["price"]))
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
    # Guard: empty or whitespace-only outfit -> feedback, no model call
    if not outfit or not outfit.strip():
        return ("Can't write a fit card without an outfit suggestion. "
                "Run suggest_outfit first and pass its result in.")

    item_desc = (
        f"{new_item['title']} ({new_item['category']}), "
        f"colors: {', '.join(new_item['colors'])}, "
        f"style: {', '.join(new_item['style_tags'])}, "
        f"${new_item['price']:.2f} on {new_item['platform']}"
    )
    if new_item.get("brand"):
        item_desc += f", brand: {new_item['brand']}"

    system = (
        "You write short social media captions about thrift finds. "
        "Write 2 to 4 sentences in a casual first-person voice, like a real post, "
        "not a product description. "
        "Mention the item, its price as a number with a $ sign, and the platform "
        "it's listed on, once each. "
        "Describe how it's styled using the outfit given, and be specific about "
        "the vibe (e.g. '90s off-duty', 'cozy library academic'), not just 'cute'. "
        "Return only the caption."
    )

    prompt = (
        f"The find:\n{item_desc}\n\n"
        f"How I'm wearing it:\n{outfit.strip()}"
    )

    response = generate(prompt, system=system)

    if not response:
        return "Couldn't write a caption this time. Please try again."
    return response.strip()