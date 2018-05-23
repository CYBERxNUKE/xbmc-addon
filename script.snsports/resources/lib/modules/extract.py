
import zipfile, xbmcgui

def auto(_in, _out):

    return allNoProgress(_in, _out)
	
def all(_in, _out, dp=None):
    if dp:
        return allWithProgress(_in, _out, dp)

    return allNoProgress(_in, _out)
        
def all_update(_in, _out, dp=None):
    if dp:
        return allWithProgress_update(_in, _out, dp)

    return allNoProgress_update(_in, _out)

def allNoProgress(_in, _out):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    
    except Exception, e:
        print str(e)
        return False

    return True


def allWithProgress(_in, _out, dp):

	try:
		zin    = zipfile.ZipFile(_in,  'r')
	except:
		dialog = xbmcgui.Dialog()
		import traceback as tb
		(etype, value, traceback) = sys.exc_info() 
		tb.print_exception(etype, value, traceback)
		error_traceback = tb.format_tb(traceback)
		if "bytes" in str(error_traceback).lower():
			dialog.ok(AddonTitle, 'Sorry, your connection to the download was lost before the file could be downloaded. Please try again.')
			dp.close()
			quit()
		elif "file is not a zip file" in str(error_traceback).lower():
			dialog.ok(AddonTitle, 'Sorry, the file is not a zip file.')
			dp.close()
			quit()
		else:
			dialog.ok(AddonTitle, 'Sorry, there was a problem extracting the file.')
			dp.close()
			quit()
	nFiles = float(len(zin.infolist()))
	count  = 0

	try:
		for item in zin.infolist():
			count += 1
			update = count / nFiles * 100
			dp.update(int(update),'','','[COLOR dodgerblue][B]' + str(item.filename) + '[/B][/COLOR]')
			try:
				zin.extract(item, _out)
			except Exception, e:
				print str(e)

    
	except Exception, e:
		print str(e)
		return False

	return True

def allWithProgress_update(_in, _out, dp):
	zin    = zipfile.ZipFile(_in,  'r')
	nFiles = float(len(zin.infolist()))
	count  = 0
	skin_selected = 0
	#try:
	for item in zin.infolist():
		count += 1
		update = count / nFiles * 100
		dp.update(int(update),'','','[COLOR dodgerblue][B]' + str(item.filename) + '[/B][/COLOR]')

		if "userdata/skin" in str(item.filename):
			if skin_selected == 0:
				choice = xbmcgui.Dialog().yesno("IMPORTANT INFORMATION", "We have detected that this segment of the update contains changes to the skin files. If you agree to install this segment of the update it could result in you losing menu items etc that you have set. Would you like to install this segment of the update?" ,yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
				skin_selected = 1
				if choice == 1:
					try:
						zin.extract(item, _out)
					except Exception, e:
						print str(e)
		else:
			try:
				zin.extract(item, _out)
			except Exception, e:
				print str(e)
    
	#except Exception, e:
	#    print str(e)
	#    return False

	return True