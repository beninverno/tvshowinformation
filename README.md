# tvshowinformation
Python Module that allows access to TV Show information in a simple way using the TVMaze API.

## Requirements
- Python 3
- urllib
- json

## Instructions
- Uses the **showInformation** class to retrieve information on TV Shows. List of functions are provided below.
- Use the *testers.py* file to test inputs and outputs.
- Import using ``` from tvshowinformation import * ```

## Functions
```
from tvshowinformation import *

tvshow = showInformation(show)

tvshow.getSeasons()                           ## Returns amount of seasons in TV Show
tvshow.getEpisodesTotal()                     ## Returns total amount of episodes in TV Show as an integer
tvshow.getEpisodesInSeason(season)            ## Returns amount of episodes in specified season of TV Show as an integer
tvshow.getEpisodeName(season, episode)        ## Returns name of episode of corresponding Episode in Season
tvshow.getCast()                              ## Returns comma-seperated cast as a string
tvshow.getGenres()                            ## Returns comma-seperated genre(s) as a string
tvshow.getTotalRuntime()                      ## Returns total runtime of TV Show as an integer
tvshow.getEpisodeRuntime(season, episode)     ## Returns runtime of Episode number in specified season
tvshow.getShowSummary()                       ## Returns the summary of the TV Show
tvshow.getEpisodeDescription(season, episode) ## Returns description of specified episode
```
## API
The API used is provided by TVmaze.com, and any information or documentation on the use of the API can be found at https://www.tvmaze.com/api.


