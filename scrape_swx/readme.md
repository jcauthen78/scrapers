# Space Weather Monitor Setup Guide

This guide will walk you through setting up a space weather monitoring script on your Raspberry Pi. The assumption is you can SSH into your raspberry pi and have some very basic understanding of file system navigation.

## Initial Setup

1. Create a new folder on the Pi:
```bash
mkdir ~/swx_monitor
```

2. Create the script file in the new folder:
```bash
nano ~/swx_monitor/scrape_swx.py
```

3. Copy & Paste the script content:
   - Navigate to the `scrape_swx.py` here on gitHub
   - Highlight & copy its contents: `Ctrl/Cmd + C`
   - Paste into the open `nano` document in your SSH window: `Ctrl + V`

4. Update the `LAT` & `LON` variables near the top of the file with your location coordinates to ensure correct sunrise/sunset calculations.

5. Save the file & close the editor:
```bash
# Press the following keys:
Ctrl + X
Y
```

## System Configuration

6. Check the OS version of your Raspberry Pi:
```bash
cat /etc/os-release
```

### For Bookworm Users Only (Skip to step 8 if using Bullseye)

7a. Set up the required virtual environment & install packages:
```bash
cd ~/swx_monitor
python3 -m venv swx_env
source swx_env/bin/activate
pip install ephem pytz requests beautifulsoup4
```

7b. Update the Python path in the script:
```bash
nano ~/swx_monitor/scrape_swx.py
```

In the editor, you'll need to:
1. Find and remove this line:
   ```
   #!/usr/lib/python3
   ```
2. Replace it with this line:
   ```
   #!/home/pi/swx_monitor/swx_env/bin/python3
   ```
3. Save and exit:
   ```bash
   Ctrl + X
   Y
   ```

## Script Setup and Testing

8. Make the script executable:
```bash
chmod +x scrape_swx.py
```

9. Test the Python script:
```bash
/home/pi/swx_monitor/swx_env/bin/python3 /home/pi/swx_monitor/scrape_swx.py
```

10. Verify the output:
```bash
# Check for generated files:
ls -l ~/allsky/config/overlay/extra/

# Verify file contents (should not be blank):
cat /home/pi/allsky/config/overlay/extra/scrape_swx.json
```

## Automation Setup

11. Create a cron job:
```bash
crontab -e
# If this is your first time running crontab, select option #1
```

12. Add the following lines to run the script every 5 minutes and at reboot:
```bash
@reboot sleep 30 && /home/pi/swx_monitor/swx_env/bin/python3 /home/pi/swx_monitor/scrape_swx.py
*/5 * * * * /home/pi/swx_monitor/swx_env/bin/python3 /home/pi/swx_monitor/scrape_swx.py
```

13. Save and close the crontab:
```bash
# Press:
Ctrl + X
Y
```

## Allsky WebUI Configuration

After completing the SSH work, configure the Allsky WebUI:

1. Open the 'Overlay Editor' page
2. Open the Variable Manager (5th icon from the left)
3. Click on "All Variables" to view all available options
4. Search for "swx" in the top right search field to display the 6 new variables
5. For each variable you want to use:
   - Click the + icon to add it
   - Provide a short, meaningful description
   - Click 'Save Changes'
6. Click "Close" in the bottom right of the variable manager
7. Click the Green save/disk icon (first icon on the left)
   > **Important**: This step must be completed before adding variables to the overlay. If skipped, you'll need to repeat the previous steps.
8. You can now return to the variable manager to add the variables as needed

### Note on Text Colors
The text color is dynamic and will change automatically based on the ranges defined in the Python script. These limits can be customized and were established by comparing various official sites and observing their color-change thresholds.
