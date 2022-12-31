import subprocess

class MacOS:

    @staticmethod
    def notify(message):
        title = 'Kindle'
        sound = "default"  # or choose a specific sound: "Glass", "Basso", etc.
        command = f'display notification "{message}" with title "{title}" sound name "{sound}"'
        subprocess.run(['osascript', '-e', command])

    @staticmethod
    def ejectKindle():
        device_name = "Kindle"

        command = f'tell application "Finder" to eject "{device_name}"'
        subprocess.run(['osascript', '-e', command])
