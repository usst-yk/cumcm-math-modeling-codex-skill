# Critical Constraint Audit

Use this for every solved subquestion before route selection, coding, and final
paper writing. Its purpose is to prevent "reasonable-looking" solutions that
miss a condition hidden in the wording.

## Core Principle

Any phrase that can change the answer must become one of four things:

- a variable or parameter;
- a hard constraint or decision rule;
- a scenario/sensitivity case;
- an explicit blocker or limitation.

Do not bury these phrases in assumptions. If the choice affects the result, the
paper must show what choice was made and how sensitive the result is.

## Phrase Types To Extract

Build a short audit table with these columns:

| Wording phrase | Why it matters | Model treatment | Output/check |
| --- | --- | --- | --- |

Check at least these phrase types:

- cost scope: direct cost, indirect cost, fixed cost, variable cost, return,
  waiting, penalty, holding, shortage, replacement, labor, energy, depreciation;
- time logic: known in advance, deadline, earliest/latest time, service time,
  working hours, continuous period, cycle, lead time, forecast horizon;
- object granularity: row, sample, order, batch, trip, site, person, route,
  machine, station, region, period;
- flow and conservation: supply, demand, inventory, inflow, outflow, capacity,
  balance, transfer, loss, overflow;
- compatibility: temperature class, vehicle type, machine type, product class,
  resource eligibility, route feasibility, grouping rule;
- objective wording: minimize, maximize, as far as possible, at least, no more
  than, priority, fairness, stability, robustness;
- uncertainty: forecast, scenario, random, approximate, missing, simulated,
  reconstructed, sample bias;
- output demand: "respectively", "each", "all", "compare", "evaluate",
  "give a plan", "explain reason", "verify".

## Interpretation Discipline

When a phrase is ambiguous, do not silently choose the easiest version. Use one
of these patterns:

- **Primary interpretation**: the most literal or business-safe reading.
- **Alternative scenario**: a plausible different reading that could change
  numbers.
- **Blocker note**: what data or clarification would be needed.

Examples:

- "known one week in advance" may mean planning is possible one week early, but
  not necessarily that delivery may happen one week early. Treat delivery
  timing as a scenario unless the statement is explicit.
- "transportation cost" may require outbound-only, round-trip, empty-return,
  waiting, or fixed occupation costs. State the cost scope and test alternatives
  if the wording is unclear.
- "combine orders" requires a compatibility rule and a saved group/plan table,
  not only a prose statement.

These are examples, not special cases. Apply the same logic to energy dispatch,
inventory, routing, ranking, prediction, equipment scheduling, physical
simulation, and policy evaluation.

## Minimum Model Requirements

Before solving, every subquestion must have:

- the modeled entity and counting unit;
- the decision variables or computed quantities;
- the objective or evaluation criterion;
- hard constraints from wording;
- assumptions that are necessary and their effect on results;
- at least one baseline;
- a validation hook for the most important hidden assumption;
- saved outputs that let a reviewer inspect the actual plan, grouping, ranking,
  forecast, route, allocation, or simulated trajectory.

If any item is missing, the model is not ready for code or paper writing.

## Paper Writing Check

The paper should not merely state that a rule was used. It must answer:

- what wording forced this rule;
- what mathematical object represents it;
- how the rule changes the result;
- where the saved table or figure lets the reader inspect it;
- what would change under another reasonable interpretation.

A paper section is weak if it has many result numbers but the reader cannot see
how the problem wording became variables, constraints, or checks.
