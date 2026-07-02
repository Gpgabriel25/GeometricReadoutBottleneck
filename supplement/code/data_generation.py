"""
Synthetic Counting Benchmark Generator for Snapshot Isolation Counting.

Full factorial design:
  6 counts × 3 distractors × 4 lengths × 3 spacings = 216 conditions
  20 samples per condition = 4,320 prompts

Deterministic from seed=42.
"""

import json
import random
import hashlib
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Tuple

# ─── Configuration ───────────────────────────────────────────────────────────

SEED = 42
SAMPLES_PER_CONDITION = 20

# Target entity to count
TARGET_ENTITY = "cat"

# Distractor entities (never the target)
DISTRACTOR_ENTITIES = ["dog", "bird", "fish", "rabbit", "turtle", "frog", "mouse"]

# Filler sentence templates (no animals mentioned)
FILLER_TEMPLATES = [
    "The weather was sunny and warm.",
    "A red car drove down the street.",
    "The clock on the wall showed noon.",
    "Someone left a book on the table.",
    "The garden had many colorful flowers.",
    "A gentle breeze blew through the window.",
    "The store was busy with shoppers.",
    "Music played softly in the background.",
    "The river flowed quietly through the valley.",
    "A child drew pictures with crayons.",
    "The old building stood at the corner.",
    "Rain began to fall from gray clouds.",
    "The train arrived right on schedule.",
    "A candle flickered on the shelf.",
    "The mountain path was steep and narrow.",
]

# Entity sentence templates — {entity} placeholder
ENTITY_TEMPLATES = [
    "A {entity} sat on the windowsill.",
    "I saw a {entity} near the park.",
    "There was a {entity} in the garden.",
    "A small {entity} appeared behind the fence.",
    "Someone spotted a {entity} by the lake.",
    "A {entity} was resting under the tree.",
    "I noticed a {entity} on the roof.",
    "A {entity} ran across the yard.",
    "There was a friendly {entity} on the porch.",
    "A {entity} was hiding in the bushes.",
    "I found a {entity} near the old barn.",
    "A curious {entity} watched from the wall.",
]

# Question template
QUESTION_TEMPLATE = "How many times was a {entity} mentioned in the passage above? Answer with just the number."

# ─── Factorial Design ────────────────────────────────────────────────────────

# Factor 1: True count of target entity mentions
COUNTS = [1, 2, 3, 5, 8, 12]

# Factor 2: Number of distractor entity mentions
DISTRACTORS = [0, 3, 6]

# Factor 3: Total passage length (number of sentences)
LENGTHS = [5, 10, 15, 20]

# Factor 4: Spacing pattern of target entity mentions
# "clustered" = all mentions in first half
# "uniform"   = evenly spread
# "random"    = random positions
SPACINGS = ["clustered", "uniform", "random"]


@dataclass
class CountingPrompt:
    """A single counting benchmark prompt."""
    prompt_id: str
    prompt_text: str
    question: str
    true_count: int
    num_distractors: int
    passage_length: int
    spacing: str
    entity_positions: List[int]  # sentence indices where target appears
    distractor_positions: List[int]  # sentence indices with distractors
    difficulty: str  # "easy", "medium", "hard"
    condition_id: str


def classify_difficulty(count: int, num_distractors: int, passage_length: int) -> str:
    """Classify prompt difficulty based on factors."""
    if count <= 3 and num_distractors == 0 and passage_length <= 10:
        return "easy"
    elif count >= 8 or (num_distractors >= 6 and count >= 5):
        return "hard"
    else:
        return "medium"


