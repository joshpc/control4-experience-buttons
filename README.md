# Control4 Experience buttons
This uses the default system provided UIButton proxy driver to create buttons (without controls) in the App/Remote.

This is desirable since the alternative is to use something that wraps the dvd proxy and it shows the dvd controls (the red/blue/yellow/green buttons) by default, despite none of them being configured.

# How to Deploy
Compress the contents of the the folders (www, driver.xml, etc. but not the wrapping folder) as a zip file. Change the filetype to `c4z` and upload to your device via Composer.
