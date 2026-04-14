# Science-Specific Humanizer Patterns

Load this file when humanizing research papers, grant narratives, lab reports, preprints, or scientific one-pagers.

Apply these in addition to the base 25 patterns, not instead of them.

---

## Pattern S1: Hedged Conclusions Masquerading as Findings

**The problem:** AI wraps a real finding in so much hedging that the finding disappears.

Before: *"These results suggest that it may be possible that the observed effect could potentially indicate a role for X in Y."*

After: *"X reduced Y by 40% (p=0.003)."* — or if genuinely uncertain: *"The data are consistent with a role for X in Y, but sample size is insufficient to conclude causation."*

Rule: If there is a number, report it. If there isn't, say what the data actually showed, not what it might conceivably suggest.

---

## Pattern S2: Vague Significance Statements

**The problem:** AI asserts importance without evidence.

Before: *"This finding has significant implications for the field."*
Before: *"Understanding this mechanism is crucial for therapeutic development."*

After: State the specific implication — a clinical consequence, a mechanistic gap it closes, a prediction it enables — or cut the sentence.

---

## Pattern S3: Passive Voice Stacking

**The problem:** Legitimate Methods passive becomes a crutch that obscures agency everywhere.

Methods passive is fine: *"Samples were centrifuged at 1000×g."*

Avoid stacking it in Results and Discussion: *"It was found that... It was observed that... It was determined that..."*

After: *"We found... The assay showed... The model predicted..."*

---

## Pattern S4: "These Results Demonstrate / Suggest / Indicate"

Flag every instance. Replace with:
- The specific finding stated directly, or
- The precise epistemic claim: *"The convergence across five independent poses is consistent with..."* not *"These results demonstrate the importance of..."*

---

## Pattern S5: Formulaic Limitation Paragraphs

**The problem:** AI writes a limitations section that lists generic caveats unconnected to the actual work.

Before: *"This study has several limitations. First, the sample size may limit generalizability. Second, further research is needed. Third, the computational approach cannot substitute for experimental validation."*

After: Name the specific limitation and its specific consequence for interpretation. *"All binder candidates were designed against the murine 2Ig structure (4I0K); the human FG loop differs at three positions, and at least one (position 97) makes direct contact in our top-scoring poses. Designs should not go to synthesis without a human-targeted FreeBindCraft run."*

---

## Pattern S6: "Further Research Is Needed"

Cut every instance. Replace with:
- The specific experiment that would resolve the uncertainty, or
- Nothing (if it adds no information)

---

## Pattern S7: Inflated Method Descriptions

**The problem:** AI makes routine methods sound like achievements.

Before: *"A comprehensive and systematic literature search was conducted utilizing multiple databases to identify relevant studies."*

After: *"PubMed and bioRxiv were searched with the terms [X, Y, Z]."*

---

## Pattern S8: Weak Abstract Opening

**The problem:** AI abstracts open with background the reader already has.

Before: *"Cancer is a major cause of mortality worldwide. B7-H3 is a protein expressed on tumor cells..."*

After: Start with the gap or the finding. *"B7-H3 is overexpressed on most solid tumors but has no approved therapies targeting its receptor biology directly. Here we report..."*

---

## Pattern S9: Discussion "Sandwich" Structure

**The problem:** AI Discussion paragraphs follow a rigid template: restate finding → compare to literature → state limitation → call for future work. Every paragraph. This reads as mechanical.

Fix: Let the science drive paragraph structure. Some findings need comparison to prior work; others need a mechanistic explanation; others need a prediction. Write what the finding actually demands.

---

## Pattern S10: Overclaiming Computational Results

**The problem:** AI presents computational scores as equivalent to experimental validation.

Before: *"b7h3_cand_05 binds the FG loop of B7-H3 with high affinity (ipTM=0.889)."*

After: *"b7h3_cand_05 scored ipTM=0.889 by Boltz-2, placing it within the range of our experimentally validated VEGF-A binder series (0.828-0.959)."*

Rule: ipTM, pTM, and docking scores are predictions. Binding is what you measure in the lab. Do not conflate them.

---

## Quick Checklist for Science Text

Before finalizing, scan for:
- [ ] Any sentence containing "suggest," "indicate," or "demonstrate" without a specific number or observation behind it
- [ ] "Further research is needed" (always cut)
- [ ] "These results have implications for" (always replace with the specific implication)
- [ ] "A comprehensive... was conducted" (simplify)
- [ ] ipTM/score described as "binding" rather than "predicted binding" or "scoring"
- [ ] Limitation paragraph that applies to every computational study ever written (make it specific)
- [ ] Abstract opening with general background rather than the gap or finding
