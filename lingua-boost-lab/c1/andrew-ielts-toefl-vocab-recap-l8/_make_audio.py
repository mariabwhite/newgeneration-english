#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate all 19 lesson audio clips via edge-tts."""
import asyncio, os, sys, io
import edge_tts

OUT = os.path.join(os.path.dirname(__file__), "audio")
os.makedirs(OUT, exist_ok=True)

AND = "en-US-AndrewMultilingualNeural"
RYAN = "en-GB-RyanNeural"
GUY = "en-US-GuyNeural"
CHRIS = "en-US-ChristopherNeural"
ARIA = "en-US-AriaNeural"
SONIA = "en-GB-SoniaNeural"
JENNY = "en-US-JennyNeural"

CLIPS = [
  # ─── BLOCK-CYCLE LISTENING CLIPS (35-45 sec each) ───
  ("s01a-listening.mp3", GUY, "+0%",
   "The single most pivotal change we are seeing in white-collar work right now is, arguably, "
   "the exponential growth of generative-A-I tools in day-to-day operations. Every stakeholder — "
   "managers, H-R, finance, even the I-T team — is being pressed to rewrite job descriptions in real time. "
   "My recommendation to managers is simple. Do not replace people wherever possible. "
   "Strike a balance between automation and the retention of experienced staff. "
   "The institutional memory you keep is, on balance, more valuable than the headcount you cut."),

  ("s01b-listening.mp3", AND, "+0%",
   "Investor speaking. Look, your growth curve is impressive, but the unit economics are below our threshold. "
   "Gross margin is nowhere near where we need it. We can call this aspirational, but operationally it does not work yet. "
   "Founder responding. Yes, that is our Achilles heel. We know. "
   "Investor. Until we see a clear path to viability — real monetization, not just engagement — "
   "we cannot lead the next round. Consider this a hard no for now."),

  ("s01c-listening.mp3", RYAN, "+0%",
   "Morning stand-up. Dispatcher reports two issues. "
   "First, one container has been held up at customs since yesterday afternoon because of a packing-list mismatch. "
   "Second, the courier is running late on today's drop-offs — about forty minutes behind schedule. "
   "Ops lead responding. Right. I will follow up with the carrier on the customs hold immediately, "
   "and I will come back to you within the hour. "
   "Let's press on with the deliveries we can still sort out this morning."),

  ("s01d-listening.mp3", CHRIS, "+0%",
   "Customer call. Hi, I am calling about reference four-four-one. "
   "Two of our containers have been held up at customs since Monday and demurrage is already accruing. "
   "Forwarder. Let me pull up the file. OK — the root cause is a mismatch between the packing list and the commercial invoice. "
   "Clearance is pending a certificate of origin from the shipper. "
   "I will chase up the broker this afternoon and get back to you by six."),

  ("s01e-listening.mp3", ARIA, "+0%",
   "Weather note for the ops team. Today is already sweltering — thirty-two degrees before ten o'clock — "
   "with very humid air across the whole southern yard. Torrential rain is forecast to hit after lunch. "
   "The most pressing operational concern is packaging degradation in the un-conditioned warehouse. "
   "Please move all moisture-sensitive pallets to Bay C before noon. "
   "Let me know if you see any discernible water damage on today's incoming containers."),

  ("s01f-listening.mp3", RYAN, "+0%",
   "Hi. This is your counsel. Short memo on the Acme dispute. "
   "I have reviewed the file. On balance, I recommend we try to settle rather than immediately bring an action. "
   "We can do this by invoking the N-D-A and the arbitration clause first — "
   "that gives us leverage without going public. "
   "The key pressure point is their alleged breach of the exclusivity clause under the governing law of Delaware. "
   "Call me back by Friday if you want to press on."),

  # ─── §02 · IELTS READING (400 words, ~2 min 40 sec) ───
  ("s02-reading-ielts.mp3", AND, "+0%",
   "When a cease-and-desist letter is only the opening move. "
   "In most commercial disputes, the first written shot is rarely the complaint itself. "
   "It is a cease-and-desist letter: a formal demand that the recipient stop a specified course of conduct "
   "before the sender brings an action in court. These letters are often misread as empty theatre, "
   "yet counsel who draw them up well know that every clause is engineered either to force a settlement "
   "or to lay out the record for later litigation. "
   "Consider the facts the U-S Federal Circuit considered in Marta versus Golden Crust. "
   "Marta, a small independent baker, alleged that a national chain had copied her distinctive gold-foil wrapper — "
   "a protectable trade dress — and sold a confusingly similar product in forty states. "
   "Her counsel's cease-and-desist letter did not merely accuse; it laid out three independent causes of action, "
   "enclosed photographs, cited the relevant statute of limitations, "
   "and promised that, failing a response within fourteen days, her client would file a lawsuit "
   "and move for a preliminary injunction. "
   "Golden Crust's in-house legal team, in turn, brought up an arbitration clause buried in a supplier agreement "
   "neither side had enforced for years. They demanded Marta waive her right to a jury trial. "
   "Marta's counsel refused, filed in the Southern District of New York, and promptly drew up a motion to enjoin "
   "further sales pending discovery. The court, on balance, dismissed the arbitration argument because the clause "
   "did not survive assignment of rights after Golden Crust's twenty-twenty-two restructuring — "
   "a point the defence had plainly not dug up before posturing. "
   "What followed is textbook. Within six months, discovery produced nearly forty thousand internal emails. "
   "Three former designers came forward and sat for depositions. The chain's C-E-O was subpoenaed. "
   "By the eve of trial, settlement discussions had resumed, and the parties settled out for a reported "
   "twelve-million-dollar settlement fund, with Marta appointed lead plaintiff of the class "
   "and a modest retainer paid to her firm. The verdict was never handed down; the chain avoided a public one. "
   "Yet for practitioners, the lesson is sharper than the price tag. "
   "A well-drafted cease-and-desist signals not threat but preparation. "
   "Subject to the facts of each matter, the party who pursues a claim first — and in writing — "
   "usually sets the tempo of the negotiation that follows."),

  # ─── §03 · TOEFL × 3 PASSAGES (~2 min total) ───
  ("s03-reading-toefl.mp3", RYAN, "+0%",
   "Passage one. Why demurrage became the carrier's quiet profit centre. "
   "During the twenty-twenty-one to twenty-twenty-three port crunch, dwell time at the largest Western container terminals "
   "climbed from an average of three days to as many as nine. Shippers who could not retrieve their containers in time "
   "accrued demurrage inside the port and detention once the box left the gate. "
   "For carriers, these fees — originally designed to deter congestion — became a quiet profit centre. "
   "Some lines reported that demurrage alone contributed four to six per cent of their quarterly operating income. "
   "Regulators have since brought up the issue in two separate rule-makings, but freight forwarders and their clients "
   "still budget for delay as a near-certainty. "
   "Passage two. Material adverse change clauses after the pandemic. "
   "Before twenty-twenty, buyers rarely relied on the material adverse change clause to walk away from a signed deal; "
   "courts in Delaware had historically upheld such triggers only on extraordinary facts. "
   "The pandemic changed the arithmetic. In at least four high-profile transactions, "
   "acquirers invoked M-A-C in combination with force majeure, limitation of liability, and even indemnification clauses. "
   "On balance, courts remanded most of these disputes to detailed fact-finding, "
   "and few were ever handed down as published opinions — the parties quietly settled out. "
   "The practical result is that M-A-C clauses now are negotiated far more aggressively, "
   "with carve-outs for industry-wide downturns and explicit treatment of government orders. "
   "Passage three. Where everyone sits, and why it matters. "
   "A U-S courtroom is a map of authority as much as architecture. "
   "The judge sits at the bench; the witness stand is placed, deliberately, within the judge's eye-line and close to the jury box. "
   "The clerk and the court reporter sit below the bench, a bailiff guards the door, "
   "and the bar separates working counsel from the public gallery. "
   "In the U-K, the defendant typically stands or sits in the dock, flanked by officers, "
   "while a solicitor instructs a barrister who argues from the podium. "
   "Each design choice — not merely decoration — nudges credibility, pacing, and the visible hierarchy of the trial."),

  # ─── §04 · Listening ×3 + Choose-a-Response ───
  ("s04a-conversation.mp3", GUY, "+0%",
   "Forwarder. Operations, Nordic Coffee speaking. How can I help. "
   "Customer. Hi, it is Lena from the café in Zurich. I am trying to chase up container reference three-two-one. "
   "It has been showing stuck at the port for four days now and the dashboard hasn't updated. "
   "Forwarder. Let me look into it. One moment. "
   "OK — the hold is a mismatch between the packing list and the commercial invoice. "
   "Customs flagged it on Tuesday. I will follow up with the broker and the carrier immediately "
   "and call you back within the hour."),

  ("s04b-lecture.mp3", AND, "+0%",
   "A quick note on material-adverse-change clauses. Before twenty-twenty, buyers almost never invoked M-A-C to walk away from a signed deal. "
   "The pandemic changed that completely. In at least four high-profile transactions, "
   "acquirers combined M-A-C with force majeure and limitation-of-liability clauses to escape obligations. "
   "The practical result is that M-A-C clauses are now negotiated far more aggressively, "
   "with explicit carve-outs for industry-wide downturns. "
   "In short: the suggestion is that every new M-A-C clause be drafted with specific carve-outs — not vague language — "
   "especially where cross-border performance is involved. "
   "That is the single biggest change in deal practice this decade."),

  ("s04b2-choose-response.mp3", ARIA, "+0%",
   "Line one. I can't get hold of the carrier. (ding) "
   "Line two. Why is clearance stalling? (ding) "
   "Line three. The supplier says it was a force-majeure event. (ding) "
   "Line four. The founder wants to pivot. (ding) "
   "Line five. Our unit economics are weak."),

  ("s04c-news.mp3", SONIA, "+0%",
   "News brief. A federal jury today returned a verdict for the plaintiff on the trade-dress claim, "
   "awarding twelve million dollars in damages. The defence immediately announced it would press on with an appeal to the circuit court. "
   "Lead counsel said the ruling, on balance, underscores the growing willingness of juries "
   "to protect distinctive packaging as a form of intellectual property."),

  # ─── §09 · LISTEN & REPEAT ×7 (progressive) ───
  ("s09-lr-01.mp3", AND, "-8%", "The container is running late."),
  ("s09-lr-02.mp3", AND, "-8%", "The forwarder will chase up the carrier."),
  ("s09-lr-03.mp3", AND, "-8%", "Customs are holding up two containers for a paperwork mismatch."),
  ("s09-lr-04.mp3", AND, "-8%", "On balance, the buyer's counsel will file a motion to compel production of the full email chain."),
  ("s09-lr-05.mp3", AND, "-8%", "Arguably, the exponential deployment of generative A-I is giving rise to new mid-level roles, not replacing them."),
  ("s09-lr-06.mp3", AND, "-8%",
   "Notwithstanding the pandemic, the firm posted record revenue, "
   "and every stakeholder in the room is now pushing for compelling evidence before the next large deployment."),
  ("s09-lr-07.mp3", AND, "-8%",
   "Were the court to overturn the verdict on appeal, the entire logistics industry would have to renegotiate "
   "the governing-law and force-majeure clauses that have, until now, been treated as boilerplate."),
]

async def gen(fn, voice, rate, text):
  path = os.path.join(OUT, fn)
  if os.path.exists(path) and os.path.getsize(path) > 2000:
    print("skip (exists):", fn)
    return
  # retry edge-tts 403 up to 3 times
  for attempt in range(3):
    try:
      if os.path.exists(path): os.remove(path)
      await edge_tts.Communicate(text, voice, rate=rate).save(path)
      sz = os.path.getsize(path)
      if sz > 2000:
        print("ok {:,} bytes · {}".format(sz, fn))
        return
      else:
        print("retry (too small {} B): {} attempt {}".format(sz, fn, attempt+1))
        await asyncio.sleep(5)
    except Exception as e:
      print("retry (err): {} attempt {} — {}".format(fn, attempt+1, e))
      await asyncio.sleep(5)
  print("FAILED:", fn)

async def main():
  for c in CLIPS:
    await gen(*c)

asyncio.run(main())
print("\nDONE · {} files in {}".format(len(os.listdir(OUT)), OUT))
