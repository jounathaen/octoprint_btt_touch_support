# coding=utf-8
from __future__ import absolute_import, division

import logging

import octoprint.plugin
from octoprint.events import Events
from octoprint.printer import PrinterCallback


logger = logging.getLogger(__name__)


class ProgressMonitor(PrinterCallback):
    def __init__(self, *args, **kwargs):
        super(ProgressMonitor, self).__init__(*args, **kwargs)
        self.reset()

    def reset(self):
        self.completion = None
        self.time_elapsed_s = None
        self.time_left_s = None

    def on_printer_send_current_data(self, data):
        self.completion = data["progress"]["completion"]
        self.time_elapsed_s = data["progress"]["printTime"]
        self.time_left_s = data["progress"]["printTimeLeft"]


class BTT_Touch_Support(
    octoprint.plugin.ProgressPlugin,
    octoprint.plugin.EventHandlerPlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.RestartNeedingPlugin,
):
    def on_after_startup(self):
        self._progress = ProgressMonitor()
        self._printer.register_callback(self._progress)

        settings = self._settings
        self.progress_from_time = settings.get_boolean(["progress_from_time"])

    def on_event(self, event, payload):
        self._logger.debug("got event {}".format(event))
        if event == Events.PRINT_STARTED or event == Events.PRINT_DONE:
            # Firmware manages progress bar when printing from SD card
            if payload.get("origin", "") == "sdcard":
                return

        if event == Events.PRINT_STARTED:
            self._progress.reset()
            self._set_progress(0)
            self._printer.commands(["M118 P0 A1 action:print_start"])
        elif event == Events.PRINT_DONE:
            self._set_progress(100, 0)
            self._printer.commands(["M118 P0 A1 action:print_end"])
        elif event == Events.PRINT_CANCELLED:
            self._printer.commands(["M118 P0 A1 action:cancel"])
        elif event == Events.PRINT_PAUSED:
            self._printer.commands(["M118 P0 A1 action:pause"])
        elif event == Events.PRINT_RESUMED:
            self._printer.commands(["M118 P0 A1 action:resume"])
        elif event == "DisplayLayerProgress_layerChanged":
            cmd = "M118 P0 A1 action:notification Layer Left {}/{}".format(
                payload.get("currentLayer", "0"), payload.get("totalLayer", "0")
            )
            self._logger.debug("layer progress changed: {}".format(cmd))
            self._printer.commands([cmd])

    def on_print_progress(self, storage, path, progress):
        if not self._printer.is_printing():
            return

        # Firmware manages progress bar when printing from SD card
        if storage == "sdcard":
            return

        progress = 0.0
        time_left = self._progress.time_left_s / 60

        if (
            self.progress_from_time
            and self._progress.time_left_s is not None
            and self._progress.time_elapsed_s is not None
        ):
            time_left_s = self._progress.time_left_s
            time_elapsed_s = self._progress.time_elapsed_s
            progress = time_elapsed_s / (time_left_s + time_elapsed_s)
            progress = progress * 100.0
        else:
            progress = self._progress.completion or 0.0

        self._set_progress(progress=progress, time_left=time_left)

    def _set_progress(self, progress, time_left=None):
        if time_left is None:
            gcode1 = "M118 P0 A1 action:notification Time Left 00h00m00s"
        else:
            gcode1 = "M118 P0 A1 action:notification Time Left {:02.0f}h{:02.0f}m{:02.0f}s".format(
                time_left / 60, time_left % 60, self._progress.time_left_s % 60
            )

        gcode2 = "M118 P0 A1 action:notification Data Left {:.0f}/100".format(progress)

        self._printer.commands([gcode1, gcode2])

    def get_settings_defaults(self):
        return dict(progress_from_time=False)

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        settings = self._settings
        self.progress_from_time = settings.get_boolean(["progress_from_time"])

    def get_template_configs(self):
        return [
            dict(
                type="settings",
                name="BTT TFT Touchscreen",
                custom_bindings=False,
            )
        ]

    def get_update_information(self):
        return dict(
            btt_touch_support=dict(
                displayName="BTT TFT Touchscreen support",
                displayVersion=self._plugin_version,
                # version check: github repository
                type="github_release",
                user="jounathaen",
                repo="OctoPrint-BTT_Touch_Support",
                current=self._plugin_version,
                # update method: pip
                pip="https://github.com/jounathaen/octoprint_btt_touch_support/archive/{target_version}.zip"
            )
        )

    def hook_actioncommands(self, comm, line, command, *args, **kwargs):
        self._logger.debug("Command received: 'action:%s'" % (command))

        if command == None:
            return

        if command == "notification remote pause":
            self._logger.debug("pausing")
            self._printer.pause_print()
        if command == "notification remote resume":
            self._logger.debug("resuming")
            self._printer.resume_print()
        if command == "notification remote cancel":
            self._logger.debug("canceling")
            self._printer.cancel_print()


__plugin_name__ = "BTT TFT TouchScreen Support"
__plugin_pythoncompat__ = ">=2.7,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = BTT_Touch_Support()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.action": __plugin_implementation__.hook_actioncommands,
    }
