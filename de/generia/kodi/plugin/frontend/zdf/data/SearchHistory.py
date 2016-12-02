from datetime import datetime
import xbmc

DATE_FORMAT = "%d.%m.%Y"

class HistoryEntry(object):
    date = None
    query = None
    
    def __init__(self, query, contentTypes=None, date=datetime.now().strftime(DATE_FORMAT)):
        self.query = query
        self.contentTypes = contentTypes
        self.date = date

    def getDateFormatted(self):
        return self.date.strftime(DATE_FORMAT)
        

class SearchHistory(object):
    entries = []
    storeFile = None
    searchHistorySize = None
    
    def __init__(self, storeFile, searchHistorySize):
        self.storeFile = storeFile
        self.searchHistorySize = searchHistorySize
                    
    def getEntries(self):
        entries = self._loadEntries()
        return entries
    
    def addEntry(self, entry):
        entries = self._loadEntries()
        
        found = False
        for e in entries:
            if e.query.lower() == entry.query.lower():
                e.query = entry.query
                e.date = entry.date
                e.contentTypes = entry.contentTypes
                found = True
                break
        
            
        #print "addEntry: size=" + str(len(entries)) + ", " + entry.query
        #xbmc.log("addEntry: " + str(len(entries)) + " > " + str(self.searchHistorySize), level=xbmc.LOGNOTICE)
        if len(entries) > self.searchHistorySize-1:
            entries = entries[0:self.searchHistorySize-1]
            #xbmc.log("addEntry-2: " + str(len(entries)) + " ?= " + str(self.searchHistorySize), level=xbmc.LOGNOTICE)

        if not found:
            entries.append(entry)

        self._saveEntries(entries)

    def _loadEntries(self):
        entries = []
        try:
            with open(self.storeFile, "r") as lines:
                entries = []
                for line in lines:
                    entry = self._parseEntry(line)
                    if entry is not None:
                        entries.append(entry)
        except IOError:
            pass
        return entries
                
    def _parseEntry(self, line):
        i = line.find(" ");
        if i == -1:
            return None        
        j = line.find(" ", i+1)
        if j == -1:
            return None        
        
        date = line[0:i]
        contentTypes = line[i+1:j]
        query = line[j+1:len(line)-1]
        xbmc.log("_parseEntry: " + str(date) + "-" + query, level=xbmc.LOGNOTICE)
        return HistoryEntry(query, contentTypes, date)  

    def _saveEntries(self, entries):
        xbmc.log("_saveEntries: " + str(len(entries)), level=xbmc.LOGNOTICE)
                 
        file = open(self.storeFile, "w")
        for entry in entries:
            date = entry.date #getDateFormatted()
            file.write('{0} {1} {2}\n'.format(date, entry.contentTypes, entry.query))
        file.close()
