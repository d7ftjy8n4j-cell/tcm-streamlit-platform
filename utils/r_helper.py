# utils/r_helper.py
import subprocess
import tempfile
import os
import json

def run_r_script(r_code: str) -> dict:
    """
    执行 R 代码并返回结果[reference:31]
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.R', delete=False) as f:
        f.write(r_code)
        r_script_path = f.name
    
    try:
        result = subprocess.run(
            ["Rscript", r_script_path],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    finally:
        os.unlink(r_script_path)
