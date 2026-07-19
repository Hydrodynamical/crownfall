# CROWNFALL — Learn to Play in 10 Minutes

*You need: one standard 52-card deck, a table, and an opponent you'd like to out-bluff.*

---

## The Game in 30 Seconds

Your 26 cards are your army **and** your life bar. Face cards (A, K, Q, J) are **agents**; number cards (2–10) are **augments** that make agents stronger. You play them **face down**, so your opponent sees *how many* cards a stack has but never *what* they are — until a battle forces the reveal, the totals are compared, and the loser's whole stack becomes **wounds**. Take 13 wounds and you're dead.

The twist: **everything costs blood**. Winning a fight costs you a card. Retreating costs a card. Running out of deck costs cards. There is no mana — your life *is* the currency, and the winner is whoever spends it smarter.

## Step 1 — Set Up the Table

1. Pull out the 16 face-value cards (A, K, Q, J). Shuffle the four Aces and deal 2 to each player, face down. Do the same with Kings, Queens, Jacks. You each now secretly hold **8 agents** — two of each rank, random suits.
2. Shuffle the 36 number cards and deal **18 to each player, face down** — that's your **deck**. **Draw 4** into your hand.
3. Each player flips their top deck card: **higher number chooses who goes first** (re-flip ties, then shuffle those cards back in).

Arrange your side like this:

```
                        ═══ OPPONENT'S SIDE (mirrored) ═══

     [ DECK ]        [ HAND — private, no size limit ]        [ WOUNDS ]
     face down          agents + augments, hidden              FACE UP
        14                        12                            public

     ┌─────────┐      ┌─────────┐      ┌─────────┐
     │ STACK 1 │      │ STACK 2 │      │ (empty) │   ← their FRONT
     └─────────┘      └─────────┘      └─────────┘     (max 3 stacks)

   ─────────────────────  THE BATTLEFIELD  ─────────────────────
              Strikes and Challenges cross this line

     ┌─────────┐      ┌─────────┐      ┌─────────┐
     │ STACK 1 │      │ STACK 2 │      │ (empty) │   ← your FRONT
     │ agent   │      │ agent   │      └─────────┘     (max 3 stacks)
     │ +augment│      └─────────┘
     └─────────┘       1 card           Stacks are FACE DOWN,
      2 cards                           agent on top, counts visible

     [ DECK ]        [ HAND — private, no size limit ]        [ WOUNDS ]
     face down          agents + augments, hidden              FACE UP

                            ═══ YOUR SIDE ═══
```

**Count check:** you own 8 agents (hand) + 4 augments (hand) + 14 deck = **26 cards**. You always own exactly 26. Your health = 26 − your wounds. **13 wounds = dead.**

## Step 2 — Understand a Stack

A **stack** is one face-down agent with face-down augments tucked under it. Each rank carries a different amount:

| Stack size you see | What it must be |
|---|---|
| 4 cards | **Jack** (11 + three augments) — the only agent that carries three |
| 3 cards | Queen or Jack |
| 2 cards | King, Queen, or Jack |
| 1 card | *Anything* — a naked Jack bluff… or an Ace (14) that needs no help |

That table is the heart of the game. Your opponent always knows a stack's **size**, never its **contents**. A 1-card stack might be a 14 or an 11. A 3-card tower might be 35 — or a Queen padded with a 2 and a 3.

**Battle math (memorize this one line):** `total = agent value + augment pips, +2 for each augment matching the agent's suit` (that bonus is called **Loyalty**). A = 14, K = 13, Q = 12, J = 11.

## Step 3 — Take a Turn

Every turn is the same shape:

1. **Draw 1 card** (mandatory). No deck left? You **Bleed**: 1 wound the first time, **2 wounds every time after**. The clock always ticks.
2. **Take up to 2 actions**, any mix:
   - **Muster** — put an agent from hand, face down, onto your Front (max 3 stacks).
   - **Arm** — tuck an augment from hand, face down, under one of your stacks (respect its slots).
   - **Strike** — send a stack at the enemy **player**.
   - **Challenge** — send a stack at an enemy **stack**.
   - **Recall** — take one of your stacks back into your hand.

(The very first turn of the game, the first player gets only 1 action and may not attack.)

## Step 4 — Fight a Battle

**When you STRIKE** the enemy player, they choose: **block** with one of their stacks (→ battle), or **take the hit** — wounds equal to your stack's *size*, and your stack stays face down, unrevealed. Yes: a 3-card stack of garbage hits for 3 real wounds if they don't call it. That's the bluff engine.

**When you CHALLENGE** an enemy stack, its owner chooses: **fight**, or **retreat** it to hand unrevealed — paying one of its augments to their wounds as an exit toll (lone agents flee free). A **King** may flip itself face up when challenging: that's the **Decree** — no retreat allowed.

**Once a battle is locked in**, both players get one last poker move — **the Raise**: defender first, each may slide **one** augment from hand under their fighter, face down, if slots allow.

**Then the reveal:**

