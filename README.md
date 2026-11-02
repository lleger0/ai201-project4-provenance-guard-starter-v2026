# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->
<!-- detector.model_signal
stylometry.style_signal(text) - like what is stylometry?
scoring.combine_signals(...)
scoring.score_to_label(...)
Audit
Go through stylometry, detector -->
This is what the model will do step by step.
1. Recieve the text
2. Use detector.py - Determine how much AI - model score - perplexity score - judges whether the next word is predictable
3. Use Stlyometry. see the sentence spread, punctuation
4. Combine detector and stylometry into a confidence score
5. Using the confidence score, label.
6. Audit the results

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** This measures perplexity which means how likely each word is. The AI asks itself if it could have written the text.

**Why that might differ between human and AI writing:** Humans are more likely to be unpredictable when they are writing. Often so they might use a word or phrase that an AI wouldn't even think of using.

**What it can't see:** If a human decides to write simplistically, it can be mistake for AI. The other issue is if an AI is instructured to use rare words in its generation. In that case the perplexity score would score it as human even though its not.

### Signal two — the style signal

**What it measures:** The style measure sentence length spread, type token ratio (how much of the vocabulary repeats), and punctuation density. It is not capable of reading the text but is instead grading it based on sentence structue.

**Why that might differ between human and AI writing:** Human writing is unpredictable. A human could have a 3 word sentence next to a 40 word sentence in one pareagraph of text. AI would write in a more structured fashion.

**What it can't see:** Since it cannot read, if the sentence structure makes it thinks that it is AI that is what it will set it as. Even if the text has typos, direct quotes from other sources, etc, that will not change its verdict.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? 
     
     My Thoughts:

     If one of the signals is really high then the text should be labeled as AI.
     Really high would mean a score of over 0.8. Like I think that if one of them is high then that would mean that maybe they see somethign the other one doesn't see.

     If both scores are high then that is 100% AI

     But maybe in the end just taking the average is still the better option?
     How do I accurately combine the scores?

     Maybe if one score is high then that score could be weighted?
     so like (low +high.0.5)//2 ?

     But what I just sait values the AI accusation more.....
     I want to weight towards the human guess. I don't want to falsely accuse humans of AI

     For now the numbers will 0.7 and 0.3
     Maybe later I'll change them to 0.6 and 0.4

     
     -->

**The rule:** The combining score will lean towards a human verdict. Which ever signal has the more human verdict will recieve the weight.

**The numbers:** The number that leans human will have a weight of 0.7. The number that leans towards AI will have a weight of 0.3.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:** My rule will apply the heavier weight to the signal that leans towards the human verdict.

Input: Model Signal, Style Signal 
Output: Combining Signal


---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.0- 0.4 | This text was written by a human.  |
| unsure | 0.4-0.6 | It is unclear whether this text was written by a human or AI |
| high-confidence AI | 0.6 - 1 | This was definitely written by an AI. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

I've decided to write this in plain english. The way I worded it leaves no room for bias nor accusation.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

Before building stylometry

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json
{
  "confidence": 0.3092,
  "content_id": "hardcoded",
  "creator_id": "me",
  "guess": "unsure",
  "label": "not built yet",
  "model_score": 0.3092,
  "style_score": null
}

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json
{
  "evidence": {
    "content_id": "c_2d2ae002675a",
    "creator_id": "demo_instructor",
    "event": "appeal",
    "reasoning": "I dont remember but Im pretty sure its human",
    "status": "under_review",
    "timestamp": "2026-11-02T04:16:56+00:00"
  },
  "message": "Your appeal has been entered."
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
 {
      "combined_score": null,
      "confidence": 0.20544225836726754,
      "content_id": "c_2d2ae002675a",
      "creator_id": "demo_instructor",
      "guess": null,
      "label": [
        "high-confidence human",
        "This text was written by a human."
      ],
      "model_score": 0.2782,
      "status": "decided",
      "style_score": 0.7204817224484503,
      "timestamp": "2026-11-02T02:23:58+00:00"
    },
    {
      "content_id": "c_2d2ae002675a",
      "creator_id": "demo_instructor",
      "event": "appeal",
      "reasoning": "I dont remember but Im pretty sure its human",
      "status": "under_review",
      "timestamp": "2026-11-02T04:16:56+00:00"
    },
```

---

## How I Used AI

I did not use AI for this unit.

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
