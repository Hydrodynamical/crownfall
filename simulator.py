#!/usr/bin/env python3
"""CROWNFALL playtest simulator.

Implements the full ruleset in RULES.md and plays two heuristic AI players
against each other. AI decisions use only information legally visible to
that player (own cards, public wounds, stack sizes, decreed agents, peeks).

Usage:
  python3 simulator.py --seed 7 --verbose          # one narrated game
  python3 simulator.py --stats 1000                # aggregate balance stats
  python3 simulator.py --scan 1 200                # find the most dramatic seed
"""

import argparse
import math
import random

SUITS = ["♠", "♥", "♦", "♣"]  # spades hearts diamonds clubs
SPADE, HEART, DIAMOND, CLUB = SUITS
AGENT_RANKS = ["A", "K", "Q", "J"]
AGENT_VALUE = {"A": 14, "K": 13, "Q": 12, "J": 11}
SLOTS = {"A": 0, "K": 1, "Q": 2, "J": 3}


class Card:
    __slots__ = ("rank", "suit")

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    @property
    def is_agent(self):
        return self.rank in AGENT_VALUE

    @property
    def pips(self):
        return int(self.rank)

    def __repr__(self):
        return f"{self.rank}{self.suit}"


class Stack:
    def __init__(self, agent):
        self.agent = agent
        self.augments = []
        self.attacked = False      # has struck/challenged this turn
        self.decreed = False       # agent flipped face up by King's Decree
        self.known_to_enemy = set()  # cards the non-owner has seen (peeks)

    @property
    def size(self):
        return 1 + len(self.augments)

    @property
    def slots_free(self):
        return SLOTS[self.agent.rank] - len(self.augments)

    def total(self):
        t = AGENT_VALUE[self.agent.rank]
        for a in self.augments:
            t += a.pips + (2 if a.suit == self.agent.suit else 0)
        return t

    def cards(self):
        return [self.agent] + list(self.augments)

    def label(self):
        return "+".join(repr(c) for c in self.cards())


class Player:
    def __init__(self, style, rng):
        self.style = style
        self.name = style["name"]
        self.rng = rng
        self.deck = []
        self.hand = []
        self.front = []
        self.wounds = []
        self.bleeds = 0
        self.club_peeks_used = set()  # Club agents whose first-muster peek is spent
        self.opp = None

    @property
    def wound_count(self):
        return len(self.wounds)

    def agents_alive(self):
        return [c for c in self.hand if c.is_agent] + [s.agent for s in self.front]

    def all_cards(self):
        cards = list(self.deck) + list(self.hand) + list(self.wounds)
        for s in self.front:
            cards += s.cards()
        return cards


STYLES = {
    "rook": dict(name="Rook", persona="aggressive tempo",
                 challenge_thresh=0.56, block_thresh=0.50, raise_thresh=0.70,
                 retreat_thresh=0.42, aggression=1.25, prefers_first=True),
    "vesper": dict(name="Vesper", persona="patient value",
                   challenge_thresh=0.64, block_thresh=0.58, raise_thresh=0.78,
                   retreat_thresh=0.48, aggression=0.90, prefers_first=False),
}


class Defeat(Exception):
    def __init__(self, winner, condition):
        self.winner = winner
        self.condition = condition


