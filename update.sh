#!/bin/bash

# Run the command
output=$(cd /opt/openjk && dotnet /root/mbiiez/updater/MBII_CommandLine_Update_XPlatform.dll)

# Check if the output contains the string 'is an upgrade'
if echo "$output" | grep -q "is an upgrade"; then
    echo "Upgrade detected. Restarting servers..."
    # Run the restart commands
    mbii -i open restart
    mbii -i training restart
    mbii -i legend restart
    echo "Servers restarted successfully."
else
    echo "No upgrade detected."
fi
