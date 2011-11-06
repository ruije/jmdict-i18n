#!/usr/bin/python3

import sys
from gettextformat import *
from jmdict import *

def createEntriesDictionary(gettextEntries):
	jEntries = {}
	for entry in gettextEntries:
		if len(entry.msgstr) == 0: continue
		msgstr = entry.msgstr
		lang = entry.lang

		eid, senseId = [ int(i) for i in entry.msgctxt.split(' ') ]
		try:
			jEntry = jEntries[eid]
		except KeyError:
			jEntry = Entry()
			jEntries[eid] = jEntry
		try:
			sense = jEntry.senses[senseId]
		except KeyError:
			sense = Sense()
			jEntry.senses[senseId] = sense
		sense.glosses[lang] = msgstr
	return jEntries

if __name__ == "__main__":
	entries = []
	for f in sys.argv[1:]:
		f = GetTextFile(f, "r")
		entries += f.readEntries()
	jmEntries = createEntriesDictionary(entries)

	jmdict = open("JMdict", "r", encoding="utf-8")
	jmdicti18n = open("JMdict-i18n", "w", encoding="utf-8")
	while True:
		l = jmdict.readline()
		match = otherGlossRe.match(l)
		if match:
			# Only replace glosses for which we have a replacement
			if eid in jmEntries and senseid in jmEntries[eid].senses and langMatch[match.group(1)] in jmEntries[eid].senses[senseid].glosses:
				continue
		match = entryStartRe.match(l)
		if match:
			eid = int(match.group(1))
			senseid = 0
		elif senseEndRe.match(l):
			if eid in jmEntries:
				jEntry = jmEntries[eid]
				if senseid in jEntry.senses:
					sense = jEntry.senses[senseid]
					for lang in ('fr', 'ru', 'de'):
						if lang in sense.glosses:
							glosses = sense.glosses[lang].split('\n')
							for gloss in glosses:
								jmdicti18n.write('<gloss xml:lang="%s">%s</gloss>\n' % (langMatchInv[lang], gloss))
			senseid += 1
		jmdicti18n.write(l)
		if len(l) == 0: break
