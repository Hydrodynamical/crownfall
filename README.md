# CROWNFALL

*A dueling card game for 2 players — Magic: The Gathering's strategy meets poker's bluffing, played with one standard 52-card deck.*

**▶ [Play it in your browser](https://hydrodynamical.github.io/crownfall/)** — offline pass-and-play, two players, one device.
**🎓 [Interactive tutorial](https://hydrodynamical.github.io/crownfall/tutorial.html)** · **⚖ [Web rulebook](https://hydrodynamical.github.io/crownfall/rules.html)**

**Bluff with your blood.** Face cards (A, K, Q, J) are your **agents**. Number cards (2–10) are hidden **augments**. Everything deploys face down; battles reveal, the higher total wins, and the loser's stack becomes **wounds** — because your 26 cards are also your life total. 13 wounds and you're dead. There's no mana: every cost in the game is paid in health.

**2 players · 15–30 minutes · one ordinary deck · teachable in 5 minutes**

## Start Here

| File | What it is |
|---|---|
| [TUTORIAL.md](TUTORIAL.md) | **Learn to play in 10 minutes** — setup, a worked example turn, beginner traps |
| [RULES.md](RULES.md) | The complete rulebook — every rule, edge case, and the Court Draft variant |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | One-page cheat sheet for the table — turn order, combat math, suit powers |
| [SCHEMATIC.md](SCHEMATIC.md) | Table layout, stack anatomy, turn/combat flow diagrams |
| [board-layout.svg](board-layout.svg) | Printable play-mat schematic |
| [MARKETING.md](MARKETING.md) | The pitch — spiel, elevator pitch, back-of-box copy |
| [DESIGN_NOTES.md](DESIGN_NOTES.md) | Why the game is shaped this way: the cost debate resolution, balance fixes, playtest questions |
| [index.html](index.html) | **Offline pass-and-play app** — open in any browser, two players share one device |
| [tutorial.html](tutorial.html) | Visual learn-to-play page — custom court emblems, combat flow, step-through example turn |
| [rules.html](rules.html) | The rulebook as a styled web page with a table of contents |
| [PLAYTEST.md](PLAYTEST.md) | AI playtest report — featured narrated game + 4,000-game balance statistics |
| [simulator.py](simulator.py) | Rules-faithful simulator with two AI players (`--verbose`, `--stats`, `--scan`) |
| [playtest-log.txt](playtest-log.txt) | Full omniscient log of the featured AI game |

## The Rules on One Napkin

1. You own 26 cards: 8 agents (two each of A=14, K=13, Q=12, J=11) and 18 augments (your deck; draw 4 to start). Health = 26 − wounds; **13 wounds = death**.
2. Each turn: **draw 1** (empty deck = Bleed wounds), then **2 actions**: Muster, Arm, Strike, Challenge, or Recall.
3. Stacks are face down. Slots: A holds 0 augments, K 1, Q 2, J 3 — so **stack size leaks rank, never strength**.
4. **Strike** the player (they block, or eat wounds equal to your stack size — no reveal). **Challenge** a stack (they fight, or retreat paying an augment).
5. Battle: one hidden **raise** each, then reveal. Total = agent + pips + 2 per suit-matched augment. Loser's stack → their wounds, agent dead forever. **Winner spends 1 augment too.**
6. Suits are classes: ♠ extra wound on wins · ♥ heal on wins · ♦ spend nothing on wins · ♣ peek on muster.
7. Win at 13 enemy wounds — or when their court has no agents left.
