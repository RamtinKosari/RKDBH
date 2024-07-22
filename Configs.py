# - Import Necessary Libraries
import psycopg2
import os

# - Database Terminal Output
DATABASE = f'\033[38;2;0;173;173m[RKDBH]\033[0m'
# - Warning Terminal Output
WARNING = f'\033[38;2;255;255;0m[WARNING]\033[0m'
# - Success Terminal Output
SUCCESS = f'\033[38;2;0;232;0m[SUCCESS]\033[0m'
# - Failed Terminal Output
FAILED = f'\033[38;2;255;0;0m[FAILED]\033[0m'
# - Log Terminal Output
LOG = f'\033[38;2;153;153;153m[LOG]\033[0m'
# - Info Color
INFO = f'\033[38;2;106;140;150m'
# - Error Color
ERR = f'\033[38;2;255;200;0m'
# - Reset Color
RESET = f'\033[0m'

# - Yellow Color
YELLOW = f'\033[38;2;255;255;0m'
# - Cyan Color
CYAN = f'\033[38;2;0;200;200m'
# - Green Color
GREEN = f'\033[38;2;0;170;0m'
# - Red Color
RED = f'\033[38;2;255;0;0m'

# symbols = "✓⚠❖⁂✘✗ ☑☐☒༻◆◈☓⬢⬡"

# - Log Messages
LOG_MESSAGES = True

# - Log Failures
LOG_FAILURES = True

# - Connection Auto Commit
CONNECTION_AUTOCOMMIT = True

# - Disable Cursor Blinking
DISABLE_CURSOR_BLINKING = False

# - Disconnect After Query Execution
DISCONNECT_AFTER_QUERY_EXECUTION = False