class Game:
    def __init__(self, style_a, style_b, seed=0, verbose=False, force_first=False):
        self.rng = random.Random(seed)
        self.seed = seed
        self.verbose = verbose
        self.force_first = force_first
        self.lines = []
        self.p1 = Player(STYLES[style_a], self.rng)
        self.p2 = Player(STYLES[style_b], self.rng)
        self.p1.opp, self.p2.opp = self.p2, self.p1
        self.turn = 0
        self.active = None
        self.metrics = dict(battles=0, retreats=0, strikes_taken=0, strikes_blocked=0,
                            decrees=0, raises=0, peeks=0, heals=0, spade_hits=0,
                            diamond_wins=0, ties=0, bleed_wounds=0, recalls=0,
                            lead_changes=0, musters=0, arms=0)
        self._lead = 0

    # ------------------------------------------------------------- logging
    def log(self, msg):
        self.lines.append(msg)
        if self.verbose:
            print(msg)

    # ------------------------------------------------------------- setup
    def setup(self):
        for rank in AGENT_RANKS:
            group = [Card(rank, s) for s in SUITS]
            self.rng.shuffle(group)
            self.p1.hand += group[:2]
            self.p2.hand += group[2:]
        numbers = [Card(str(n), s) for n in range(2, 11) for s in SUITS]
        self.rng.shuffle(numbers)
        self.p1.deck = numbers[:18]
        self.p2.deck = numbers[18:]
        for p in (self.p1, self.p2):
            p.hand += p.deck[:4]
            p.deck = p.deck[4:]
        # decide first player: higher revealed top card chooses
        while True:
            c1, c2 = self.p1.deck[0], self.p2.deck[0]
            if c1.pips != c2.pips:
                break
            self.rng.shuffle(self.p1.deck)
            self.rng.shuffle(self.p2.deck)
        chooser = self.p1 if c1.pips > c2.pips else self.p2
        self.log(f"Opening reveal: {self.p1.name} {c1} vs {self.p2.name} {c2} — "
                 f"{chooser.name} chooses seating.")
        if self.force_first:
            goes_first = self.p1
        else:
            goes_first = chooser if chooser.style["prefers_first"] else chooser.opp
        for p in (self.p1, self.p2):
            self.rng.shuffle(p.deck)
        self.first = goes_first
        self.log(f"{goes_first.name} ({goes_first.style['persona']}) goes first. "
                 f"{goes_first.opp.name} ({goes_first.opp.style['persona']}) second.")

    # ------------------------------------------------------------- wounds
    def wound_specific(self, p, card, reason):
        """A named card (battle stack, spend, retreat toll) goes to wounds."""
        p.wounds.append(card)
        self.log(f"      {p.name} wounds: {card} → {p.wound_count}/13 ({reason})")

    def take_wound(self, p, reason):
        """One wound via the source order: deck top, blind hand pull, front."""
        if p.deck:
            c = p.deck.pop(0)
        elif p.hand:
            c = p.hand.pop(self.rng.randrange(len(p.hand)))
        else:
            aug_stacks = [s for s in p.front if s.augments]
            if aug_stacks:
                # owner picks: globally lowest-value augment
                best = None
                for s in aug_stacks:
                    for a in s.augments:
                        eff = a.pips + (2 if a.suit == s.agent.suit else 0)
                        if best is None or eff < best[2]:
                            best = (s, a, eff)
                s, c, _ = best
                s.augments.remove(c)
                s.known_to_enemy.discard(c)
            elif p.front:
                s = min(p.front, key=lambda s: AGENT_VALUE[s.agent.rank])
                p.front.remove(s)
                c = s.agent
            else:
                return  # no cards anywhere; defeat checks handle it
        p.wounds.append(c)
        self.log(f"      {p.name} wounds: {c} → {p.wound_count}/13 ({reason})")

    def check_defeat_now(self):
        """Instant defeat check (outside battle resolution)."""
        for p in (self.active, self.active.opp):
            if p.wound_count >= 13:
                raise Defeat(p.opp, "wounds")
            if not p.agents_alive():
                raise Defeat(p.opp, "agents")

    def check_defeat_after_battle(self):
        a, b = self.active, self.active.opp
        a_dead = a.wound_count >= 13 or not a.agents_alive()
        b_dead = b.wound_count >= 13 or not b.agents_alive()
        if a_dead and b_dead:
            if a.wound_count < b.wound_count:
                raise Defeat(a, "simultaneous")
            if b.wound_count < a.wound_count:
                raise Defeat(b, "simultaneous")
            raise Defeat(self.active, "simultaneous")  # tie: active player wins
        if b_dead:
            raise Defeat(a, "wounds" if b.wound_count >= 13 else "agents")
        if a_dead:
            raise Defeat(b, "wounds" if a.wound_count >= 13 else "agents")

    # ------------------------------------------------------------- estimation
    def unseen_pip_mean(self, viewer):
        seen = [c for c in viewer.hand if not c.is_agent]
        for s in viewer.front:
            seen += s.augments
        seen += [c for c in viewer.wounds if not c.is_agent]
        seen += [c for c in viewer.opp.wounds if not c.is_agent]
        for s in viewer.opp.front:
            seen += [c for c in s.known_to_enemy if not c.is_agent]
        total_pips, total_n = 216, 36  # sum/count of all number cards
        for c in seen:
            total_pips -= c.pips
            total_n -= 1
        return (total_pips / total_n) if total_n else 6.0

    def estimate_stack(self, viewer, s):
        """Viewer's estimate of an enemy stack's total, using legal info only."""
        owner = viewer.opp
        n_aug = s.size - 1
        if s.decreed or s.agent in s.known_to_enemy:
            agent_val = AGENT_VALUE[s.agent.rank]
        else:
            dead = {r: 0 for r in AGENT_RANKS}
            for c in owner.wounds:
                if c.is_agent:
                    dead[c.rank] += 1
            counts = {}
            for r in AGENT_RANKS:
                if SLOTS[r] >= n_aug:
                    n = 2 - dead[r]
                    for other in owner.front:
                        if other is not s and other.decreed and other.agent.rank == r:
                            n -= 1
                    counts[r] = max(0, n)
            tot = sum(counts.values())
            if tot == 0:
                counts = {r: 1 for r in AGENT_RANKS if SLOTS[r] >= n_aug}
                tot = sum(counts.values())
            agent_val = sum(AGENT_VALUE[r] * n for r, n in counts.items()) / tot
        mean = self.unseen_pip_mean(viewer)
        est = agent_val
        for a in s.augments:
            if a in s.known_to_enemy:
                est += a.pips + (2 if (s.decreed or s.agent in s.known_to_enemy)
                                 and a.suit == s.agent.suit else 0.5)
            else:
                est += mean + 0.5  # 0.5 = expected Loyalty
        return est

    @staticmethod
    def pwin(my_total, enemy_est):
        return 1.0 / (1.0 + math.exp(-(my_total - enemy_est) / 3.5))

    # ------------------------------------------------------------- AI pieces
    def best_arm(self, p, s):
        """Best augment in hand for stack s, or None."""
        if s.slots_free <= 0:
            return None
        augs = [c for c in p.hand if not c.is_agent]
        if not augs:
            return None
        return max(augs, key=lambda a: a.pips + (2 if a.suit == s.agent.suit else 0))

    def muster_choice(self, p):
        agents = [c for c in p.hand if c.is_agent]
        if not agents or len(p.front) >= 3:
            return None
        augs = [c for c in p.hand if not c.is_agent]

        def score(a):
            room = SLOTS[a.rank]
            support = sorted((x.pips + (2 if x.suit == a.suit else 0) for x in augs),
                             reverse=True)[:room]
            return AGENT_VALUE[a.rank] + 0.6 * sum(support)
        return max(agents, key=score)

    def do_peek(self, p, stack_played):
        """Clubs Veil: first muster of this club agent — peek enemy stack card."""
        targets = p.opp.front
        if not targets:
            return
        s = max(targets, key=lambda s: s.size)
        # peek the top card (the agent) — most informative
        card = s.agent
        s.known_to_enemy.add(card)
        self.metrics["peeks"] += 1
        self.log(f"    ♣ The Veil: {p.name} peeks the top of {p.opp.name}'s "
                 f"{s.size}-stack — sees [{card}].")

    # ------------------------------------------------------------- battle
    def raise_step(self, p, s, enemy_est_before):
        """One player's raise decision. Returns True if raised."""
        if s.slots_free <= 0:
            return False
        aug = self.best_arm(p, s)
        if aug is None:
            return False
        cur = self.pwin(s.total(), enemy_est_before)
        gain = aug.pips + (2 if aug.suit == s.agent.suit else 0)
        if cur >= p.style["raise_thresh"]:
            return False
        if cur < 0.12 and s.size <= 2:
            return False  # don't throw good cards after a lost cause
        if gain < 4 and cur > 0.45:
            return False
        p.hand.remove(aug)
        s.augments.append(aug)
        self.metrics["raises"] += 1
        self.log(f"    Raise: {p.name} slides a hidden augment under the stack "
                 f"[{aug}] — now {s.size} cards.")
        return True

    def battle(self, att_p, att_s, def_p, def_s):
        self.metrics["battles"] += 1
        # raise round: defender first
        d_est = self.estimate_stack(def_p, att_s)
        self.raise_step(def_p, def_s, d_est)
        a_est = self.estimate_stack(att_p, def_s)
        self.raise_step(att_p, att_s, a_est)
        # reveal
        at, dt = att_s.total(), def_s.total()
        self.log(f"    ⚔ REVEAL: {att_p.name} {att_s.label()} = {at}  vs  "
                 f"{def_p.name} {def_s.label()} = {dt}")
        if att_s in att_p.front:
            att_p.front.remove(att_s)
        if def_s in def_p.front:
            def_p.front.remove(def_s)
        if at == dt:
            self.metrics["ties"] += 1
            for p, s in ((att_p, att_s), (def_p, def_s)):
                if s.agent.rank == "A" and not s.augments:
                    p.hand.append(s.agent)
                    self.log(f"      Tie — {p.name}'s {s.agent} walks away (Ace).")
                else:
                    for c in s.cards():
                        self.wound_specific(p, c, "tie: stack destroyed")
            self.check_defeat_after_battle()
            return None
        winner_p, winner_s = (att_p, att_s) if at > dt else (def_p, def_s)
        loser_p, loser_s = (def_p, def_s) if at > dt else (att_p, att_s)
        self.log(f"    {winner_p.name} WINS {max(at,dt)}–{min(at,dt)}.")
        # loser's stack to loser's wounds (agent dies forever)
        for c in loser_s.cards():
            self.wound_specific(loser_p, c, "battle loss")
        # winner spends one augment (Diamonds exempt)
        spent = None
        if winner_s.agent.suit == DIAMOND:
            self.metrics["diamond_wins"] += 1
            self.log(f"      ♦ The Exchange: {winner_p.name} spends nothing; "
                     f"augments return (and are now known).")
        elif winner_s.augments:
            spent = min(winner_s.augments,
                        key=lambda a: (a.pips + (2 if a.suit == winner_s.agent.suit else 0)))
            winner_s.augments.remove(spent)
            self.wound_specific(winner_p, spent, "victory spend")
        # remaining cards home
        winner_p.hand.append(winner_s.agent)
        winner_p.hand += winner_s.augments
        # suit power
        suit = winner_s.agent.suit
        if suit == SPADE:
            self.metrics["spade_hits"] += 1
            self.log(f"      ♠ The Legion: extra wound to {loser_p.name}.")
            self.take_wound(loser_p, "Legion bonus")
        elif suit == HEART and spent is not None:
            pool = [c for c in winner_p.wounds if not c.is_agent and c is not spent]
            if pool:
                back = max(pool, key=lambda c: c.pips)
                winner_p.wounds.remove(back)
                winner_p.hand.append(back)
                self.metrics["heals"] += 1
                self.log(f"      ♥ The Cloister: {winner_p.name} recovers {back} "
                         f"from wounds → {winner_p.wound_count}/13.")
        self.check_defeat_after_battle()
        return winner_p

    # ------------------------------------------------------------- actions
    def act_strike(self, p, s):
        s.attacked = True
        d = p.opp
        self.log(f"  STRIKE: {p.name}'s {s.size}-stack [{s.label()}] attacks {d.name}.")
        blocker = None
        if d.front:
            best = max(d.front, key=lambda b: self.pwin(b.total(), self.estimate_stack(d, s)))
            bp = self.pwin(best.total(), self.estimate_stack(d, s))
            must = d.wound_count + s.size >= 13
            if bp >= d.style["block_thresh"] or (must and d.front):
                blocker = best
        if blocker is None:
            self.metrics["strikes_taken"] += 1
            self.log(f"    {d.name} takes the hit: {s.size} wound(s). Striker stays hidden.")
            for _ in range(s.size):
                self.take_wound(d, "unblocked strike")
                self.check_defeat_now()
        else:
            self.metrics["strikes_blocked"] += 1
            self.log(f"    {d.name} BLOCKS with a {blocker.size}-stack.")
            self.battle(p, s, d, blocker)

    def act_challenge(self, p, s, target, decree):
        s.attacked = True
        d = p.opp
        if decree:
            s.decreed = True
            self.metrics["decrees"] += 1
            self.log(f"  CHALLENGE + KING'S DECREE: {p.name} flips {s.agent} face up "
                     f"— no retreat. Target: {d.name}'s {target.size}-stack.")
        else:
            self.log(f"  CHALLENGE: {p.name}'s {s.size}-stack [{s.label()}] calls out "
                     f"{d.name}'s {target.size}-stack.")
        if not decree:
            pw = self.pwin(target.total(), self.estimate_stack(d, s))
            if pw < d.style["retreat_thresh"]:
                self.metrics["retreats"] += 1
                toll = None
                if target.augments:
                    toll = min(target.augments,
                               key=lambda a: a.pips + (2 if a.suit == target.agent.suit else 0))
                    target.augments.remove(toll)
                d.front.remove(target)
                d.hand += target.cards()
                if toll is not None:
                    self.wound_specific(d, toll, "retreat toll")
                    self.log(f"    {d.name} RETREATS the stack (pays {toll}).")
                else:
                    self.log(f"    {d.name} RETREATS the lone agent (free).")
                self.check_defeat_now()
                return
        self.battle(p, s, d, target)

    def act_muster(self, p, agent):
        p.hand.remove(agent)
        s = Stack(agent)
        p.front.append(s)
        self.metrics["musters"] += 1
        self.log(f"  MUSTER: {p.name} deploys a face-down agent [{agent}] "
                 f"(front: {len(p.front)}).")
        if agent.suit == CLUB and agent not in p.club_peeks_used:
            p.club_peeks_used.add(agent)  # first muster only, used or not
            self.do_peek(p, s)

    def act_arm(self, p, s, aug):
        p.hand.remove(aug)
        s.augments.append(aug)
        self.metrics["arms"] += 1
        self.log(f"  ARM: {p.name} slides a hidden augment [{aug}] under a stack "
                 f"(now {s.size} cards, total {s.total()}).")

    def act_recall(self, p, s):
        p.front.remove(s)
        p.hand += s.cards()
        self.metrics["recalls"] += 1
        self.log(f"  RECALL: {p.name} pulls a {s.size}-stack [{s.label()}] back to hand.")

    # ------------------------------------------------------------- turn AI
    def candidate_actions(self, p, allow_attack):
        cands = []
        st = p.style
        opp = p.opp
        urgency = 1.0 + opp.wound_count / 13.0
        for s in p.front:
            if s.attacked or not allow_attack:
                continue
            # strike
            if opp.front:
                best_b = max(opp.front,
                             key=lambda b: self.pwin(self.estimate_stack(p, b),
                                                     s.total()))
                blocker_est = self.estimate_stack(p, best_b)
                p_block = 0.75 if blocker_est > s.size * 6 + 8 else 0.35
                bw = self.pwin(s.total(), blocker_est)
                battle_ev = bw * (best_b.size + 2) - (1 - bw) * (s.size + 2)
                ev = (1 - p_block) * s.size * urgency + p_block * battle_ev
            else:
                ev = s.size * urgency * 1.5
            cands.append((ev * st["aggression"], "strike", s, None, False))
            # challenges
            for t in opp.front:
                w = self.pwin(s.total(), self.estimate_stack(p, t))
                if w < st["challenge_thresh"]:
                    continue
                ev = (w * (t.size + 2) - (1 - w) * (s.size + 2)) * st["aggression"]
                decree = (s.agent.rank == "K" and w > 0.72)
                cands.append((ev, "challenge", s, t, decree))
        # muster
        m = self.muster_choice(p)
        if m is not None:
            base = 3.0 if len(p.front) < 2 else 1.2
            cands.append((base + AGENT_VALUE[m.rank] / 10.0, "muster", m, None, False))
        # arm
        for s in p.front:
            a = self.best_arm(p, s)
            if a is not None and s.total() < 34:
                eff = a.pips + (2 if a.suit == s.agent.suit else 0)
                cands.append((1.0 + eff / 3.0, "arm", s, a, False))
        # recall a hopeless known-weak stack when front is clogged
        if len(p.front) == 3:
            weakest = min(p.front, key=lambda s: s.total())
            if weakest.total() < 16 and any(c.is_agent for c in p.hand):
                cands.append((1.1, "recall", weakest, None, False))
        cands.append((0.4, "pass", None, None, False))
        return cands

    def play_turn(self, p, first_game_turn):
        self.turn += 1
        self.active = p
        for s in p.front:
            s.attacked = False
        self.log(f"── Turn {self.turn} — {p.name} "
                 f"(wounds {p.wound_count}/13, deck {len(p.deck)}, "
                 f"hand {len(p.hand)}, front {len(p.front)}) ──")
        # 1. draw or bleed
        if p.deck:
            c = p.deck.pop(0)
            p.hand.append(c)
            self.log(f"  Draws [{c}] (deck {len(p.deck)}).")
        else:
            p.bleeds += 1
            n = 1 if p.bleeds == 1 else 2
            self.metrics["bleed_wounds"] += n
            self.log(f"  Deck empty — BLEEDS {n}.")
            for _ in range(n):
                self.take_wound(p, "bleed")
                self.check_defeat_now()
        # 2. actions
        n_actions = 1 if first_game_turn else 2
        allow_attack = not first_game_turn
        for _ in range(n_actions):
            cands = self.candidate_actions(p, allow_attack)
            score, kind, a, b, decree = max(cands, key=lambda c: c[0] + self.rng.uniform(0, 0.25))
            if kind == "pass":
                self.log("  Passes.")
                break
            elif kind == "strike":
                self.act_strike(p, a)
            elif kind == "challenge":
                self.act_challenge(p, a, b, decree)
            elif kind == "muster":
                self.act_muster(p, a)
            elif kind == "arm":
                self.act_arm(p, a, b)
            elif kind == "recall":
                self.act_recall(p, a)
            self.check_defeat_now()
        # lead-change tracking
        diff = self.p1.wound_count - self.p2.wound_count
        if diff != 0:
            sign = 1 if diff > 0 else -1
            if self._lead != 0 and sign != self._lead:
                self.metrics["lead_changes"] += 1
            self._lead = sign

    # ------------------------------------------------------------- audit
    def audit(self):
        seen_ids = set()
        for p in (self.p1, self.p2):
            cards = p.all_cards()
            assert len(cards) == 26, f"{p.name} owns {len(cards)} cards, not 26"
            for c in cards:
                assert id(c) not in seen_ids, f"duplicate card {c}"
                seen_ids.add(id(c))
            for s in p.front:
                assert s.agent.is_agent, "stack led by a non-agent"
                assert len(s.augments) <= SLOTS[s.agent.rank], "over-slot stack"
        assert len(seen_ids) == 52

    # ------------------------------------------------------------- driver
    def play(self):
        self.setup()
        order = [self.first, self.first.opp]
        try:
            game_turn = 0
            while True:
                game_turn += 1
                if game_turn > 400:
                    raise RuntimeError("no-end bug: 400 turns exceeded")
                self.play_turn(order[0] if game_turn % 2 == 1 else order[1],
                               first_game_turn=(game_turn == 1))
                self.audit()
        except Defeat as d:
            w = d.winner
            l = w.opp
            self.log("")
            self.log(f"☠ GAME OVER on turn {self.turn}: {w.name} WINS "
                     f"({d.condition}). Final wounds — {w.name} {w.wound_count}/13, "
                     f"{l.name} {l.wound_count}/13.")
            return dict(winner=w.name, condition=d.condition, turns=self.turn,
                        winner_seat=1 if w is self.first else 2,
                        winner_wounds=w.wound_count, loser_wounds=l.wound_count,
                        seed=self.seed, metrics=dict(self.metrics))


