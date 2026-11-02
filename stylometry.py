"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. ← TODO

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.
    """
    # TODO: replace this

    # Thought process
    # maybe use a for loop to iterate through each sentence and 
    # obtain the length? should the length be in characters or words? It is in words.
    # sentences() and words() are given to split into sentences and words

    lengths = []
    for i in sentences(text):
        lengths.append(len(words(i)))

    # This only works when there is more than once sentence. I'll have 
    # to do research on standard deviation and variance

   
    # according to google the standard deviation of a single number is 0 since it doesn't deviate

    if len(lengths) == 1:
        return 0

    # standard deviation = expressed in the same unit as the data. variation of values from the mean
    # low standard deviation means values are close to the average

    # my example: "In the event where you have to test a certain amount of text, I ask you to think and wonder to yourself: Was this written by a human or AI? Now let me add another sentence."
    # one sentence is 30, the other is 6. the standard deviation is 16.97

    # if an input only has one sentence then standard deviation shouldn't be used to determine if its AI.
    
    # the lower the standard deviation, the more likely it's AI
    mean = statistics.mean(lengths)
    #print(mean)
    # I think i'll have to compare the standard deviation to the mean to decide if its high right?
    # or should i technically do that right now?
    #print("Standard Deviation / mean")
    #print(statistics.stdev(lengths)/mean) # I think i could return this... It makes sense... I just have to look at the instructions again to make sure.
    return (statistics.stdev(lengths)/mean)
    return(statistics.stdev(lengths))
    
    #return 0.0


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words. ← TODO

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.
    """
    # TODO: replace this

    # unique words over total words
    # make a list or dictionary of common words 
    # common words / total words 
    # 1 - common words / total words = percentage of unique words.

    # another strat could be.... instead of counting the common words i could count the uncommon words then divide that by the total words

    # words are already in lower case
    #for word in words(text):
    from words import get_common_words

    common = get_common_words()
    count = 0
     
    for w in words(text.lower()):
        # time complexity wise.... isn't finding a word better than checking if a word is not somewhere?
        if w in common:
            count +=1

    # the higher amount of uncommon words, the more likely its human
    return 1 - (count/ len(words(text))) # should be the percentage of unique words

    #return 0.0


def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length. ← TODO

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.
    """
    # TODO: replace this

    #print(sentences(text)) # punction is included in sentences.
    
    punc = (re.findall(r"[^\w\s^.]+",text))
    char_count = 0

    for sentence in sentences(text):
        #punc.append(re.findall(r"[^\w\s]+",sentence))
        for character in sentence:
            char_count +=1
            
    #print(len(punc))
    #print(char_count)
    # so what does this score mean? - I guess I would say that perhaps AI is more likely to use more punction. So the higher the score the more likely its AI
    # to be honest let me exclude periods because everybody has to use a period. # like what amount of period usage would be above average? 
    return len(punc)/char_count


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    # TODO: replace this
    # sentence spread should get flipped
    spread = 1-sentence_length_spread(text)
    uniqueness = 1-type_token_ratio(text)
    # I'm going to say that humans have higher punctuation density because an AI is more likely to make it's sentences longer
    punc_density = 1- punctuation_density(text)
    return (spread + uniqueness + punc_density)/ 3
    #return 0.5


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
