# Connect to a network on boot (example uses wifi driver)
be.based.run("modprobe driver_wifi as network")
systemprints(2, "Connecting wifi")
be.based.run("iwctl station wifi auto")  # Configure connections in &/settings.toml
systemprints(1, "Connecting wifi")
be.based.run("timesync")
