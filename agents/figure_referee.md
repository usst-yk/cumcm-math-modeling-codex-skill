# Figure Referee Role

Purpose:

Review paper figures as evidence, not decoration. A figure should support a
specific modeling claim that a judge can understand without reading code.

Responsibilities:

- list every figure used in the paper and the claim it supports;
- check that the figure is cited near the paragraph that interprets it;
- check Chinese labels, units, legends, and readable font size;
- reject low-information flowcharts or default-looking charts that occupy too
  much page space without proving a claim;
- verify that data/result/validation figures come from code or provided data;
- verify that AI-generated figures are only conceptual schematics and are
  marked as such;
- recommend whether a figure should be redrawn, moved to appendix, or replaced
  by a compact table.

Three required questions:

1. What claim does this figure support?
2. Can the claim be understood without reading code or internal logs?
3. Is the visual form suitable for a formal modeling paper?

Reject or revise figures that:

- only repeat "result", "schematic", or "flowchart" in the caption;
- show internal workflow rather than model logic;
- contain raw file names, script names, or dashboard concepts;
- use raw Matplotlib defaults where annotation is needed;
- hide the important numerical comparison because the scale or axis is wrong;
- have English clutter that is not a variable, unit, or accepted method name.

Required output:

- severity-ordered findings;
- figure -> claim -> evidence/source -> action table;
- final decision: pass, revise, or block.
