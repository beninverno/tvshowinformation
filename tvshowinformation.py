import json
import sys
from urllib import request, error


class showInformation(object):
    def __init__(self, show):
        """Initiates all the variables required for the functions below to work.

        Args:
            show: String: TV Show used in the URL to lookup information

        Variables:
            self.seasonepisodedict: Dictionary containing the seasons as key with the amount of episodes in that season
            self.show: Show name stored as a lowercase string
            self.episodenamelist: Nested list of episode names, accessed by first index being season and second index being episode number in season.
            self.runtimedescriptionofepisodes: Dictionary that stores episode name as a key, with the running time and description of that episode as the value as a list, with running time at index 0 and description at index 1.
            self.cast: Stores cast members as seperate strings inside a list
            self.genres: Stores genre(s) as seperate strings inside a list
            self.showdescription: String that stores the description of the show
            self.infourl: url of API needed to retrieve the information (more importantly, the ID number)
            self.showid: Retrieves ID of the show through API and a seperate function called 'getid'
            self.episodesurl: The url that gets all the information about the episodes of the show.
            self.casturl: The url used that retrieves the cast members in a show

        Returns:
            N/A

0        Raises:
            N/A
        """
        self.seasonsepisodedict = {}
        self.show = show.lower()
        self.episodenamelist = []
        self.runtimedescriptionofepisodes = {}
        self.cast = []
        self.genres = []
        self.showdescription = ''
        self.infourl = 'http://api.tvmaze.com/singlesearch/shows?q=' + self.show
        self.showid = showInformation.getIdShowInfo(self)
        self.episodesurl = 'http://api.tvmaze.com/shows/' + str(self.showid) + '/episodes'
        self.casturl = 'http://api.tvmaze.com/shows/' + str(self.showid) + '/cast'
        self.rating = showInformation.getShowRating(self)

        showInformation.populate(self)

    def getJson(link):
        """"Returns JSON from API link

        Args:
            link: string with the link to API where you're extracting the JSON from

        Returns:
            python-decoded JSON of information

        Raises:
            Exception if HTTP Error occurs.
        """
        try:
            with request.urlopen(link) as url:
                data = (json.loads(url.read().decode()))
        except error.HTTPError:
            return None
            
        return data

    def getIdShowInfo(self):
        """Retrieves the identification number used to get other information about the show from API,
        also retrieves the summary of the show and appends it to self.showdescription.

        Args:
            N/A

        Returns:
            N/A

        Raises:
            Exception: If TV Show is not found in API
            Exception: If ID was not found in JSON file
        """
        data = showInformation.getJson(self.infourl)
        if data == None:
            print('TV Show could not be found')
            sys.exit()
        elif "id" in data:
            if "summary" in data:
                self.showdescription = data["summary"]
            return data["id"]
        else:
            raise Exception('Could not retrieve ID!')

    def getShowRating(self):
        """Retrives the average rating of the TV show

        Args:
            N/A

        Returns:
            Average rating as floating point number

        Raises:
            N/A
        """
        data = showInformation.getJson(self.infourl)
        rating = float(data["rating"]["average"])
        return rating
        

    def populateCast(self):
        """Populates a list of cast of tv show, and returns it
        
        Args:
            N/A

        Returns:
            Cast members in a list

        Raises:
            Exception: If cast is not found in API
        """
        data = showInformation.getJson(self.casturl)
        cast = []
        for index in data:
            new = index["person"]
            cast.append(new["name"])
        return cast
                    

    def populateGenre(self):
        """Populates a list with genres of TV show, and returns the list

        Args:
            N/A

        Returns:
            Genre(s) in a list

        Raises:
            N/A
        """
        
        data = showInformation.getJson(self.infourl)
        if "genres" in data:
            return data["genres"]
        else:
            return False
        
    def stringsToRemove(self, stringtoedit):
        """Removes html tags from description strings

        Args:
            stringtoedit: string that you want to remove tags from

        Returns:
            string with tags removed

        Raises:
            N/A
        """
        stringsToRemove = ['<p>', '<b>', '</p>', '</b>']
        try:
            for strings in stringsToRemove:
                stringtoedit = stringtoedit.replace(strings, '')
            return stringtoedit
        except AttributeError:
            return None
        
    def populate(self):
        """
        Populates the self.seasonsepisodedict with information about the seasons and episodes.
        Populates self.episodenamelist with episode names.
        Populates self.cast with a list of cast members.
        Populates self.genres with a list of the TV Show's genre(s).

        Args:
            N/A

        Returns:
            N/A

        Raises:
            N/A
        """
        seasons = [0]
        season = 0
        episodes = [0]
        namelist = [[0]]
        runtimelist = [[0]]
        episodedescriptionlist = [[0]]
        data = showInformation.getJson(self.episodesurl)
        for dicts in data:
            for keys in dicts:
                if keys == "season" and dicts[keys] not in seasons: 
                    seasons.append(dicts[keys])
                    season = dicts[keys]
                    episodes.append(0)
                    namelist.append([0])
                    runtimelist.append([0])
                    episodedescriptionlist.append([0])
                if keys == "number":
                    episodes[season] += 1
            namelist[season].append(dicts["name"])
            runtimelist[season].append(dicts["runtime"])
            episodedescriptionlist[season].append(self.stringsToRemove(dicts["summary"]))
            
        for i in range(1, len(seasons)):
            self.seasonsepisodedict[seasons[i]] = episodes[i]

        for i in range(len(namelist)):
            for j in range(len(namelist[i])):
                self.runtimedescriptionofepisodes[namelist[i][j]] = [runtimelist[i][j], episodedescriptionlist[i][j]]
                   
        self.cast = showInformation.populateCast(self)
        self.genres = showInformation.populateGenre(self)
        self.episodenamelist = namelist
        
    def getSeasons(self):
        """Retrieves the amount of seasons the show has

        Args:
            N/A

        Returns:
            Amount of Seasons in TV Show as an Integer

        Raises:
            N/A
        """
        return(max(self.seasonsepisodedict))

    def getEpisodesTotal(self):
        """Retrieves amount of total episodes the show has and returns as an integer

        Args:
            N/A

        Returns:
            Amount of total episodes in the show as Integer

        Raises:
            N/A
        """
        totalepisodes = 0
        for seasons in self.seasonsepisodedict:
            totalepisodes += self.seasonsepisodedict[seasons]
        return totalepisodes

    def getEpisodesInSeason(self, seasonnum):
        """Retrieves amount of episodes in specified season and returns as an integer

        Args:
            seasonnum: Season Number that you want to retrieve amount of episodes for

        Returns:
            Amount of episodes in specified season (seasonnum) as an integer.

        Raises:
            N/A
        """
        if type(seasonnum) is not int:
            return('Invalid Input, must be integer.')
        try:
            return self.seasonsepisodedict[seasonnum]
        except KeyError:
            return('N/A (Does not exist)')

    def getEpisodeName(self, seasonnum, episodenum):
        """Retrieves the episode name from nested list and returns as a string

        Args:
            seasonnum: Season number that you want to retrieve episode name
            episodenum: Episode number that you want to retrieve episode name

        Returns:
            Episode name from specified season and episode

        Raises:
            N/A
        """
        if (type(seasonnum) is not int) and (type(episodenum) is not int):
            return('Invalid input, season number and episode number must be integers.')
        try:
            return self.episodenamelist[seasonnum][episodenum]
        except IndexError:
            print('Season or Episode is out of range.')
            return

    def getCast(self):
        """Retrieves cast from list and returns it as a single string with actors seperate by commas.
        Args:
            N/A

        Returns:
            Cast as a string

        Raises:
            N/A
        """
        caststring = ''
        if self.cast == []:
            return 'No Cast List'
        for castmember in self.cast:
            caststring += (castmember)
            if castmember != self.cast[-1]:
                caststring += ', '
        return caststring

    def getGenres(self):
        """Retrieves genre(s) from list and returns them as a single string with genre(s) seperate by commas.

        Args:
            N/A

        Returns:
            Genre(s) as a string

        Raises:
            N/A
        """
        genresstring = ''
        if self.genres == []:
            return 'No Genre Listed'
        for genre in self.genres:
            genresstring += genre
            if genre != self.genres[-1]:
                genresstring += ', '
        return genresstring

    def getTotalRuntime(self):
        """Retrieves runtime of each episode and returns the sum of all episode runtimes.

        Args:
            N/A

        Returns:
            Total Runtime of show as an integer

        Raises:
            N/A
        """
        totalRuntime = 0
        for keys in  self.runtimedescriptionofepisodes:
            totalRuntime +=  self.runtimedescriptionofepisodes[keys][0]
        return totalRuntime

    def getEpisodeRuntime(self, seasonnum, episodenum):
        """Returns run time of certain episode which is specified by
        season (seasonnum) and the episode (episodenum) in corresponding season

        Args:
            seasonnum: Season Number which corresponds to episode you want to get runtime of
            episodenum: Episode in corresponding season that you want to get runtime of

        Returns:
            Episode runtime as an integer

        Raises:
            N/A
        """
        if (type(seasonnum) is not int) and (type(episodenum) is not int):
            return('Invalid input, season number and episode number must be integers.')
        try:
            episodename = showInformation.getEpisodeName(self, seasonnum, episodenum)
            return self.runtimedescriptionofepisodes[episodename][0]
        except IndexError:
            return('N/A (Runtime not found)')
        except KeyError:
            return('N/A (Runtime not found)')

    def getShowSummary(self):
        """Returns summary of the show as a string, stripped of its <b> and <p> elements.

        Args:
            N/A

        Returns:
            Summary as a string

        Raises:
            N/A
        """ 
        return self.stringsToRemove(self.showdescription)

    def getEpisodeDescription(self, seasonnum, episodenum):
        """Retrieves episode description from runtimeofepisodes dictionary, and returns
        it.

        Args:
            seasonnum: Season number of episode you want to retrieve
            episodenum: Episode number in season you want to retrieve

        Returns:
            Description of episode as a string

        Raises:
            N/A
        """
        if (type(seasonnum) is not int) and (type(episodenum) is not int):
            return('Invalid input, season number and episode number must be integers.')
        try:
            episodename = showInformation.getEpisodeName(self, seasonnum, episodenum)
            return self.runtimedescriptionofepisodes[episodename][1]
        except IndexError:
            return('N/A (Description not found)')
        except KeyError:
            return('N/A (Description not found)')

