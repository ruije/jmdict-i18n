import re

msgctxRe = re.compile('msgctxt "(.*)"')
msgidRe = re.compile('msgid "(.*)"')
msgstrRe = re.compile('msgstr "(.*)"')
strRe = re.compile('"(.*)"')
languageRe = re.compile('"Language: (..)')

class GetTextEntry:
	def __init__(self, lang):
		self.msgctx = ""
		self.msgid = ""
		self.msgstr = ""
		self.lang = lang

	def __str__(self):
		r = ""
		if self.msgctx:
			r += 'msgctxt "%s"\n' % (self.msgctx,)
		s = self.msgid.replace('"', '\\"').replace('\n', '\\n"\n"')
		if '\n' in s: s = '"\n"' + s
		r += 'msgid "%s"\n' % (s,)
		s = self.msgstr.replace('"', '\\"').replace('\n', '\\n"\n"')
		if '\n' in s: s = '"\n"' + s
		r += 'msgstr "%s"\n' % (s,)
		r += '\n'
		return r

class GetTextFile:
	def __init__(self, name, mode):
		self.f = open(name, mode, encoding='utf-8')

	def readEntries(self):
		# Find language in header
		while True:
			l = self.f.readline()
			match = languageRe.match(l)
			if (match):
				lang = match.group(1)
				break
			if len(l) == 0: break
		# Skip until first entry
		while True:
			l = self.f.readline()
			if l == '\n': break
			if len(l) == 0: break
		# Now we can parse the entries
		entries = []
		currentEntry = None
		mode = None
		while True:
			l = self.f.readline()
			if l == '\n':
				if currentEntry:
					entries.append(currentEntry)
					currentEntry = None
					mode = None
				continue
			if mode == "ID" and strRe.match(l):
				currentEntry.msgid += strRe.match(l).group(1)
				continue
			elif mode == "STR" and strRe.match(l):
				currentEntry.msgstr += strRe.match(l).group(1)
				continue
			else: mode = None
			match = msgctxRe.match(l)
			if match:
				if not currentEntry: currentEntry = GetTextEntry(lang)
				currentEntry.msgctx = match.group(1)
				continue
			match = msgidRe.match(l)
			if match:
				if not currentEntry: currentEntry = GetTextEntry(lang)
				s = match.group(1)
				if len(s): currentEntry.msgid += s
				mode = "ID"
				continue
			match = msgstrRe.match(l)
			if match:
				s = match.group(1)
				if len(s): currentEntry.msgstr += s
				mode = "STR"
				continue
			if len(l) == 0: break
		if currentEntry: entries.append(currentEntry)
		for entry in entries:
			entry.msgid = entry.msgid.replace('\\"', '"').replace('\\n', '\n')
			entry.msgstr = entry.msgstr.replace('\\"', '"').replace('\\n', '\n')
		return entries
