# CROWNFALL — Table Schematic & Flow Diagrams

*A visual companion to [RULES.md](RULES.md). Printable SVG play mat: [board-layout.svg](board-layout.svg).*

---

## 1. The Play Mat

```
                          ═══════ OPPONENT'S SIDE ═══════

      [ DECK ]           [ HAND — private, no limit ]          [ WOUNDS ]
      face down             agents + augments, hidden           FACE  UP
      draw 1/turn                                               13 = death

      ┌─────────┐         ┌─────────┐         ┌─────────┐
      │ STACK 1 │         │ STACK 2 │         │ STACK 3 │   ←  FRONT
      │  ????   │         │  ????   │         │  ????   │      (max 3)
      └─────────┘         └─────────┘         └─────────┘
        3 cards             1 card              2 cards
      "Q or J..."         "Ace? bluff?"       "K, Q or J"

    ═══════════════════════ THE BATTLEFIELD ═══════════════════════
         STRIKE → attacks the player     CHALLENGE → attacks a stack

      ┌─────────┐         ┌─────────┐         ┌─────────┐
      │ STACK 1 │         │ STACK 2 │         │ STACK 3 │   ←  FRONT
      │  ????   │         │  ????   │         │  ????   │      (max 3)
      └─────────┘         └─────────┘         └─────────┘
       agent on top, augments tucked under, ALL face down
       card COUNT is always public — contents never

      [ DECK ]           [ HAND — private, no limit ]          [ WOUNDS ]
      face down             agents + augments, hidden           FACE  UP

                            ═══════ YOUR SIDE ═══════
```

### Zone glossary

| Zone | Face | Public info | Purpose |
|---|---|---|---|
| **Deck** | down | card count | 18 augments dealt (14 left after the opening draw); mandatory draw each turn; empty deck = Bleed |
| **Hand** | hidden | card count | agents + augments; no size limit; wounds pull from it blind when deck is gone |
| **Front** | down | count & size of each stack | up to 3 stacks; where all fighting happens |
| **Wounds** | **up** | everything | your damage, your death clock (13 = dead), and everyone's card-counting ledger |

**The invariant:** every one of your 26 cards is always in exactly one of these four zones. Health = 26 − wounds. Nothing ever changes owners.

## 2. Anatomy of a Stack

```
        ┌──────────────┐
        │   AGENT      │  ← face down on top   (A=14 · K=13 · Q=12 · J=11)
        │ ┌──────────────┐
        └─│   AUGMENT    │  ← face down beneath (2–10, adds its pips)
          │ ┌──────────────┐
          └─│   AUGMENT    │  ← +2 Loyalty each if it matches agent's suit
            └──────────────┘
                              SLOTS:  A holds 0 · K holds 1 · Q holds 2 · J holds 3

   SIZE IS PUBLIC, CONTENTS ARE NOT:
   4 cards → certainly a Jack          2 cards → K, Q, or J
   3 cards → Queen or Jack             1 card  → anything at all
```

## 3. Turn Flow

```
   ┌────────────────────────────────────────────────────────────┐
   │ 1. DRAW 1 (mandatory)                                      │
   │    deck empty? → BLEED: 1 wound first time, 2 thereafter   │
   ├────────────────────────────────────────────────────────────┤
   │ 2. UP TO 2 ACTIONS, any mix:                               │
   │    MUSTER    agent from hand → Front, face down (max 3)    │
   │    ARM       augment from hand → under a stack (slots!)    │
   │    STRIKE    stack attacks the enemy PLAYER                │
   │    CHALLENGE stack attacks an enemy STACK                  │
   │    RECALL    stack returns to hand                         │
   │    (each stack attacks ≤1× per your turn; blocking free)   │
   ├────────────────────────────────────────────────────────────┤
   │ 3. Pass turn.   (Game turn 1 only: 1 action, no attacks)   │
   └────────────────────────────────────────────────────────────┘
```

## 4. Combat Flow

```
  STRIKE (at player)                     CHALLENGE (at stack)
        │                                      │
   defender chooses                       defender chooses
        │                                      │
   ┌────┴─────────┐                    ┌───────┴────────┐
   ▼              ▼                    ▼                ▼
 BLOCK       TAKE THE HIT            FIGHT           RETREAT
 with any    wounds = striker's        │             stack → hand, unrevealed
 one stack   card count;               │             toll: 1 of its augments
   │         striker stays face        │             → owner's wounds
   │         down and deployed         │             (lone agent: free)
   │              [no battle]          │             [no battle]
   │                                   │        ♚ KING'S DECREE: challenger
   │                                   │          flips King face up →
   │                                   │          retreat FORBIDDEN
   └───────────────┬───────────────────┘
                   ▼
        ╔═════════════════════╗
        ║      THE RAISE      ║   defender first, then attacker:
        ║  (before any reveal)║   each may slide ≤1 augment from
        ╚═════════════════════╝   hand, face down, slots permitting
                   ▼
        ╔═════════════════════╗
        ║       REVEAL        ║   total = agent value
        ║     both stacks     ║         + augment pips
        ╚═════════════════════╝         + 2 × (suit-matched augments)
                   ▼
       ┌───────────┴────────────┐
       ▼                        ▼
  HIGHER TOTAL WINS           TIE → both stacks entirely
       │                       to their owners' Wounds
       │                       (exception: Aces return to hand)
       ▼
  ONE SIMULTANEOUS STEP:
  · loser's whole stack → loser's Wounds (agent dead forever)
  · winner spends exactly 1 augment → winner's OWN Wounds
  · winner's agent + rest → back to hand
  · winner's suit power triggers:
      ♠ loser takes 1 extra wound      ♦ spend nothing, augments come home
      ♥ swap spent augment for an      ♣ (power fires on muster, not wins)
        older wounded number card
  · THEN check for death (13+ wounds)
```

## 5. The Wound Cascade

Where wounds come from — always in this order, re-checked card by card:

```
   wound! ──►  1. top of DECK        (face up → Wounds)
                    │ deck empty
                    ▼
               2. HAND — opponent pulls one card BLIND
                    │ hand empty
                    ▼
               3. FRONT — you pick, but augments anywhere
                  on your Front must go before any agent
```

## 6. The Death Spiral (why the game always ends)

```
   draw compulsory ─► deck shrinks ─► deck empties ─► BLEED 1, then 2/turn
        │                                                  │
        ▼                                                  ▼
   battles kill agents forever (Ace-tie excepted)   wounds only ever grow
        │                                                  │
        └──────────────► 13 wounds OR 0 agents = death ◄───┘
```

Two turtles bleed out — and the first player, who draws first, bleeds out first. Aggression is not optional; it's the only exit.