def drama_score(r):
    m = r["metrics"]
    s = 0.0
    s += 2.0 * m["battles"] + 3.0 * m["lead_changes"] + 1.5 * m["decrees"]
    s += m["heals"] + m["peeks"] + m["retreats"] + 2.0 * m["ties"]
    s += 2.0 if r["condition"] == "simultaneous" else 0.0
    s += 2.0 - abs(r["loser_wounds"] - r["winner_wounds"]) * 0.3  # closeness
    if 18 <= r["turns"] <= 34:
        s += 3.0
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--stats", type=int, default=0)
    ap.add_argument("--styles", type=str, default=None,
                    help="force a style pairing for --stats, e.g. rook,rook")
    ap.add_argument("--force-first", action="store_true",
                    help="first listed style always takes seat 1 (for --stats)")
    ap.add_argument("--scan", type=int, nargs=2, metavar=("LO", "HI"))
    args = ap.parse_args()

    if args.scan:
        best = None
        for seed in range(args.scan[0], args.scan[1]):
            for a, b in (("rook", "vesper"), ("vesper", "rook")):
                r = Game(a, b, seed=seed).play()
                sc = drama_score(r)
                if best is None or sc > best[0]:
                    best = (sc, seed, a, b, r)
        sc, seed, a, b, r = best
        print(f"most dramatic: seed={seed} styles=({a},{b}) score={sc:.1f}")
        print(f"  {r['turns']} turns, winner {r['winner']} ({r['condition']}), "
              f"wounds {r['winner_wounds']}-{r['loser_wounds']}, {r['metrics']}")
        return

    if args.stats:
        results = []
        pair = args.styles.split(",") if args.styles else None
        for i in range(args.stats):
            if pair:
                a, b = pair
            else:
                a, b = (("rook", "vesper") if i % 2 == 0 else ("vesper", "rook"))
            results.append(Game(a, b, seed=10_000 + i,
                                force_first=args.force_first).play())
        n = len(results)
        by_seat = sum(1 for r in results if r["winner_seat"] == 1)
        by_style = {}
        for r in results:
            by_style[r["winner"]] = by_style.get(r["winner"], 0) + 1
        conds = {}
        for r in results:
            conds[r["condition"]] = conds.get(r["condition"], 0) + 1
        turns = sorted(r["turns"] for r in results)
        battles = [r["metrics"]["battles"] for r in results]
        print(f"games: {n}")
        print(f"first player wins: {by_seat} ({100*by_seat/n:.1f}%)")
        for k, v in sorted(by_style.items()):
            print(f"{k} wins: {v} ({100*v/n:.1f}%)")
        print(f"win conditions: {conds}")
        print(f"turns: mean {sum(turns)/n:.1f}, median {turns[n//2]}, "
              f"min {turns[0]}, max {turns[-1]}")
        print(f"battles/game: mean {sum(battles)/n:.1f}")
        agg = {}
        for r in results:
            for k, v in r["metrics"].items():
                agg[k] = agg.get(k, 0) + v
        print("per-game averages: " +
              ", ".join(f"{k} {v/n:.2f}" for k, v in sorted(agg.items())))
        return

    Game("rook", "vesper", seed=args.seed, verbose=True).play()


if __name__ == "__main__":
    main()
