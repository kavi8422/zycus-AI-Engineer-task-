# Design Note

## 1. What Could Go Wrong (Failure Modes)

**The AI sometimes replies in a messy format.** It's supposed to give clean data (JSON),
but sometimes it wraps that data in extra formatting. Since my code needs clean data every
time, I added a cleanup step that strips out the extra formatting before reading the
answer. This means my code keeps working even when the AI's reply isn't perfectly
formatted. In a real company, I'd also add a stronger safety check that verifies the data
is correct before using it anywhere important.

**Sending too many requests too fast gets blocked.** While testing, I sent 10 requests to
the AI quickly and got blocked for going over the limit (5 requests per minute on the free
plan). To handle this without crashing, I added a "wait and retry" feature — if it gets
blocked, it waits 30 seconds and tries again automatically. This lets my code recover on
its own instead of failing outright. In a real company, we'd also pay for a higher limit
and queue up requests so they don't all hit at once.

**Long documents might get cut off.** I only send the AI the first part of our
help-documents to keep things fast, so if the right answer is further down, the AI never
sees it. For this project I accepted that limit since it kept things simple to build. For
a bigger, real system, I'd build a smarter search that finds only the relevant part of the
documents first, instead of sending everything every time.

## 2. Fast vs. Accurate — What I Chose

I had two options: send the AI the whole help-document every time (simpler, faster to
build), or build a smart search that finds only the relevant part first (more accurate,
but more work). I chose the simpler option, since it was faster to build, even though it
can miss things buried deep in a long document. If speed mattered even more than it does
now, I'd actually go the opposite direction — build the smart search — since sending the
AI less text per question can also make it respond faster.

## 3. Keeping Customer Information Safe

The tickets and customer info in this project are fake, practice data. But real customer
data usually includes private details — names, emails, company info — and I made sure to
think through how I'd protect that if this were real. Before sending anything to an AI
service, I'd hide or remove private details first, use an AI provider that promises not to
store or learn from our data, and keep records of exactly what information was shared, in
case it ever needs to be checked. This project is safe to run as-is, using only made-up
data, but this is the plan I'd add before ever touching real customer information.

## 4. What Happens With 10x More Tickets

Tonight, I saw firsthand that sending just 10 requests quickly caused the AI to block me.
That's a small taste of what would happen at a much bigger scale — with 10x more tickets,
the AI request limit would be the very first thing to break. To handle that, a real
company would need to pay for a higher-limit plan, process requests through an organized
queue instead of all at once, and avoid asking the AI the same question twice by
remembering past answers instead of repeating the same request.