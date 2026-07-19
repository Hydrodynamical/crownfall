# CROWNFALL — AI Playtest Report

*A rules-faithful simulator ([simulator.py](simulator.py)) played two heuristic AIs against each other — one featured narrated game plus 4,000 games of balance statistics. Full omniscient log of the featured game: [playtest-log.txt](playtest-log.txt).*

---

## The Players

Both AIs decide using only information legally visible to them (own cards, public wounds piles, stack sizes, decreed agents, Veil peeks). They differ in temperament:

| | **Rook** — aggressive tempo | **Vesper** — patient value |
|---|---|---|
| Challenges when win odds exceed | 56% | 64% |
| Blocks strikes when win odds exceed | 50% | 58% |
| Retreats when win odds fall below | 42% | 48% |
| Overall bias | attacks 1.25× more | builds and holds |

## Featured Game — Seed 207: *The War of Attrition That Ate Its Own Court*

**23 turns · 4 battles · 4 retreats · 6 lead changes · ends in simultaneous defeat, 13 wounds to 14.**

**Act I — The bully and the engine (turns 1–10).** Rook opens with J♠ and arms it to a lean 28. His J♣ muster triggers the Veil: he peeks Vesper's 2-stack and sees **J♦** — a warlord under construction. Vesper, meanwhile, is assembling something beautiful: **J♦ + 10♦ + 9♦, an all-diamond 34** with full Loyalty. Rook's answer is pure tempo: his J♠ stack challenges Vesper's *other*, half-built stacks three turns running. She retreats every time — paying **10♣, then 9♠, then 8♥** in tolls. Three wounds inflicted and Rook never showed a card.

**Act II — The Exchange never pays (turns 11–19).** Rook finally cashes his bluff: his 4-card J♣ tower strikes, Vesper blocks with the diamond engine — **34 beats 32**. And because the Exchange spends nothing, her entire stack returns to hand, ready to do it again. It does: the diamond engine wins **three battles** this game (34–32, 34–28, 34–29), killing J♣, J♠, and Q♦ — a third of Rook's court — while spending *zero* cards. The catch, exactly as designed: after each win Rook has seen her cards, and her rebuild costs tempo. Rook spends that tempo on unblocked strikes — 5 chip wounds — and the score seesaws: six lead changes.

**Act III — The hoarder's bill comes due (turns 20–23).** Vesper's patience has a price: her hand has swollen to **17 cards, but her deck is gone**. The Bleed clock starts: 1 wound, then 2 — and blind hand pulls execute her **A♠, Q♣, and A♣**. Three agents dead without a fight. At turn 23, Rook (10 wounds) throws his last real punch: **Q♥+8♣+9♥ = 31** into Vesper's fresh diamond stack — **J♦+9♦+7♦ = 31. TIE.** Both stacks are destroyed entirely. Rook lands on exactly 13 wounds; Vesper on 14. Both dead after the battle resolves — **simultaneous defeat: fewer wounds wins. Rook takes it by a single card.**

*Playtest verdict: the game's three core tensions — bluff vs. call, spend vs. hoard, lean vs. tall — all decided this game, and the obscure simultaneous-defeat rule earned its keep on the final turn.*

## Balance Statistics (4,000 games)

**Seat advantage — the first-turn handicap works.** In mirror matches (identical AIs), seat 1 wins almost exactly half:

| Battery (1,000 games each) | First player wins |
|---|---|
| Rook vs Rook | 49.9% |
| Vesper vs Vesper | 50.0% |
| Rook (seat 1) vs Vesper | 53.8% |
| Vesper (seat 1) vs Rook | 41.1% |

**Style advantage — aggression is favored but not dominant.** Rook beats Vesper ~56% overall (53.8% from seat 1, 58.9% from seat 2). This matches the design thesis: when cards are health, passivity must never be the best line — but a 56/44 split leaves patient play entirely viable, and better heuristics could close it.

**Pace and endings:**

| Metric | Value |
|---|---|
| Game length | mean ~16 turns (≈15–25 minutes at the table), min 9, max 27 |
| Win by 13 wounds | ~98.5% |
| Win by simultaneous-defeat tiebreak | ~1.5% |
| Win by agent extinction | ~0% (exists as a threat, not a route) |
| Battles per game | 2.4–2.8 |
| Strikes taken vs blocked | ≈ 1.5 vs 1.6 — a genuine call-or-fold equilibrium |
| Retreats per game | 1.4–2.5 (patient players retreat less; they build stronger before deploying) |
| Bleed wounds per game | ~0.3 (the clock threatens more than it fires — as intended) |

**Suit powers all pull their weight per game:** Veil peeks ~1.2, Exchange free-wins ~0.6, Cloister heals ~0.4, Legion bonus wounds ~0.6.

**Suit balance (4,000-game deal study):** winners and losers hold statistically near-identical amounts of every suit. The largest edges are tiny — winners average +0.08 more Spades and −0.12 fewer Clubs out of 26 cards (a per-suit win-rate skew on the order of 1–2%). The slight Spade lean and Club dip make sense for AI play: an extra wound per battle win is worth full value to a calculator, while the Veil's information is worth more to a human planner than to these heuristics. No suit is broken in either direction.

## What the Playtest Validated

1. **The card-conservation invariant held for all 4,000 games** — every player owns exactly 26 cards at every audit point; wounds only grow; no rules dead-ends or unplayable states were reached; every game terminated.
2. **The first-turn handicap almost perfectly neutralizes seat advantage** (49.9–50.1% in mirrors).
3. **The bluff economy is real**: unblocked strikes dealt meaningful damage (Rook's 5 chip wounds in the featured game) but calling stayed profitable enough that ~52% of strikes get blocked.
4. **Retreat tolls matter**: Rook's toll-farming line in the featured game (3 wounds with zero reveals) is a legitimate, beatable strategy — the counter (arm faster, block sooner) is exactly the decision the game wants to pose.
5. **Hoarding loses**: Vesper's 17-card hand became three dead agents via blind Bleed pulls — the anti-turtle clock works narratively as well as mathematically.
6. **The code itself was audited against RULES.md** by an independent review pass. It found one rules deviation — the Veil was peeking on *every* muster instead of only each Club agent's first (~30% of peeks were illegal) — which was fixed before the statistics above were produced. The audit also surfaced one genuine hole in the rulebook (simultaneous defeat was only defined for double-13+-wounds, not for a tie battle killing both players' last agents), now patched in RULES.md §10.

## What It Didn't Exercise (watch in human play)

- **King's Decree** fired only ~2% of games — the AI's threshold is conservative; humans will use it for drama. Untested at volume.
- **Recall** was never chosen by either AI — its value is bluff-reset psychology, which heuristics undervalue.
- **Agent extinction** never decided a game — it functions as a constraint on reckless trading, not a win route.
- **Hearts sustain** is the least-triggered suit power (~0.4/game); worth watching whether human Cloister decks feel strong enough.
- **The Ace tie-survival rule** never fired (no Ace-vs-Ace or equal-total-Ace battles occurred in 2,000 audited games) — correct in code, untested in play.
- **Front-sourced wounds** (deck and hand both empty) were never reached — games end before players are that poor.
- **The illegal-stack auto-loss rule** can't be exercised by an AI that never cheats; it exists for human tables only.

## Reproduce It

```bash
python3 simulator.py --seed 207 --verbose      # replay the featured game
python3 simulator.py --stats 1000              # aggregate statistics
python3 simulator.py --scan 1 250              # hunt for dramatic games
```
