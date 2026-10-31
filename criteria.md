# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

  <!-- I'm assuming that each test will be one text that will be run 3 times. 
  
      But it is 10 pieces of writings. So I should write criteria regarding that number as well.

      Will all 10 pieces be human written 

      So I think all 10 is human written so all the tests will be against human text.
      Is that a fair way to test this model though? Should it also be tested with AI generated text?

      I'm not sure how tohe appeal system would work.....
  
  -->

---
## 1. At most only 2/10 of my written writings will be labeled as AI

<!-- Your criterion. It must name a number. -->



**Why this target:** I want my model to prevent false positives. I'll allow 2 false positives in case of error. This means that the model should have a rate of being 80% correnct.



---

## 2. An AI text should be labeled AI in 2/3 tries.

<!-- Your criterion. --> 



**Why this target:**  This is to ensure the model correctly labels an AI text as AI most of the time



---

## 3. Properly handles invalid inputs in 3/3 tries

<!-- Your criterion. -->



**Why this target:** This is to ensure that invalid inputs such as empty text is not accepted as input.



---

## 4. Appeals changes label of a post to under review.

<!-- Your criterion. -->



**Why this target:** This is to ensure that the appeal function is working properly. 



---

## 5. All labels are reachable. 

<!-- Your criterion. -->



**Why this target:** This is to ensure that mislabeling is not occurring due to no access to a label.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
