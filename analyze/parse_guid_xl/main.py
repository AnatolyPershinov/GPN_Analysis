from pathlib import Path
import sys

print(sys.path.insert(0, str(Path(__file__).parent.parent.parent)))

from analyze import getfiles

