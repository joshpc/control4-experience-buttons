from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

@dataclass
class DriverConfig:
    device_name: str
    manufacturer: str
    model_name: str
    creator: str
    version: str
    min_os: str
    documentation: str

class DriverGenerator:
    def __init__(self, config: DriverConfig):
        self.config = config
        self.driver_name = f"uibutton_{config.device_name.lower()}"

    def generate(self, base_path: Path):
        """Generate all driver files"""
        self._ensure_directories(base_path)
        self._create_driver_xml(base_path)
        self._create_driver_lua(base_path)

    def _ensure_directories(self, base_path: Path):
        """Create required directory structure"""
        (base_path / "icons" / "device").mkdir(parents=True, exist_ok=True)
        (base_path / "www").mkdir(parents=True, exist_ok=True)

    def _create_driver_xml(self, base_path: Path):
        """Generate the driver.xml file"""
        current_date = datetime.now().strftime("%m/%d/%Y %H:%M")

        content = f"""<devicedata>
    <copyright>N/A</copyright>
    <manufacturer>{self.config.manufacturer}</manufacturer>
    <name>{self.config.model_name} - UI Button</name>
    <model>{self.config.model_name}</model>
    <creator>{self.config.creator}</creator>
    <created>{current_date}</created>
    <modified>{current_date}</modified>
    <version>{self.config.version}</version>
    <control>lua_gen</control>
    <driver>DriverWorks</driver>
    <auto_update>true</auto_update>
    <minimum_auto_update_version>100</minimum_auto_update_version>
    <minimum_os_version>{self.config.min_os}</minimum_os_version>
    <small image_source="c4z">icons/device_sm.png</small>
    <large image_source="c4z">icons/device_lg.png</large>
    <config>
        <script file="driver.lua"/>
        <documentation file="www/documentation.rtf">
{self.config.documentation}
</documentation>
        <properties>
            <property>
                <name>Driver Version</name>
                <default></default>
                <type>STRING</type>
                <readonly>true</readonly>
            </property>
            <property>
                <name>Selection</name>
                <type>LIST</type>
                <items>
                    <item>Audio</item>
                    <item>Video</item>
                </items>
                <default>Video</default>
                <readonly>false</readonly>
            </property>
        </properties>
        <commands>
        </commands>
    </config>
    <proxies>
        <proxy proxybindingid="5001" name="{self.config.model_name}" primary="True" image_source="c4z" large_image="icons/device_lg.png" small_image="icons/device_sm.png">uibutton</proxy>
    </proxies>
    <capabilities>
        <navigator_display_option proxybindingid="5001">
            <display_icons>
                <Icon height="70" width="70">controller://driver/{self.driver_name}/icons/device/experience_70.png</Icon>
                <Icon height="90" width="90">controller://driver/{self.driver_name}/icons/device/experience_90.png</Icon>
                <Icon height="300" width="300">controller://driver/{self.driver_name}/icons/device/experience_300.png</Icon>
                <Icon height="512" width="512">controller://driver/{self.driver_name}/icons/device/experience_512.png</Icon>
                <Icon height="1024" width="1024">controller://driver/{self.driver_name}/icons/device/experience_1024.png</Icon>
                <state id="Idle">
                    <Icon height="70" width="70">controller://driver/{self.driver_name}/icons/device/experience_70.png</Icon>
                    <Icon height="90" width="90">controller://driver/{self.driver_name}/icons/device/experience_90.png</Icon>
                    <Icon height="300" width="300">controller://driver/{self.driver_name}/icons/device/experience_300.png</Icon>
                    <Icon height="512" width="512">controller://driver/{self.driver_name}/icons/device/experience_512.png</Icon>
                    <Icon height="1024" width="1024">controller://driver/{self.driver_name}/icons/device/experience_1024.png</Icon>
                </state>
                <state id="Selected">
                    <Icon height="70" width="70">controller://driver/{self.driver_name}/icons/device/experience_70.png</Icon>
                    <Icon height="90" width="90">controller://driver/{self.driver_name}/icons/device/experience_90.png</Icon>
                    <Icon height="300" width="300">controller://driver/{self.driver_name}/icons/device/experience_300.png</Icon>
                    <Icon height="512" width="512">controller://driver/{self.driver_name}/icons/device/experience_512.png</Icon>
                    <Icon height="1024" width="1024">controller://driver/{self.driver_name}/icons/device/experience_1024.png</Icon>
                </state>
            </display_icons>
        </navigator_display_option>
    </capabilities>
    <events>
    </events>
    <connections>
        <connection>
            <id>5001</id>
            <facing>6</facing>
            <connectionname>UIBUTTON</connectionname>
            <type>2</type>
            <consumer>False</consumer>
            <audiosource>True</audiosource>
            <videosource>True</videosource>
            <linelevel>True</linelevel>
            <classes>
                <class>
                    <classname>UIBUTTON</classname>
                </class>
            </classes>
        </connection>
        <connection>
            <id>2000</id>
            <type>5</type>
            <connectionname>AV Out</connectionname>
            <consumer>False</consumer>
            <linelevel>True</linelevel>
            <classes>
                <class>
                    <classname>HDMI</classname>
                </class>
            </classes>
        </connection>
    </connections>
</devicedata>"""

        with open(base_path / "driver.xml", "w", encoding="utf-8") as f:
            f.write(content)

    def _create_driver_lua(self, base_path: Path):
        """Generate the driver.lua file"""
        content = """do -- globals
    PROXY_CMDS = {}
        if (C4.GetDriverConfigInfo) then
        VERSION = C4:GetDriverConfigInfo ("version")
    else
        VERSION = 'Incompatible with this OS'
    end
    C4:UpdateProperty ('Driver Version', VERSION)
end

function ReceivedFromProxy (idBinding, strCommand, tParams)
    if type(PROXY_CMDS[strCommand]) == "function" then
        local success, retVal = pcall(PROXY_CMDS[strCommand], tParams)
        if success then
            return retVal
        end
    end
    return nil
end

function PROXY_CMDS.OFF (tParams)
    C4:SendToProxy(5001, "ICON_CHANGED", {icon = "Idle"})
end

function PROXY_CMDS.SELECT (tParams)
    C4:SendToProxy(5001, "ICON_CHANGED", {icon = "Selected"})
    local selection = string.upper(Properties["Selection"] or "Video")
    local deviceid = C4:GetProxyDevices(C4:GetDeviceID())
    if (selection == "VIDEO") then
        C4:SendToDevice (tParams.Room, 'SELECT_VIDEO_DEVICE', {deviceid = deviceid})
    else
        C4:SendToDevice (tParams.Room, 'SELECT_AUDIO_DEVICE', {deviceid = deviceid})
    end
end"""

        with open(base_path / "driver.lua", "w", encoding="utf-8") as f:
            f.write(content)
