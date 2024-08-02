---

# Scripts Collection

Welcome to the **Scripts Collection** repository! This repository contains a variety of utility scripts designed to automate everyday tasks, enhance productivity, and simplify complex processes.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Scripts Overview](#scripts-overview)
  - [Weather Fetch Script](#weather-fetch-script)
  - [Backup Documents Script](#backup-documents-script)
  - [System Update Script](#system-update-script)
  - [Others](#others)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

This repository houses a collection of scripts that cater to various needs, from fetching weather data to automating backups and notifications. Each script is crafted with error handling and SMART properties to ensure reliability and efficiency.

## Installation

To get started, clone this repository to your local machine:

```bash
git clone https://github.com/currentsuspect/scripts.git
cd scripts
```

Ensure you have the necessary dependencies installed. For example:

```bash
sudo apt-get install curl rsync jq notify-send rclone feh
```

## Usage

Each script is located in the `scripts/` directory. To run a script, simply navigate to the directory and execute it. Make sure to provide necessary permissions:

```bash
chmod +x scripts/script_name.sh
./scripts/script_name.sh
```

You can also integrate these scripts with your crontab for scheduled execution.

## Scripts Overview

### Weather Fetch Script

**Description:** Fetches the weather information for Nairobi every morning at 10:05 AM and appends it to `weather.txt`.

**Script:**
```bash
#!/bin/bash
curl -s "wttr.in/nairobi" >> ~/weather.txt
```

**Crontab Entry:**
```
5 9 * * * /path/to/scripts/weather_fetch.sh
```

### Backup Documents Script

**Description:** Backs up the `Documents` folder to an external drive every day at 11 AM.

**Script:**
```bash
#!/bin/bash
rsync -av --delete ~/Documents /mnt/external_drive/Documents
```

**Crontab Entry:**
```
0 11 * * * /path/to/scripts/backup_documents.sh
```

### System Update Script

**Description:** Checks for system updates every day at 11:30 AM and logs the output to `update.log`.

**Script:**
```bash
#!/bin/bash
yay -Syu --noconfirm >> ~/update.log
```

**Crontab Entry:**
```
30 11 * * * /path/to/scripts/system_update.sh
```

### Others

#### Break Reminder Script

**Description:** Sends a notification to take a break every hour from 10 AM to 8 PM.

**Script:**
```bash
#!/bin/bash
notify-send "Time to take a break and stretch!"
```

**Crontab Entry:**
```
0 10-20 * * * /path/to/scripts/break_reminder.sh
```

#### Daily Summary Email Script

**Description:** Sends a daily summary email at 6 PM.

**Script:** (Replace with your own implementation)

**Crontab Entry:**
```
0 18 * * * /path/to/scripts/send_summary_email.sh
```

## Error Handling

Each script is equipped with error handling to ensure smooth execution and provide meaningful error messages. For example:

```bash
#!/bin/bash
set -e

# Check if curl is installed
if ! command -v curl &> /dev/null; then
    echo "curl could not be found"
    exit 1
fi

# Fetch weather data
curl -s "wttr.in/nairobi" >> ~/weather.txt
```

## Contributing

We welcome contributions to enhance and expand this collection of scripts. To contribute, please fork the repository, create a new branch, make your changes, and submit a pull request.

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to the open-source community for providing tools and inspiration.
- Special thanks to all contributors for their valuable input and effort.

---


