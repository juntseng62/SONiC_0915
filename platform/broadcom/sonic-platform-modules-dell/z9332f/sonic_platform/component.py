#!/usr/bin/env python

########################################################################
# DELLEMC Z9332F
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Components' (e.g., BIOS, CPLD, FPGA, BMC etc.) available in
# the platform
#
########################################################################

try:
    import subprocess
    from sonic_platform_base.component_base import ComponentBase
    import sonic_platform.hwaccess as hwaccess
    
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


def get_bios_version():
    return subprocess.check_output(
        ['dmidecode', '-s', 'bios-version']).decode('utf-8').strip()

def get_fpga_version():
    val = hwaccess.pci_get_value('/sys/bus/pci/devices/0000:09:00.0/resource0', 0)
    return '{}.{}'.format((val >> 8) & 0xff, val & 0xff)
    
def get_bmc_version():
    return subprocess.check_output(
        ['cat', '/sys/class/ipmi/ipmi0/device/bmc/firmware_revision']
        ).decode('utf-8').strip()

def get_cpld_version(bus, i2caddr):
    return '{}'.format(hwaccess.i2c_get(bus, i2caddr, 0))

def get_cpld0_version():
    return get_cpld_version(37, 0x0d)

def get_cpld1_version():
    return get_cpld_version(36, 0x30)

def get_cpld2_version():
    return get_cpld_version(36, 0x31)



class Component(ComponentBase):
    """DellEMC Platform-specific Component class"""

    CHASSIS_COMPONENTS = [
        ['BIOS',
         'Performs initialization of hardware components during booting',
         get_bios_version
         ],

        ['FPGA',
         'Used for managing the system LEDs',
         get_fpga_version
         ],

        ['BMC',
         'Platform management controller for on-board temperature monitoring,in-chassis power, Fan and LED control',
         get_bmc_version
         ],

        ['Baseboard CPLD',
         'Used for managing the CPU power sequence and CPU states',
         get_cpld0_version
         ],

        ['Switch CPLD 1',
         'Used for managing QSFP-DD/QSFP28/SFP port transceivers ',
         get_cpld1_version
         ],

        ['Switch CPLD 2',
         'Used for managing QSFP-DD/QSFP28/SFP port transceivers',
         get_cpld2_version
         ]

    ]

    def __init__(self, component_index = 0):
        ComponentBase.__init__(self)
        self.index = component_index
        self.name = self.CHASSIS_COMPONENTS[self.index][0]
        self.description = self.CHASSIS_COMPONENTS[self.index][1]
        self.version = self.CHASSIS_COMPONENTS[self.index][2]()

    def get_name(self):
        """
        Retrieves the name of the component
        Returns:
        A string containing the name of the component
        """
        return self.name

    def get_description(self):
        """
        Retrieves the description of the component
        Returns:
        A string containing the description of the component
        """
        return self.description

    def get_firmware_version(self):
        """
        Retrieves the firmware version of the component
        Returns:
            A string containing the firmware version of the component
        """
        return self.version

    def install_firmware(self, image_path):
        """
        Installs firmware to the component
        Args:
        image_path: A string, path to firmware image
        Returns:
        A boolean, True if install was successful, False if not
        """
        return False

    def get_presence(self):
        """
        Retrieves the presence of the component
        Returns:
            bool: True if  present, False if not
        """
        return True

    def get_model(self):
        """
        Retrieves the part number of the component
        Returns:
            string: Part number of component
        """
        return 'NA'

    def get_serial(self):
        """
        Retrieves the serial number of the component
        Returns:
            string: Serial number of component
        """
        return 'NA'

    def get_status(self):
        """
        Retrieves the operational status of the component
        Returns:
            bool: True if component is operating properly, False if not
        """
        return True

    def get_position_in_parent(self):
        """
        Retrieves 1-based relative physical position in parent device.
        Returns:
            integer: The 1-based relative physical position in parent
            device or -1 if cannot determine the position
        """
        return -1

    def is_replaceable(self):
        """
        Indicate whether component is replaceable.
        Returns:
            bool: True if it is replaceable.
        """
        return False
