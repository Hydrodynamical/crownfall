# CROWNFALL — Design Notes

*How the game was designed, why the key calls were made, and what to watch in playtesting.*

---

## The Cost Debate — Resolved: implicit costs, no mana

You were debating whether cards should have costs. The answer this design lands on: **yes, everything has a cost — but the currency is health, not a separate resource.**

Because health = cards in your possession (your constraint #5), every card committed to the table is already a fraction of your life wagered. Adding a mana-style system would **double-tax the one resource the game is about** and dilute the load-bearing health constraint. Instead, every price in Crownfall is denominated in cards-off-your-life-total:

| Priced action | Its cost in blood |
|---|---|
| Winning a battle | exactly 1 augment, spent to your own Wounds |
| Losing a battle | your entire stack + a permanently dead agent |
| Retreating from a Challenge | 1 augment toll (lone agents flee free) |
| Ignoring a Strike | wounds equal to the striker's stack size |
| Hoarding / inaction | the Bleed clock: 1 wound, then 2 per turn once your deck empties |

Committing, losing, hoarding, and fleeing are all the same economy. Every decision every turn is a costed decision, with **zero added rule weight and no second currency to teach**. Notably, all four independent designers in the design fan-out reached this same conclusion from different angles — the strongest signal in the whole process.

## The Process

Four designers drafted complete independent rulesets under your constraints, each with a different obsession:

| Candidate | Angle | Judge total (3 judges × 5 dims × 10) |
|---|---|---|
| Court of Knives | economy purism — deck as unified resource | 111 |
| Ante Mortem | poker brain — betting, folding, reads | 113 |
| Cloak & Crown | class fantasy — 16 distinct agents, suit-pair drafting | 110 |
| **CROWNFALL** | **tournament balance — airtight math, anti-stall clocks** | **131 — unanimous winner (3/3 votes)** |

Judges (a veteran player, a designer, and a rules referee) then nominated **grafts** — the best ideas from the losers — and a three-lens red team (degenerate-strategy hunter, rules lawyer, playtest simulator) filed **25 issues, 5 critical**, against the winning draft. The final ruleset fixes all of them.

## The Critical Fixes (what almost broke the game)

1. **The economy inversion (worst bug).** The draft made a battle's winner spend *all* augments — so winning a big fight cost more health than losing a small one. Tall stacks were self-executions and half the rank table was a trap. **Fix:** winner spends **exactly one** augment, chooser's pick. Victory stays blood-priced (the cost thesis survives) but Jacks, aggression, and blocking are real again.
2. **The stall clock ran backwards.** As drafted, the *second* player bled out first, so the first player could turtle to victory. **Fix:** the first player draws from turn 1 but gets a 1-action, no-attack first turn — now the first player's deck empties first, and passivity always loses for whoever moved first.
3. **The Ace chip loop.** Lone Aces could Strike forever — unchallengeable at favorable math, unrevealable, no downside — deleting the bluff game. **Fix:** unblocked strikers **stay deployed** and exposed to Challenge, and the Raise lets a naked King — or a Queen or Jack with a big-enough raise — execute a bare Ace on the spot.
4. **Diamonds negated the cost model** (win battles for literally free, forever). **Fix:** with the one-spend baseline, the Exchange's "spend nothing" is worth exactly +1 card per win — the same magnitude as Spades' bonus wound and Hearts' retrieval — and is priced by full disclosure of the revealed augments.
5. **Death-timing paradoxes.** "13th wound = instant loss" collided with battles that wound both players mid-resolution. **Fix:** a battle resolves as one simultaneous step, death is checked after (so Hearts can save you at 12), and simultaneous defeat goes to fewer wounds, then to the **active** player — rewarding whoever moves in the late game.

## Grafts Taken from the Losing Designs

- **The Raise** (from *Ante Mortem*) — the pre-reveal betting round. Three sentences of rules; all three judges asked for it. It's the poker moment.
- **King's Decree** (from *Ante Mortem*) — Kings force the call; serial bluffers get punished; priced by self-revelation.
- **Retreat pays a toll** (from *Cloak & Crown*) — battles can't be refused for free, keeping known-strong stacks mortal.
- **Ace tie-survival** (from *Cloak & Crown*) — one sentence of pure identity for the lone blade.
- **The audit rule** (from *Court of Knives* / the referee judge) — all counts public on request; the information game stays bounded and honest.
- **The Court Draft variant** (from *Cloak & Crown*) — suits as *chosen* classes, with a 1-2-1 snake to fix draft-order advantage.

**Grafts declined:** Diamond card-theft (breaks the clean "you always own 26 cards" health invariant), a second King aura (bloat), Loyalty-scaling suit powers (asymmetric complexity).

## Why It's Balanced (the intended good strategies)

The aesthetic goal was several *shapes* of good play, each beautiful, none dominant:

- **The Lean Duelist** — naked Aces and one-augment Kings that win reveals by 1-3 points. Minimal blood staked, maximal information denied.
- **Legion Aggro (♠)** — trade constantly; every win compounds with the extra wound. Beats turtles, bleeds against Diamonds' economy.
- **Cloister Attrition (♥)** — fight *often but small*, recycling wounds back to hand. The only deck that walks the Bleed clock backwards.
- **Exchange Tempo (♦)** — win cheap, rebuild instantly, out-resource everyone. Priced in disclosure: the table learns your cards.
- **Veil Control (♣)** — peek, then Challenge exactly the stacks you can beat and Strike exactly where they're weak. Information as a weapon.
- **The Bluff Wall** — garbage stacks that Strike for real chip damage. Kept honest by Challenges, the Decree, and retreat tolls.

Anti-degeneracy guarantees: hoarding loses to the escalating Bleed; every battle except an Ace-versus-Ace tie permanently kills an agent (16 total, so the game converges); stalemates are impossible; and overkill is pointless because winning by 30 costs the same one augment as winning by 1 — so the *smallest sufficient force* is always the elegant and the correct play.

## Open Questions for Playtesting

1. **Loyalty at +2** makes suit-matching a real arming decision and the rank ceilings exactly 14/25/35/44. If suit-stacking dominates, try +1.
2. **Bleed at 1-then-2.** If games outrun 30 minutes, escalate 1-2-3; if too fast, flat 1.
3. **First-turn handicap** (1 action, no attack). Watch win rates by seat over ~10 games.
4. **Hearts power rate.** It requires a spent augment and can't retrieve the card just spent — if Hearts still over-sustains, restrict retrieval to cards ≤5.
5. **The Court Draft** changes Loyalty availability dramatically (all 9 of your suit's augments). Confirm the 1-2-1 snake compensates for first pick.
