import sublime, sublime_plugin, urllib, urllib2, threading, os, json
settings = sublime.load_settings('EventStore.sublime-settings')
urlBase = settings.get('EventStoreUrl')

def makeApiCall(url, operation, data, ignore404):
	try:
		request = urllib2.Request(url, data)
		request.get_method = lambda: operation
		http_file = urllib2.urlopen(request, timeout=30)
		result = http_file.read()
		return result
	except (urllib2.HTTPError) as (e):
		err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
		code = e.code;
	except (urllib2.URLError) as (e):
		err = '%s: URL error %s contacting API' % (__name__, str(e.reason))
		code = e.reason;
	
	#special case for the get to check if exists, 404 is expected
	if ignore404 and code == 404:
		return None

	sublime.error_message(err)
	return None;

#extend WindowCommand, lets you act on the current window
class SaveProjectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.status_message("Uploading projection")
		if self.view.settings().has("projectionName"):
			projectionName = self.view.settings().get("projectionName")
			self.doUpload()
		else:
			#ask for a projection name
			startingText = ""
			if not self.view.file_name() == None:
				self.onDone(os.path.splitext(os.path.basename(self.view.file_name()))[0])
			else: 
				self.view.window().show_input_panel("Choose a name for this projection", startingText , self.onDone, self.onChange, self.onCancel)

	def onDone(self, result):
		self.view.settings().set("projectionName", result)
		self.doUpload()

	def onChange(self, result):
		return

	def onCancel(self):
		return

	def doUpload(self):
		projectionName = urllib.quote(self.view.settings().get("projectionName"))
		projectionText = self.view.substr(sublime.Region(0, self.view.size()))
		
		queryUrl = urlBase + "/projection/" +  projectionName + "/query"
		postUrl = urlBase + "/projections/persistent?name=" + projectionName
		existingProjection = makeApiCall(queryUrl,"GET",None, True)
		if existingProjection != None:
			#do nothing if projection has not actually changed
			if existingProjection != projectionText:
				makeApiCall(queryUrl,"PUT",projectionText, False)
		else:
			makeApiCall(postUrl,"POST", projectionText, False)
		sublime.status_message("Upload Complete")
		self.view.set_syntax_file("Packages/Javascript/Javascript.tmLanguage")
	

class OpenProjectionCommand(sublime_plugin.WindowCommand):
	
	def run(self):
		self.projectionNameList = []
		sublime.status_message("Getting projections list")
		projectionsList = makeApiCall(urlBase + "/projections/any", "GET", None, False)
		decodedList = json.loads(projectionsList)["projections"]
		for projection in decodedList:
			if not projection["name"].startswith("$"):
				self.projectionNameList.append(projection["name"])
		self.window.show_quick_panel(self.projectionNameList, self.projectionChosen)

	def projectionChosen(self,index):
		if not index == -1:
			print index
			projectionName = self.projectionNameList[index]
			emptyView = self.window.new_file()
			emptyView.set_name(projectionName + ".js")
			#get the projection query
			queryUrl = urlBase + "/projection/" +  projectionName + "/query"
			existingProjection = makeApiCall(queryUrl,"GET",None, False)
			theEdit = emptyView.begin_edit()
			emptyView.insert(theEdit, 0, existingProjection)
			emptyView.end_edit(theEdit)
			emptyView.set_syntax_file("Packages/Javascript/Javascript.tmLanguage")
			theSettings = emptyView.settings()
			theSettings.set("projectionName", projectionName)
