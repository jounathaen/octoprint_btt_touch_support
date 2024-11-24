# OctoPrint-BTT TFT Touchscreen support

This plugin adds support for the remote printing features of the [BigTreeTech TFT Touchscreen](https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware) for [OctoPrint](https://github.com/OctoPrint/OctoPrint).

- Automatically switch to printing mode on the TFT upon print start.
- Update the progress indicator on the TFT during print.
- Update the remaining time on the TFT during print.
- Update the Layer progress on the TFT (requires [DisplayLayerProgress](https://github.com/OllisGit/OctoPrint-DisplayLayerProgress))
- React to the TFT's _Pause_, _Resume_ and _Cancel_ buttons on in OctoPrint.

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
