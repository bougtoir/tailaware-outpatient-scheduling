"""Format and expand numbered citations without implying uncited references."""
import re

CITATION_RE = re.compile(r"\[([1-9]\d*(?:-[1-9]\d*)?(?:,\s*[1-9]\d*(?:-[1-9]\d*)?)*)\]")


def format_citation(numbers):
    groups = []
    for number in sorted(set(numbers)):
        if not groups or number != groups[-1][-1] + 1:
            groups.append([])
        groups[-1].append(number)
    labels = [
        f"{group[0]}-{group[-1]}" if len(group) >= 3
        else ", ".join(str(number) for number in group)
        for group in groups
    ]
    return "[" + ", ".join(labels) + "]"


def cited_numbers(text):
    for match in CITATION_RE.finditer(text):
        numbers = []
        for token in match.group(1).split(","):
            bounds = [int(number) for number in token.strip().split("-")]
            if len(bounds) == 1:
                numbers.append(bounds[0])
            elif bounds[1] >= bounds[0]:
                numbers.extend(range(bounds[0], bounds[1] + 1))
            else:
                raise ValueError(f"Reversed citation range: {match.group(0)}")
        if format_citation(numbers) != match.group(0):
            raise ValueError(f"Noncanonical citation format: {match.group(0)}")
        yield from numbers
