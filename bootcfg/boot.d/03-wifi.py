# Connect to a network on boot (example uses wifi driver)
ljinux.based.run("modprobe driver_wifi as network")
systemprints(2, "Connecting wifi")
ljinux.based.run("iwctl station wifi auto")  # Configure connections in &/settings.toml
systemprints(1, "Connecting wifi")
ljinux.based.run("timesync")
