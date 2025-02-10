do -- globals
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
end

