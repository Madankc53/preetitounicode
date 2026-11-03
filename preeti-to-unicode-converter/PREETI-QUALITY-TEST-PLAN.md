# Preeti conversion quality test plan

This checklist is the acceptance gate for changes to the Preeti conversion engine. Do not mark a case as passing until its expected Unicode output has been checked against a trusted Preeti reference/sample.

## Test corpus

For every fixture, record:
- Original Preeti input (preserve spaces, punctuation, and line breaks)
- Expected Unicode output, independently verified
- Actual converter output
- Pass/fail result
- Source of the expected output

Required coverage:

- [ ] Basic vowels and consonants
- [ ] Independent vowels and dependent vowel signs (matras)
- [ ] Pre-base i-matra placement, including consecutive combinations
- [ ] Reph and rakar
- [ ] Common conjuncts and half-letters
- [ ] Nasal signs and chandrabindu
- [ ] Visarga, halant, danda, and punctuation
- [ ] Nepali digits and ordinary ASCII digits
- [ ] Spaces, tabs, multiple lines, and paragraph breaks
- [ ] Mixed Nepali and English text
- [ ] Repeated characters and unknown/unmapped input
- [ ] Long pasted passages and file-extracted text

## Functional regression checks

- [ ] Typing and pasting update output without losing input
- [ ] Copy output matches the visible output exactly
- [ ] Clear resets both panels and counters
- [ ] Font size and dark mode do not affect converted text
- [ ] Unicode-to-Preeti is tested separately; do not assume it can reconstruct the original legacy keystrokes
- [ ] TXT upload and DOCX text extraction are checked against the same known fixtures
- [ ] Mobile viewport: input, output, controls, and copy actions remain usable

## Acceptance rule

A mapping or rule change must include at least one regression fixture for the bug it fixes. Never infer correctness from a visually plausible Devanagari result alone. Keep uncertain cases documented as unresolved rather than silently treating them as supported.

## Other legacy fonts

Kantipur and Sagarmatha remain outside the active converter workflow until each has its own independently verified mapping corpus and regression results. Their current mappings are not evidence of verified support.
