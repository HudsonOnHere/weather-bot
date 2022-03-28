# Change Log

v2.1.0 - 3/28/2022
- v2.1.0 Code refactor
	- Refactored functions into classes
		- Allow for different users to interact with the bot without collision
	- Fixed hourly forecast data printing
		- now based off startTime API data, converted from UTC to EST
	- Changed Alerts data requests to be dynamic
		- Now based on users real location
	- Weather locations are truly hyoer-local now
		- based on users location data, not hardcoded NYC location
	- Updated License formatting better printing on mobile
	- Bot message text formatting in some instances
	- Proper logging introduced


v2.0.0 - 12/18/2021
- v2.0.0 UPDATE, complete overhaul
	- original version now deprecated
	- moved away from OpenWeather API to National Weather Service
	- moved away from telebot python library to pyTelegramAPI library
	- added several additional functions
		- /forecast - displays daily weather data
		- /hourly - displays hour-to-hour data for a 12 hour period
		- /alerts - notifies of any active weather alerts in area
	- more to come...


v1.1.0
- Initial push
	- relatively stable for long periods of time
	- Telegram API times out sometimes, possibly related to VPN connectivity drops on wifi
	- added /start & /help commands
- Future versions
	- should include percentage chance of rain
	- an option to switch to ˚C or display both ˚F/˚C
	- triggers and/or automation to run at set times
	- more functionality via the OpenWeather API
		- option to pull specified data?

