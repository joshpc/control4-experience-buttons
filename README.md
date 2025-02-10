# Control4 Experience buttons
This uses the default system provided UIButton proxy driver to create buttons (without controls) in the App/Remote.

This is desirable since the alternative is to use something that wraps the dvd proxy and it shows the dvd controls (the red/blue/yellow/green buttons) by default, despite none of them being configured.

# How to Manually Deploy
Compress the contents of the the folders (www, driver.xml, etc. but not the wrapping folder) as a zip file. Change the filetype to `c4z` and upload to your device via Composer.

# How to Build your Own
Without needing to know Control4's driver structure, you can simply replicate the existing driver structure and update the following pieces:

## `driver.xml`
1. Update the `manufacturer`, `name`, `model`, `creator`, `created`, `modified`, and `version` tags. The values you choose here will show up in the UI. Ensure that you increase the `version` number so that updates get processed correctly.
2. Update the `documentation` to say whatever you want it to say (at least update the device name)
3. Provide new `display_icons` and update the path to match the **driver name** (see below). You can optionally add "selected" versions of the icons as long as you reference them separately under the `<state id="Selected">` tag.

## **Driver Name**
You'll have noticed that the path for the images will be something along the lines of: `controler://driver/<SOMETHING HERE>/icons/device/....png`. The `<SOMETHING HERE>` represents your driver name which is really just the name of the `c4z` file you'll generate in the next section. Ensure that this identical otherwise the images won't load correctly since this isn't referenced in the `driver.xml`.

## Github Workflow
Update `.github/workflows/release.yml` to include your driver. Simply add a new section (as below) to generate a `c4z` file and it'll be picked up immediately be the release action.

```
      - name: Package <YOUR DEVICE> Driver
        run: |
          cd <FOLDER WITH YOUR DRIVER>
          zip -r ../<DEVICE_NAME>.c4z ./*
          cd ..
```