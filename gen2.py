import html, os, re
BASE="https://youram470-art.github.io/notes/"
ART=[
("h3video-org","One-day delivery: the short-form checklist that actually saves time","https://h3video.org","H3 Video",
 "When a client hands you a single day for a social clip, the constraint is not rendering speed, it is decision speed. A fixed checklist removes about half of the back-and-forth.",
 ["Start by locking the output frame before anything is generated. Aspect ratio, safe margins for captions, and the delivery codec decide whether a shot is usable long before any aesthetic question comes up.",
 "Next, write the shot as a verb plus a subject plus a camera behaviour, one line each. If a line needs a comma to stay truthful, it is two shots wearing one sentence, and the model will average them into mush.",
 "Then cap the number of generations per shot at four. The fifth attempt almost never beats the second, and the time is better spent on the edit, where small trims and speed ramps fix pacing problems that no re-render solves.",
 "Finally, keep a written log of the seed and the prompt for the take you shipped. The next job usually asks for a variation of it, and reconstructing it from memory costs more than the log did."]),
("seedance25-kr","Camera vocabulary that survives the trip into a prompt","https://seedance25.kr","Seedance 2.5",
 "Camera language is the part of a prompt that degrades most in translation. Words that are precise on a set become vague once a model reads them.",
 ["The reliable terms are the ones that describe where the camera is and what it does over time: static, slow push in, pull back, pan left, tilt up, orbit around the subject. Each maps to a physical motion the model has seen in training data.",
 "The unreliable terms are the ones borrowed from criticism: cinematic, dynamic, epic. They describe a feeling rather than a movement, so the model substitutes whatever style cluster those words usually appear next to.",
 "A practical test is to remove the adjective and ask whether the sentence still tells an operator what to do. If it does not, it is decoration and belongs in a style note, not in the shot line.",
 "One more habit worth keeping: describe the speed. A push in that takes four seconds reads as deliberate, the same move in one second reads as a whip, and models do respond to the difference when the duration is stated."]),
("grokaiimagegenerator-net","Stills that animate: a lighting checklist","https://grokaiimagegenerator.net","Grok AI Image Generator",
 "Most images that fail to animate fail for a lighting reason rather than a composition one. Flat light gives a video model nothing to move through.",
 ["Before accepting a still, check for three things: a clear key light direction, a shadow that falls on a surface rather than on the subject only, and a background that is measurably darker or lighter than the foreground.",
 "Those three cues let the model infer depth. Without them, motion tends to look like a cutout sliding over a backdrop, which is the single most common giveaway in generated footage.",
 "The second check is texture. Fabric, hair and foliage give the model something to displace; smooth plastic surfaces and clean gradients give it nothing, so motion reads as warping instead of movement.",
 "If a frame is beautiful but fails these checks, it is worth regenerating with a lighting phrase added rather than trying to rescue it in the video stage. The cost of a new still is minutes; the cost of a failed render is an afternoon."]),
("reversevideosearch-org","Tracing a clipped repost back to its original upload","https://reversevideosearch.org","Reverse video search",
 "A repost arrives as a fifteen-second clip with the watermark cropped out, and the question is where it came from. Reverse search answers it, but only if the query is prepared correctly.",
 ["The mistake is uploading the whole clip. Platforms index keyframes, and a clip that has been re-encoded, cropped and captioned matches poorly at the frame level. Take three frames from moments where the image is least obstructed.",
 "Crop out overlays before searching. Captions, progress bars and account watermarks are the strongest visual signal in the frame, and they pull the search toward other reposts of the same edited version rather than the original.",
 "If the first pass returns only mirrors, flip the frame horizontally and search again. Many reposts are mirrored to dodge detection, and the flipped frame frequently matches the source directly.",
 "Record the earliest upload date you can verify, along with the account. That date is what settles attribution disputes, and screenshots of search results are not a substitute for it."]),
("viddiai-com","Batch re-renders: the two settings worth changing first","https://viddiai.com","Viddi AI",
 "When a batch of clips comes back with the same flaw, the instinct is to rework the prompts. Usually the flaw lives in two settings that apply to the whole batch.",
 ["The first is duration. A model asked for eight seconds when it was trained mostly on four tends to repeat a gesture or stall in the last third. Cutting the requested length and extending in the edit often fixes the batch without touching a single prompt.",
 "The second is motion strength. Too low and the subject drifts; too high and geometry collapses mid-shot. Moving it in small steps across a three-clip test tells you where the batch sits far faster than a full re-render.",
 "Change one setting at a time and keep the prompts fixed, otherwise the result tells you nothing about which change did the work. This sounds obvious and is skipped constantly under deadline pressure.",
 "Keep the failed batch. It is the cheapest control group you will ever have, and comparing it against the fix is how you learn where a given model's limits actually sit."]),
("wan-3-io","Writing a shot list before you open the generator","https://wan-3.io","Wan 3",
 "A shot list written before generation is different from one written for a crew. It has to survive being read by a model that will not ask clarifying questions.",
 ["Each line should carry four things: subject, action, camera, and duration. Anything else is optional. A line missing the duration is the most common cause of a clip that feels either rushed or padded.",
 "Order the list by dependency rather than by story. Shots that establish a location should be generated before shots that return to it, because the first render becomes the de facto reference for colour and light.",
 "Mark the two or three shots the piece cannot survive without. Those get the extra attempts; the rest can be covered by inserts and cutaways, which are cheap to generate and easy to drop in.",
 "Finally, note what must not appear. Negative constraints are easier to honour than positive ones, and a shot list that names the exclusions up front saves a whole round of rejects."]),
("memoriessong-com","Music for memory videos: tempo before genre","https://memoriessong.com","Memories Song",
 "The genre question comes up first and matters least. For a photo or clip montage of a family memory, tempo decides whether the piece feels like a recollection or a slideshow.",
 ["A useful rule: match the tempo to the number of image changes, not to the mood. Sixty to seventy beats per minute gives roughly one change every two bars, which is slow enough for a viewer to register faces.",
 "Faster tempos push the edit toward celebration, which is right for a birthday and wrong for a memorial. The same track slowed by fifteen percent often reads as nostalgic without any change of instrumentation.",
 ["Lyrics compete with narration. If there is a voiceover, choose an instrumental or leave the vocal for the final third, where it can carry the ending without stepping on the words."] if False else "Lyrics compete with narration. If there is a voiceover, choose an instrumental, or hold the vocal until the final third where it can carry the ending without stepping on anyone's words.",
 "Leave eight to ten seconds of quiet at the end. Memory pieces usually need a beat of silence to land, and a track that stops dead on the last frame feels abrupt rather than finished."]),
("kling4-co-kr","Multi-shot consistency without a reference image","https://kling4.co.kr","Kling 4",
 "Reference images solve consistency, but they are not always available. When a character has to appear in four shots and there is no still to anchor them, description has to do the work.",
 ["Write the character once, in a fixed order: age range, build, hair, one garment with a colour, one accessory. The order matters because it keeps the phrasing identical across prompts, and identical phrasing is what keeps the model's interpretation stable.",
 "Repeat that paragraph verbatim in every shot prompt. Paraphrasing between shots is the main cause of a character who looks related but not the same, and the drift is much easier to prevent than to fix.",
 "Keep the lighting direction consistent too. A character described identically but lit from opposite sides will read as a different person, especially in close-ups where the shadow shape carries most of the recognition.",
 "Accept that the fourth shot will need the most attempts. Consistency degrades with each generation, so schedule the shots that share a character early in the session while your patience and the model's agreement are both intact."]),
("pavoai-app","Dubbing passes: catching timing drift early","https://pavoai.app","Pavo AI",
 "Dubbing a finished video is mostly a timing problem. The voice is the easy part; keeping it aligned with the picture is where projects lose days.",
 ["Check drift at three points rather than watching the whole file: the first sentence, the longest sentence, and the last sentence. If the last sentence lands early or late, the middle is already off and no amount of local nudging will fix it.",
 "The usual cause is a target language that runs longer than the source. A ten percent expansion over a two-minute clip is twelve seconds of slack, which has to be absorbed by pauses rather than by speeding the voice up past natural.",
 "Mark the pauses before recording rather than after. Cutting silence into a finished take is possible, but each cut changes the rhythm of the sentence that follows, and the effect compounds across a long piece.",
 "Keep the untouched source audio track in the project. It is the only reliable reference when a client asks whether a line was always that long, and it costs nothing to leave in place."]),
("gta6aivideo-art","Fan trailers: matching the grain of the source footage","https://gta6aivideo.art","GTA 6 AI video",
 "A fan trailer lives or dies on whether the generated shots look like they came from the same camera as the original material. Grain and contrast do more of that work than content.",
 ["Sample two frames from the source at full resolution and look at the noise pattern rather than the colour. Game capture usually carries fine, even noise; film emulation carries coarser, uneven grain that clumps in shadows.",
 "Apply matching grain to the whole timeline at the end, not per clip. Per-clip grain creates visible seams at every cut, which reads as amateur even when each shot is convincing on its own.",
 "Contrast matters as much as grain. Generated footage tends to arrive with clean blacks, and source footage rarely has them, so lifting the shadow floor slightly before the grain pass does more for plausibility than any colour grade.",
 "Finally, cut on motion. Generated shots often start and end on a held frame, and hiding those holds behind a cut on movement is the cheapest way to make a trailer feel edited rather than assembled."]),
]
TPL="""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{base}{slug}.html">
<style>
  :root {{ color-scheme: light dark; }}
  body {{ max-width: 42rem; margin: 3rem auto; padding: 0 1.2rem;
         font: 17px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
  h1 {{ font-size: 1.6rem; line-height: 1.28; margin-bottom: .3rem; }}
  .meta {{ font-size: .85rem; opacity: .6; margin-bottom: 1.6rem; }}
  a {{ color: inherit; }}
  footer {{ margin-top: 2.8rem; font-size: .9rem; opacity: .65; }}
</style>
</head>
<body>
<nav><a href="../">← AI video tools</a></nav>
<h1>{title}</h1>
<div class="meta">{date} · field notes</div>
{body}
<footer>Notes on AI video production. Written and maintained by the site author; no sponsored placement.</footer>
</body>
</html>
"""
DATE="2026-11-25"
links=[]
for slug,title,target,name,desc,paras in ART:
    ps=[html.escape(p) for p in paras]
    ps[1]=ps[1]+' For a closer look at '+html.escape(name)+', the <a href="'+target+'">tool page is here</a>.'
    body="\n".join("<p>"+p+"</p>" for p in ps)
    open(f"/tmp/ghp2/notes/{slug}.html","w").write(TPL.format(title=html.escape(title),desc=html.escape(desc),base=BASE,slug=slug,date=DATE,body=body))
    links.append((slug,title))
# sitemap
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm+=f"<url><loc>https://youram470-art.github.io/</loc><lastmod>{DATE}</lastmod></url>\n"
for slug,_ in links:
    sm+=f"<url><loc>{BASE}{slug}.html</loc><lastmod>{DATE}</lastmod></url>\n"
sm+="</urlset>\n"
open("/tmp/ghp2/sitemap.xml","w").write(sm)
open("/tmp/ghp2/robots.txt","w").write("User-agent: *\nAllow: /\nSitemap: https://youram470-art.github.io/sitemap.xml\n")
open("/tmp/ghp2/.nojekyll","w").write("")
KEY="a7c41f9b2e5d48c6b0f3a91d7e28c504"
open(f"/tmp/ghp2/{KEY}.txt","w").write(KEY)
print(len(links),"pages")
