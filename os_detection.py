import platform

class OSDetector:
    @staticmethod
    def detect_platform():
        os_name = platform.system()
        architecture = platform.machine()

        if os_name == "Darwin":
            # For macOS, Intel CPUs will report as "x86_64"
            if architecture in ["x86_64", "i386"]:
                return "mac-x64"
            else:
                return "other"
        elif os_name == "Windows":
            return "win64"
        else:
            return "other"

platform = OSDetector.detect_platform()