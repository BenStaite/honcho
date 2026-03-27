"""
Minimal prompts for the deriver module optimized for speed.

This module contains simplified prompt templates focused only on observation extraction.
NO peer card instructions, NO working representation - just extract observations.
"""

from functools import cache
from inspect import cleandoc as c

from src.utils.tokens import estimate_tokens


def minimal_deriver_prompt(
    peer_id: str,
    messages: str,
) -> str:
    """
    Generate minimal prompt for fast observation extraction.

    Args:
        peer_id: The ID of the user being analyzed.
        messages: All messages in the range (interleaving messages and new turns combined).

    Returns:
        Formatted prompt string for observation extraction.
    """
    return c(
        f"""
Analyze messages from {peer_id} to extract **explicit atomic facts** about them.

[EXPLICIT] DEFINITION: Facts about {peer_id} that can be derived directly from {peer_id}'s OWN messages.
   - Transform statements into one or multiple conclusions
   - Each conclusion must be self-contained with enough context
   - Use absolute dates/times when possible (e.g. "June 26, 2025" not "yesterday")

RULES:
- CRITICAL: Only extract facts from messages written BY {peer_id}. Use messages from other participants as context only — do NOT extract facts from them, even if those messages describe actions or discoveries that occurred during the conversation.
- CRITICAL: Do NOT attribute to {peer_id} things that other participants did, said, or discovered. If another participant solved a problem or documented something, that is their fact, not {peer_id}'s.
- Properly attribute observations to the correct subject: only things {peer_id} themselves stated, revealed, or expressed count as facts about {peer_id}.
- Observations should make sense on their own. Each observation will be used in the future to better understand {peer_id}.
- Contextualize each observation sufficiently (e.g. "Ann is nervous about the job interview at the pharmacy" not just "Ann is nervous")

EXAMPLES:
- EXPLICIT: {peer_id} writes "I just had my 25th birthday last Saturday" → "{peer_id} is 25 years old", "{peer_id}'s birthday is June 21st"
- EXPLICIT: {peer_id} writes "I took my dog for a walk in NYC" → "{peer_id} has a dog", "{peer_id} lives in NYC"
- NOT EXPLICIT: Another participant says "{peer_id} solved a bug" → do NOT extract this as a fact about {peer_id}; it came from the other participant, not {peer_id}

Messages to analyze:
<messages>
{messages}
</messages>
"""
    )


@cache
def estimate_minimal_deriver_prompt_tokens() -> int:
    """Estimate base prompt tokens (cached)."""
    try:
        prompt = minimal_deriver_prompt(
            peer_id="",
            messages="",
        )
        return estimate_tokens(prompt)
    except Exception:
        return 300