```
  STRIKE (at player)                CHALLENGE (at stack)
        │                                 │
  defender chooses ───────┐         defender chooses ─────┐
        │                 │               │               │
      BLOCK          TAKE THE HIT       FIGHT          RETREAT
        │           (wounds = stack      │          (pay 1 augment
        │            size; no reveal)    │           to your wounds)
        └────────────┬───────────────────┘
                     ▼
              THE RAISE — defender first,
              up to 1 hidden augment each
                     ▼
              REVEAL BOTH STACKS
       total = agent + pips + Loyalty (+2/matching suit)
                     ▼
        ┌────────────┴─────────────┐
     HIGHER TOTAL WINS           TIE: both stacks die
        │                        (Aces walk away)
        ▼
  Loser: whole stack → their Wounds (agent dead forever)
  Winner: spends 1 augment of choice → own Wounds,
          rest returns to hand, suit power triggers
```

Read that last line again: **the winner pays too.** Every fight bleeds both courts — the loser just bleeds more.

## Step 5 — Know Your Courts

Loyalty (+2 per suit-matched augment) applies to everyone. Each suit also has a signature power on the **agent** leading the stack:

- ♠ **Spades — The Legion.** Win a battle → the loser takes **1 extra wound**. The aggro suit: every won fight hits harder.
- ♥ **Hearts — The Cloister.** Win a battle where you spent an augment → **recover a different number card from your Wounds** to hand. The attrition suit: you literally heal.
- ♦ **Diamonds — The Exchange.** Win a battle → **spend nothing**; your augments come home. The economy suit: victory is free, but your cards have been seen.
- ♣ **Clubs — The Veil.** First time each Club agent hits the table → **peek at one face-down enemy card** (named by position). The espionage suit: you play with the lights on.

## A Worked Turn (follow along with real cards)

Mid-game. **Maya** has 6 wounds; her Front holds one 2-card stack — secretly **K♦ + 9♦**. **Liam** has 8 wounds — his face-up Wounds pile includes a **7♠** — and two stacks: a 2-card stack (secretly **J♥ + 4♥**) and a 1-card mystery. He's holding an **8♥**.

1. **Draw.** Maya draws the 3♣.
2. **Action 1 — Muster.** She plays **J♣ face down** as a new stack. First muster of that Club, so **the Veil fires**: she names "bottom card of your 2-card stack" and sees Liam's **4♥**. A 2-card stack is K, Q, or J with one augment — with only a 4♥ aboard, it totals **at most 19** (K♥+4♥ = 13+4+2 Loyalty).
3. **Action 2 — Strike.** Her K♦+9♦ stack (2 cards, secretly 24) attacks Liam directly. Taking it means 2 wounds — he'd be at 10 of 13 with the striker still standing. He **blocks** with the stack Maya just scouted. *Gulp?*
4. **The Raise — defender first.** Liam slides his **8♥ face down** under the blocker. Three cards now — so it's a Queen or Jack, and Maya knows its 19 just grew by an unknown amount. Her King's single slot is already full: she cannot raise back.
5. **Reveal.** Maya: **K♦ + 9♦ = 13 + 9 + 2 = 24**. Liam: **J♥ + 4♥ + 8♥ = 11 + 6 + 10 = 27**. **Liam wins, 27–24.**
6. **Resolution (one simultaneous step).** Maya's whole stack goes face up to her Wounds — **8 of 13**, and her K♦ is dead forever. Liam, the winner, spends one augment of his choice: the 4♥ goes to his Wounds (**9 of 13**). His ♥ agent won *and* spent — the Cloister triggers, returning the old **7♠** from his Wounds to his hand (**back to 8 of 13**). J♥ and 8♥ return to his hand.
7. **The ledger.** Maya is down a King and two wounds — but her fresh J♣ sits unread, and armed with its best clubs it could grow toward 44. Liam won, yet Maya now knows three cards in his hand. Nobody got away clean. Nobody ever does.

## Beginner Traps (read before your first game)

1. **Don't build a tower and admire it.** A 4-card stack telegraphs "Jack," invites retreats, and unless the pips inside are genuinely huge, it's a 4-wound catastrophe when a lean 3-card Queen out-reveals it. Lean stacks that win by 1 are the aesthetic.
2. **Don't take every hit.** Chip Strikes cost wounds equal to stack *size* — but blocking a bluff with a real stack executes their agent. Somewhere around the third unblocked Strike, start calling.
3. **Don't hoard.** Cards in hand are health, but your deck is a fuse: when it empties, Bleed eats you at 2 wounds a turn. Turtling is just losing slowly, on purpose.
4. **Count the dead.** Wounds piles are face up. If three tens are dead and you hold the fourth, no 2-card stack can out-reveal your 25-point King — just remember the Raise can grow one to three cards. The endgame is a card-counter's paradise.
5. **Respect the naked Ace.** One card, total 14, kills any lone King, Queen, or Jack, walks away from ties with a rival Ace… and can't ever get stronger. It teaches you the whole game.

## What Winning Looks Like

You win the moment your opponent has **13 wounds** — or **no agents left** in hand or Front. Most games end in blood; agent-extinction happens to players who spend their court like it's free. It isn't. Nothing here is.

*Full rules with every edge case: [RULES.md](RULES.md) · One-page cheat sheet: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)*
