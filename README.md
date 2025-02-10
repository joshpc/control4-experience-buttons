# Control4 Experience buttons
This uses the default system provided UIButton proxy driver to create buttons (without controls) in the App/Remote.

This is desirable since the alternative is to use something that wraps the dvd proxy and it shows the dvd controls (the red/blue/yellow/green buttons) by default, despite none of them being configured.

# How to Build your Own

1. (If necessary) install [Python](https://www.python.org/downloads/) -- The version shouldn't matter too much but this was built with 3.11
2. Install Python requirements:
```bash
pip install -r requirements.txt
```

3. Run the following script:
```bash
python scripts/generate_driver.py
```
4. Update the workflow or manually deploy (see below)

## **Notes**
While generating the drive you'll be asked for the following parameters

```
device_name - This is used to generate the driver (i.e. if you enter 'xbox' you will get a driver named 'uibutton_xbox'.) These must be unique.
manufacturer - This is only displayed in Composer
model_name - This is the model name displayed to the user (i.e. Xbox Series X)
creator - This is only displayed in Composer. Your name.
source image - This is a large image (ideally over 1024x1024) used to generate all of the icons.
driver version - The value doesn't matter but if you update your driver in the future, increment this
OS Version - Update this if you plan on requiring features that are only available in later Control4 OS versions
```

## Deploying with Github Actions
Update `.github/workflows/release.yml` to include your driver. Simply add a new section (as below) to generate a `c4z` file and it'll be picked up immediately be the release action which runs on every push to `main`.

```
      - name: Package <YOUR DEVICE> Driver
        run: |
          cd <FOLDER WITH YOUR DRIVER>
          zip -r ../<DEVICE_NAME>.c4z ./*
          cd ..
```

# How to Manually Deploy
Compress the contents of the the folders (www, driver.xml, etc. but not the wrapping folder) as a zip file. Change the filetype to `c4z` and upload to your device via Composer.

# How to Manually Build your Own
Without needing to know Control4's driver structure, you can simply replicate the existing driver structure and update only the following pieces:

1. **driver.xml**: Update the `manufacturer`, `name`, `model`, `creator`, `created`, `modified`, and `version` tags. The values you choose here will show up in the UI. Ensure that you increase the `version` number so that updates get processed correctly.
2. **driver.xml**: Update the `documentation` to say whatever you want it to say (at least update the device name)
3. Provide new `display_icons` and update the path to match the **driver name** (see below). You can optionally add "selected" versions of the icons as long as you reference them separately under the `<state id="Selected">` tag.