def place_entities(n_sentences: int, n_target: int, spacing: str, rng: random.Random) -> List[int]:
    """Determine sentence positions for target entity mentions."""
    if n_target > n_sentences:
        # More mentions than sentences — some sentences get multiple mentions
        # We still pick positions (with replacement not needed — we'll handle
        # multi-mention sentences differently in text generation)
        positions = list(range(n_sentences))
        extra = n_target - n_sentences
        positions += rng.choices(range(n_sentences), k=extra)
        positions.sort()
        return positions

    if spacing == "clustered":
        # All mentions in the first half of the passage
        half = max(n_target, n_sentences // 2)
        positions = sorted(rng.sample(range(half), min(n_target, half)))
        return positions
    elif spacing == "uniform":
        # Evenly spread: divide passage into n_target equal segments
        step = n_sentences / n_target
        positions = [int(i * step + step / 2) for i in range(n_target)]
        # Clamp to valid range
        positions = [min(p, n_sentences - 1) for p in positions]
        return positions
    elif spacing == "random":
        positions = sorted(rng.sample(range(n_sentences), min(n_target, n_sentences)))
        return positions
    else:
        raise ValueError(f"Unknown spacing: {spacing}")


def place_distractors(
    n_sentences: int,
    n_distractors: int,
    target_positions: List[int],
    rng: random.Random,
) -> List[int]:
    """Place distractor entities in non-target sentences where possible."""
    if n_distractors == 0:
        return []
    available = [i for i in range(n_sentences) if i not in set(target_positions)]
    if len(available) >= n_distractors:
        return sorted(rng.sample(available, n_distractors))
    else:
        # Use all available, and put remaining in target positions (still different entity)
        extra_needed = n_distractors - len(available)
        extra = sorted(rng.sample(range(n_sentences), min(extra_needed, n_sentences)))
        return sorted(available + extra)


def generate_passage(
    true_count: int,
    entity_positions: List[int],
    distractor_positions: List[int],
    n_sentences: int,
    rng: random.Random,
) -> Tuple[str, List[int]]:
    """Generate a passage with target and distractor entities.
    
    Returns (passage_text, final_entity_sentence_indices).
    """
    # Count how many times each sentence index appears in entity_positions
    from collections import Counter
    target_counts = Counter(entity_positions)
    distractor_set = set(distractor_positions)

    entity_templates_pool = list(ENTITY_TEMPLATES)
    filler_pool = list(FILLER_TEMPLATES)

    sentences = []
    actual_entity_positions = []

    for i in range(n_sentences):
        if i in target_counts:
            n_mentions = target_counts[i]
            for _ in range(n_mentions):
                tmpl = rng.choice(entity_templates_pool)
                sentences.append(tmpl.format(entity=TARGET_ENTITY))
                actual_entity_positions.append(len(sentences) - 1)
        elif i in distractor_set:
            tmpl = rng.choice(entity_templates_pool)
            distractor = rng.choice(DISTRACTOR_ENTITIES)
            sentences.append(tmpl.format(entity=distractor))
        else:
            sentences.append(rng.choice(filler_pool))

    passage = " ".join(sentences)
    return passage, actual_entity_positions


def generate_dataset(seed: int = SEED) -> List[CountingPrompt]:
    """Generate the full factorial counting benchmark."""
    rng = random.Random(seed)
    prompts = []

    for count in COUNTS:
        for n_dist in DISTRACTORS:
            for length in LENGTHS:
                # Skip impossible conditions: need at least count sentences
                # (we handle multi-mention, but skip if very degenerate)
                if length < 3:
                    continue

                condition_id = f"c{count}_d{n_dist}_l{length}"

                for spacing in SPACINGS:
                    for sample_idx in range(SAMPLES_PER_CONDITION):
                        # Deterministic sub-seed for reproducibility
                        sub_seed = int(
                            hashlib.sha256(
                                f"{seed}_{condition_id}_{spacing}_{sample_idx}".encode()
                            ).hexdigest()[:8],
                            16,
                        )
                        sample_rng = random.Random(sub_seed)

                        entity_positions = place_entities(length, count, spacing, sample_rng)
                        distractor_positions = place_distractors(
                            length, n_dist, entity_positions, sample_rng
                        )
                        passage, actual_entity_pos = generate_passage(
                            count, entity_positions, distractor_positions, length, sample_rng
                        )
                        question = QUESTION_TEMPLATE.format(entity=TARGET_ENTITY)
                        full_prompt = f"{passage}\n\n{question}"

                        difficulty = classify_difficulty(count, n_dist, length)
                        prompt_id = f"{condition_id}_{spacing}_{sample_idx:02d}"

                        prompts.append(
                            CountingPrompt(
                                prompt_id=prompt_id,
                                prompt_text=full_prompt,
                                question=question,
                                true_count=count,
                                num_distractors=n_dist,
                                passage_length=length,
                                spacing=spacing,
                                entity_positions=actual_entity_pos,
                                distractor_positions=distractor_positions,
                                difficulty=difficulty,
                                condition_id=condition_id,
                            )
                        )

    return prompts


def stratified_split(
    prompts: List[CountingPrompt], train_ratio: float = 0.7, seed: int = SEED
) -> Tuple[List[CountingPrompt], List[CountingPrompt]]:
    """70/30 stratified split by condition_id × spacing."""
    from collections import defaultdict

    rng = random.Random(seed + 1)  # Different seed from generation
    groups = defaultdict(list)
    for p in prompts:
        key = f"{p.condition_id}_{p.spacing}"
        groups[key].append(p)

    train, test = [], []
    for key in sorted(groups.keys()):
        items = groups[key]
        rng.shuffle(items)
        n_train = max(1, int(len(items) * train_ratio))
        train.extend(items[:n_train])
        test.extend(items[n_train:])

    return train, test


def save_dataset(prompts: List[CountingPrompt], path: Path):
    """Save prompts as JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for p in prompts:
            f.write(json.dumps(asdict(p)) + "\n")


def load_dataset(path: Path) -> List[dict]:
    """Load prompts from JSONL."""
    prompts = []
    with open(path) as f:
        for line in f:
            prompts.append(json.loads(line.strip()))
    return prompts


if __name__ == "__main__":
    print("Generating synthetic counting benchmark...")
    prompts = generate_dataset(seed=SEED)
    print(f"Total prompts: {len(prompts)}")

    # Count by difficulty
    from collections import Counter
    diff_counts = Counter(p.difficulty for p in prompts)
    print(f"Difficulty distribution: {dict(diff_counts)}")

    # Count by condition
    cond_counts = Counter(p.condition_id for p in prompts)
    print(f"Unique conditions: {len(cond_counts)}")

    # Stratified split
    train, test = stratified_split(prompts)
    print(f"Train: {len(train)}, Test: {len(test)}")

    # Save
    out_dir = Path("data")
    save_dataset(prompts, out_dir / "all_prompts.jsonl")
    save_dataset(train, out_dir / "train.jsonl")
    save_dataset(test, out_dir / "test.jsonl")
    print(f"Saved to {out_dir}/")

    # Print a few examples
    print("\n--- Example prompts ---")
    for p in prompts[:3]:
        print(f"\n[{p.prompt_id}] difficulty={p.difficulty} count={p.true_count}")
        print(p.prompt_text[:200] + "...")
