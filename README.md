# OctoPrint-BTT TFT Touchscreen support

This plugin adds support for the remote printing features of the [BigTreeTech TFT Touchscreen](https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware).

- Update the progress indicator.
- Update the remaining time.
- Update the Layer progress (requires [DisplayLayerProgress](https://github.com/OllisGit/OctoPrint-DisplayLayerProgress))
- Support for _Pause_, _Resume_ and _Cancel_ buttons.

This is a fork of the [M73Progress Plugin](https://github.com/cesarvandevelde/OctoPrint-M73Progress) - thanks for the work!

<p align="center">
    <img style="width: 35%;" src="https://github.com/jounathaen/octoprint_btt_touch_support/blob/master/btt_touchscreen.jpg" alt="Picture of a BTT TFT Touchscreen">
</p>

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/jounathaen/octoprint_btt_touch_support/archive/master.zip

## Configuration

You can fine-tune the plugin's behavior in the `BTT TFT Touchscreen` tab in the OctoPrint settings:

* `Use time estimate`: By default, the plugin uses OctoPrint's built-in progress
  estimate, which is based on the progress inside a G-code file. In some cases,
  a better progress estimate can be calculated from the time elapsed and the
  time remaining: `P = elapsed / (elapsed + remaining)`. This option is
  particularly useful for
  [PrintTimeGenius](https://github.com/eyal0/OctoPrint-PrintTimeGenius) users.
