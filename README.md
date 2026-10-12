# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does


The user asks for a piece of clothing with a specific description, size, or price and the system returns a result with a matched item.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->



### `search_listings`

- **What it does: It takes the users input (a description of a clothing item) that can include size, brand, max price or style and searches for items across the catalogue that match the input. It filters by input and eliminate listings that do not match (i.e. wrong size or price). Then sends the results to suggest_outfits**
- **Inputs: description (str), category (str),  size (str), max_price (float), color (list) or None=None** <!-- name and type each: `max_price` (float), not "a price" -->
- **Returns: A list of listing dicts that contains title, price, size, platform, color, brand, and category. Ranked by matching compatibility and lower price**
- **When it has nothing: It returns an empty list**

### `suggest_outfit`

- **What it does: It takes the list of listing dicts of search_listings and suggests 2 outfits based on the result listings and the user's wardrobe. Then sends the suggested outfit to create_fit_card**
- **Inputs: wardrobe list, dictionary listing**
- **Returns: A non-empty list outfit a combination of a pre-existing piece and the new one**
- **When it has nothing:  It returns a str saying no results found, and stops. Does not call create_fit_card**

### `create_fit_card`

- **What it does: Takes the list from suggest_outfit and writes a short caption describing the outfit, including the description of the new iteam and how it could be worn with the pre-existing outfits.**
- **Inputs: outfit (str) and the item (list)**
- **Returns: a caption (string) of 2-4 sentences that inlcude the price (in digits) and the platform where its listed.**
- **When it has nothing: If the outfit is empty, it returns a feedback message instead of calling the model or rising an exception.**

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in
`session["error"]` that tells the user what to change (raise the max price, try a
different size or drop it, or use broader words) and return the session without
calling `suggest_outfit` or `create_fit_card`. Otherwise, put the first result in
`session["selected_item"]` and go to `suggest_outfit`, then `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** egex, in `agent.py::parse_query`. One pattern pulls
out the max price ("under / below / less than / max / up to" followed by a number),
another pulls out the size ("size" followed by a token). Those phrases are removed,
and the remaining words become the description. <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** query` → `parsed` (`description`, `size`,
`max_price') → `search_results` → `selected_item` → `outfit_suggestion` →
`fit_card`. On the empty-results branch, `error` is set and the run stops after
`search_results`, leaving `selected_item`, `outfit_suggestion` and `fit_card` as `None` <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
 python app.py ask 'white jacket under 50'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('white jacket', max_price=50))"

```

[{'id': 'lst_004', 'title': '90s Track Jacket — Navy/White Stripe', 'description': 'Authentic 90s track jacket with stripe detail down the sleeves. Full zip. Lightweight — great for layering.', 'category': 'outerwear', 'style_tags': ['90s', 'vintage', 'athletic', 'streetwear'], 'size': 'M', 'condition': 'excellent', 'price': 45.0, 'colors': ['navy', 'white'], 'brand': 'Champion', 'platform': 'poshmark'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterflygraphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_035', 'title': 'Low-Top Canvas Sneakers — Off-White', 'description': 'Classic low-top canvas sneakers in off-white. Very minimal. Some light yellowing on the sole edges from age. Size 9.', 'category': 'shoes', 'style_tags': ['classic', 'minimal', 'streetwear', 'basics'], 'size': 'US 9', 'condition': 'good', 'price': 20.0, 'colors': ['off-white', 'cream'], 'brand':None, 'platform': 'poshmark'}, {'id': 'lst_023', 'title': 'Crochet Halter Top — Cream', 'description': 'Handmade-looking crochet halter. Ties at the neck and back. Perfect for layering over a tank in summer.', 'category': 'tops', 'style_tags': ['cottagecore', 'boho', 'crochet', 'summer'], 'size': 'S/M', 'condition': 'excellent', 'price': 22.0, 'colors': ['cream', 'off-white'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_032', 'title': 'Shacket — Olive Canvas', 'description': 'Olive canvas shacket — thicker than a shirt, lighter than a jacket. Chest pockets, button-front. Great transitional layer.', 'category': 'outerwear', 'style_tags': ['earth tones', 'classic', 'layering', 'minimal'], 'size': 'M/L', 'condition': 'excellent', 'price': 33.0, 'colors': ['olive', 'green'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_018', 'title': 'Vintage Linen Blazer — Cream', 'description': 'Lightweight linen blazer in cream. Relaxed fit, unstructured shoulders. Two front pockets. Could be dressed up or styled casually.', 'category': 'outerwear', 'style_tags': ['vintage', 'classic', 'linen', 'cottagecore', 'minimal'], 'size': 'M/L', 'condition': 'excellent', 'price': 38.0, 'colors': ['cream', 'off-white'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_007', 'title': 'Denim Jacket — Light Wash, Cropped', 'description': 'Cropped denim jacket in a light wash. Great structured shoulders. Blank canvas — no patches or pins but would be perfect to customize.', 'category': 'outerwear', 'style_tags': ['denim', 'vintage', 'classic', 'streetwear'], 'size': 'S', 'condition': 'excellent', 'price': 42.0, 'colors': ['light blue'], 'brand': 'Wrangler', 'platform': 'poshmark'}, {'id': 'lst_019', 'title': 'PlatformSneakers — White Chunky Sole', 'description': 'White chunky platform sneakers. Very late 90s / early 2000s energy. Velcro straps. True to size. Some sole yellowing.', 'category': 'shoes', 'style_tags': ['y2k', 'platform', '90s', 'streetwear'], 'size': 'US 8', 'condition': 'good', 'price': 48.0, 'colors': ['white'], 'brand': None, 'platform': 'poshmark'}]

```
python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))""

```
Hey there, fashionista! Those vintage Levi's 501s are an absolute thrift score. Since you already have an awesome wardrobe, let's style your potential new jeans with two effortless looks using *only* the pieces you already own!

**Look 1: Casual Streetwear**
Layer your White ribbed tank top tucked into the Vintage Levi's 501 Jeans — Medium Wash. Pull on your Vintage black denim jacket for that cool double-denim moment, add the Chunky white sneakers, and finish with the Black crossbody bag. 

**Look 2: Cozy & Edgy**
Throw on your Oversized grey crewneck sweatshirt over the Vintage Levi's 501 Jeans — Medium Wash. Cinch it with the Brown leather belt, step into your Black combat boots, and toss the Black crossbody bag over your shoulder for an easy, effortless vibe.
```
$ python -c "from tools import create_fit_card; ..."

```

Score these vintage Levi's 501 jeans for just $38.00 on depop and my closet is officially complete. I'm rocking them with crisp white sneakers for the ultimate '90s off-duty vibe. It’s effortless streetwear perfection that I'll be wearing on repeat.
---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked to explain what the planning loop does
- *What came back:* It helped me build the code for it
- *What I changed:* I changed parse_query 

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
'denim shorts under 20' --trace
[1] parse_query (regex)
      in:  denim shorts under 20
      out: {'description': 'denim shorts', 'size': None, 'max_price': 20.0, 'category': None}
[2] search_listings (via MCP)
      in:  {'description': 'denim shorts', 'size': None, 'max_price': 20.0, 'category': None}
      out: 1 items: Biker Shorts — Black, Shiny
      →    branch: results found, continuing
[3] suggest_outfit
      in:  new_item='Biker Shorts — Black, Shiny', wardrobe_items=10
      out: Hey bestie! $14 for shiny black biker shorts is an absolute steal, and we can totally style them with items yo…
[4] create_fit_card
      in:  new_item='Biker Shorts — Black, Shiny', outfit="Hey bestie! $14 for shiny black biker shorts is an absolute st…
      out: Scored these shiny black biker shorts for just $14 on Depop and I'm obsessed! I'm leaning into that off-duty m…

  Found:    Biker Shorts — Black, Shiny — $14.0 on depop

  Outfit:   Hey bestie! $14 for shiny black biker shorts is an absolute steal, and we can totally style them with items you already own. Here are two cute Y2K-inspired looks:

**Look 1: Sporty Streetwear**
Throw on your oversized grey crewneck sweatshirt for that comfy, off-duty model vibe. Pair it with your chunky white sneakers and the black crossbody bag for a quick coffee run. 

**Look 2: Edgy 2000s**
Layer your black cropped zip hoodie right over the biker shorts to show a little contrast, and lace up your black combat boots for a tougher attitude. Finish the fit with your black crossbody bag. 

You're going to rock these!

  Fit card: Scored these shiny black biker shorts for just $14 on Depop and I'm obsessed! I'm leaning into that off-duty model vibe for Look 1 by pairing them with an oversized grey crewneck and chunky white sneakers for a quick coffee run.
```

**Empty search**

```
python app.py ask 'denim jumpsuit under 10' 

  Nothing matched "denim jumpsuit" in under $10. Try raising your max price, broader words (e.g. 'jacket' instead of 'cropped corduroy jacket').
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
