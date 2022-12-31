import subprocess

# sample output of diskutil
# ***DiskAppeared ('disk5', DAVolumePath = '<null>', DAVolumeKind = 'msdos', DAVolumeName = 'Kindle') Time=20221231-16:38:26.6321
# ***DiskMountApproval ('disk5', DAVolumePath = '<null>', DAVolumeKind = 'msdos', DAVolumeName = 'Kindle') Comment=Approving Time=20221231-16:38:26.6327
# ***DiskDescriptionChanged ('disk5', DAVolumePath = 'file:///Volumes/Kindle/') Time=20221231-16:38:26.9476
# ***DAIdle (no DADiskRef) Time=20221231-16:38:26.9477
class Diskutil:

    def waitForKindleConnection(self):
        # execute diskutil activity process and read each output line
        process = subprocess.Popen(['diskutil', 'activity'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # while reading lines from process
        while True:
                line = process.stdout.readline()
                if not line:
                    break
                line = line.decode('utf-8')

                # if line starts with '***DiskAppeared', parse line
                if line.startswith('***DiskMountApproval') and 'Kindle' in line:
                    print('Kindle connected')
                    yield True
