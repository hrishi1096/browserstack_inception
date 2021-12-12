# Browserstack Inception
Technical assignment - BrowserStack Inception

`bstack_inception.py`

# What does it do?

* visit google.com
* search for "Browserstack"
* click on the correct entry from the google search results to visit Browserstack.com
* click on Sign in, thus, landing on the sign in page 
* enter the email id and password and click submit
* from the live dashboard now, go to windows 11, and launch a live session with chrome 96
* inside the live session, there appears a banner for 'self signed certificate', click 'got it'
* search for browserstack on google inside the live session
* finally, stop the live session


The steps mentioned above are automated by `bstack_inception.py`

## Some problems while running this with Browserstack remote driver

Visiting google.com fires up google in Dutch, because of which some element searches fail.
for eg. `input[aria-label="Search"]` is actually `input[aria-label="Zock"]` (or something like that)
Dutch.

Can be seen here - [failure_due_to_location](https://automate.browserstack.com/dashboard/v2/builds/cd4c261a0442aa967752c42fda723c6b079bbb4a/sessions/228b8b1a1e7b003290fa543ca499c06f64c5763b?buildUserIds=5508823)

### Ways to solve this problem

* Using Browserstack local testing with the `--force-local` flag. [Force-local-session](https://automate.browserstack.com/dashboard/v2/builds/d850cd3a2fd5aac93254d0478611726ce052e75f?buildUserIds=5508823) 

* Using `"browserstack.geoLocation": "IE"` in capabilitites. [geolocation-session](https://automate.browserstack.com/dashboard/v2/builds/690a6348ce06ccd8da27fd9c294ce603f5f389b1?buildUserIds=5508823)

## Jenkins integration 

[Jenkins-build](https://automate.browserstack.com/dashboard/v2/builds/138bc76e7eacda1142cf5cff77d348b9303f24ee?buildUserIds=5508823)




