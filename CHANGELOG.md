# Change Log

v2.0.0 - 12/18/2021
- v2.0.0 UPDATE, complete overhaul
	- original version now deprecated
	- moved away from OpenWeather API to National Weather Service for much better data
	- moved away from telebot python library to pyTelegramAPI library (highly recommended)
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

