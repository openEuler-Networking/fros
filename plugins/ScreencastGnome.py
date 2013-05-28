"""
  <interface name="org.gnome.Shell.Screencast">

    <!--
        Screencast:
        @file_template: the template for the filename to use
        @options: a dictionary of optional parameters
        @success: whether the screencast was started successfully
        @filename_used: the file where the screencast is being saved

        Records a screencast of the whole screen and saves it
        (by default) as webm video under a filename derived from
        @file_template. The template is either a relative or absolute
        filename which may contain some escape sequences - %d and %t
        will be replaced by the start date and time of the recording.
        If a relative name is used, the screencast will be saved in the
        $XDG_VIDEOS_DIR if it exists, or the home directory otherwise.
        The actual filename of the saved video is returned in @filename_used.
        The set of optional parameters in @options currently consists of:
            'draw-cursor'(b): whether the cursor should be included in the
                              recording (true)
            'framerate'(i): the number of frames per second that should be
                            recorded if possible (30)
            'pipeline'(s): the GStreamer pipeline used to encode recordings
                           in gst-launch format; if not specified, the
                           recorder will produce vp8 (webm) video (unset)
    -->
    <method name="Screencast">
      <arg type="s" direction="in" name="file_template"/>
      <arg type="a{sv}" direction="in" name="options"/>
      <arg type="b" direction="in" name="flash"/>
      <arg type="b" direction="out" name="success"/>
      <arg type="s" direction="out" name="filename_used"/>
    </method>

    <!--
        ScreencastArea:
        @x: the X coordinate of the area to capture
        @y: the Y coordinate of the area to capture
        @width: the width of the area to capture
        @height: the height of the area to capture
        @file_template: the template for the filename to use
        @options: a dictionary of optional parameters
        @success: whether the screencast was started successfully
        @filename_used: the file where the screencast is being saved

        Records a screencast of the passed in area and saves it
        (by default) as webm video under a filename derived from
        @file_template. The template is either a relative or absolute
        filename which may contain some escape sequences - %d and %t
        will be replaced by the start date and time of the recording.
        If a relative name is used, the screencast will be saved in the
        $XDG_VIDEOS_DIR if it exists, or the home directory otherwise.
        The actual filename of the saved video is returned in @filename_used.
        The set of optional parameters in @options currently consists of:
            'draw-cursor'(b): whether the cursor should be included in the
                              recording (true)
            'framerate'(i): the number of frames per second that should be
                            recorded if possible (30)
            'pipeline'(s): the GStreamer pipeline used to encode recordings
                           in gst-launch format; if not specified, the
                           recorder will produce vp8 (webm) video (unset)
    -->
    <method name="ScreencastArea">
      <arg type="i" direction="in" name="x"/>
      <arg type="i" direction="in" name="y"/>
      <arg type="i" direction="in" name="width"/>
      <arg type="i" direction="in" name="height"/>
      <arg type="s" direction="in" name="file_template"/>
      <arg type="a{sv}" direction="in" name="options"/>
      <arg type="b" direction="out" name="success"/>
      <arg type="s" direction="out" name="filename_used"/>
    </method>

    <!--
        StopScreencast:
        @success: whether stopping the recording was successful

        Stop the recording started by either Screencast or ScreencastArea.
    -->
    <method name="StopScreencasta">
      <arg type="b" direction="out" name="success"/>
    </method>

  </interface>
"""
from ScreencastBase import ScreencastBase
import dbus

BUS_NAME = 'org.gnome.Shell.Screencast'
BUS_PATH = '/org/gnome/Shell/Screencast'
BUS_IFACE = 'org.gnome.Shell.Screencast'


class ScreencastGnome(ScreencastBase):
    def __init__(self):
        super(ScreencastGnome, self).__init__()
        bus = dbus.SessionBus()
        self._proxy = dbus.Interface(
            bus.get_object(
                BUS_NAME, BUS_PATH,
                follow_name_owner_changes=False
            ),
            BUS_IFACE
        )

    def Screencast(self):
        succ, filename = self._proxy.Screencast("/home/jmoskovc/screencast.ogv", {})
        return filename

    def ScreencastArea(self):
        raise NotImplementedError

    def StopScreencast(self):
        return self._proxy.StopScreencast()

    def IsSuitable(self):
        return True
